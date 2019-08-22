import dill
import logging
from contracts.matchTree import MatchTree
from contracts.fact import Fact
from generators.constants import *
from helpers.connectivityHelper import *

class Network:
    def __init__(self, fsa, ruleGenerator, debug = False):
        self.fsa = fsa
        self.generator = ruleGenerator
        self.debug = debug
        self.fromFile = None
        self.inheritanceStructure = None

    def useStorageFile(self, file):
        self.fromFile = file
        return self

    def useInheritanceStructure(self, inheritanceStructure):
        self.inheritanceStructure = inheritanceStructure
        return self

    def build(self):
        if(self.fromFile != None):
            return dill.load(open(self.fromFile))
        else:
            self.facts = {}
            self.rules = {}
            self.assertions = {}
            self.interns = []
            self.bases = {}
            self.neuron = -1
            self.factIndex = 0
            self.connections = []
            self.activations = []
            return self

    def addNeuron(self):
        self.neuron += 1
        return self.neuron

    def addCA(self):
        start = self.neuron + 1
        self.neuron += 10

        makeCA(
            self.connections,
            self.fsa.CA_SIZE, 
            self.fsa.CA_INHIBS,
            start,
            self.fsa.INTRA_CA_WEIGHT,
            self.fsa.INTRA_CA_TO_INHIB_WEIGHT,
            self.fsa.INTRA_CA_FROM_INHIB_WEIGHT)

        return range(start, self.neuron+1)

    def neuronTurnsOffCa(self, fromNeuron, toCa, connectionType):
        neuronToCa(self.connections, self.fsa.CA_SIZE, self.fsa.CA_INHIBS, fromNeuron, toCa, self.fsa.ONE_NEURON_STOPS_CA_WEIGHT, connectionType)

    def neuronTurnsOnCa(self, fromNeuron, toCa, connectionType):
        neuronToCa(self.connections, self.fsa.CA_SIZE, self.fsa.CA_INHIBS, fromNeuron, toCa, self.fsa.ONE_NEURON_STARTS_CA_WEIGHT, connectionType)

    def neuronHalfTurnOnCa(self, fromNeuron, toNeuron, connectionType):
        neuronToNeruon(self.connections, fromNeuron, toNeuron, self.fsa.ONE_HALF_ON_ONE_WEIGHT, connectionType)

    def caTurnsOnNeuron(self, fromCa, toNeuron, connectionType):
        caToNeuron(self.connections, self.fsa.CA_SIZE, self.fsa.CA_INHIBS, fromCa, toNeuron, self.fsa.STATE_TO_ONE_WEIGHT, connectionType)

    def caHalfTurnsOnNeuron(self, fromCa, toNeuron, connectionType):
        caToNeuron(self.connections, self.fsa.CA_SIZE, self.fsa.CA_INHIBS, fromCa, toNeuron, self.fsa.HALF_ON_ONE_WEIGHT, connectionType)

    def twoCaTurnOnNeuron(self, fromOne, fromTwo, toNeuron, firstConnectionType, secondConnectionType):
        self.caHalfTurnsOnNeuron(fromOne, toNeuron, firstConnectionType)
        self.caHalfTurnsOnNeuron(fromTwo, toNeuron, secondConnectionType)

    def neuronAndCaTurnOnNeuron(self, fromNeuron, fromCa, toNeuron, neuronConnectionType, caConnectionType):
        self.neuronHalfTurnOnCa(fromNeuron,toNeuron, neuronConnectionType)
        self.caHalfTurnsOnNeuron(fromCa,toNeuron, caConnectionType)

    def addTwoStateIntermediate(self, pop1, pop2, firstConnectionType, secondConnectionType):
        intermediate = self.addNeuron()
        self.twoCaTurnOnNeuron(pop1,pop2,intermediate, firstConnectionType, secondConnectionType)
        self.interns.append(intermediate)
        return intermediate

    def addNeuronAndStateIntermediate(self, pop1, pop2, neuronConnectionType, caConnectionType):
        intermediate = self.addNeuron()
        self.neuronAndCaTurnOnNeuron(pop1, pop2, intermediate, neuronConnectionType, caConnectionType)
        self.interns.append(intermediate)
        return intermediate

    def findGroup(self, name):
        if(name not in self.facts):
            return None
        return self.facts[name]

    def getGroup(self, name):
        group = self.findGroup(name)
        if(group == None):
            group = []
            self.facts[name] = group
        return group

    def addFact(self, fact, active = True, applyRules = True):
        group = self.getGroup(fact.group)
        fact.ca = self.addCA()
        self.factIndex += 1
        fact.index = self.factIndex
        group.append(fact)

        if(active):
            self.activations.append(fact.ca)

        if(applyRules):
            self.applyRulesToFacts()

        return fact

    def getFact(self, fact, applyRules = True):
        group = self.getGroup(fact.group)

        found = None
        for f in group:
            match = True
            for i,p in enumerate(f.attributes):
                if(p != fact.attributes[i]):
                    match = False
                    break
            if(match):
                found = f
        
        if(found == None):
            found = self.addFact(fact, False, applyRules)
        
        return found

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
        if(name not in self.facts):
            return None
        
        group = self.facts[name]
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

    def extractVariables(self, var, found, precon):
        for i,prop in enumerate(precon):
            if(isinstance(prop, str) and len(prop) > 1 and prop[0] == "?" and prop not in var):
                var[prop] = found.attributes[i]
        return var

    def extractValue(self, item, match):
        if(isinstance(item, tuple)):
            c = item[0]
            left = item[1]
            right = item[2]
            if(isinstance(left, str) and left[0] == "?"):
                left = match[left]
            
            if(isinstance(right, str) and right[0] == "?"):
                right = match[right]

            if(c == "+"):
                value = left + right
            elif(c == "-"):
                value = left - right
            elif(c == "*"):
                value = left * right
            elif(c == "/"):
                value = left / right
        else:
            if(isinstance(item, str) and item[0] == "?"):
                if(item in match):
                    value = match[item]
                else:
                    value = None
            else:
                value = item
        
        return value

    def testVariables(self, item, var):
        op = item[1]
        left = self.extractValue(item[2], var)
        right = self.extractValue(item[3], var)

        if(left == None):
            return True
        if(right == None):
            return True

        if(op == ">"):
            return left > right
        elif(op == "<"):
            return left < right
        elif(op == "=" or op == "=="):
            return left == right
        elif(op == "<>" or op == "!="):
            return left != right
        else:
            return False

    def buildFounds(self, matches, condition, tests, bases):
        newTree = []
        existing = []

        if(self.inheritanceStructure):
            for base in bases:
                if(not self.inheritanceStructure.inUnits(base[1])):
                    return newTree
             
        for f in matches:
            search = self.getSearchExpression(condition, f.variables)
            founds = self.getMatchingFacts(search[0], search[1], search[2])

            if(founds == None):
                continue

            for found in founds:
                var = f.variables.copy()
                var = self.extractVariables(var, found, condition[2])

                treeItem = MatchTree(var, f.matches + [(found, condition[3])])
                if(treeItem.label in existing):
                    continue

                testPass = True
                for test in tests:
                    testPass = self.testVariables(test, var)
                    if(testPass == False):
                        break

                if(testPass == False):
                    continue
                
                existing.append(treeItem.label)

                newTree.append(treeItem)

        return newTree

    def createRule(self, ma, assertions, retractions, bases):
        label = ""

        indexes = []
        for m in ma.matches:
            indexes.append(m[0].index)
        indexes.sort()

        for i,m in enumerate(indexes):
            if(i == 0):
                label = "{}".format(m)
            else:
                label = "{} and {}".format(label, m)

        if(len(assertions) > 0):
            label += " => "
            variables = ma.variables

            for i,a in enumerate(assertions):
                properties = a[1]
                newProps = []

                for p in properties:
                    prop = self.extractValue(p, variables)
                    newProps.append(prop)

                if(i == 0):
                    label += "{}".format((a[0],tuple(newProps)))
                else:
                    label += " and {}".format((a[0],tuple(newProps)))

        if(len(retractions) > 0):
            label += " <= "
            for i,a in enumerate(retractions):
                f = None
                for m in ma.matches:
                    if m[1] == a:
                        f = m[0]
                        break
                
                if(f == None):
                    for b in bases:
                        if(b[3] == a):
                            text = "({}, {}, {})".format(b[0], b[1], b[2])
                            break
                else:
                    text = "({}, {})".format(f.group, f.attributes)

                if(i == 0):
                    label += text
                else:
                    label += " and {}".format(text)

        if(label in self.assertions):
            return None

        rulePop = self.addNeuron()
        self.assertions[label] = rulePop

        return rulePop

    def addAssertions(self, asssertions, match, rulePop):
        for assertion in asssertions:
            variables = match.variables
            properties = assertion[1]
            newProps = []

            for p in properties:
                prop = self.extractValue(p, variables)
                newProps.append(prop)
        
            fact = Fact(assertion[0],tuple(newProps))
            fact = self.getFact(fact)

            self.neuronTurnsOnCa(rulePop, fact.ca, CONNECTION_NETWORK)

    def addRetractions(self, retractions, match, ruleCa, bases):
        for retraction in retractions:
            applied = False

            for m in match.matches:
                if m[1] == retraction:
                    self.neuronTurnsOffCa(ruleCa, m[0].ca, CONNECTION_NETWORK)
                    applied = True
                    break

            if(applied == False):
                for b in bases:
                    if(b[3] == retraction):
                        if(b[2] == "amToFact"):
                            self.neuronTurnsOffCa(ruleCa, self.getBase(b[1]), CONNECTION_NETWORK)
                        elif(b[2] == "factToAm"):
                            self.neuronTurnsOffCa(ruleCa, self.caFromUnit(b[1]), CONNECTION_NETWORK_INHERITANCE)
                        elif(b[2] == "correlated"):
                            self.neuronTurnsOffCa(ruleCa, self.getBase(b[1]), CONNECTION_NETWORK)
                            self.neuronTurnsOffCa(ruleCa, self.caFromUnit(b[1]), CONNECTION_NETWORK_INHERITANCE)
                        else:
                            raise "Invalid link type: '{}'. Available values: 'amToFact', 'factToAm' and 'correlated'.".format(b[2])

                        break

    def addBaseAssertions(self, baseAssertions, ruleCa):
        for assertion in baseAssertions:
            assertionType = assertion[1]

            if(assertionType == "am"):
                ca = self.inheritanceStructure.caFromUnit(assertion[0])
                connType = CONNECTION_NETWORK_INHERITANCE
            elif(assertionType == "fact"):
                ca = self.getBase(assertion[0])
                connType = CONNECTION_NETWORK
            else:
                raise "Base assertion type: '{}' is invalid.".format(assertionType)
            
            self.neuronTurnsOnCa(ruleCa, ca, connType)

    def caFromUnit(self, unit):
        unit = self.inheritanceStructure.getUnitNumber(unit)
        start = (unit * self.fsa.CA_SIZE)
        return range(start, start + 10)

    def getBase(self, unit):
        if(unit in self.bases):
            ca = self.bases[unit]
        else:
            ca = self.addCA()
            self.bases[unit] = ca
        return ca

    def getCas(self, match, bases):
        cas = []
        for m in match:
            cas.append(m[0].ca)
        
        for a in bases:

            amCa = self.caFromUnit(a[1])
            ca = self.getBase(a[1])

            if(a[2] == "amToFact"):
                caToCa(self.connections, self.fsa.CA_SIZE, self.fsa.CA_INHIBS, amCa, ca, self.fsa.FULL_ON_WEIGHT, CONNECTION_INHERITANCE_NETWORK)
            elif(a[2] == "factToAm"):
                caToCa(self.connections, self.fsa.CA_SIZE, self.fsa.CA_INHIBS, ca, amCa, self.fsa.FULL_ON_WEIGHT, CONNECTION_NETWORK_INHERITANCE)
            elif(a[2] == "correlated"):
                caToCa(self.connections, self.fsa.CA_SIZE, self.fsa.CA_INHIBS, ca, amCa, self.fsa.FULL_ON_WEIGHT, CONNECTION_NETWORK_INHERITANCE)
                caToCa(self.connections, self.fsa.CA_SIZE, self.fsa.CA_INHIBS, amCa, ca, self.fsa.FULL_ON_WEIGHT, CONNECTION_INHERITANCE_NETWORK)
            else:
                raise "Invalid link type: '{}'. Available values: 'amToFact', 'factToAm' and 'correlated'.".format(a[2])

            cas.append(ca)
        return cas

    def applyRulesToFacts(self):
        for key in self.rules:
            
            self.writeDebug("Applying Rule: {}".format(key))

            rule = self.rules[key]
            
            conditions,tests,bases,assertions,retractions,baseAssertions = rule.extract()

            matches = [MatchTree({},[])]
            for c in conditions:
                matches = self.buildFounds(matches, c, tests, bases)
                if(len(matches) == 0):
                    break

            self.writeDebug("Found {} Matches for Rule: {}".format(len(matches), key))

            for ma in matches:
                ruleCa = self.createRule(ma, assertions, retractions, bases)
                if(ruleCa == None):
                    continue

                if(len(assertions) > 0):
                    self.addAssertions(assertions, ma, ruleCa)
                if(len(retractions) > 0):
                    self.addRetractions(retractions, ma, ruleCa, bases)
                if(len(baseAssertions) > 0):
                    self.addBaseAssertions(baseAssertions, ruleCa)

                ca = self.getCas(ma.matches, bases)
                self.generator.setupActivations(self, ca, ruleCa)
            
    def writeDebug(self, msg):
        if(self.debug):
            logging.info(msg)

    def save(self, fileName):
        dill.dump(self, open(fileName, "wb"))