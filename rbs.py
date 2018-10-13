"""
Rule Based System using Nest Simulator
"""

from stateMachineClass import FSAHelperFunctions
import pyNN.nest as sim

fsa = FSAHelperFunctions("nest")

class RBS:

    def __init__(self):
        self.factGroups = {}
        self.rules = {}
        self.retractions = {}
        self.assertions = {}
        self.interns = []

    def findGroup(self, name):
        if(name not in self.factGroups):
            return None
        return self.factGroups[name]

    def getGroup(self, name):
        group = self.findGroup(name)
        if(group == None):
            group = []
            self.factGroups[name] = group
        
        return group

    def addFact(self, fact, active = True):
        group = self.getGroup(fact[0])

        ca = sim.Population(fsa.CA_SIZE, sim.IF_cond_exp, fsa.CELL_PARAMS, label = fact)
        fsa.makeCA(ca, 0)

        if(active):
            spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
            spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
            fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)

        ca.record("spikes")

        f = (fact[1],ca)
        group.append([f])

        self.applyRulesToFacts()

        return f

    def getFact(self, fact):
        group = self.getGroup(fact[0])

        found = None
        for f in group:
            match = True
            for i,p in enumerate(f[0][0]):
                if(p != fact[1][i]):
                    match = False
                    break
            if(match):
                found = f[0]
        
        if(found == None):
            found = self.addFact(fact, active = False)
        
        return found

    def addRule(self, rule):
        self.rules[rule[0]] = rule[1]
        self.applyRulesToFacts()


    def getMatchingFacts(self, positive,name,properties):
        if(name not in self.factGroups):
            return None
        
        group = self.factGroups[name]
        found = []

        for fact in group:
            match = True
            for propGroup in fact:
                for i,prop in enumerate(propGroup[0]):

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
                    found.append(propGroup)
                    
        return found

    def findMatches(self, precon):
        return self.getMatchingFacts(precon[0], precon[1], precon[2])

    def getSearch(self, item, variables):
        params = []            
        for p in item[2]:
            if(p in variables):
                params.append(variables[p])
            else:
                params.append(p)

        search = (item[0],item[1],tuple(params),item[3])

        return search

    def extractVariables(self, var, found, precon):
        for i,prop in enumerate(precon):
            if(isinstance(prop, str) and len(prop) > 1 and prop[0] == "?" and prop not in var):
                var[prop] = found[0][i]
        return var

    def buildFounds(self, tree, item, tests):
        newTree = []
        for f in tree:
            search = self.getSearch(item, f[0])
            founds = self.findMatches(search)

            if(founds == None):
                continue

            for found in founds:
                var = f[0].copy()
                var = self.extractVariables(var, found, item[2])
                treeItem = (var, f[1] + [(found,item[3])])

                testPass = True
                for test in tests:
                    testPass = self.testVariables(treeItem, test)
                    if(testPass == False):
                        break

                if(testPass == False):
                    continue

                newTree.append(treeItem)

        return newTree

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

    def testVariables(self, match, item):
        op = item[1]
        left = self.extractValue(item[2], match[0])
        right = self.extractValue(item[3], match[0])

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


    def addAssertions(self, asssertions, match):
        label = ""
        for i,m in enumerate(match[1]):
            newLabel = "({} == {})".format(m[1],m[0][1].label)
            if (i == 0):
                label = label+newLabel
            else:
                label = label+" and "+newLabel

        if(label in self.assertions):
            return

        facts = []
        for assertion in asssertions:
            variables = match[0]
            properties = assertion[1]
            newProps = []
            for p in properties:
                prop = self.extractValue(p, variables)
                newProps.append(prop)
        
            fact = (assertion[0],tuple(newProps))

            # allocate temporary before adding new fact
            self.assertions[label] = None

            # create new fact to be asserted
            fact = self.getFact(fact)
            facts.append(fact)
        
        #create assertion ca
        aaPop = sim.Population(1, sim.IF_cond_exp, fsa.CELL_PARAMS, label="{} asserts {}".format(label, fact[1].label))
        aaPop.record("spikes")
        self.assertions[label] = aaPop

        #apply assertion
        for fact in facts:
            fsa.oneNeuronTurnsOnState(aaPop,0,fact[1],0)

        return aaPop
    
    def addRetractions(self, retractions, match):
        label = ""
        for i,m in enumerate(match):
            newLabel = "({} == {})".format(m[1],m[0][1].label)
            if (i == 0):
                label = label+newLabel
            else:
                label = label+" and "+newLabel

        if(label in self.retractions):
            return

        #create retraction CA
        rePop = sim.Population(1, sim.IF_cond_exp, fsa.CELL_PARAMS, label="{} retracts {}".format(label, retractions))
        rePop.record("spikes")
        self.retractions[label] = rePop
        
        #apply retraction
        for retraction in retractions:
            for m in match: 
                if m[1] == retraction:
                    turnOfCa = m[0][1]
                    break
            fsa.oneNeuronTurnsOffState(rePop, 0, turnOfCa, 0)

        return rePop        


    def twoStatesTurnOnOneNueron(self, pop1, pop2, pop3):
        fsa.stateHalfTurnsOnOneNueron(pop1, 0, pop3, 0)
        fsa.stateHalfTurnsOnOneNueron(pop2, 0, pop3, 0)

    def neuronAndStateTurnsOnNeuron(self, pop1, pop2, pop3):
        fsa.oneNeuronHalfTurnsOnOneNeuron(pop1, 0, pop3, 0)
        fsa.stateHalfTurnsOnOneNueron(pop2, 0, pop3, 0)

    def addTwoStateIntermediate(self, pop1, pop2):
        intermediate = sim.Population(1, sim.IF_cond_exp, fsa.CELL_PARAMS, label="{} and {}".format(pop1.label,pop2.label))
        intermediate.record("spikes")
        self.twoStatesTurnOnOneNueron(pop1,pop2,intermediate)
        self.interns.append(intermediate)
        return intermediate

    def addNeuronAndStateIntermediate(self, pop1, pop2):
        intermediate = sim.Population(1, sim.IF_cond_exp, fsa.CELL_PARAMS, label="{} and {}".format(pop1.label,pop2.label))
        intermediate.record("spikes")
        self.neuronAndStateTurnsOnNeuron(pop1, pop2, intermediate)
        self.interns.append(intermediate)
        return intermediate

    def setUpActivations(self, match, aaPop, rePop):
        if len(match) == 1:
            if(aaPop != None): fsa.stateTurnsOnOneNeuron(match[0][0][1],0,aaPop,0)
            if(rePop != None): fsa.stateTurnsOnOneNeuron(match[0][0][1],0,rePop,0)
        elif (len(match) == 2):
            if(aaPop != None): self.twoStatesTurnOnOneNueron(match[0][0][1],match[1][0][1],aaPop)
            if(rePop != None): self.twoStatesTurnOnOneNueron(match[0][0][1],match[1][0][1],rePop)
        else:
            index = 0

            pop1 = match[index][0][1]
            pop2 = match[index+1][0][1]

            intermediate = self.addTwoStateIntermediate(pop1,pop2)
            while(index < len(match)-2):
                pop3 = match[index+2][0][1]
                if(index == len(match)-3):
                    if(aaPop != None): self.neuronAndStateTurnsOnNeuron(intermediate, pop3, aaPop)
                    if(rePop != None): self.neuronAndStateTurnsOnNeuron(intermediate, pop3, rePop)
                else:
                    inter2 = self.addNeuronAndStateIntermediate(intermediate, pop3)
                    intermediate = inter2

                index = index + 1


    def applyRulesToFacts(self):
        for key in list(self.rules):
            rule = self.rules[key]
            ifs = rule[0]
            thens = rule[1]

            assertions = []
            retractions = []
            for t in thens:
                option,item = t
                if(option == "assert"):
                    assertions.append(item)
                elif(option == "retract"):
                    retractions.append(item)
                else:
                    raise "Invalid Rule Configuration"

            tests = []
            conditions = []
            for i in range(0, len(ifs)):
                if(ifs[i][0] == "Test"):
                    tests.append(ifs[i])
                else:
                    conditions.append(ifs[i])

            matches = [({},[])]
            for i in range(0, len(conditions)):
                matches = self.buildFounds(matches, conditions[i], tests)      
                if(len(matches) == 0):
                    break;        

            for m in matches:
                aaPop = None
                rePop = None

                if(len(assertions) > 0):
                    aaPop = self.addAssertions(assertions, m)
                if(len(retractions) > 0):
                    rePop = self.addRetractions(retractions, m[1])

                self.setUpActivations(m[1],aaPop,rePop)