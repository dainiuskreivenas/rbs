from executor import Executor

class ExecutorBuilder:
    def __init__(self, 
        sim, 
        simulator, 
        fsa,
        neuronRepository, 
        connectionsRepository, 
        activationsRepository,
        logger):
        self.__simulator = simulator
        self.__fsa = fsa
        self.__sim = sim
        self.__neuronRepository = neuronRepository
        self.__connectionsRepository = connectionsRepository
        self.__activationsRepository = activationsRepository
        self.__logger = logger
        self.__neuralHierarchyTopology = None

    def useAssociationTopology(self, topology):
        self.__neuralHierarchyTopology = topology
        return self

    def build(self):
        return Executor(self.__sim,
            self.__simulator, 
            self.__fsa,
            self.__neuronRepository,
            self.__connectionsRepository,
            self.__activationsRepository, 
            self.__neuralHierarchyTopology,
            self.__logger)