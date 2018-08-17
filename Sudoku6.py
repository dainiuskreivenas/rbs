
import pyNN.nest as sim
from rbs import RBS
from stateMachineClass import FSAHelperFunctions

fsa = FSAHelperFunctions("nest")

class Sudoku6:

    def addItem(self, x):
        for y in range(1,7):
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
            self.rbs.addFact(("Box", (x, y, boxIndex)))

            for j in range(1, 7):
                self.rbs.addFact(("Item", (x, y, j, boxIndex)), False)

    def setupBoard(self):
        for i in range(1,7):
            self.rbs.addFact(("Number",(i,)))
            self.rbs.addFact(("X-Axis",(i,)))
            self.rbs.addFact(("Y-Axis",(i,)))
            self.addItem(i)

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
                "Distinct-Box-Value",
                (
                    [
                        (True, "Item", ("?x1","?y1", "?1", "?b"), "1"),
                        (True, "Item", ("?x2","?y1", "?2", "?b"), "2"),
                        (True, "Item", ("?x3","?y1", "?3", "?b"), "3"),
                        (True, "Item", ("?x4","?y2", "?4", "?b"), "4"),
                        (True, "Item", ("?x5","?y2", "?5", "?b"), "5"),
                        (True, "Number", ("?other",), "n6"),
                        (True, "Y-Axis", ("?y6",), "y6"),
                        (True, "X-Axis", ("?x6",), "x6"),
                        ("Test","<","?x1","?x2"),
                        ("Test","<","?x2","?x3"),
                        ("Test","=","?x1","?x4"),
                        ("Test","=","?x2","?x5"),
                        ("Test","=","?x3","?x6"),
                        ("Test","<","?y1","?y2"),
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
                        ("assert", ("Item", ("?x6", "?y6", "?other", "?b")))
                    ]
                )
            )
        )

        # End
        self.rbs.addRule(
            (
                "End",
                (
                    [
                        (True, "Item", (1,1,"?","?"), "i1"),
                        (True, "Item", (1,2,"?","?"), "i2"),
                        (True, "Item", (1,3,"?","?"), "i3"),
                        (True, "Item", (1,4,"?","?"), "i4"),
                        (True, "Item", (1,5,"?","?"), "i5"),
                        (True, "Item", (1,6,"?","?"), "i6"),

                        (True, "Item", (2,1,"?","?"), "i7"),
                        (True, "Item", (2,2,"?","?"), "i8"),
                        (True, "Item", (2,3,"?","?"), "i9"),
                        (True, "Item", (2,4,"?","?"), "i10"),
                        (True, "Item", (2,5,"?","?"), "i11"),
                        (True, "Item", (2,6,"?","?"), "i12"),

                        (True, "Item", (3,1,"?","?"), "i13"),
                        (True, "Item", (3,2,"?","?"), "i14"),
                        (True, "Item", (3,3,"?","?"), "i15"),
                        (True, "Item", (3,4,"?","?"), "i16"),
                        (True, "Item", (3,5,"?","?"), "i17"),
                        (True, "Item", (3,6,"?","?"), "i18"),
                        
                        (True, "Item", (4,1,"?","?"), "i19"),
                        (True, "Item", (4,2,"?","?"), "i20"),
                        (True, "Item", (4,3,"?","?"), "i21"),
                        (True, "Item", (4,4,"?","?"), "i22"),
                        (True, "Item", (4,5,"?","?"), "i23"),
                        (True, "Item", (4,6,"?","?"), "i24"),
                        
                        (True, "Item", (5,1,"?","?"), "i25"),
                        (True, "Item", (5,2,"?","?"), "i26"),
                        (True, "Item", (5,3,"?","?"), "i27"),
                        (True, "Item", (5,4,"?","?"), "i28"),
                        (True, "Item", (5,5,"?","?"), "i29"),
                        (True, "Item", (5,6,"?","?"), "i30"),
                        
                        (True, "Item", (6,1,"?","?"), "i31"),
                        (True, "Item", (6,2,"?","?"), "i32"),
                        (True, "Item", (6,3,"?","?"), "i33"),
                        (True, "Item", (6,4,"?","?"), "i34"),
                        (True, "Item", (6,5,"?","?"), "i35"),
                        (True, "Item", (6,6,"?","?"), "i36"),
                    ],
                    [
                        ("retract", "i1"),
                        ("retract", "i2"),
                        ("retract", "i3"),
                        ("retract", "i4"),
                        ("retract", "i5"),
                        ("retract", "i6"),
                        ("retract", "i7"),
                        ("retract", "i8"),
                        ("retract", "i9"),
                        ("retract", "i10"),
                        ("retract", "i11"),
                        ("retract", "i12"),
                        ("retract", "i13"),
                        ("retract", "i14"),
                        ("retract", "i15"),
                        ("retract", "i16"),
                        ("retract", "i17"),
                        ("retract", "i18"),
                        ("retract", "i19"),
                        ("retract", "i20"),
                        ("retract", "i21"),
                        ("retract", "i22"),
                        ("retract", "i23"),
                        ("retract", "i24"),
                        ("retract", "i25"),
                        ("retract", "i26"),
                        ("retract", "i27"),
                        ("retract", "i28"),
                        ("retract", "i29"),
                        ("retract", "i30"),
                        ("retract", "i31"),
                        ("retract", "i32"),
                        ("retract", "i33"),
                        ("retract", "i34"),
                        ("retract", "i35"),
                        ("retract", "i36"),
                    ]
                )
            )
        )

        """
        # Match missing based on row, column and box
        self.rbs.addRule(
            (
                "Find-Missing",
                (
                    [
                        (True, "Item", ("?x1", "?y1", "?n1", "?b"), "n"),
                        (True, "Item", ("?x2", "?y2", "?n2", "?b"), "n"),
                        (True, "Item", ("?x3", "?y3", "?n3", "?b"), "n"),
                        (True, "Item", ("?x4", "?y4", "?n4", "?b"), "n"),
                        (True, "Item", ("?x5", "?y5", "?n5", "?b"), "n"),
                        # is ?1 in Y or X or Box?
                        # is ?2 in Y or X or Box?
                        # is ?3 in Y or X or Box?
                        # is ?4 in Y or X or Box?
                        # is ?5 in Y or X or Box?

                        # X-Axis ?x6
                        # Y-Axis ?y6
                        # Number ?6
                        # Box ?x6 ?y6 ?b6
                    ],
                    [
                        # assert ?x6 ?y6 ?6 ?b6
                    ]
                )
            )
        )
        """
    
    def activateBoard(self, sudoku):
        group = self.rbs.factGroups["Item"]
        for i in range(0,6):
            for j in range(0,6):
                val = sudoku[j][i]
                if(val == None):
                    continue
                
                for f in group:
                    if(f[0][0][0] == j+1 and f[0][0][1] == i+1 and f[0][0][2] == val):
                        ca = f[0][1]
                        spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
                        spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
                        fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)
                        break

