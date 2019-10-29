"""
Rule Based System
"""
from executor import Executor
from contracts import Fact
from contracts import Rule

class NeuralCognitiveArchitecture:
    def __init__(self, 
        exe, 
        rulesService, 
        rulesRepository, 
        neuronRepository, 
        factGroupRepository, 
        factRepository, 
        assertionsRepository, 
        primeRepository, 
        linksRepository, 
        generator, 
        topology,
        baseService,
        propertyService,
        relationshipService):
        self.exe = exe
        self.__rulesService = rulesService
        self.__rulesRepository = rulesRepository
        self.__neuronRepository = neuronRepository
        self.__primeRepository = primeRepository
        self.__linksRepository = linksRepository
        self.__factGroupRepository = factGroupRepository
        self.__factRepository = factRepository
        self.__assertionsRepository = assertionsRepository
        self.__generator = generator
        self.__topology = topology
        self.__baseService = baseService
        self.__propertyService = propertyService
        self.__relationshipService = relationshipService
        

    def addFact(self, name, attributes, active = True, apply = True):
        fact = self.__factRepository.addFact(Fact(name, attributes), active)

        if(apply):
            self.__rulesService.applyRulesToFacts(self.__generator)
            self.exe.apply()

        return fact

    def getFact(self, group, attributes, autoApply = True):
        fact = self.__factRepository.getFact(Fact(group, attributes))

        if(autoApply):
            self.__rulesService.applyRulesToFacts(self.__generator)
            self.exe.apply()

        return fact

    def addRule(self, name, ifs, thens, autoApply = True):
        self.__rulesRepository.addRule(Rule(name, ifs, thens))

        if(autoApply):
            self.__rulesService.applyRulesToFacts(self.__generator)
            self.exe.apply()

    def printSpikes(self):
        data = self.get_data()

        assertions = self.__assertionsRepository.get()
        for a in assertions:
            pop = self.exe.get_population(assertions[a])
            d = data[pop.pop.label]            
            st = d.segments[0].spiketrains[assertions[a]-pop.fromIndex]
            print "(Assertion: {})".format(a)
            if(len(st) > 0):
                for s in st.magnitude:
                    print "{} {}".format(assertions[a], s)

        primes = self.__primeRepository.get()
        for p in primes:
            prime = primes[p]
            print "(Prime: {})".format(p)
            for n in prime:
                pop = self.exe.get_population(n)
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
                        pop = self.exe.get_population(n)
                        d = data[pop.pop.label]
                        st = d.segments[0].spiketrains[n-pop.fromIndex]
                        if(len(st) > 0):
                            for s in st.magnitude:
                                print "{} {}".format(n, s)

        interns = self.__neuronRepository.getInterns()
        for a in interns:  
            pop = self.exe.get_population(a)
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
                    pop = self.exe.get_population(n)
                    d = data[pop.pop.label]
                    st = d.segments[0].spiketrains[n-pop.fromIndex]
                    if(len(st) > 0):
                        for s in st.magnitude:
                            print "{} {}".format(n, s)
        
        
        if(self.__topology):
            inheritanceData = self.__topology.neuralHierarchyTopology.cells.get_data()

            baseStructure = self.__baseService.getInheritance()
            for u in baseStructure.units:
                print "(Base: {})".format(u)
                index = baseStructure.getUnitNumber(u)
                for n in range(index*10,(index*10)+10):
                    st = inheritanceData.segments[0].spiketrains[n]
                    if(len(st) > 0):
                        for s in st.magnitude:
                            print "{} {}".format(n, s)

            propertyStructure = self.__propertyService.getStructure()
            for u in propertyStructure.units:
                print "(Property: {})".format(u)
                index = propertyStructure.getUnitNumber(u)
                for n in range(index*10,(index*10)+10):
                    st = inheritanceData.segments[0].spiketrains[n]
                    if(len(st) > 0):
                        for s in st.magnitude:
                            print "{} {}".format(n, s)

            relationshipStructure = self.__relationshipService.getStructure()
            for u in relationshipStructure.units:
                print "(Relationship: {})".format(u)
                index = relationshipStructure.getUnitNumber(u)
                for n in range(index*10,(index*10)+10):
                    st = inheritanceData.segments[0].spiketrains[n]
                    if(len(st) > 0):
                        for s in st.magnitude:
                            print "{} {}".format(n, s)

        return data

    def get_data(self):
        return self.exe.get_data()