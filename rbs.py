"""
Rule Based System using Nest Simulator
"""
from nealCoverClass import NealCoverFunctions
from stateMachineClass import FSAHelperFunctions

from network.network import Network
from network.contracts.fact import Fact
from network.contracts.rule import Rule
from network.generators.sequentialRuleGenerator import SequentialRuleGenerator
from executor.executor import Executor

class RuleBasedSystem:
    def __init__(self, sim, simulator, spinnakerVersion = -1, debug = False):
        if(simulator not in ["nest", "spinnaker"]):
            raise Exception("simulator type: '{}' is invalid. Use one of the following: nest, spinnaker.".format(simulator)) 
        self.sim = sim
        self.simulator = simulator
        self.debug = debug
        self.spinnakerVersion = spinnakerVersion
        self.generator = SequentialRuleGenerator()
        self.fromFile = None
        self.basesFile = None

    def useRuleGenerator(self, generator):
        self.generator = generator
        return self

    def useStorageFile(self, file):
        self.fromFile = file
        return self

    def useBases(self, baseFile):
        self.basesFile = baseFile
        return self

    def buildNet(self):
        self.net = \
            self.net = \
                Network(self.fsa, self.generator, self.debug) \
                    .useStorageFile(self.fromFile) \

        self.net = self.net.build()

    def buildExe(self):
        self.exe = \
            self.exe = \
                Executor(self.sim, self.simulator, self.fsa, self.net, self.debug)
        
        self.exe = self.exe.build()

        if(self.fromFile != None):
            self.exe.apply()

    def build(self, runTime):
        self.runTime = runTime
        spinnVersion = -1

        self.neal = NealCoverFunctions(self.simulator, self.sim, spinnVersion)
        self.fsa = FSAHelperFunctions(self.simulator, self.sim,self.neal)

        self.buildNet()
        self.buildExe()

        return self
    
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
            print "({})".format(a)
            if(len(st) > 0):
                for s in st.magnitude:
                    print "{} {}".format(self.net.assertions[a], s)
        for a in self.net.interns:  
            pop = self.get_population(a)
            d = data[pop.pop.label]
            st = d.segments[0].spiketrains[a-pop.fromIndex]
            print "({})".format(a)
            if(len(st) > 0):
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

    def printAllSpikes(self):
        index = 0
        for pop in self.exe.populations:
            outFile = "temp" + str(index) + ".pkl"
            pop.pop.printSpikes(outFile)
            index = index + 1
