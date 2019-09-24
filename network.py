import dill
import logging
from contracts.matchTree import MatchTree
from contracts.fact import Fact
from generators.constants import *
from helpers.labelHelper import LabelHelper
from helpers.variableHelper import VariableHelper

class Network:
    def __init__(self, 
        fsa, 
        ruleGenerator,
        connectionsService,
        neuronRepository,
        linkRepository,
        factGroupRepository,
        factRepository,
        primeRepository,
        debug = False):
        self.__fsa = fsa
        self.__generator = ruleGenerator
        self.__debug = debug
        self.__association = None
        self.__connectionsService = connectionsService
        self.__neuronRepository = neuronRepository
        self.__linkRepository = linkRepository
        self.__factGroupRepository = factGroupRepository
        self.__factRepository = factRepository
        self.__primeRepository = primeRepository

    def useAssociation(self, association):
        self.__association = association
        return self

    def build(self):
        self.rules = {}
        self.assertions = {}

        return self

    def addFact(self, fact, active = True, applyRules = True):
        fact = self.__factRepository.addFact(fact, active)

        if(applyRules):
            self.applyRulesToFacts()

        return fact

    def getFact(self, fact, applyRules = True):
        fact = self.__factRepository.getFact(fact)
        
        if(applyRules):
            self.applyRulesToFacts()
        
        return fact

    def addRule(self, rule, apply = True):
        self.rules[rule.name] = rule
        if(apply):
            self.applyRulesToFacts() 

    def getSearchExpression(self, item, variables):
        params = []            
        for p in item[2]:
            if(p in variables):
                params.append(variables[p])
            else:
                params.append(p)

        search = (item[0],item[1],tuple(params),item[3])

        return search

    def getMatchingFacts(self, positive, name, properties):
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

    def buildFounds(self, matches, condition, rule):
        newTree = []
        existing = []
             
        for f in matches:
            search = self.getSearchExpression(condition, f.variables)
            founds = self.getMatchingFacts(search[0], search[1], search[2])

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
                    testPass = self.__association.testBase(base[1], var)
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

    def createRule(self, match, rule):
        label = LabelHelper.generateRuleLabel(rule, match)

        if(label in self.assertions):
            return None

        rulePop = self.__neuronRepository.addNeuron()
        self.assertions[label] = rulePop

        return rulePop

    def addAssertions(self, asssertions, match, rulePop):
        for assertion in asssertions:
            variables = match.variables
            properties = assertion[1]
            newProps = []

            for p in properties:
                prop = VariableHelper.extractValue(p, variables)
                newProps.append(prop)
        
            fact = Fact(assertion[0],tuple(newProps))
            fact = self.getFact(fact)

            self.__connectionsService.neuronTurnsOnCa(rulePop, fact.ca)

    def addRetractions(self, retractions, match, ruleCa, bases, primes, links):
        for retraction in retractions:
            applied = False

            for m in match.matches:
                if m[1] == retraction:
                    self.__connectionsService.neuronTurnsOffCA(ruleCa, m[0].ca)
                    applied = True
                    break

            if(applied == False):
                for b in bases:
                    if(b[2] == retraction):
                        unit = b[1]
                        if(unit[0] == "?"):
                            unit = VariableHelper.extractValue(unit, match.variables)
                        ca = self.__association.caFromUnit(unit)
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

    def addBaseAssertions(self, baseAssertions, match, ruleCa):       
        for assertion in baseAssertions:
            unit = assertion
            if(unit[0] == "?"):
                variables = match.variables
                unit = VariableHelper.extractValue(unit, variables)
            ca = self.__association.caFromUnit(unit)
            self.__connectionsService.neuronTurnsOnAssociationCA(ruleCa, ca)

    def addPrimeAssertions(self, primeAssertions, ruleCa):
        for assertion in primeAssertions:
            ca = self.__primeRepository.addOrGet(assertion)
            self.__connectionsService.neuronTurnsOnCa(ruleCa, ca)

    def addLinkAssertions(self, linkAssertions, match, ruleCa):
        for assertion in linkAssertions:
            linkTo, unit, linkType = assertion
            if(unit[0] == "?"):
                variables = match.variables
                unit = VariableHelper.extractValue(unit, variables)
            ca = self.__linkRepository.addOrGetLink(linkTo, unit, linkType)
            if(linkType == "correlate" or linkType == "stimulate"):
                self.__connectionsService.neuronTurnsOnCa(ruleCa, ca)

    def getCas(self, match, bases, primes, links):
        cas = []
        for m in match.matches:
            cas.append((m[0].ca,CONNECTION_NETWORK))
        
        for a in bases:
            unit = a[1]
            if(unit[0] == "?"):
                unit = VariableHelper.extractValue(unit, match.variables)
            ca = self.__association.caFromUnit(unit)
            cas.append((ca,CONNECTION_INHERITANCE_NETWORK))
        
        for p in primes:
            ca = self.__primeRepository.addOrGet(p[1])
            cas.append((ca,CONNECTION_NETWORK))

        for l in links:
            linkTo, unit, linkType = l[1]
            if(unit[0] == "?"):
                unit = VariableHelper.extractValue(unit, match.variables)
            ca = self.__linkRepository.addOrGetLink(linkTo, unit, linkType)
            cas.append((ca,CONNECTION_NETWORK))

        return cas
        
    def applyRulesToFacts(self):
        for key in self.rules:
            self.writeDebug("Applying Rule: {}".format(key))
            rule = self.rules[key]

            matches = [MatchTree({},[])]
            for c in rule.conditions:
                matches = self.buildFounds(matches, c, rule)
                if(len(matches) == 0):
                    break

            self.writeDebug("Found {} Matches for Rule: {}".format(len(matches), key))

            for ma in matches:
                ruleCa = self.createRule(ma, rule)
                if(ruleCa == None):
                    continue

                self.addAssertions(rule.assertions, ma, ruleCa)
                self.addBaseAssertions(rule.baseAssertions, ma, ruleCa)
                self.addPrimeAssertions(rule.primeAssertions, ruleCa)
                self.addRetractions(rule.retractions, ma, ruleCa, rule.bases, rule.primes, rule.links)
                self.addLinkAssertions(rule.linkAssertions, ma, ruleCa)

                ca = self.getCas(ma, rule.bases, rule.primes, rule.links)
                self.__generator.setupActivations(self, ca, ruleCa)
            
    def writeDebug(self, msg):
        if(self.__debug):
            logging.info(msg)

    def save(self, fileName):
        dill.dump(self, open(fileName, "wb"))