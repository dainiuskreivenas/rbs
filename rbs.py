"""
Rule Based System using Nest Simulator
"""
import nealParams

if (nealParams.simulator=="spinnaker"):
    import pyNN.spiNNaker as sim
elif (nealParams.simulator=="nest"):
    import pyNN.nest as sim

from stateMachineClass import FSAHelperFunctions
fsa = FSAHelperFunctions(nealParams.simulator)

import pickle

class Fact:
    def __init__(self, group, attributes):
        self.group = group
        self.attributes = attributes
        self.ca = None
        self.index = -1

class Rule:
    def __init__(self, name, ifs, thens):
        self.name = name
        self.ifs = ifs
        self.thens = thens

    def extract(self):
        assertions = []
        retractions = []
        tests = []
        conditions = []

        for t in self.thens:
            option,item = t
            if(option == "assert"):
                assertions.append(item)
            elif(option == "retract"):
                retractions.append(item)

        for f in self.ifs:
            if(f[0] == "Test"):
                tests.append(f)
            else:
                conditions.append(f)

        return conditions,tests,assertions,retractions

class MatchTree:
    def __init__(self, variables, matches):
        self.variables = variables
        self.matches = matches

class SequentialRuleGenerator:

    def setupActivations(self, net, match, ruleNeuron):
        if len(match) == 1:
            net.caTurnsOnNeuron(match[0][0].ca, ruleNeuron)
        elif (len(match) == 2):
            net.twoCaTurnOnNeuron(match[0][0].ca, match[1][0].ca, ruleNeuron)
        else:
            index = 0

            pop1 = match[index][0].ca
            pop2 = match[index+1][0].ca

            intermediate = net.addTwoStateIntermediate(pop1,pop2)
            while(index < len(match)-2):
                pop3 = match[index+2][0].ca
                if(index == len(match)-3):
                    net.neuronAndCaTurnOnNeuron(intermediate, pop3, ruleNeuron)
                else:
                    inter2 = net.addNeuronAndStateIntermediate(intermediate, pop3)
                    intermediate = inter2

                index = index + 1
        
class ParallelRuleGenerator:
    def setupActivations(self, net, match, ruleNeuron):
        if len(match) == 1:
            net.caTurnsOnNeuron(match[0][0].ca, ruleNeuron)
        elif (len(match) == 2):
            net.twoCaTurnOnNeuron(match[0][0].ca, match[1][0].ca, ruleNeuron)
        else:
            index = 0

            pop1 = match[index][0].ca
            pop2 = match[index+1][0].ca

            intermediate = net.addTwoStateIntermediate(pop1,pop2)
            while(index < len(match)-2):
                pop3 = match[index+2][0].ca
                if(index == len(match)-3):
                    net.neuronAndCaTurnOnNeuron(intermediate, pop3, ruleNeuron)
                else:
                    inter2 = net.addNeuronAndStateIntermediate(intermediate, pop3)
                    intermediate = inter2

                index = index + 1

