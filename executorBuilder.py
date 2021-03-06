from executor import Executor

class ExecutorBuilder:
    def __init__(self, 
        sim, 
        simulator, 
        spinnVersion,
        fsa,
        neal,
        neuronRepository, 
        connectionsRepository, 
        activationsRepository,
        logger):
        self.__simulator = simulator
        self.__fsa = fsa
        self.__neal = neal
        self.__sim = sim
        self.__spinnVersion = spinnVersion
        self.__neuronRepository = neuronRepository
        self.__connectionsRepository = connectionsRepository
        self.__activationsRepository = activationsRepository
        self.__logger = logger
        self.__associationTopology = None

    def useAssociationTopology(self, topology):
        if(topology):
            self.__associationTopology = topology
        return self

    def build(self):
        return Executor(self.__sim,
            self.__simulator, 
            self.__fsa,
            self.__neal,
            self.__spinnVersion,
            self.__neuronRepository,
            self.__connectionsRepository,
            self.__activationsRepository, 
            self.__associationTopology,
            self.__logger)