"""
Rule Based System
"""
from network import Network
from executor import Executor
from contracts.fact import Fact
from contracts.rule import Rule

class RuleBasedSystem: 
    def __init__(self, net, exe, association, neuronRepository, factGroupRepository, primeRepository, linksRepository):
        self.net = net
        self.exe = exe
        self.__association = association
        self.__neuronRepository = neuronRepository
        self.__primeRepository = primeRepository
        self.__linksRepository = linksRepository
        self.__factGroupRepository = factGroupRepository

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

        primes = self.__primeRepository.get()
        for p in primes:
            prime = primes[p]
            print "(Prime: {})".format(p)
            for n in prime:
                pop = self.get_population(n)
                d = data[pop.pop.label]
                st = d.segments[0].spiketrains[n-pop.fromIndex]
                if(len(st) > 0):
                    for s in st.magnitude:
                        print "{} {}".format(n, s)

        links = self.__linksRepository.get()
        for linkTo in links:
            linkGroup = links[linkTo]
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

        interns = self.__neuronRepository.getInterns()
        for a in interns:  
            pop = self.get_population(a)
            d = data[pop.pop.label]
            st = d.segments[0].spiketrains[a-pop.fromIndex]
            print "(Intern: {})".format(a)
            if(len(st) > 0):
                for s in st.magnitude:
                    print "{} {}".format(a, s)

        groups = self.__factGroupRepository.get()
        for g in groups:
            for f in groups[g]:
                print "(f-{} - {} {})".format(f.index, f.group, f.attributes)
                for n in f.ca:
                    pop = self.get_population(n)
                    d = data[pop.pop.label]
                    st = d.segments[0].spiketrains[n-pop.fromIndex]
                    if(len(st) > 0):
                        for s in st.magnitude:
                            print "{} {}".format(n, s)
        
        inheritanceData = self.__association.topology.neuralHierarchyTopology.cells.get_data()
        if(self.__association):
            for u in self.__association.inheritance.units:
                print "(Base: {})".format(u)
                index = self.__association.inheritance.getUnitNumber(u)
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