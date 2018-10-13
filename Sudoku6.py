
import pyNN.nest as sim
from rbs import RBS
from stateMachineClass import FSAHelperFunctions

fsa = FSAHelperFunctions("nest")

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
        for i in range(1,7):
            self.rbs.addFact(("Number",(i,)))
            self.rbs.addFact(("X-Axis",(i,)))
            self.rbs.addFact(("Y-Axis",(i,)))

            for x in range(1,7):
                for y in range(1,7):
                    boxIndex = self.getBoxIndex(x, y)
                    self.rbs.addFact(("Box", (x, y, boxIndex)))

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
                        (True, "Number", ("?other",), "n6"),
                        (True, "X-Axis", ("?x6",), "x6"),
                        (True, "Box", ("?x6", "?y1", "?b"), "b"),
                        ("Test","<","?x1","?x2"),
                        ("Test","<","?x2","?x3"),
                        ("Test","<","?x3","?x4"),
                        ("Test","<","?x4","?x5"),
                        ("Test","<>","?x1","?x2"),
                        ("Test","<>","?x1","?x3"),
                        ("Test","<>","?x1","?x4"),
                        ("Test","<>","?x1","?x5"),
                        ("Test","<>","?x1","?x6"),
                        ("Test","<>","?x2","?x3"),
                        ("Test","<>","?x2","?x4"),
                        ("Test","<>","?x2","?x5"),
                        ("Test","<>","?x2","?x6"),
                        ("Test","<>","?x3","?x4"),
                        ("Test","<>","?x3","?x5"),
                        ("Test","<>","?x3","?x6"),
                        ("Test","<>","?x4","?x5"),
                        ("Test","<>","?x4","?x6"),
                        ("Test","<>","?x5","?x6"),
                        ("Test","<>","?1","?2"),
                        ("Test","<>","?1","?3"),
                        ("Test","<>","?1","?4"),
                        ("Test","<>","?1","?5"),
                        ("Test","<>","?1","?other"),
                        ("Test","<>","?2","?3"),
                        ("Test","<>","?2","?4"),
                        ("Test","<>","?2","?5"),
                        ("Test","<>","?2","?other"),
                        ("Test","<>","?3","?4"),
                        ("Test","<>","?3","?5"),
                        ("Test","<>","?3","?other"),
                        ("Test","<>","?4","?5"),
                        ("Test","<>","?4","?other"),
                        ("Test","<>","?5","?other")
                    ],
                    [
                        ("assert", ("Item", ("?x6", "?y1", "?other", "?b")))
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
                        (True, "Number", ("?other",), "n6"),
                        (True, "Y-Axis", ("?y6",), "y6"),
                        (True, "Box", ("?x1", "?y6", "?b"), "b"),
                        ("Test","<","?y1","?y2"),
                        ("Test","<","?y2","?y3"),
                        ("Test","<","?y3","?y4"),
                        ("Test","<","?y4","?y5"),
                        ("Test","<>","?y1","?y2"),
                        ("Test","<>","?y1","?y3"),
                        ("Test","<>","?y1","?y4"),
                        ("Test","<>","?y1","?y5"),
                        ("Test","<>","?y1","?y6"),
                        ("Test","<>","?y2","?y3"),
                        ("Test","<>","?y2","?y4"),
                        ("Test","<>","?y2","?y5"),
                        ("Test","<>","?y2","?y6"),
                        ("Test","<>","?y3","?y4"),
                        ("Test","<>","?y3","?y5"),
                        ("Test","<>","?y3","?y6"),
                        ("Test","<>","?y4","?y5"),
                        ("Test","<>","?y4","?y6"),
                        ("Test","<>","?y5","?y6"),
                        ("Test","<>","?1","?2"),
                        ("Test","<>","?1","?3"),
                        ("Test","<>","?1","?4"),
                        ("Test","<>","?1","?5"),
                        ("Test","<>","?1","?other"),
                        ("Test","<>","?2","?3"),
                        ("Test","<>","?2","?4"),
                        ("Test","<>","?2","?5"),
                        ("Test","<>","?2","?other"),
                        ("Test","<>","?3","?4"),
                        ("Test","<>","?3","?5"),
                        ("Test","<>","?3","?other"),
                        ("Test","<>","?4","?5"),
                        ("Test","<>","?4","?other"),
                        ("Test","<>","?5","?other")
                    ],
                    [
                        ("assert", ("Item", ("?x1","?y6","?other", "?b")))
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
                        (True, "Number", ("?6",), "n6"),
                        (True, "Box", ("?x3", "?y2", "?b"), "b"),

                        ("Test", "<>","?x1","?x2"),
                        ("Test", "<>","?x1","?x3"),
                        ("Test", "<>","?x2","?x3"),                        
                        ("Test", "<>","?y1","?y2"),

                        ("Test","<>","?1","?2"),
                        ("Test","<>","?1","?3"),
                        ("Test","<>","?1","?4"),
                        ("Test","<>","?1","?5"),
                        ("Test","<>","?1","?6"),
                        ("Test","<>","?2","?3"),
                        ("Test","<>","?2","?4"),
                        ("Test","<>","?2","?5"),
                        ("Test","<>","?2","?6"),
                        ("Test","<>","?3","?4"),
                        ("Test","<>","?3","?5"),
                        ("Test","<>","?3","?6"),
                        ("Test","<>","?4","?5"),
                        ("Test","<>","?4","?6"),
                        ("Test","<>","?5","?6")
                    ],
                    [
                        ("assert", ("Item", ("?x3", "?y2", "?6", "?b")))
                    ]
                )
            )
        )

        # TODO : Match missing based on row, column and box
    
    def solve(self, sudoku):
        for y,s in enumerate(sudoku):
            for x,i in enumerate(s):
                if (i <> None):
                    boxIndex = self.getBoxIndex(x+1, y+1)
                    f = self.rbs.getFact(("Item", (x+1, y+1, i, boxIndex)))
                    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
                    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
                    fsa.turnOnStateFromSpikeSource(spikeGen,f[1],0)        

