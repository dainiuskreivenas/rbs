"""
Neural Cognitive Architecture
"""
from executor import Executor
from models import Fact, Rule

class NeuralCognitiveArchitecture:
    def __init__(self,
        exe,
        rulesService, 
        rulesRepository, 
        neuronRepository,
        internRepository,
        factGroupRepository, 
        factRepository, 
        assertionsRepository, 
        primeRepository, 
        linksRepository, 
        generator, 
        topology,
        baseService,
        propertyService,
        relationshipService,
        connectionService):
        self.exe = exe
        self.__rulesService = rulesService
        self.__rulesRepository = rulesRepository
        self.neuronRepository = neuronRepository
        self.__internRepository = internRepository
        self.__primeRepository = primeRepository
        self.__linksRepository = linksRepository
        self.factGroupRepository = factGroupRepository
        self.factRepository = factRepository
        self.__assertionsRepository = assertionsRepository
        self.__generator = generator
        self.__topology = topology
        self.__baseService = baseService
        self.__propertyService = propertyService
        self.__relationshipService = relationshipService
        self.connectionService = connectionService
        
    def apply(self):
        # generate network
        self.__rulesService.applyRulesToFacts(self.__generator)

        # build neurons
        self.exe.apply()

    def addFact(self, name, attributes, active = True):
        return self.factRepository.addFact(Fact(name, attributes), active)

    def getFact(self, group, attributes):
        return self.factRepository.getFact(Fact(group, attributes))

    def addRule(self, name, ifs, thens):
        self.__rulesRepository.addRule(Rule(name, ifs, thens))

    def __printCa(self, data, pop, caIndex):
        start = (caIndex-pop.fromIndex)*10
        end = start + 10
        for n in range(start, end):
            st = data.segments[0].spiketrains[n]
            if(len(st) > 0):
                for s in st.magnitude:
                    print("{} {}".format(n, s))

    def printSpikes(self):
        neuronData = self.get_neuron_data()
        caData = self.get_ca_data()

        assertions = self.__assertionsRepository.get()
        for a in assertions:
            assertion = assertions[a]
            pop = self.exe.getPopulationFromNeuron(assertion.neuronIndex)
            d = neuronData[pop.pop.label]
            st = d.segments[0].spiketrains[assertion.neuronIndex-pop.fromIndex]
            print("(Assertion: {})".format(a))
            if(len(st) > 0):
                for s in st.magnitude:
                    print("{} {}".format(assertion.neuronIndex, s))

        primes = self.__primeRepository.get()
        for p in primes:
            print("(Prime: {})".format(p))
            prime = primes[p]
            pop = self.exe.getPopulationFromCA(prime.caIndex)
            d = caData[pop.pop.label]
            self.__printCa(d, pop, prime.caIndex)

        links = self.__linksRepository.get()
        for linkTo in links:
            linkGroup = links[linkTo]
            for linkType in linkGroup:
                linkTypes = linkGroup[linkType]
                for unit in linkTypes:
                    print("(Link: {}, {}, {})".format(linkTo, unit, linkType))
                    link = linkTypes[unit]
                    pop = self.exe.getPopulationFromCA(link.caIndex)
                    d = caData[pop.pop.label]
                    self.__printCa(d, pop, link.caIndex)

        interns = self.__internRepository.get()
        for a in interns: 
            pop = self.exe.getPopulationFromNeuron(a.neuronIndex)
            d = neuronData[pop.pop.label]
            st = d.segments[0].spiketrains[a.neuronIndex-pop.fromIndex]
            print("(Intern: {})".format(a.neuronIndex))
            if(len(st) > 0):
                for s in st.magnitude:
                    print("{} {}".format(a.neuronIndex, s))

        groups = self.factGroupRepository.get()
        for g in groups:
            for f in groups[g]:
                print("(f-{} - {} {})".format(f.caIndex, f.group, f.attributes))
                pop = self.exe.getPopulationFromCA(f.caIndex)
                d = caData[pop.pop.label]
                self.__printCa(d, pop, f.caIndex)
        
        
        if(self.__topology):
            inheritanceData = self.__topology.neuralHierarchyTopology.cells.get_data()
            baseStructure = self.__baseService.getInheritance()
            for u in baseStructure.units:
                print("(Base: {})".format(u))
                index = baseStructure.getUnitNumber(u)
                for n in range(index*10,(index*10)+10):
                    st = inheritanceData.segments[0].spiketrains[n]
                    if(len(st) > 0):
                        for s in st.magnitude:
                            print("{} {}".format(n, s))

            propertyStructure = self.__propertyService.getStructure()
            propertyData = self.__topology.propertyCells.get_data()
            for u in propertyStructure.units:
                print("(Property: {})".format(u))
                index = propertyStructure.getUnitNumber(u)
                for n in range(index*10,(index*10)+10):
                    st = propertyData.segments[0].spiketrains[n]
                    if(len(st) > 0):
                        for s in st.magnitude:
                            print("{} {}".format(n, s))

            relationshipStructure = self.__relationshipService.getStructure()
            relationshipData = self.__topology.relationCells.get_data()
            for u in relationshipStructure.units:
                print("(Relationship: {})".format(u))
                index = relationshipStructure.getUnitNumber(u)
                for n in range(index*10,(index*10)+10):
                    st = relationshipData.segments[0].spiketrains[n]
                    if(len(st) > 0):
                        for s in st.magnitude:
                            print("{} {}".format(n, s))

    def get_ca_data(self):
        return self.exe.get_ca_data()

    def get_neuron_data(self):
        return self.exe.get_neuron_data()