from executorBuilder import ExecutorBuilder
from rbs import RuleBasedSystem
from generators import SequentialRuleGenerator
from repositories import *
from services import *

class RuleBasedSystemBuilder:
    def __init__(self, sim, simulator, fsa, spinnakerVersion = -1, debug = False):
        if(simulator not in ["nest", "spinnaker"]):
            raise Exception("simulator type: '{}' is invalid. Use one of the following: nest, spinnaker.".format(simulator)) 
        self.__sim = sim
        self.__fsa = fsa
        self.__simulator = simulator
        self.__debug = debug
        self.__spinnakerVersion = spinnakerVersion
        self.__association = None
        self.__generatorType = None
        self.__generator = None

    def useAssociation(self, association):
        self.__association = association
        return self

    def build(self):
        self.__initDependencies()

        generator = self.__getGenerator()
        exe = self.__buildExe()

        return RuleBasedSystem(exe,
            self.__rulesService,
            self.__rulesRepository,
            self.__neuronRepository,
            self.__factGroupRepository,
            self.__factRepository,
            self.__assertionRepository,
            self.__primeRepository,
            self.__linkRepository,
            generator,
            self.__association)
    
    def __initDependencies(self):        
        self.__logger = LoggerService(self.__debug)
        self.__connectionsRepository = ConnectionsRepository()
        self.__connectionsService = ConnectionsService(self.__fsa, self.__connectionsRepository)
        self.__neuronRepository = NeuronRepository(self.__connectionsService, self.__fsa)
        self.__linkRepository = LinkRepository(self.__neuronRepository, self.__connectionsService, self.__association)
        self.__factGroupRepository = FactGroupRepository()
        self.__activationsRepository = ActivationsRepository()
        self.__factRepository = FactRepository(self.__factGroupRepository, self.__neuronRepository, self.__activationsRepository)
        self.__primeRepository = PrimeRepository(self.__neuronRepository, self.__connectionsService, self.__association)
        self.__assertionRepository = AssertionRepository(self.__neuronRepository)
        self.__rulesRepository = RulesRepository()
        self.__rulesService = RulesService(self.__rulesRepository, 
            self.__primeRepository,
            self.__linkRepository,
            self.__factGroupRepository,
            self.__factRepository,
            self.__assertionRepository,
            self.__connectionsService,
            self.__association,
            self.__logger)

    def __buildExe(self):
        exeBuilder = ExecutorBuilder(self.__sim,
            self.__simulator, 
            self.__fsa,
            self.__neuronRepository,
            self.__connectionsRepository,
            self.__activationsRepository, 
            self.__logger)
        
        if(self.__association):
            exeBuilder.useAssociationTopology(self.__association.getNeuralTopology())
        
        return exeBuilder.build()

    def __getGenerator(self):
        return SequentialRuleGenerator(self.__connectionsService, self.__neuronRepository)