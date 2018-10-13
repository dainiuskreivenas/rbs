
import pyNN.nest as sim
from rbs import RBS
from stateMachineClass import FSAHelperFunctions

fsa = FSAHelperFunctions("nest")

class Sudoku9:

    def getBoxIndex(self, x, y):
        if(x < 4 and y < 4):
            return 1
        elif(3 < x and x < 7 and y < 4):
            return 2
        elif(x > 6 and y < 4):
            return 3
        elif(x < 4 and 3 < y and y < 7):
            return 4
        elif(3 < x and x < 7 and 3 < y and y < 7):
            return 5
        elif(x > 6 and 3 < y and y < 7):
            return 6
        elif(x < 4 and y > 6):
            return 7
        elif(3 < x and x < 7 and y > 6):
            return 8
        elif(x > 6 and y > 6):
            return 9

    def setupBoard(self):
        for i in range(1,10):
            self.rbs.addFact(("Number",(i,)))
            self.rbs.addFact(("X-Axis",(i,)))
            self.rbs.addFact(("Y-Axis",(i,)))

            for y in range(1,10):
                boxIndex = self.getBoxIndex(i, y)
                self.rbs.addFact(("Box", (i, y, boxIndex)))

    def __init__(self):
        self.rbs = RBS()

        self.setupBoard()
        
        # Fill in 1 missing row value
        self.rbs.addRule(
            (
                "Distinct-H-Line",
                (
                    [
                        (True, "Item", ("?x1","?y1", "?1", "?"), "1"),
                        (True, "Item", ("?x2","?y1", "?2", "?"), "2"),
                        (True, "Item", ("?x3","?y1", "?3", "?"), "3"),
                        (True, "Item", ("?x4","?y1", "?4", "?"), "4"),
                        (True, "Item", ("?x5","?y1", "?5", "?"), "5"),
                        (True, "Item", ("?x6","?y1", "?6", "?"), "6"),
                        (True, "Item", ("?x7","?y1", "?7", "?"), "7"),
                        (True, "Item", ("?x8","?y1", "?8", "?"), "8"),
                        (True, "Number", ("?other",), "n9"),
                        (True, "X-Axis", ("?x9",), "x9"),
                        (True, "Box", ("?x9", "?y1", "?b"), "b"),
                        ("Test","<","?x1","?x2"),
                        ("Test","<","?x2","?x3"),
                        ("Test","<","?x3","?x4"),
                        ("Test","<","?x4","?x5"),
                        ("Test","<","?x5","?x6"),
                        ("Test","<","?x6","?x7"),
                        ("Test","<","?x7","?x8"),
                        ("Test","<>","?x1","?x2"),
                        ("Test","<>","?x1","?x3"),
                        ("Test","<>","?x1","?x4"),
                        ("Test","<>","?x1","?x5"),
                        ("Test","<>","?x1","?x6"),
                        ("Test","<>","?x1","?x7"),
                        ("Test","<>","?x1","?x8"),
                        ("Test","<>","?x1","?x9"),
                        ("Test","<>","?x2","?x3"),
                        ("Test","<>","?x2","?x4"),
                        ("Test","<>","?x2","?x5"),
                        ("Test","<>","?x2","?x6"),
                        ("Test","<>","?x2","?x7"),
                        ("Test","<>","?x2","?x8"),
                        ("Test","<>","?x2","?x9"),
                        ("Test","<>","?x3","?x4"),
                        ("Test","<>","?x3","?x5"),
                        ("Test","<>","?x3","?x6"),
                        ("Test","<>","?x3","?x7"),
                        ("Test","<>","?x3","?x8"),
                        ("Test","<>","?x3","?x9"),
                        ("Test","<>","?x4","?x5"),
                        ("Test","<>","?x4","?x6"),
                        ("Test","<>","?x4","?x7"),
                        ("Test","<>","?x4","?x8"),
                        ("Test","<>","?x4","?x9"),
                        ("Test","<>","?x5","?x6"),
                        ("Test","<>","?x5","?x7"),
                        ("Test","<>","?x5","?x8"),
                        ("Test","<>","?x5","?x9"),
                        ("Test","<>","?x6","?x7"),
                        ("Test","<>","?x6","?x8"),
                        ("Test","<>","?x6","?x9"),
                        ("Test","<>","?x7","?x8"),
                        ("Test","<>","?x7","?x9"),
                        ("Test","<>","?x8","?x9"),

                        ("Test","<>","?1","?2"),
                        ("Test","<>","?1","?3"),
                        ("Test","<>","?1","?4"),
                        ("Test","<>","?1","?5"),
                        ("Test","<>","?1","?6"),
                        ("Test","<>","?1","?7"),
                        ("Test","<>","?1","?8"),
                        ("Test","<>","?1","?other"),

                        ("Test","<>","?2","?3"),
                        ("Test","<>","?2","?4"),
                        ("Test","<>","?2","?5"),
                        ("Test","<>","?2","?6"),
                        ("Test","<>","?2","?7"),
                        ("Test","<>","?2","?8"),
                        ("Test","<>","?2","?other"),
                        ("Test","<>","?3","?4"),
                        ("Test","<>","?3","?5"),
                        ("Test","<>","?3","?6"),
                        ("Test","<>","?3","?7"),
                        ("Test","<>","?3","?8"),
                        ("Test","<>","?3","?other"),
                        ("Test","<>","?4","?5"),
                        ("Test","<>","?4","?6"),
                        ("Test","<>","?4","?7"),
                        ("Test","<>","?4","?8"),
                        ("Test","<>","?4","?other"),
                        ("Test","<>","?5","?6"),
                        ("Test","<>","?5","?7"),
                        ("Test","<>","?5","?8"),
                        ("Test","<>","?5","?other"),
                        ("Test","<>","?6","?7"),
                        ("Test","<>","?6","?8"),
                        ("Test","<>","?6","?other"),
                        ("Test","<>","?7","?8"),
                        ("Test","<>","?7","?other"),
                        ("Test","<>","?8","?other")
                    ],
                    [
                        ("assert", ("Item", ("?x9", "?y1", "?other", "?b")))
                    ]
                )
            ))

        # Fill in 1 Missing column value
        self.rbs.addRule(
            (
                "Distinct-Y-Line",
                (
                    [
                        (True, "Item", ("?x1","?y1", "?1", "?"), "1"),
                        (True, "Item", ("?x1","?y2", "?2", "?"), "2"),
                        (True, "Item", ("?x1","?y3", "?3", "?"), "3"),
                        (True, "Item", ("?x1","?y4", "?4", "?"), "4"),
                        (True, "Item", ("?x1","?y5", "?5", "?"), "5"),
                        (True, "Item", ("?x1","?y6", "?6", "?"), "6"),
                        (True, "Item", ("?x1","?y7", "?7", "?"), "7"),
                        (True, "Item", ("?x1","?y8", "?8", "?"), "8"),
                        (True, "Number", ("?other",), "n9"),
                        (True, "Y-Axis", ("?y9",), "y9"),
                        (True, "Box", ("?x1", "?y9", "?b"), "b"),
                        ("Test","<","?y1","?y2"),
                        ("Test","<","?y2","?y3"),
                        ("Test","<","?y3","?y4"),
                        ("Test","<","?y4","?y5"),
                        ("Test","<","?y5","?y6"),
                        ("Test","<","?y6","?y7"),
                        ("Test","<","?y7","?y8"),
                        ("Test","<>","?y1","?y2"),
                        ("Test","<>","?y1","?y3"),
                        ("Test","<>","?y1","?y4"),
                        ("Test","<>","?y1","?y5"),
                        ("Test","<>","?y1","?y6"),
                        ("Test","<>","?y1","?y7"),
                        ("Test","<>","?y1","?y8"),
                        ("Test","<>","?y1","?y9"),
                        ("Test","<>","?y2","?y3"),
                        ("Test","<>","?y2","?y4"),
                        ("Test","<>","?y2","?y5"),
                        ("Test","<>","?y2","?y6"),
                        ("Test","<>","?y2","?y7"),
                        ("Test","<>","?y2","?y8"),
                        ("Test","<>","?y2","?y9"),
                        ("Test","<>","?y3","?y4"),
                        ("Test","<>","?y3","?y5"),
                        ("Test","<>","?y3","?y6"),
                        ("Test","<>","?y3","?y7"),
                        ("Test","<>","?y3","?y8"),
                        ("Test","<>","?y3","?y9"),
                        ("Test","<>","?y4","?y5"),
                        ("Test","<>","?y4","?y6"),
                        ("Test","<>","?y4","?y7"),
                        ("Test","<>","?y4","?y8"),
                        ("Test","<>","?y4","?y9"),
                        ("Test","<>","?y5","?y6"),
                        ("Test","<>","?y5","?y7"),
                        ("Test","<>","?y5","?y8"),
                        ("Test","<>","?y5","?y9"),
                        ("Test","<>","?y6","?y7"),
                        ("Test","<>","?y6","?y8"),
                        ("Test","<>","?y6","?y9"),
                        ("Test","<>","?y7","?y8"),
                        ("Test","<>","?y7","?y9"),
                        ("Test","<>","?y8","?y9"),
                        ("Test","<>","?1","?2"),
                        ("Test","<>","?1","?3"),
                        ("Test","<>","?1","?4"),
                        ("Test","<>","?1","?5"),
                        ("Test","<>","?1","?6"),
                        ("Test","<>","?1","?7"),
                        ("Test","<>","?1","?8"),
                        ("Test","<>","?1","?other"),
                        ("Test","<>","?2","?3"),
                        ("Test","<>","?2","?4"),
                        ("Test","<>","?2","?5"),
                        ("Test","<>","?2","?6"),
                        ("Test","<>","?2","?7"),
                        ("Test","<>","?2","?8"),
                        ("Test","<>","?2","?other"),
                        ("Test","<>","?3","?4"),
                        ("Test","<>","?3","?5"),
                        ("Test","<>","?3","?6"),
                        ("Test","<>","?3","?7"),
                        ("Test","<>","?3","?8"),
                        ("Test","<>","?3","?other"),
                        ("Test","<>","?4","?5"),
                        ("Test","<>","?4","?6"),
                        ("Test","<>","?4","?7"),
                        ("Test","<>","?4","?8"),
                        ("Test","<>","?4","?other"),
                        ("Test","<>","?5","?6"),
                        ("Test","<>","?5","?7"),
                        ("Test","<>","?5","?8"),
                        ("Test","<>","?5","?other"),
                        ("Test","<>","?6","?7"),
                        ("Test","<>","?6","?8"),
                        ("Test","<>","?6","?other"),
                        ("Test","<>","?7","?8"),
                        ("Test","<>","?7","?other"),
                        ("Test","<>","?8","?other")
                    ],
                    [
                        ("assert", ("Item", ("?x1","?y9","?other", "?b")))
                    ]
                )
            ))
        
        # Fill in 1 Missing box value
        self.rbs.addRule(
            (
                "Distinct-Box-Top-Value",
                (
                    [
                        (True, "Item", ("?x1","?y1", "?1", "?b"), "1"),
                        (True, "Item", ("?x2","?y1", "?2", "?b"), "2"),
                        (True, "Item", ("?x3","?y1", "?3", "?b"), "3"),
                        (True, "Item", ("?x1","?y2", "?4", "?b"), "4"),
                        (True, "Item", ("?x2","?y2", "?5", "?b"), "5"),
                        (True, "Item", ("?x3","?y2", "?6", "?b"), "6"),
                        (True, "Item", ("?x1","?y3", "?7", "?b"), "7"),
                        (True, "Item", ("?x2","?y3", "?8", "?b"), "8"),

                        (True, "Number", ("?9",), "n9"),
                        (True, "Box", ("?x3", "?y3", "?b"), "b"),

                        ("Test",">","?y1","?y2"),

                        ("Test","<>","?y1","?y2"),
                        ("Test","<>","?y1","?y3"),
                        ("Test","<>","?y2","?y3"),

                        ("Test","<>","?x1","?x2"),
                        ("Test","<>","?x1","?x3"),
                        ("Test","<>","?x2","?x3"),

                        ("Test","<>","?1","?2"),
                        ("Test","<>","?1","?3"),
                        ("Test","<>","?1","?4"),
                        ("Test","<>","?1","?5"),
                        ("Test","<>","?1","?6"),
                        ("Test","<>","?1","?7"),
                        ("Test","<>","?1","?8"),
                        ("Test","<>","?1","?9"),
                        ("Test","<>","?2","?3"),
                        ("Test","<>","?2","?4"),
                        ("Test","<>","?2","?5"),
                        ("Test","<>","?2","?6"),
                        ("Test","<>","?2","?7"),
                        ("Test","<>","?2","?8"),
                        ("Test","<>","?2","?9"),
                        ("Test","<>","?3","?4"),
                        ("Test","<>","?3","?5"),
                        ("Test","<>","?3","?6"),
                        ("Test","<>","?3","?7"),
                        ("Test","<>","?3","?8"),
                        ("Test","<>","?3","?9"),
                        ("Test","<>","?4","?5"),
                        ("Test","<>","?4","?6"),
                        ("Test","<>","?4","?7"),
                        ("Test","<>","?4","?8"),
                        ("Test","<>","?4","?9"),
                        ("Test","<>","?5","?6"),
                        ("Test","<>","?5","?7"),
                        ("Test","<>","?5","?8"),
                        ("Test","<>","?5","?9"),
                        ("Test","<>","?6","?7"),
                        ("Test","<>","?6","?8"),
                        ("Test","<>","?6","?9"),
                        ("Test","<>","?7","?8"),
                        ("Test","<>","?7","?9"),
                        ("Test","<>","?8","?9")
                        
                    ],
                    [
                        ("assert", ("Item", ("?x3", "?y3", "?9", "?b")))
                    ]
                )
            )
        )
    
    def solve(self, sudoku):
        for y,s in enumerate(sudoku):
            for x,i in enumerate(s):
                if (i <> None):
                    boxIndex = self.getBoxIndex(x+1, y+1)
                    f = self.rbs.getFact(("Item", (x+1, y+1, i, boxIndex)))
                    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
                    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
                    fsa.turnOnStateFromSpikeSource(spikeGen,f[1],0)        

