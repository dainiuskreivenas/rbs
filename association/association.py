from lib.readInheritanceFile import InheritanceReaderClass
from lib.stateMachineClass import FSAHelperFunctions
from lib.nealCoverClass import NealCoverFunctions
from lib.make3Assoc import NeuralThreeAssocClass

class Association:
    def __init__(self, sim, simulator, spinnakerVersion = -1):
        self.sim = sim
        self.simulator = simulator
        self.spinnakerVersion = spinnakerVersion

    def useBases(self, bases):
        self.bases = bases
        return self

    def init(self):
        if(self.bases):
            self.neal = NealCoverFunctions(self.simulator, self.sim, self.spinnakerVersion)
            self.fsa = FSAHelperFunctions(self.simulator, self.sim, self.neal, self.spinnakerVersion)
            self.inheritance = InheritanceReaderClass()
            self.inheritance.readInheritanceFile(self.bases)
            self.topology = NeuralThreeAssocClass(self.simulator, self.sim, self.neal, self.spinnakerVersion, self.fsa)
            self.topology.createBaseNet(self.inheritance)


    def build(self):
        self.init()
        self.neal.nealApplyProjections()
        return self


