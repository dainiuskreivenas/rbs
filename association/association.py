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

    #Initialize the associative memory properly (assuming there is
    #a memory), but reading in the data.  This probably should be
    #called with both an instantiated NEAL and an FSA, but for
    #compatibility, we can create them here if necessary.  
    def init(self, NEAL = None, FSA = None):
        if(self.bases):
            if NEAL is None:
                self.neal = NealCoverFunctions(self.simulator, self.sim, self.spinnakerVersion)
            else:
                self.neal = NEAL
            if FSA is None:
                self.fsa = FSAHelperFunctions(self.simulator, self.sim, self.neal, self.spinnakerVersion)
            else:
                self.fsa = FSA

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

    def build(self, runTime,NEAL=None,FSA=None):
        self.init(NEAL,FSA)
        self.setActivation(runTime)
        self.neal.nealApplyProjections()
        return self


