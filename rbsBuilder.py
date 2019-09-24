from rbs import RuleBasedSystem
from network import Network
from executor import Executor
from generators.sequentialRuleGenerator import SequentialRuleGenerator
from repositories.neuronRepository import NeuronRepository
from repositories.connectionsRepository import ConnectionsRepository
from repositories.factGroupRepository import FactGroupRepository
from repositories.factRepository import FactRepository
from repositories.activationsRepository import ActivationsRepository
from repositories.linkRepository import LinkRepository
from repositories.primeRepository import PrimeRepository
from services.connectionsService import ConnectionsService

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
        self.__generator = None

    def useRuleGenerator(self, generator):
        self.__generator = generator
        return self

    def useAssociation(self, association):
        self.__association = association
        return self

    def build(self):

        self.__initDependencies()
        net = self.__buildNet()
        exe = self.__buildExe()

        return RuleBasedSystem(net, 
            exe, 
            self.__association,
            self.__neuronRepository,
            self.__factGroupRepository,
            self.__primeRepository,
            self.__linkRepository)

    
    def __initDependencies(self):
        self.__connectionsRepository = ConnectionsRepository()
        self.__connectionsService = ConnectionsService(self.__fsa, self.__connectionsRepository)
        self.__neuronRepository = NeuronRepository(self.__connectionsService, self.__fsa)
        self.__linkRepository = LinkRepository(self.__neuronRepository, self.__connectionsService, self.__association)
        self.__factGroupRepository = FactGroupRepository()
        self.__activationsRepository = ActivationsRepository()
        self.__factRepository = FactRepository(self.__factGroupRepository, self.__neuronRepository, self.__activationsRepository)
        self.__primeRepository = PrimeRepository(self.__neuronRepository, self.__connectionsService, self.__association)

    def __buildNet(self):
        if(self.__generator == None):
            generator = SequentialRuleGenerator(self.__connectionsService, self.__neuronRepository)
        else:
            generator = self.__generator

        net = Network(self.__fsa, 
            generator, 
            self.__connectionsService, 
            self.__neuronRepository, 
            self.__linkRepository,
            self.__factGroupRepository,
            self.__factRepository,
            self.__primeRepository,
            self.__debug)

        if(self.__association):
            net.useAssociation(self.__association)
        
        return net.build()

    def __buildExe(self):
        exe = Executor(self.__sim, 
            self.__simulator, 
            self.__fsa, 
            self.__neuronRepository,
            self.__connectionsRepository,
            self.__activationsRepository, 
            self.__debug)
        
        if(self.__association):
            exe.useAssociationTopology(self.__association.topology.neuralHierarchyTopology)
        
        return exe.build()
