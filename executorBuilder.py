from executor import Executor

class ExecutorBuilder:
    def __init__(self, 
        sim, 
        simulator, 
        spinnVersion,
        fsa,
        neuronRepository, 
        connectionsRepository, 
        activationsRepository,
        logger):
        self.__simulator = simulator
        self.__fsa = fsa
        self.__sim = sim
        self.__spinnVersion = spinnVersion
        self.__neuronRepository = neuronRepository
        self.__connectionsRepository = connectionsRepository
        self.__activationsRepository = activationsRepository
        self.__logger = logger
        self.__neuralHierarchytopology = None

    def useAssociationTopology(self, topology):
        if(topology):
            self.__neuralHierarchytopology = topology.neuralHierarchyTopology
        return self

    def build(self):
        return Executor(self.__sim,
            self.__simulator, 
            self.__fsa,
            self.__spinnVersion,
            self.__neuronRepository,
            self.__connectionsRepository,
            self.__activationsRepository, 
            self.__neuralHierarchytopology,
            self.__logger)