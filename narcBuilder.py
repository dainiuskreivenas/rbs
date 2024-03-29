"""
Neural Cognitive Architecture Builder

Builder service to build the Neural Coginitive Architecture.
"""
from generators.sequentialRuleGenerator import SequentialRuleGenerator
from repositories.activationsRepository import ActivationsRepository
from repositories.assertionRepository import AssertionRepository
from repositories.connectionsRepository import ConnectionsRepository
from repositories.factGroupRepository import FactGroupRepository
from repositories.factRepository import FactRepository
from repositories.internRepository import InternRepository
from repositories.linkRepository import LinkRepository
from repositories.neuronRepository import NeuronRepository
from repositories.primeRepository import PrimeRepository
from repositories.rulesRepository import RulesRepository
from services.associationService import AssociationService
from services.baseService import BaseService
from services.connectionsService import ConnectionsService
from services.internService import InternService
from services.loggerService import LoggerService
from services.propertyService import PropertyService
from services.relationshipService import RelationshipService
from services.rulesService import RulesService
from lib.make3Assoc import NeuralThreeAssocClass
from executorBuilder import ExecutorBuilder
from narc import NeuralCognitiveArchitecture

class NeuralCognitiveArchitectureBuilder:
    def __init__(self, simulator, sim, fsa, neal, spinnakerVersion = -1, debug = False):
        if(simulator not in ["nest", "spinnaker"]):
            raise Exception("simulator type: '{}' is invalid. Use one of the following: nest, spinnaker.".format(simulator)) 
        self.__sim = sim
        self.__fsa = fsa
        self.__neal = neal
        self.__simulator = simulator
        self.__debug = debug
        self.__spinnakerVersion = spinnakerVersion
        self.__basesFile = None
        self.__propertiesFile = None
        self.__relationshipsFile = None
        self.__associationsFile = None
        self.__topology = None
        self.__baseService = None
        self.__propertyService = None
        self.__relationshipService = None
        self.__generatorType = None
        self.__generator = None

    def useBasesFile(self, basesFile):
        self.__basesFile = basesFile
        return self

    def useRelationshipsFiles(self, propertiesFile, relationshipsFile, associationsFile):
        self.__propertiesFile = propertiesFile
        self.__relationshipsFile = relationshipsFile
        self.__associationsFile = associationsFile
        return self


    def build(self):
        self.__initDependencies()

        generator = self.__getGenerator()
        exe = self.__buildExe()

        return NeuralCognitiveArchitecture(exe,
            self.__rulesService,
            self.__rulesRepository,
            self.__neuronRepository,
            self.__internRepository,
            self.__factGroupRepository,
            self.__factRepository,
            self.__assertionRepository,
            self.__primeRepository,
            self.__linkRepository,
            generator,
            self.__topology,
            self.__baseService,
            self.__propertyService,
            self.__relationshipService,
            self.__connectionsService)
    
    def __initDependencies(self):
        if(self.__basesFile):
            self.__topology = NeuralThreeAssocClass(self.__simulator, self.__sim, self.__neal, self.__spinnakerVersion, self.__fsa)
            self.__baseService = BaseService(self.__fsa, self.__basesFile)
            self.__topology.createBaseNet(self.__baseService.getInheritance())
        
        if(self.__propertiesFile and self.__relationshipsFile and self.__associationsFile):
            self.__propertyService = PropertyService(self.__fsa, self.__propertiesFile)
            self.__relationshipService = RelationshipService(self.__fsa, self.__relationshipsFile)
            self.__associationService = AssociationService(self.__associationsFile)
            self.__topology.createAssociationTopology(self.__propertyService.getStructure(), self.__relationshipService.getStructure())
            self.__topology.addAssociations(self.__associationService.getAssociations())

        self.__logger = LoggerService(self.__debug)
        self.__connectionsRepository = ConnectionsRepository()
        self.__neuronRepository = NeuronRepository()
        self.__internRepository = InternRepository()
        self.__internService = InternService(self.__neuronRepository, self.__internRepository)
        self.__connectionsService = ConnectionsService(self.__connectionsRepository, self.__internService)
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
            self.__neal,
            self.__neuronRepository,
            self.__connectionsRepository,
            self.__activationsRepository, 
            self.__logger)
        
        if(self.__topology):
            exeBuilder.useAssociationTopology(self.__topology)
        
        return exeBuilder.build()

    def __getGenerator(self):
        return SequentialRuleGenerator(self.__connectionsService, self.__internService)