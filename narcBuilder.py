from executorBuilder import ExecutorBuilder
from narc import NeuralCognitiveArchitecture
from generators import SequentialRuleGenerator
from repositories import *
from services import *
from lib import NeuralThreeAssocClass

class NeuralCognitiveArchitectureBuilder:
    def __init__(self, sim, simulator, fsa, neal, spinnakerVersion = -1, debug = False):
        if(simulator not in ["nest", "spinnaker"]):
            raise Exception("simulator type: '{}' is invalid. Use one of the following: nest, spinnaker.".format(simulator)) 
        self.__sim = sim
        self.__fsa = fsa
        self.__neal = neal
        self.__simulator = simulator
        self.__debug = debug
        self.__spinnakerVersion = spinnakerVersion
        self.__bases = None
        self.__properties = None
        self.__relationships = None
        self.__associations = None
        self.__topology = None
        self.__baseService = None
        self.__propertyService = None
        self.__relationshipService = None
        self.__generatorType = None
        self.__generator = None

    def useBases(self, bases):
        self.__bases = bases
        return self

    def useRelationships(self, properties, relationships, associations):
        self.__properties = properties
        self.__relationships = relationships
        self.__associations = associations
        return self

    def build(self):
        self.__initDependencies()

        generator = self.__getGenerator()
        exe = self.__buildExe()

        return NeuralCognitiveArchitecture(exe,
            self.__rulesService,
            self.__rulesRepository,
            self.__neuronRepository,
            self.__factGroupRepository,
            self.__factRepository,
            self.__assertionRepository,
            self.__primeRepository,
            self.__linkRepository,
            generator,
            self.__topology,
            self.__baseService,
            self.__propertyService,
            self.__relationshipService)
    
    def __initDependencies(self):
        if(self.__bases and self.__relationships and self.__associations):
            self.__topology = NeuralThreeAssocClass(self.__simulator, self.__sim, self.__neal, self.__spinnakerVersion, self.__fsa)

        if(self.__bases):
            self.__baseService = BaseService(self.__fsa, self.__bases)
            self.__topology.createBaseNet(self.__baseService.getInheritance())
        
        if(self.__properties and self.__relationships and self.__associations):
            self.__propertyService = UnitService(self.__fsa, self.__properties)
            self.__relationshipService = UnitService(self.__fsa, self.__relationships)
            self.__associationService = AssociationService(self.__associations)
            self.__topology.createAssociationTopology(self.__propertyService.getStructure(), self.__relationshipService.getStructure())
            self.__topology.addAssociations(self.__associationService.getAssociations())

        self.__logger = LoggerService(self.__debug)
        self.__connectionsRepository = ConnectionsRepository()
        self.__connectionsService = ConnectionsService(self.__fsa, self.__connectionsRepository)
        self.__neuronRepository = NeuronRepository(self.__connectionsService)
        self.__linkRepository = LinkRepository(self.__neuronRepository, self.__connectionsService, self.__baseService, self.__propertyService, self.__relationshipService)
        self.__factGroupRepository = FactGroupRepository()
        self.__activationsRepository = ActivationsRepository()
        self.__factRepository = FactRepository(self.__factGroupRepository, self.__neuronRepository, self.__activationsRepository)
        self.__primeRepository = PrimeRepository(self.__neuronRepository, self.__connectionsService, self.__baseService, self.__propertyService, self.__relationshipService)
        self.__assertionRepository = AssertionRepository(self.__neuronRepository)
        self.__rulesRepository = RulesRepository()
        self.__rulesService = RulesService(self.__rulesRepository, 
            self.__primeRepository,
            self.__linkRepository,
            self.__factGroupRepository,
            self.__factRepository,
            self.__assertionRepository,
            self.__connectionsService,
            self.__baseService,
            self.__propertyService,
            self.__relationshipService,
            self.__logger)

    def __buildExe(self):
        exeBuilder = ExecutorBuilder(self.__sim,
            self.__simulator, 
            self.__spinnakerVersion,
            self.__fsa,
            self.__neuronRepository,
            self.__connectionsRepository,
            self.__activationsRepository, 
            self.__logger)
        
        if(self.__topology):
            exeBuilder.useAssociationTopology(self.__topology)
        
        return exeBuilder.build()

    def __getGenerator(self):
        return SequentialRuleGenerator(self.__connectionsService, self.__neuronRepository)