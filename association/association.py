from lib.readInheritanceFile import InheritanceReaderClass
from lib.stateMachineClass import FSAHelperFunctions
from lib.nealCoverClass import NealCoverFunctions
from lib.make3Assoc import NeuralThreeAssocClass

class Association:
    def __init__(self, sim, simulator, spinnakerVersion):
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

    def setActivation(self, runTime):
        primeTimes = []
        for t in range(0, runTime / 50):
            primeTimes.append(t*50+5)
        primeArray = {'spike_times': [primeTimes]}
        generator = self.sim.Population(1, self.sim.SpikeSourceArray, primeArray)

        for u in self.inheritance.units:
            num = self.inheritance.getUnitNumber(u)
            self.fsa.halfTurnOnStateFromSpikeSource(generator, self.topology.neuralHierarchyTopology.cells, num)

    def build(self, runTime):
        self.init()
        self.setActivation(runTime)
        self.neal.nealApplyProjections()
        return self


