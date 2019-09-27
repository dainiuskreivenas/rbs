

class Association:
    def __init__(self, topology, baseService, propertyService, relationshipService):
        self.__topology = topology
        self.__baseService = baseService
        self.__propertyService = propertyService
        self.__relationshipService = relationshipService

    def getNeuralTopology(self):
        return self.__topology.neuralHierarchyTopology

    def getBaseService(self):
        return self.__baseService

    def getPropertyService(self):
        return self.__propertyService

    def getRelationshipService(self):
        return self.__relationshipService