class RbsNetwork:
    def __init__(self, ruleGenerator = "sequential", fromFile = None):        
        if(fromFile != None):
            net = pickle.load(open(fromFile))
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
        
        if (ruleGenerator == "sequential"):
            self.ruleGenerator = SequentialRuleGenerator()
        elif (ruleGenerator == "parallel"):
            self.ruleGenerator = ParallelRuleGenerator()
        else:
            raise ValueError("Invalid Rule Generator: available options: [sequential, parallel]")

    def addNeuron(self):
        self.neuron += 1
        return self.neuron

    def addCA(self):
        start = self.neuron + 1
        self.neuron += 10

        connector = []
        #excitatory turn each other on
        for fromNeuron in range (start,start+(fsa.CA_SIZE-fsa.CA_INHIBS)):
            for toNeuron in range (start,start+(fsa.CA_SIZE-fsa.CA_INHIBS)):
                if (fromNeuron != toNeuron):
                    connector = connector + [(fromNeuron,toNeuron,fsa.INTRA_CA_WEIGHT, 1.0)]

        #excitatory turn on inhibitory
        for fromNeuron in range (start,start + fsa.CA_SIZE - fsa.CA_INHIBS):
            for toNeuron in range (start + fsa.CA_SIZE - fsa.CA_INHIBS,start + fsa.CA_SIZE):
                connector = connector + [(fromNeuron,toNeuron,fsa.INTRA_CA_TO_INHIB_WEIGHT, 1.0)]

        #inhibitory slows excitatory 
        for fromNeuron in range (start + fsa.CA_SIZE - fsa.CA_INHIBS, start + fsa.CA_SIZE):
            for toNeuron in range (start,start+fsa.CA_SIZE-fsa.CA_INHIBS):
                connector = connector + [(fromNeuron,toNeuron,fsa.INTRA_CA_FROM_INHIB_WEIGHT, 1.0)]

        self.connections += connector

        return range(start, self.neuron+1)

    def neuronToCa(self, neuron, ca, weight):
        for n in range(ca[0], ca[10-fsa.CA_INHIBS]):
            self.connections.append((neuron,n,weight,1.0))

    def neuronToNeruon(self, fromNeruon, toNeuron, weight):
        self.connections.append((fromNeruon,toNeuron,weight,1.0))

    def caToNeuron(self, ca, neuron, weight):
        for n in range(ca[0], ca[10-fsa.CA_INHIBS]):
            self.connections.append((n,neuron,weight,1.0))

    def caToCa(self, fromCa, toCa, weight):
        for n in range(fromCa[0], fromCa[10-fsa.CA_INHIBS]):
            for m in range(toCa[0], toCa[10-fsa.CA_INHIBS]):
                self.connections.append((n,m,weight,1.0))

    def neuronTurnsOffCa(self, fromNeuron, toCa):
        self.neuronToCa(fromNeuron, toCa, fsa.ONE_NEURON_STOPS_CA_WEIGHT)

    def neuronTurnsOnCa(self, fromNeuron, toCa):
        self.neuronToCa(fromNeuron, toCa, fsa.ONE_NEURON_STARTS_CA_WEIGHT)

    def neuronHalfTurnOnCa(self, fromNeuron, toNeuron):
        self.neuronToNeruon(fromNeuron, toNeuron, fsa.ONE_HALF_ON_ONE_WEIGHT)

    def caTurnsOnNeuron(self, fromCa, toNeuron):
        self.caToNeuron(fromCa, toNeuron, fsa.STATE_TO_ONE_WEIGHT)

    def caHalfTurnsOnNeuron(self, fromCa, toNeuron):
        self.caToNeuron(fromCa, toNeuron, fsa.HALF_ON_ONE_WEIGHT)

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

    def addFact(self, fact, active = True):
        group = self.getGroup(fact.group)
        fact.ca = self.addCA()
        self.factIndex += 1
        fact.index = self.factIndex
        group.append(fact)

        if(active):
            self.activations.append(fact.ca)

        self.applyRulesToFacts()

        return fact

    def getFact(self, fact):
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
            found = self.addFact(fact, active = False)
        
        return found

    def addRule(self, rule):
        self.rules[rule.name] = rule
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
        elif(op == "="):
            return left == right
        elif(op == "<>"):
            return left != right
        else:
            return False

    def buildFounds(self, matches, condition, tests):
        newTree = []
             
        for f in matches:
            search = self.getSearchExpression(condition, f.variables)
            founds = self.getMatchingFacts(search[0], search[1], search[2])

            if(founds == None):
                continue

            for found in founds:
                var = f.variables.copy()
                var = self.extractVariables(var, found, condition[2])

                treeItem = MatchTree(var, f.matches + [(found, condition[3])])

                testPass = True
                for test in tests:
                    testPass = self.testVariables(test, var)
                    if(testPass == False):
                        break

                if(testPass == False):
                    continue

                newTree.append(treeItem)

        return newTree

    def createRule(self, ma):
        label = ""
        for i,m in enumerate(ma.matches):
            if(i == 0):
                label = "{}".format(m[0].index)
            else:
                label = "{} and {}".format(label, m[0].index)

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
            rule = self.rules[key]
            
            conditions,tests,assertions,retractions = rule.extract()

            matches = [MatchTree({},[])]
            for c in conditions:
                matches = self.buildFounds(matches, c, tests)
                if(len(matches) == 0):
                    break 

            for ma in matches:
                ruleCa = self.createRule(ma)
                if(ruleCa == None):
                    continue

                if(len(assertions) > 0):
                    self.addAssertions(assertions, ma, ruleCa)
                if(len(retractions) > 0):
                    self.addRetractions(retractions, ma, ruleCa)

                self.ruleGenerator.setupActivations(self, ma.matches, ruleCa)
            
    def save(self, fileName):
        pickle.dump(self, open(fileName, "wb"))

class RbsNetWrapper:
    def __init__(self, net):
        self.net = net
        self.population = None
        self.neurons = net.neuron

class RbsPopulation:
    def __init__(self, neurons, fromIndex):
        self.pop = sim.Population(neurons, sim.IF_cond_exp, fsa.CELL_PARAMS)
        self.pop.record("spikes")
        self.fromIndex = fromIndex
        self.toIndex = fromIndex + neurons

