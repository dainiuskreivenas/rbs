from lib import NealCoverFunctions, FSAHelperFunctions, NeuralThreeAssocClass
from services import BaseService, UnitService, AssociationService
from association import Association

class AssociationBuilder:
    def __init__(self, sim, fsa, neal, simulator, spinnakerVersion = -1):
        self.__sim = sim
        self.__fsa = fsa
        self.__neal = neal
        self.__simulator = simulator
        self.__spinnakerVersion = spinnakerVersion
        self.__bases = None
        self.__properties = None
        self.__relationships = None
        self.__associations = None

    def useBases(self, bases):
        self.__bases = bases
        return self

    def useRelationships(self, properties, relationships, associations):
        self.__properties = properties
        self.__relationships = relationships
        self.__associations = associations
        return self

    def build(self):

        topology = NeuralThreeAssocClass(self.__simulator, self.__sim, self.__neal, self.__spinnakerVersion, self.__fsa)
        baseService = None
        propertyService = None
        relationshipService = None

        if(self.__bases):
            baseService = BaseService(self.__fsa, self.__bases)
            topology.createBaseNet(baseService.getInheritance())

        if(self.__properties and self.__relationships and self.__associations):
            propertyService = UnitService(self.__fsa, self.__properties)
            relationshipService = UnitService(self.__fsa, self.__relationships)
            associationService = AssociationService(self.__associations)
            topology.createAssociationTopology(propertyService.getStructure(), relationshipService.getStructure())
            topology.addAssociations(associationService.getAssociations())

        return (topology, baseService, propertyService, relationshipService)