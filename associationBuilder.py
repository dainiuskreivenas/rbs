from lib import NealCoverFunctions, FSAHelperFunctions, NeuralThreeAssocClass
from services import BaseService, UnitService, AssociationService
from association import Association

class AssociationBuilder:
    def __init__(self, sim, simulator, spinnakerVersion = -1):
        self.__sim = sim
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

        neal = NealCoverFunctions(self.__simulator, self.__sim, self.__spinnakerVersion)
        fsa = FSAHelperFunctions(self.__simulator, self.__sim, neal, self.__spinnakerVersion)
        topology = NeuralThreeAssocClass(self.__simulator, self.__sim, neal, self.__spinnakerVersion, fsa)

        if(self.__bases):
            baseService = BaseService(fsa, self.__bases)
            topology.createBaseNet(baseService.getInheritance())

        if(self.__properties and self.__relationships and self.__associations):
            propertyService = UnitService(fsa, self.__properties)
            relationshipService = UnitService(fsa, self.__relationships)
            associationService = AssociationService(self.__associations)
            topology.createAssociationTopology(propertyService.getStructure(), relationshipService.getStructure())
            topology.addAssociations(associationService.getAssociations())

        neal.nealApplyProjections()

        return Association(topology, baseService, propertyService, relationshipService)