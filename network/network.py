import dill
import logging
from contracts.matchTree import MatchTree
from contracts.fact import Fact

class Network:
    def __init__(self, fsa, ruleGenerator, fromFile = None, debug = False):
        self.fsa = fsa
        self.ruleGenerator = ruleGenerator
        self.debug = debug

        if(fromFile != None):
            net = dill.load(open(fromFile))
            self.facts = net.facts
            self.rules = net.rules
            self.assertions = net.assertions
            self.interns = net.interns
            self.neuron = net.neuron
            self.factIndex = net.factIndex
            self.connections = net.connections
            self.activations = net.activations
            self.generator = net.generator
            ruleGenerator = net.generator
        else:
            self.generator = ruleGenerator
            self.facts = {}
            self.rules = {}
            self.assertions = {}
            self.interns = []
            self.neuron = -1
            self.factIndex = 0
            self.connections = []
            self.activations = []

    def addNeuron(self):
        self.neuron += 1
        return self.neuron

    def addCA(self):
        start = self.neuron + 1
        self.neuron += 10

        connector = []
        #excitatory turn each other on
        for fromNeuron in range (start,start+(self.fsa.CA_SIZE-self.fsa.CA_INHIBS)):
            for toNeuron in range (start,start+(self.fsa.CA_SIZE-self.fsa.CA_INHIBS)):
                if (fromNeuron != toNeuron):
                    connector = connector + [(fromNeuron,toNeuron,self.fsa.INTRA_CA_WEIGHT, 1.0)]

        #excitatory turn on inhibitory
        for fromNeuron in range (start,start + self.fsa.CA_SIZE - self.fsa.CA_INHIBS):
            for toNeuron in range (start + self.fsa.CA_SIZE - self.fsa.CA_INHIBS,start + self.fsa.CA_SIZE):
                connector = connector + [(fromNeuron,toNeuron,self.fsa.INTRA_CA_TO_INHIB_WEIGHT, 1.0)]

        #inhibitory slows excitatory 
        for fromNeuron in range (start + self.fsa.CA_SIZE - self.fsa.CA_INHIBS, start + self.fsa.CA_SIZE):
            for toNeuron in range (start,start+self.fsa.CA_SIZE-self.fsa.CA_INHIBS):
                connector = connector + [(fromNeuron,toNeuron,self.fsa.INTRA_CA_FROM_INHIB_WEIGHT, 1.0)]

        self.connections += connector

        return range(start, self.neuron+1)

    def neuronToCa(self, neuron, ca, weight):
        for n in range(ca[0], ca[10-self.fsa.CA_INHIBS]):
            self.connections.append((neuron,n,weight,1.0))

    def neuronToNeruon(self, fromNeruon, toNeuron, weight):
        self.connections.append((fromNeruon,toNeuron,weight,1.0))

    def caToNeuron(self, ca, neuron, weight):
        for n in range(ca[0], ca[10-self.fsa.CA_INHIBS]):
            self.connections.append((n,neuron,weight,1.0))

    def caToCa(self, fromCa, toCa, weight):
        for n in range(fromCa[0], fromCa[10-self.fsa.CA_INHIBS]):
            for m in range(toCa[0], toCa[10-self.fsa.CA_INHIBS]):
                self.connections.append((n,m,weight,1.0))

    def neuronTurnsOffCa(self, fromNeuron, toCa):
        self.neuronToCa(fromNeuron, toCa, self.fsa.ONE_NEURON_STOPS_CA_WEIGHT)

    def neuronTurnsOnCa(self, fromNeuron, toCa):
        self.neuronToCa(fromNeuron, toCa, self.fsa.ONE_NEURON_STARTS_CA_WEIGHT)

    def neuronHalfTurnOnCa(self, fromNeuron, toNeuron):
        self.neuronToNeruon(fromNeuron, toNeuron, self.fsa.ONE_HALF_ON_ONE_WEIGHT)

    def caTurnsOnNeuron(self, fromCa, toNeuron):
        self.caToNeuron(fromCa, toNeuron, self.fsa.STATE_TO_ONE_WEIGHT)

    def caHalfTurnsOnNeuron(self, fromCa, toNeuron):
        self.caToNeuron(fromCa, toNeuron, self.fsa.HALF_ON_ONE_WEIGHT)

    def twoCaTurnOnNeuron(self, fromOne, fromTwo, toNeuron):
        self.caHalfTurnsOnNeuron(fromOne, toNeuron)
        self.caHalfTurnsOnNeuron(fromTwo, toNeuron)

    def neuronAndCaTurnOnNeuron(self, fromNeuron, fromCa, toNeuron):
        self.neuronHalfTurnOnCa(fromNeuron,toNeuron)
        self.caHalfTurnsOnNeuron(fromCa,toNeuron)

    def addTwoStateIntermediate(self, pop1, pop2):
        intermediate = self.addNeuron()
        self.twoCaTurnOnNeuron(pop1,pop2,intermediate)
        self.interns.append(intermediate)
        return intermediate

    def addNeuronAndStateIntermediate(self, pop1, pop2):
        intermediate = self.addNeuron()
        self.neuronAndCaTurnOnNeuron(pop1, pop2, intermediate)
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

    def buildFounds(self, matches, condition, tests):
        newTree = []
        existing = []
             
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

    def createRule(self, ma, assertions, retractions):
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
                if(i == 0):
                    label += "({}, {})".format(f.group, f.attributes)
                else:
                    label += " and ({}, {})".format(f.group, f.attributes)

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

            self.neuronTurnsOnCa(rulePop, fact.ca)

    def addRetractions(self, retractions, match, ruleCa):
        for retraction in retractions:
            for m in match.matches:
                if m[1] == retraction:
                    turnOfCa = m[0].ca
                    break
            self.neuronTurnsOffCa(ruleCa, turnOfCa)

    def applyRulesToFacts(self):
        for key in self.rules:
            
            self.writeDebug("Applying Rule: {}".format(key))

            rule = self.rules[key]
            
            conditions,tests,assertions,retractions = rule.extract()

            matches = [MatchTree({},[])]
            for c in conditions:
                matches = self.buildFounds(matches, c, tests)
                if(len(matches) == 0):
                    break 

            self.writeDebug("Found {} Matches for Rule: {}".format(len(matches), key))

            for ma in matches:
                ruleCa = self.createRule(ma, assertions, retractions)
                if(ruleCa == None):
                    continue

                if(len(assertions) > 0):
                    self.addAssertions(assertions, ma, ruleCa)
                if(len(retractions) > 0):
                    self.addRetractions(retractions, ma, ruleCa)

                self.ruleGenerator.setupActivations(self, ma.matches, ruleCa)
            

    def writeDebug(self, msg):
        if(self.debug):
            logging.info(msg)

    def save(self, fileName):
        dill.dump(self, open(fileName, "wb"))