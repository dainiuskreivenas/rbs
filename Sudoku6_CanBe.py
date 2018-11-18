
from rbs import RBS
import os.path

class Sudoku6_CanBe:

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

            for y in range(1,7):
                boxIndex = self.getBoxIndex(i, y)
                self.rbs.addFact(("Box", (i, y, boxIndex)))

    def __init__(self):
        if(os.path.exists("sudoku6_canBe.rbs")):
            self.rbs = RBS(fromFile="sudoku6_canBe.rbs")
        else:

            self.rbs = RBS()

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
            )
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
            )
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
                        ("Test", "<>", "?x1", "?x2"),
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
            )
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
                        ("Test", "<>", "?1", "?2"),
                        ("Test", "<>", "?1", "?3"),
                        ("Test", "<>", "?1", "?4"),
                        ("Test", "<>", "?1", "?5"),
                        ("Test", "<>", "?1", "?6"),
                        ("Test", "<>", "?2", "?3"),
                        ("Test", "<>", "?2", "?4"),
                        ("Test", "<>", "?2", "?5"),
                        ("Test", "<>", "?2", "?6"),
                        ("Test", "<>", "?3", "?4"),
                        ("Test", "<>", "?3", "?5"),
                        ("Test", "<>", "?3", "?6"),
                        ("Test", "<>", "?4", "?5"),
                        ("Test", "<>", "?4", "?6"),
                        ("Test", "<>", "?5", "?6"),                        
                    ],
                    [
                        ("assert", ("Item", ("?x1","?y1","?6", "?b")))
                    ]
                )
            )
            )

            self.rbs.addRule(
            (
                "BoxCellIs",
                (
                    [
                        (True, "CantBe", ("?x1","?y1", "?1"), "1"),
                        (True, "CantBe", ("?x2","?y1", "?1"), "2"),
                        (True, "CantBe", ("?x3","?y1", "?1"), "3"),
                        (True, "CantBe", ("?x1","?y2", "?1"), "4"),
                        (True, "CantBe", ("?x2","?y2", "?1"), "5"),
                        (True, "Box", ("?x1", "?y1", "?b"), "6"),
                        (True, "Box", ("?x2", "?y1", "?b"), "7"),
                        (True, "Box", ("?x3", "?y1", "?b"), "8"),
                        (True, "Box", ("?x1", "?y2", "?b"), "9"),
                        (True, "Box", ("?x2", "?y2", "?b"), "10"),
                        (True, "Box", ("?x3", "?y2", "?b"), "11"),
                        ("Test", "<>", "?x1", "?x2"),
                        ("Test", "<>", "?x1", "?x3"),
                        ("Test", "<>", "?x2", "?x3"),
                        ("Test", "<>", "?y1", "?y2"),
                        ("Test", "<>", "?1", "?2"),
                        ("Test", "<>", "?1", "?3"),
                        ("Test", "<>", "?1", "?4"),
                        ("Test", "<>", "?1", "?5"),
                        ("Test", "<>", "?1", "?6"),
                        ("Test", "<>", "?2", "?3"),
                        ("Test", "<>", "?2", "?4"),
                        ("Test", "<>", "?2", "?5"),
                        ("Test", "<>", "?2", "?6"),
                        ("Test", "<>", "?3", "?4"),
                        ("Test", "<>", "?3", "?5"),
                        ("Test", "<>", "?3", "?6"),
                        ("Test", "<>", "?4", "?5"),
                        ("Test", "<>", "?4", "?6"),
                        ("Test", "<>", "?5", "?6"),
                    ],
                    [
                        ("assert", ("Item", ("?x3","?y2","?1", "?b")))
                    ]
                )
            )
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
            )
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
            )
            )

            self.rbs.addRule(
            (
                "CellCantBe",
                (
                    [
                        (True, "Item", ("?x1","?y1", "?1", "?b"), "1"),
                        (True, "Number", ("?2",), "2"),
                        (True, "Number", ("?3",), "2"),
                        (True, "Number", ("?4",), "2"),
                        (True, "Number", ("?5",), "2"),
                        (True, "Number", ("?6",), "2"),
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
                        ("assert", ("CantBe", ("?x1", "?y1", "?2"))),
                        ("assert", ("CantBe", ("?x1", "?y1", "?3"))),
                        ("assert", ("CantBe", ("?x1", "?y1", "?4"))),
                        ("assert", ("CantBe", ("?x1", "?y1", "?5"))),
                        ("assert", ("CantBe", ("?x1", "?y1", "?6")))
                    ]
                )
            )
            )

            self.rbs.net.save("sudoku6_canBe.rbs")
    
    def solve(self, sudoku):
        for y,s in enumerate(sudoku):
            for x,i in enumerate(s):
                if (i <> None):
                    boxIndex = self.getBoxIndex(x+1, y+1)
                    f = self.rbs.getFact(("Item", (x+1, y+1, i, boxIndex)))
                    if f.ca not in self.rbs.net.activations:
                        self.rbs.net.activations.append(f.ca)
                print "{} {} - Done".format(x, y)
                        
        self.rbs.exe.apply()
        self.rbs.net.save("sudoku6_canBe.rbs")