class RbsExecutor:
    def __init__(self, net):
        self.net = net
        self.connections = 0
        self.populations = []
        self.neuron = 0
        self.actived = 0

    def getConnection(self, conn):
        fromPop = None
        toPop = None

        fromN = conn[0]
        toN = conn[1]

        for pop in self.populations:
            if(pop.fromIndex <= fromN and pop.toIndex > fromN):
                fromPop = pop
                if(toPop != None):
                    break
            
            if(pop.fromIndex <= toN and pop.toIndex > toN):
                toPop = pop
                if(fromPop != None):
                    break
        
        connector = (conn[0]-fromPop.fromIndex,conn[1]-toPop.fromIndex,conn[2],conn[3])
        connType = "excitatory"
        
        if(conn[2] < 0):
            connType = "inhibitory"
            if(nealParams.simulator == "spinnaker"):
                connector = (conn[0],conn[1],conn[2]*-1,conn[3])
        
        return (
            fromPop.pop,
            toPop.pop,
            connector,
            connType
        )

    def connect(self, connections):
        if(len(connections) > 0):
            excitatory = {}
            inhibitory = {}
            for c in connections:
                conn = self.getConnection(c)
                label = "{}{}".format(conn[0].label,conn[1].label)
                if(nealParams.simulator == "nest" or conn[3] == "excitatory"):
                    if(label in excitatory):
                        excitatory[label][2] = excitatory[label][2] + [conn[2]]
                    else:
                        excitatory[label] = [conn[0],conn[1],[conn[2]]]
                else:
                    if(label in inhibitory):
                        inhibitory[label][2] = inhibitory[label][2] + [conn[2]]
                    else:
                        inhibitory[label] = [conn[0],conn[1],[conn[2]]]
            
            for e in excitatory:
                ex = excitatory[e]
                conn = sim.FromListConnector(ex[2])
                sim.Projection(ex[0], ex[1], conn, receptor_type="excitatory")

            for i in inhibitory:
                inh = inhibitory[i]
                conn = sim.FromListConnector(inh[2])
                sim.Projection(inh[0], inh[1], conn, receptor_type="inhibitory")

    def apply(self):
        population = None
        connections = []

        addNeurons = 0
        if(self.neuron == 0):
            self.neuron += self.net.neuron + 1
            addNeurons = self.neuron
        else:
            addNeurons = self.net.neuron + 1 - self.neuron
            self.neuron += addNeurons

        if(addNeurons > 0):
            population = RbsPopulation(addNeurons, self.neuron - addNeurons)
            self.populations.append(population)

        connections = None
        if(self.connections == 0):
            connections = self.net.connections[:]
            self.connections = len(connections)
        else:
            start = self.connections-1
            connections = self.net.connections[start:]
            self.connections += len(connections)
        
        self.connect(connections)

        activate = []
        if(self.actived == 0):
            activate = self.net.activations
        else:
            activate = self.net.activations[self.actived:]

        if(len(activate) > 0):
            spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
            spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
            for a in activate:
                population = None
                for pop in self.populations:
                    if(pop.fromIndex <= a[0] and pop.toIndex > a[0]):
                        population = pop
                        break

                fsa.turnOnStateFromSpikeSource(spikeGen, population.pop, a[0]-population.fromIndex)
                self.actived += 1

class RBS:
    def __init__(self, ruleGenerator = "sequential", fromFile = None):
        self.net = RbsNetwork(ruleGenerator = ruleGenerator, fromFile=fromFile)
        self.exe = RbsExecutor(self.net)
        if(fromFile != None):
            self.exe.apply()

    def addFact(self, fact, active = True):
        fact = self.net.addFact(Fact(fact[0],fact[1]),active)
        self.exe.apply()
        return fact

    def getFact(self, fact):
        fact = self.net.getFact(Fact(fact[0],fact[1]))
        self.exe.apply()
        return fact

    def addRule(self, rule):
        self.net.addRule(Rule(rule[0],rule[1][0],rule[1][1]))
        self.exe.apply()

     
    def get_population(self, index):
        for pop in self.exe.populations:
            if(pop.fromIndex <= index and pop.toIndex > index):
                return pop
        return None

    def printSpikes(self):
        data = self.get_data()

        for a in self.exe.net.assertions:
            pop = self.get_population(self.net.assertions[a])
            d = data[pop.pop.label]            
            st = d.segments[0].spiketrains[self.net.assertions[a]-pop.fromIndex]
            if(len(st) > 0):
                print "({})".format(a)
                for s in st.magnitude:
                    print "{} {}".format(self.net.assertions[a], s)
        for a in self.net.interns:
            pop = self.get_population(a)
            d = data[pop.pop.label]
            st = d.segments[0].spiketrains[a-pop.fromIndex]
            if(len(st) > 0):
                print "({})".format(a)
                for s in st.magnitude:
                    print "{} {}".format(a, s)
        for g in self.net.facts:
            for f in self.net.facts[g]:
                print "(f-{} - {} {})".format(f.index, f.group, f.attributes)
                for n in f.ca:
                    pop = self.get_population(n)
                    d = data[pop.pop.label]
                    st = d.segments[0].spiketrains[n-pop.fromIndex]
                    if(len(st) > 0):
                        for s in st.magnitude:
                            print "{} {}".format(n, s)


    def get_data(self):
        data = {}
        for pop in self.exe.populations:
            data[pop.pop.label] = pop.pop.get_data()
        return data