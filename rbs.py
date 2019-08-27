"""
Rule Based System using Nest Simulator
"""
from stateMachineClass import FSAHelperFunctions
from network.network import Network
from network.contracts.fact import Fact
from network.contracts.rule import Rule
from network.generators.sequentialRuleGenerator import SequentialRuleGenerator
from executor.executor import Executor
from association.association import Association

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
        self.association = None

    def useRuleGenerator(self, generator):
        self.generator = generator
        return self

    def useStorageFile(self, file):
        self.fromFile = file
        return self

    def useAssociation(self, association):
        self.association = association
        return self

    def buildNet(self):
        self.net = \
            self.net = \
                Network(self.fsa, self.generator, self.debug) \
                    .useStorageFile(self.fromFile) \

        if(self.association):
            self.net = \
                self.net \
                    .useAssociation(self.association)
        
        self.net = self.net.build()

    def buildExe(self):
        self.exe = \
            self.exe = \
                Executor(self.sim, self.simulator, self.fsa, self.net, self.debug)
        
        if(self.association):
            self.exe = \
                self.exe \
                    .useAssociationTopology(self.association.topology.neuralHierarchyTopology)
        
        self.exe = self.exe.build()

        if(self.fromFile != None):
            self.exe.apply()

    def build(self):
        self.fsa = FSAHelperFunctions(self.sim, self.simulator)

        self.buildNet()
        self.buildExe()

        return self
    
    def addFact(self, name, attributes, active = True, apply = True):
        fact = self.net.addFact(Fact(name, attributes), active, apply)
        if(apply):
            self.exe.apply()
        return fact

    def getFact(self, group, attributes, apply = True):
        fact = self.net.getFact(Fact(group, attributes), apply)
        if(apply):
            self.exe.apply()
        return fact

    def addRule(self, name, ifs, thens, apply = True):
        self.net.addRule(Rule(name, ifs, thens), apply)
        if(apply):
            self.exe.apply()

    def get_population(self, index):
        for pop in self.exe.populations:
            if(pop.fromIndex <= index and pop.toIndex > index):
                return pop
        return None

    def printSpikes(self):
        data = self.get_data()

        for a in self.net.assertions:
            pop = self.get_population(self.net.assertions[a])
            d = data[pop.pop.label]            
            st = d.segments[0].spiketrains[self.net.assertions[a]-pop.fromIndex]
            print "(Assertion: {})".format(a)
            if(len(st) > 0):
                for s in st.magnitude:
                    print "{} {}".format(self.net.assertions[a], s)
        for p in self.net.primes:
            prime = self.net.primes[p]
            print "(Prime: {})".format(p)
            for n in prime:
                pop = self.get_population(n)
                d = data[pop.pop.label]
                st = d.segments[0].spiketrains[n-pop.fromIndex]
                if(len(st) > 0):
                    for s in st.magnitude:
                        print "{} {}".format(n, s)
        for linkTo in self.net.links:
            linkGroup = self.net.links[linkTo]
            for linkType in linkGroup:
                linkTypes = linkGroup[linkType]
                for unit in linkTypes:
                    link = linkTypes[unit]
                    print "(Link: {}, {}, {})".format(linkTo, unit, linkType)
                    for n in link:
                        pop = self.get_population(n)
                        d = data[pop.pop.label]
                        st = d.segments[0].spiketrains[n-pop.fromIndex]
                        if(len(st) > 0):
                            for s in st.magnitude:
                                print "{} {}".format(n, s)
        for a in self.net.interns:  
            pop = self.get_population(a)
            d = data[pop.pop.label]
            st = d.segments[0].spiketrains[a-pop.fromIndex]
            print "(Intern: {})".format(a)
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
        
        inheritanceData = self.association.topology.neuralHierarchyTopology.cells.get_data()
        if(self.association):
            for u in self.association.inheritance.units:
                print "(Base: {})".format(u)
                index = self.association.inheritance.getUnitNumber(u)
                for n in range(index*10,(index*10)+10):
                    st = inheritanceData.segments[0].spiketrains[n]
                    if(len(st) > 0):
                        for s in st.magnitude:
                            print "{} {}".format(n, s)

        return data

    def get_data(self):
        data = {}
        for pop in self.exe.populations:
            data[pop.pop.label] = pop.pop.get_data()
        return data