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

    def updateFact(self, factToUpdate,  fact):
        ca = sim.Population(fsa.CA_SIZE, sim.IF_cond_exp, fsa.CELL_PARAMS, label = fact)
        fsa.makeCA(ca, 0)
        ca.record("spikes")

        factToUpdate[1].append((fact[1][0],ca))

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

                    if(val == "?" and positive):
                        continue

                    if(isinstance(val,str) and list(val)[0] == "?"):
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
            if(len(prop) > 1 and prop[0] == "?" and prop not in var):
                var[prop] = found[0][i]
        return var

    def buildFounds(self, tree, item):
        newTree = []
        for f in tree:
            search = self.getSearch(item, f[0])
            founds = self.findMatches(search)
            if(founds == None):
                continue
            for found in founds:
                var = f[0].copy()
                var = self.extractVariables(var, found, item[2])
                newTree.append((var, f[1] + [(found,item[3])]))

        return newTree

    def applyRulesToFacts(self):
        for key in list(self.rules):
            rule = self.rules[key]
            ifs = rule[0]
            thens = rule[1]

            matches = [({},[])]
            for i in range(0, len(ifs)):
                matches = self.buildFounds(matches, ifs[i])

            for m in matches:
                for t in thens:
                    option,item = t
                    if(option == "assert"):
                        self.addAssertion(item, m)
                    elif(option == "retract"):
                        self.addRetraction(item, m[1]) 
                    else:
                        raise "Invalid Rule Configuration"

    def twoTurnOnOne(self,pop1,pop2,pop3):
        #print "[{} and {}] turns on [{}]".format(pop1.label,pop2.label,pop3.label)
        fsa.stateHalfTurnsOnState(pop1,0,pop3,0)
        fsa.stateHalfTurnsOnState(pop2,0,pop3,0)

    def addIntermediate(self, pop1, pop2):
        intermediate = sim.Population(fsa.CA_SIZE, sim.IF_cond_exp, fsa.CELL_PARAMS, label="{} and {}".format(pop1.label,pop2.label))
        intermediate.record("spikes")
        fsa.makeCA(intermediate, 0)
        self.twoTurnOnOne(pop1,pop2,intermediate)
        self.interns.append(intermediate)
        return intermediate

    def matchesTurnOnOperator(self, match, ca):
        if len(match) == 1:
            fsa.stateTurnsOnState(match[0][0][1],0,ca,0)
        elif (len(match) == 2):
            self.twoTurnOnOne(match[0][0][1],match[1][0][1],ca)
        else:
            index = 0

            pop1 = match[index][0][1]
            pop2 = match[index+1][0][1]

            intermediate = self.addIntermediate(pop1,pop2)
            while(index < len(match)-2):

                pop3 = match[index+2][0][1]

                if(index == len(match)-3):
                    self.twoTurnOnOne(intermediate,pop3,ca)
                    fsa.stateTurnsOffState(ca,0,intermediate,0)
                else:
                    inter2 = self.addIntermediate(intermediate,pop3)
                    fsa.stateTurnsOffState(inter2,0,intermediate,0)
                    intermediate = inter2

                index = index + 1

    def addAssertion(self, assertion, match):       
        label = ""
        for i,m in enumerate(match[1]):
            newLabel = "({} == {})".format(m[1],m[0][1].label)
            if (i == 0):
                label = label+newLabel
            else:
                label = label+" and "+newLabel

        if(label in self.assertions):
            return

        var = match[0]
        properties = assertion[1]
        newProps = []
        for p in properties:
            if(p in var):
                newProps.append(var[p])
            else:
                newProps.append(p)
        
        fact = (assertion[0],tuple(newProps))
        # allocate temporary before adding new fact
        self.assertions[label] = None

        # create new fact to be asserted
        fact = self.getFact(fact)
        
        #create assertion ca
        aaPop = sim.Population(fsa.CA_SIZE, sim.IF_cond_exp, fsa.CELL_PARAMS, label="{} asserts {}".format(label, fact[1].label))
        aaPop.record("spikes")
        fsa.makeCA(aaPop, 0)
        self.assertions[label] = aaPop
        
        #apply assertion
        fsa.stateTurnsOnState(aaPop,0,fact[1],0)
        fsa.stateTurnsOffState(aaPop,0,aaPop,0)

        self.matchesTurnOnOperator(match[1], aaPop)

    def addRetraction(self, retraction, match):
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
        rePop = sim.Population(fsa.CA_SIZE, sim.IF_cond_exp, fsa.CELL_PARAMS, label="{} retracts {}".format(label, retraction))
        rePop.record("spikes")
        fsa.makeCA(rePop, 0)
        self.retractions[label] = rePop
        fsa.stateTurnsOffState(rePop,0,rePop,0)
        
        #apply retraction
        for m in match:
            if m[1] == retraction:
                turnOfCa = m[0][1]       
        fsa.stateTurnsOffState(rePop, 0, turnOfCa, 0)

        self.matchesTurnOnOperator(match, rePop)

    
