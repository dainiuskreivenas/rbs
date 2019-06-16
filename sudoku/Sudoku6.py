import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from rbs import RBS
from stateMachineClass import FSAHelperFunctions
import os.path

class Sudoku6:

    def getBoxIndex(self, x, y):
        boxIndex = 0
        if(x < 4 and y < 3):
            boxIndex = 1
        elif(x > 2 and y < 3):
            boxIndex = 2
        elif(x < 4 and y > 2 and y < 5):
            boxIndex = 3
        elif(x > 2 and y > 2 and y < 5):
            boxIndex = 4
        elif(x < 4 and y > 4):
            boxIndex = 5
        else:
            boxIndex = 6
        return boxIndex

    def setupBoard(self):
        self.resetNeuron = self.rbs.net.addNeuron()

        for i in range(1,7):
            self.rbs.addFact(("Number",(i,)), apply=False)
            self.rbs.addFact(("X-Axis",(i,)), apply=False)
            self.rbs.addFact(("Y-Axis",(i,)), apply=False)

            for y in range(1,7):
                boxIndex = self.getBoxIndex(i, y)
                self.rbs.addFact(("Box", (i, y, boxIndex)), apply=False)
                for n in range(1,7):
                    item = self.rbs.addFact(("Item", (i, y, n, boxIndex)), False, False)
                    cantbe = self.rbs.addFact(("CantBe", (i, y, n)), False, False)

                    self.rbs.net.neuronToCa(self.resetNeuron, cantbe.ca, self.fsa.ONE_NEURON_STOPS_CA_WEIGHT)
                    self.rbs.net.neuronToCa(self.resetNeuron, item.ca, self.fsa.ONE_NEURON_STOPS_CA_WEIGHT)

    def __init__(self, sim, simulator):
        self.sim = sim
        self.fsa = FSAHelperFunctions(sim, simulator)
    
        if(os.path.exists("sudoku/sudoku6_canBe.rbs")):
            self.rbs = RBS(sim, simulator=simulator, fromFile="sudoku/sudoku6_canBe.rbs", debug=True)
            self.resetNeuron = 0
        else:

            self.rbs = RBS(sim, simulator=simulator, debug=True)

            self.setupBoard()

            self.rbs.addRule(
            (
                "CantBeHorizontal",
                (
                    [
                        (True, "Item", ("?x1", "?y1", "?1", "?"), "1"),
                        (True, "X-Axis", ("?x2",), "2"),
                        (True, "X-Axis", ("?x3",), "3"),
                        (True, "X-Axis", ("?x4",), "4"),
                        (True, "X-Axis", ("?x5",), "5"),
                        (True, "X-Axis", ("?x6",), "6"),
                        ("Test", "<>", "?x1", "?x2"),
                        ("Test", "<>", "?x1", "?x3"),
                        ("Test", "<>", "?x1", "?x4"),
                        ("Test", "<>", "?x1", "?x5"),
                        ("Test", "<>", "?x1", "?x6"),
                        ("Test", "<", "?x2", "?x3"),
                        ("Test", "<", "?x3", "?x4"),
                        ("Test", "<", "?x4", "?x5"),
                        ("Test", "<", "?x5", "?x6")
                    ],
                    [
                        ("assert", ("CantBe", ("?x2", "?y1", "?1"))),
                        ("assert", ("CantBe", ("?x3", "?y1", "?1"))),
                        ("assert", ("CantBe", ("?x4", "?y1", "?1"))),
                        ("assert", ("CantBe", ("?x5", "?y1", "?1"))),
                        ("assert", ("CantBe", ("?x6", "?y1", "?1")))
                    ]
                )
            ),
            False
            )

            self.rbs.addRule(
            (
                "CantBeVertical",
                (
                    [
                        (True, "Item", ("?x1", "?y1", "?1", "?"), "1"),
                        (True, "Y-Axis", ("?y2",), "2"),
                        (True, "Y-Axis", ("?y3",), "3"),
                        (True, "Y-Axis", ("?y4",), "4"),
                        (True, "Y-Axis", ("?y5",), "5"),
                        (True, "Y-Axis", ("?y6",), "6"),
                        ("Test", "<>", "?y1", "?y2"),
                        ("Test", "<>", "?y1", "?y3"),
                        ("Test", "<>", "?y1", "?y4"),
                        ("Test", "<>", "?y1", "?y5"),
                        ("Test", "<>", "?y1", "?y6"),
                        ("Test", "<", "?y2", "?y3"),
                        ("Test", "<", "?y3", "?y4"),
                        ("Test", "<", "?y4", "?y5"),
                        ("Test", "<", "?y5", "?y6")
                    ],
                    [
                        ("assert", ("CantBe", ("?x1", "?y2", "?1"))),
                        ("assert", ("CantBe", ("?x1", "?y3", "?1"))),
                        ("assert", ("CantBe", ("?x1", "?y4", "?1"))),
                        ("assert", ("CantBe", ("?x1", "?y5", "?1"))),
                        ("assert", ("CantBe", ("?x1", "?y6", "?1")))
                    ]
                )
            ),
            False
            )

            self.rbs.addRule(
            (
                "CantBeBox",
                (
                    [
                        (True, "Item", ("?x1", "?y1", "?1", "?b"), "1"),
                        (True, "Box", ("?x2", "?y1", "?b"), "2"),
                        (True, "Box", ("?x3", "?y1", "?b"), "3"),
                        (True, "Box", ("?x1", "?y2", "?b"), "4"),
                        (True, "Box", ("?x2", "?y2", "?b"), "5"),
                        (True, "Box", ("?x3", "?y2", "?b"), "6"),

                        ("Test", "<", "?x1", "?x2"),
                        ("Test", "<>", "?x1", "?x3"),
                        ("Test", "<>", "?x2", "?x3"),
                        ("Test", "<>", "?y1", "?y2"),
                    ],
                    [
                        ("assert", ("CantBe", ("?x2", "?y1", "?1"))),
                        ("assert", ("CantBe", ("?x3", "?y1", "?1"))),
                        ("assert", ("CantBe", ("?x1", "?y2", "?1"))),
                        ("assert", ("CantBe", ("?x2", "?y2", "?1"))),
                        ("assert", ("CantBe", ("?x3", "?y2", "?1")))
                    ]
                )
            ),
            False
            )

            self.rbs.addRule(
            (
                "CellIs",
                (
                    [
                        (True, "CantBe", ("?x1","?y1", "?1"), "1"),
                        (True, "CantBe", ("?x1","?y1", "?2"), "2"),
                        (True, "CantBe", ("?x1","?y1", "?3"), "3"),
                        (True, "CantBe", ("?x1","?y1", "?4"), "4"),
                        (True, "CantBe", ("?x1","?y1", "?5"), "5"),
                        (True, "Box", ("?x1", "?y1", "?b"), "6"),
                        (True, "Number", ("?6",), "7"),
                        ("Test", "<>", "?6", "?1"),
                        ("Test", "<>", "?6", "?2"),
                        ("Test", "<>", "?6", "?3"),
                        ("Test", "<>", "?6", "?4"),
                        ("Test", "<>", "?6", "?5"),
                        ("Test", "<", "?1", "?2"),
                        ("Test", "<", "?2", "?3"),
                        ("Test", "<", "?3", "?4"),
                        ("Test", "<", "?4", "?5"),                        
                    ],
                    [
                        ("assert", ("Item", ("?x1","?y1","?6", "?b")))
                    ]
                )
            ),
            False
            )

            self.rbs.addRule(
            (
                "BoxCellIs",
                (
                    [
                        (True, "Box", ("?x1", "?y1", "?b"), "6"),
                        (True, "Box", ("?x2", "?y1", "?b"), "7"),
                        (True, "Box", ("?x3", "?y1", "?b"), "8"),
                        (True, "Box", ("?x1", "?y2", "?b"), "9"),
                        (True, "Box", ("?x2", "?y2", "?b"), "10"),

                        (True, "CantBe", ("?x1","?y1", "?1"), "1"),
                        (True, "CantBe", ("?x2","?y1", "?1"), "2"),
                        (True, "CantBe", ("?x3","?y1", "?1"), "3"),
                        (True, "CantBe", ("?x1","?y2", "?1"), "4"),
                        (True, "CantBe", ("?x2","?y2", "?1"), "5"),

                        ("Test", "<", "?x1", "?x2"),
                        ("Test", "<>", "?x3", "?x1"),
                        ("Test", "<>", "?x3", "?x2"),
                        ("Test", "<>", "?y1", "?y2"),
                    ],
                    [
                        ("assert", ("Item", ("?x3","?y2","?1", "?b")))
                    ]
                )
            ),
            False
            )

            self.rbs.addRule(
            (
                "RowCellIs",
                (
                    [
                        (True, "CantBe", ("?x1","?y1", "?1"), "1"),
                        (True, "CantBe", ("?x2","?y1", "?1"), "2"),
                        (True, "CantBe", ("?x3","?y1", "?1"), "3"),
                        (True, "CantBe", ("?x4","?y1", "?1"), "4"),
                        (True, "CantBe", ("?x5","?y1", "?1"), "5"),
                        (True, "Box", ("?x6","?y1","?b"), "6"),
                        ("Test","<","?x1","?x2"),
                        ("Test","<","?x2","?x3"),
                        ("Test","<","?x3","?x4"),
                        ("Test","<","?x4","?x5"),
                        ("Test","<>","?x6","?x1"),
                        ("Test","<>","?x6","?x2"),
                        ("Test","<>","?x6","?x3"),
                        ("Test","<>","?x6","?x4"),
                        ("Test","<>","?x6","?x5")
                    ],
                    [
                        ("assert", ("Item", ("?x6", "?y1", "?1", "?b")))
                    ]
                )
            ),
            False
            )

            self.rbs.addRule(
            (
                "ColumnCellIs",
                (
                    [
                        (True, "CantBe", ("?x1","?y1", "?1"), "1"),
                        (True, "CantBe", ("?x1","?y2", "?1"), "2"),
                        (True, "CantBe", ("?x1","?y3", "?1"), "3"),
                        (True, "CantBe", ("?x1","?y4", "?1"), "4"),
                        (True, "CantBe", ("?x1","?y5", "?1"), "5"),
                        (True, "Box", ("?x1","?y6","?b"), "6"),
                        ("Test","<","?y1","?y2"),
                        ("Test","<","?y2","?y3"),
                        ("Test","<","?y3","?y4"),
                        ("Test","<","?y4","?y5"),
                        ("Test","<>","?y6","?y1"),
                        ("Test","<>","?y6","?y2"),
                        ("Test","<>","?y6","?y3"),
                        ("Test","<>","?y6","?y4"),
                        ("Test","<>","?y6","?y5"),
                    ],
                    [
                        ("assert", ("Item", ("?x1", "?y6", "?1", "?b")))
                    ]
                )
            ),
            False
            )

            self.rbs.addRule(
            (
                "CellCantBe",
                (
                    [
                        (True, "Item", ("?x1","?y1", "?1", "?b"), "1"),
                        (True, "Number", ("?2",), "2"),
                        (True, "Number", ("?3",), "3"),
                        (True, "Number", ("?4",), "4"),
                        (True, "Number", ("?5",), "5"),
                        (True, "Number", ("?6",), "6"),
                        ("Test","<>","?1","?2"),
                        ("Test","<>","?1","?3"),
                        ("Test","<>","?1","?4"),
                        ("Test","<>","?1","?5"),
                        ("Test","<>","?1","?6"),
                        ("Test","<","?2","?3"),
                        ("Test","<","?3","?4"),
                        ("Test","<","?4","?5"),
                        ("Test","<","?5","?6")
                    ],
                    [
                        ("assert", ("CantBe", ("?x1", "?y1", "?2"))),
                        ("assert", ("CantBe", ("?x1", "?y1", "?3"))),
                        ("assert", ("CantBe", ("?x1", "?y1", "?4"))),
                        ("assert", ("CantBe", ("?x1", "?y1", "?5"))),
                        ("assert", ("CantBe", ("?x1", "?y1", "?6")))
                    ]
                )
            ),False)
            

            self.rbs.net.applyRulesToFacts()

            for a in self.rbs.net.assertions:
                assertion = self.rbs.net.assertions[a]
                self.rbs.net.neuronToNeruon(self.resetNeuron, assertion, self.fsa.ONE_NEURON_STOPS_CA_WEIGHT)

            for i in self.rbs.net.interns:
                self.rbs.net.neuronToNeruon(self.resetNeuron, i, self.fsa.ONE_NEURON_STOPS_CA_WEIGHT)

            self.rbs.net.save("sudoku/sudoku6_canBe.rbs")
            self.rbs.exe.apply()

    def run(self, puzzles):
        runtime = 0
        resetTimes = []
        for p in puzzles:
            puzzleActivationTimes = {'spike_times': [[runtime+5]]}
            puzzleSpikeGen = self.sim.Population(1, self.sim.SpikeSourceArray, puzzleActivationTimes)
            for y,s in enumerate(p):
                for x,i in enumerate(s):
                    if (i <> None):
                        boxIndex = self.getBoxIndex(x+1, y+1)
                        f = self.rbs.getFact(("Item", (x+1, y+1, i, boxIndex)), apply=False)
                        population = None
                        for pop in self.rbs.exe.populations:
                            if(pop.fromIndex <= f.ca[0] and pop.toIndex > f.ca[0]):
                                population = pop
                                break

                        self.fsa.turnOnStateFromSpikeSource(puzzleSpikeGen, population.pop, f.ca[0]-population.fromIndex)
                        
            runtime += 600
            resetTimes.append(runtime)
            resetTimes.append(runtime+10)
            runtime += 100

        resetSpikeGen = self.sim.Population(1, self.sim.SpikeSourceArray, {'spike_times': [resetTimes]})

        population = None
        for pop in self.rbs.exe.populations:
            if(pop.fromIndex <= self.resetNeuron and pop.toIndex > self.resetNeuron):
                population = pop
                break
        
        self.fsa.turnOnNeuronFromSpikeSource(resetSpikeGen, population.pop, self.resetNeuron-population.fromIndex)
        
        self.sim.run(runtime)

    def printSpikes(self):
        data = self.rbs.get_data()

        for f in self.rbs.net.facts["Item"]:
               pop = self.rbs.get_population(f.ca[0])
               d = data[pop.pop.label]
               st = d.segments[0].spiketrains[f.ca[0]-pop.fromIndex]
               if(len(st) > 0):
                   for s in st.magnitude:
                       print "{} {} {}".format(f.attributes, f.ca[0]-pop.fromIndex, s)
        
        pop = self.rbs.get_population(self.resetNeuron)
        d = data[pop.pop.label]
        print "RESET AT: {}".format(d.segments[0].spiketrains[self.resetNeuron-pop.fromIndex])
