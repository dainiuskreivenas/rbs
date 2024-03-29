from models.matchTree import MatchTree
from models.fact import Fact
from helpers.variableHelper import VariableHelper

class RulesService:
    def __init__(self, 
        rulesRepository, 
        primeRepository, 
        linkRepository, 
        factGroupRepository, 
        factRepository, 
        assertionRepository, 
        connectionsService, 
        baseService, 
        propertyService,
        relationshipService,
        logger):
        self.__rulesRepository = rulesRepository
        self.__primeRepository = primeRepository
        self.__linkRepository = linkRepository
        self.__factGroupRepository = factGroupRepository
        self.__factRepository = factRepository
        self.__assertionRepository = assertionRepository
        self.__connectionsService = connectionsService
        self.__baseService = baseService
        self.__propertyService = propertyService
        self.__relationshipService = relationshipService
        self.__logger = logger

    def applyRulesToFacts(self, generator):
        rules = self.__rulesRepository.get()

        for ruleName in rules:
            self.__logger.writeDebug("Applying Rule: {}".format(ruleName))
            rule = rules[ruleName]

            matches = [MatchTree({},[])]
            for condition in rule.conditions:
                matches = self.__buildFounds(matches, condition, rule)
                if(len(matches) == 0):
                    break

            self.__logger.writeDebug("Found {} Matches for Rule: {}".format(len(matches), ruleName))

            for match in matches:
                assertionNeuron = self.__assertionRepository.createAssertion(match, rule)
                if(assertionNeuron == None):
                    continue

                self.__setupFactAssertions(rule.assertions, match, assertionNeuron, generator)
                self.__setupBaseAssertions(rule.baseAssertions, match, assertionNeuron)
                self.__setupPrimeAssertions(rule.primeAssertions, assertionNeuron)
                self.__setupLinkAssertions(rule.linkAssertions, match, assertionNeuron)
                self.__setupPropertyAssertions(rule.propertyAssertions,  match, assertionNeuron)
                self.__setupRelationshipAssertions(rule.relationshipAssertions, match, assertionNeuron)
                self.__setupRetractions(rule.retractions, match, assertionNeuron, rule.bases, rule.primes, rule.links)

                ca = self.__getCas(match, rule.bases, rule.primes, rule.links, rule.properties, rule.relationships)
                generator.setupActivations(self, ca, assertionNeuron)

    def __buildFounds(self, matches, condition, rule):
        newTree = []
        existing = []

        for f in matches:
            search = self.__getSearchExpression(condition, f.variables)
            founds = self.__getMatchingFacts(search[0], search[1], search[2])

            if(founds == None):
                continue

            for found in founds:
                var = f.variables.copy()
                var = VariableHelper.extractVariables(var, found, condition[2])

                treeItem = MatchTree(var, f.matches + [(found, condition[3])])
                if(treeItem.label in existing):
                    continue

                testPass = True
                for base in rule.bases:
                    testPass = self.__baseService.test(base[1], var)
                    if(testPass == False):
                        break

                for prop in rule.properties:
                    testPass = self.__propertyService.test(prop[1], var)
                    if(testPass == False):
                        break

                for rel in rule.relationships:
                    testPass = self.__relationshipService.test(rel[1], var)
                    if(testPass == False):
                        break

                if(testPass == False):
                    continue

                for test in rule.tests:
                    testPass = VariableHelper.testVariables(test, var)
                    if(testPass == False):
                        break

                if(testPass == False):
                    continue
                
                existing.append(treeItem.label)

                newTree.append(treeItem)

        return newTree

    def __getSearchExpression(self, item, variables):
        params = []            
        for p in item[2]:
            if(p in variables):
                params.append(variables[p])
            else:
                params.append(p)

        search = (item[0],item[1],tuple(params),item[3])

        return search

    def __getMatchingFacts(self, positive, name, properties):
        group = self.__factGroupRepository.get(name)
        if(group == None):
            return None
        
        found = []

        for fact in group:
            match = True
            for i,prop in enumerate(fact.attributes):
                if(match == False):
                    break
                val = properties[i]

                #is anything?
                if(val == "?" and positive):
                    continue

                if(isinstance(val, str)):
                    lVal = list(val)
                    #is variable?
                    if(lVal[0] == "?"):
                        val = val[:1]

                if(positive):
                    if(val != "?" and val != prop):
                        match = False
                else:
                    if(val == "?" or val == prop):
                        match = False
                            
            if(match):
                found.append(fact)
                    
        return found

    def __setupFactAssertions(self, asssertions, match, rulePop, generator):
        for assertion in asssertions:
            variables = match.variables
            properties = assertion[1]
            newProps = []

            for p in properties:
                prop = VariableHelper.extractValue(p, variables)
                newProps.append(prop)
        
            fact = Fact(assertion[0], tuple(newProps))
            foundFact = self.__factRepository.find(fact)

            if(foundFact == None):
                fact = self.__factRepository.addFact(fact, False)
                self.applyRulesToFacts(generator)
            else:
                fact = foundFact

            self.__connectionsService.neuronTurnsOnCa(rulePop, fact)

    def __setupRetractions(self, retractions, match, ruleCa, bases, primes, links):
        for retraction in retractions:
            applied = False

            for m in match.matches:
                if m[1] == retraction:
                    self.__connectionsService.neuronTurnsOffCA(ruleCa, m[0])
                    applied = True
                    break

            if(applied == False):
                for b in bases:
                    if(b[2] == retraction):
                        unit = b[1]
                        if(unit[0] == "?"):
                            unit = VariableHelper.extractValue(unit, match.variables)
                        ca = self.__baseService.caFromUnit(unit)
                        self.__connectionsService.neuronTurnsOffAssociationCA(ruleCa, ca)        
                        applied = True     
                        break

            if(applied == False):
                for p in primes:
                    if(p[2] == retraction):
                        ca = self.__primeRepository.addOrGet(p[1])
                        self.__connectionsService.neuronTurnsOffCA(ruleCa, ca)
                        applied = True
                        break

            if(applied == False):
                for l in links:
                    if(l[2] == retraction):
                        linkTo, unit, linkType = l[1]
                        if(unit[0] == "?"):
                            unit = VariableHelper.extractValue(unit, match.variables)
                        ca = self.__linkRepository.addOrGetLink(linkTo, unit, linkType)
                        self.__connectionsService.neuronTurnsOffCA(ruleCa, ca)

    def __setupBaseAssertions(self, baseAssertions, match, ruleCa):       
        for assertion in baseAssertions:
            unit = assertion
            if(unit[0] == "?"):
                variables = match.variables
                unit = VariableHelper.extractValue(unit, variables)
            ca = self.__baseService.fromUnit(unit)
            self.__connectionsService.neuronTurnsOnAssociationCA(ruleCa, ca)

    def __setupPrimeAssertions(self, primeAssertions, ruleCa):
        for assertion in primeAssertions:
            ca = self.__primeRepository.addOrGet(assertion)
            self.__connectionsService.neuronTurnsOnCa(ruleCa, ca)

    def __setupLinkAssertions(self, linkAssertions, match, ruleCa):
        for assertion in linkAssertions:
            linkTo, unit, linkType = assertion
            if(unit[0] == "?"):
                variables = match.variables
                unit = VariableHelper.extractValue(unit, variables)
            ca = self.__linkRepository.addOrGetLink(linkTo, unit, linkType)
            if(linkType == "correlate" or linkType == "stimulate"):
                self.__connectionsService.neuronTurnsOnCa(ruleCa, ca)

    def __setupPropertyAssertions(self, propertyAssertions, match, ruleCa):
        for assertion in propertyAssertions:
            unit = assertion
            if(unit[0] == "?"):
                variables = match.variables
                unit = VariableHelper.extractValue(unit, variables)
            ca = self.__propertyService.fromUnit()
            self.__connectionsService.neuronTurnsOnAssociationCA(ruleCa, ca)

    def __setupRelationshipAssertions(self, relationshipAssertions, match, ruleCa):
        for assertion in relationshipAssertions:
            unit = assertion
            if(unit[0] == "?"):
                variables = match.variables
                unit = VariableHelper.extractValue(unit, variables)
            ca = self.__relationshipService.fromUnit()
            self.__connectionsService.neuronTurnsOnAssociationCA(ruleCa, ca)

    def __getCas(self, match, bases, primes, links, props, relationships):
        cas = []
        for m in match.matches:
            cas.append(m[0])
        
        for a in bases:
            unit = a[1]
            if(unit[0] == "?"):
                unit = VariableHelper.extractValue(unit, match.variables)
            ca = self.__baseService.fromUnit(unit)
            cas.append(ca)

        for p in props:
            unit = p[1]
            if(unit[0] == "?"):
                unit = VariableHelper.extractValue(unit, match.variables)
            ca = self.__propertyService.fromUnit(unit)
            cas.append(ca)

        for r in relationships:
            unit = r[1]
            if(unit[0] == "?"):
                unit = VariableHelper.extractValue(unit, match.variables)
            ca = self.__relationshipService.fromUnit(unit)
            cas.append(ca)
        
        for p in primes:
            ca = self.__primeRepository.addOrGet(p[1])
            cas.append(ca)

        for l in links:
            linkTo, unit, linkType = l[1]
            if(unit[0] == "?"):
                unit = VariableHelper.extractValue(unit, match.variables)
            ca = self.__linkRepository.addOrGetLink(linkTo, unit, linkType)
            cas.append(ca)

        return cas