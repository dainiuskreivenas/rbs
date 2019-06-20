"""
Rule Based System using Nest Simulator
"""
from stateMachineClass import FSAHelperFunctions
from network.network import Network
from network.contracts.fact import Fact
from network.contracts.rule import Rule
from network.contracts.population import Population
from network.generators.sequentialRuleGenerator import SequentialRuleGenerator
from network.executor import Executor

class RBS:
    def __init__(self, sim, simulator = "nest", ruleGenerator = SequentialRuleGenerator(), fromFile = None, debug = False):
        fsa = FSAHelperFunctions(sim, simulator)
        self.net = Network(fsa, ruleGenerator, fromFile=fromFile, debug=debug)
        self.exe = Executor(sim, simulator, fsa, self.net, debug=debug)
        if(fromFile != None):
            self.exe.apply()

    def addFact(self, fact, active = True, apply = True):
        fact = self.net.addFact(Fact(fact[0],fact[1]), active, apply)
        if(apply):
            self.exe.apply()
        return fact

    def getFact(self, fact, apply = True):
        fact = self.net.getFact(Fact(fact[0],fact[1]), apply)
        if(apply):
            self.exe.apply()
        return fact

    def addRule(self, rule, apply = True):
        self.net.addRule(Rule(rule[0],rule[1][0],rule[1][1]), apply)
        if(apply):
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

        return data


    def get_data(self):
        data = {}
        for pop in self.exe.populations:
            data[pop.pop.label] = pop.pop.get_data()
        return data