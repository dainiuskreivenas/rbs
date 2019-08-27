from lib.readInheritanceFile import InheritanceReaderClass
from lib.stateMachineClass import FSAHelperFunctions
from lib.nealCoverClass import NealCoverFunctions
from lib.make3Assoc import NeuralThreeAssocClass
from lib.readUnitFile import UnitReaderClass
from lib.readAssocFile import AssocReaderClass

class Association:
    def __init__(self, sim, simulator, spinnakerVersion = -1):
        self.sim = sim
        self.simulator = simulator
        self.spinnakerVersion = spinnakerVersion
        self.bases = None
        self.properties = None
        self.relationships = None
        self.associations = None
        self.inheritance = None
        self.propertyStructure = None
        self.relationshipStructure = None
        self.associationStructure = None

    def useBases(self, bases):
        self.bases = bases
        return self

    def useProperties(self, properties, relationships, associations):
        self.properties = properties
        self.relationships = relationships
        self.associations = associations
        return self

    def init(self):
        self.neal = NealCoverFunctions(self.simulator, self.sim, self.spinnakerVersion)
        self.fsa = FSAHelperFunctions(self.simulator, self.sim, self.neal, self.spinnakerVersion)
        self.topology = NeuralThreeAssocClass(self.simulator, self.sim, self.neal, self.spinnakerVersion, self.fsa)

        if(self.bases):
            self.inheritance = InheritanceReaderClass()
            self.inheritance.readInheritanceFile(self.bases)
            self.topology.createBaseNet(self.inheritance)

        if(self.properties and self.relationships and self.associations):
            self.propertyStructure = UnitReaderClass()
            self.propertyStructure.readUnitFile(self.properties)
            self.relationshipStructure = UnitReaderClass()
            self.relationshipStructure.readUnitFile(self.relationships)
            self.associationStructure = AssocReaderClass()
            self.associationStructure.readAssocFile(self.associations)
            self.topology.createAssociationTopology(self.propertyStructure, self.relationshipStructure)
            self.topology.addAssociations(self.associationStructure)
        
    def build(self):
        self.init()
        self.neal.nealApplyProjections()
        return self


