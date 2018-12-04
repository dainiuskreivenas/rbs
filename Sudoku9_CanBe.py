from rbs import RBS
import os.path

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
            self.rbs.addFact(("Number",(i,)), apply=False)
            self.rbs.addFact(("X-Axis",(i,)), apply=False)
            self.rbs.addFact(("Y-Axis",(i,)), apply=False)

            for y in range(1,10):
                boxIndex = self.getBoxIndex(i, y)
                self.rbs.addFact(("Box", (i, y, boxIndex)), apply=False)
                for n in range(1, 10):
                    self.rbs.addFact(("Item", (i, y, n, boxIndex)), False, False)
                    self.rbs.addFact(("CantBe", (i, y, n)), False, False)


    def __init__(self, debug = True):
        if(os.path.exists("sudoku9_canBe.rbs")):
            self.rbs = RBS(fromFile="sudoku9_canBe.rbs", debug = debug)
        else:
            self.rbs = RBS(debug = debug)

            self.setupBoard()


            self.rbs.addRule(
            (
                "CantBeHorizontal",
                (
                    [
                        (True, "X-Axis", ("?x2",), "2"),
                        (True, "X-Axis", ("?x3",), "3"),
                        (True, "X-Axis", ("?x4",), "4"),
                        (True, "X-Axis", ("?x5",), "5"),
                        (True, "X-Axis", ("?x6",), "6"),
                        (True, "X-Axis", ("?x7",), "7"),
                        (True, "X-Axis", ("?x8",), "8"),
                        (True, "X-Axis", ("?x9",), "9"),
                        (True, "Item", ("?x1", "?y1", "?1", "?"), "1"),
                        ("Test", "<", "?x2", "?x3"),
                        ("Test", "<", "?x3", "?x4"),
                        ("Test", "<", "?x4", "?x5"),
                        ("Test", "<", "?x5", "?x6"),
                        ("Test", "<", "?x6", "?x7"),
                        ("Test", "<", "?x7", "?x8"),
                        ("Test", "<", "?x8", "?x9"),
                        ("Test", "<>", "?x1", "?x2"),
                        ("Test", "<>", "?x1", "?x3"),
                        ("Test", "<>", "?x1", "?x4"),
                        ("Test", "<>", "?x1", "?x5"),
                        ("Test", "<>", "?x1", "?x6"),
                        ("Test", "<>", "?x1", "?x7"),
                        ("Test", "<>", "?x1", "?x8"),
                        ("Test", "<>", "?x1", "?x9")
                    ],
                    [
                        ("assert", ("CantBe", ("?x2", "?y1", "?1"))),
                        ("assert", ("CantBe", ("?x3", "?y1", "?1"))),
                        ("assert", ("CantBe", ("?x4", "?y1", "?1"))),
                        ("assert", ("CantBe", ("?x5", "?y1", "?1"))),
                        ("assert", ("CantBe", ("?x6", "?y1", "?1"))),
                        ("assert", ("CantBe", ("?x7", "?y1", "?1"))),
                        ("assert", ("CantBe", ("?x8", "?y1", "?1"))),
                        ("assert", ("CantBe", ("?x9", "?y1", "?1")))
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
                        (True, "Y-Axis", ("?y2",), "2"),
                        (True, "Y-Axis", ("?y3",), "3"),
                        (True, "Y-Axis", ("?y4",), "4"),
                        (True, "Y-Axis", ("?y5",), "5"),
                        (True, "Y-Axis", ("?y6",), "6"),
                        (True, "Y-Axis", ("?y7",), "7"),
                        (True, "Y-Axis", ("?y8",), "8"),
                        (True, "Y-Axis", ("?y9",), "9"),
                        (True, "Item", ("?x1", "?y1", "?1", "?"), "1"),
                        ("Test", "<", "?y2", "?y3"),
                        ("Test", "<", "?y3", "?y4"),
                        ("Test", "<", "?y4", "?y5"),
                        ("Test", "<", "?y5", "?y6"),
                        ("Test", "<", "?y6", "?y7"),
                        ("Test", "<", "?y7", "?y8"),
                        ("Test", "<", "?y8", "?y9"),
                        ("Test", "<>", "?y1", "?y2"),
                        ("Test", "<>", "?y1", "?y3"),
                        ("Test", "<>", "?y1", "?y4"),
                        ("Test", "<>", "?y1", "?y5"),
                        ("Test", "<>", "?y1", "?y6"),
                        ("Test", "<>", "?y1", "?y7"),
                        ("Test", "<>", "?y1", "?y8"),
                        ("Test", "<>", "?y1", "?y9"),
                    ],
                    [
                        ("assert", ("CantBe", ("?x1", "?y2", "?1"))),
                        ("assert", ("CantBe", ("?x1", "?y3", "?1"))),
                        ("assert", ("CantBe", ("?x1", "?y4", "?1"))),
                        ("assert", ("CantBe", ("?x1", "?y5", "?1"))),
                        ("assert", ("CantBe", ("?x1", "?y6", "?1"))),
                        ("assert", ("CantBe", ("?x1", "?y7", "?1"))),
                        ("assert", ("CantBe", ("?x1", "?y8", "?1"))),
                        ("assert", ("CantBe", ("?x1", "?y9", "?1")))
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
                        (True, "Box", ("?x2", "?y1", "?b"), "2"),
                        (True, "Box", ("?x3", "?y1", "?b"), "3"),
                        (True, "Box", ("?x1", "?y2", "?b"), "4"),
                        (True, "Box", ("?x2", "?y2", "?b"), "5"),
                        (True, "Box", ("?x3", "?y2", "?b"), "6"),
                        (True, "Box", ("?x1", "?y3", "?b"), "7"),
                        (True, "Box", ("?x2", "?y3", "?b"), "8"),
                        (True, "Box", ("?x3", "?y3", "?b"), "9"),
                        (True, "Item", ("?x1", "?y1", "?1", "?b"), "1"),
                        ("Test", "<>", "?x1", "?x2"),
                        ("Test", "<>", "?x1", "?x3"),
                        ("Test", "<", "?x2", "?x3"),
                        ("Test", "<>", "?y1", "?y2"),
                        ("Test", "<>", "?y1", "?y3"),
                        ("Test", "<", "?y2", "?y3")
                    ],
                    [
                        ("assert", ("CantBe", ("?x2", "?y1", "?1"))),
                        ("assert", ("CantBe", ("?x3", "?y1", "?1"))),
                        ("assert", ("CantBe", ("?x1", "?y2", "?1"))),
                        ("assert", ("CantBe", ("?x2", "?y2", "?1"))),
                        ("assert", ("CantBe", ("?x3", "?y2", "?1"))),
                        ("assert", ("CantBe", ("?x1", "?y3", "?1"))),
                        ("assert", ("CantBe", ("?x2", "?y3", "?1"))),
                        ("assert", ("CantBe", ("?x3", "?y3", "?1")))
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
                        (True, "CantBe", ("?x1","?y1", "?6"), "6"),
                        (True, "CantBe", ("?x1","?y1", "?7"), "7"),
                        (True, "CantBe", ("?x1","?y1", "?8"), "8"),   
                        (True, "Box", ("?x1", "?y1", "?b"), "9"),                     
                        (True, "Number", ("?9",), "10"),
                        ("Test", "<", "?1", "?2"),
                        ("Test", "<", "?2", "?3"),
                        ("Test", "<", "?3", "?4"),
                        ("Test", "<", "?4", "?5"),
                        ("Test", "<", "?5", "?6"),
                        ("Test", "<", "?6", "?7"),
                        ("Test", "<", "?7", "?8"),
                        ("Test", "<>", "?9", "?1"),
                        ("Test", "<>", "?9", "?2"),
                        ("Test", "<>", "?9", "?3"),
                        ("Test", "<>", "?9", "?4"),
                        ("Test", "<>", "?9", "?5"),
                        ("Test", "<>", "?9", "?6"),
                        ("Test", "<>", "?9", "?7"),
                        ("Test", "<>", "?9", "?8")
                    ],
                    [
                        ("assert", ("Item", ("?x1","?y1","?9", "?b")))
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
                        (True, "Box", ("?x1", "?y1", "?b"), "9"),
                        (True, "Box", ("?x2", "?y1", "?b"), "10"),
                        (True, "Box", ("?x3", "?y1", "?b"), "11"),
                        (True, "Box", ("?x1", "?y2", "?b"), "12"),
                        (True, "Box", ("?x2", "?y2", "?b"), "13"),
                        (True, "Box", ("?x3", "?y2", "?b"), "14"),
                        (True, "Box", ("?x1", "?y3", "?b"), "12"),
                        (True, "Box", ("?x2", "?y3", "?b"), "13"),

                        (True, "CantBe", ("?x1","?y1", "?1"), "1"),
                        (True, "CantBe", ("?x2","?y1", "?1"), "2"),
                        (True, "CantBe", ("?x3","?y1", "?1"), "3"),
                        (True, "CantBe", ("?x1","?y2", "?1"), "4"),
                        (True, "CantBe", ("?x2","?y2", "?1"), "5"),
                        (True, "CantBe", ("?x3","?y2", "?1"), "6"),
                        (True, "CantBe", ("?x1","?y3", "?1"), "7"),
                        (True, "CantBe", ("?x2","?y3", "?1"), "8"),

                        ("Test", "<>", "?x3", "?x1"),
                        ("Test", "<>", "?x3", "?x2"),
                        ("Test", "<", "?x1", "?x2"),

                        ("Test", "<>", "?y3", "?y1"),
                        ("Test", "<>", "?y3", "?y2"),
                        ("Test", "<", "?y1", "?y2")
                    ],
                    [
                        ("assert", ("Item", ("?x3","?y3","?1", "?b")))
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
                        (True, "CantBe", ("?x6","?y1", "?1"), "6"),
                        (True, "CantBe", ("?x7","?y1", "?1"), "7"),
                        (True, "CantBe", ("?x8","?y1", "?1"), "8"),
                        (True, "Box", ("?x9","?y1","?b"), "9"),
                        ("Test","<","?x1","?x2"),
                        ("Test","<","?x2","?x3"),
                        ("Test","<","?x3","?x4"),
                        ("Test","<","?x4","?x5"),
                        ("Test","<","?x5","?x6"),
                        ("Test","<","?x6","?x7"),
                        ("Test","<","?x7","?x8"),
                        ("Test", "<>", "?x9", "?x1"),
                        ("Test", "<>", "?x9", "?x2"),
                        ("Test", "<>", "?x9", "?x3"),
                        ("Test", "<>", "?x9", "?x4"),
                        ("Test", "<>", "?x9", "?x5"),
                        ("Test", "<>", "?x9", "?x6"),
                        ("Test", "<>", "?x9", "?x7"),
                        ("Test", "<>", "?x9", "?x8")
                    ],
                    [
                        ("assert", ("Item", ("?x9", "?y1", "?1", "?b")))
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
                        (True, "CantBe", ("?x1","?y6", "?1"), "6"),
                        (True, "CantBe", ("?x1","?y7", "?1"), "7"),
                        (True, "CantBe", ("?x1","?y8", "?1"), "8"),
                        (True, "Box", ("?x1","?y9","?b"), "9"),
                        ("Test","<","?y1","?y2"),
                        ("Test","<","?y2","?y3"),
                        ("Test","<","?y3","?y4"),
                        ("Test","<","?y4","?y5"),
                        ("Test","<","?y5","?y6"),
                        ("Test","<","?y6","?y7"),
                        ("Test","<","?y7","?y8"),
                        ("Test", "<>", "?y9", "?y1"),
                        ("Test", "<>", "?y9", "?y2"),
                        ("Test", "<>", "?y9", "?y3"),
                        ("Test", "<>", "?y9", "?y4"),
                        ("Test", "<>", "?y9", "?y5"),
                        ("Test", "<>", "?y9", "?y6"),
                        ("Test", "<>", "?y9", "?y7"),
                        ("Test", "<>", "?y9", "?y8")
                    ],
                    [
                        ("assert", ("Item", ("?x1", "?y9", "?1", "?b")))
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
                        (True, "Number", ("?2",), "2"),
                        (True, "Number", ("?3",), "3"),
                        (True, "Number", ("?4",), "4"),
                        (True, "Number", ("?5",), "5"),
                        (True, "Number", ("?6",), "6"),
                        (True, "Number", ("?7",), "7"),
                        (True, "Number", ("?8",), "8"),
                        (True, "Number", ("?9",), "9"),
                        (True, "Item", ("?x1","?y1", "?1", "?b"), "1"),
                        ("Test", "<", "?2", "?3"),
                        ("Test", "<", "?3", "?4"),
                        ("Test", "<", "?4", "?5"),
                        ("Test", "<", "?5", "?6"),
                        ("Test", "<", "?6", "?7"),
                        ("Test", "<", "?7", "?8"),
                        ("Test", "<", "?8", "?9"),
                        ("Test", "<>", "?1", "?2"),
                        ("Test", "<>", "?1", "?3"),
                        ("Test", "<>", "?1", "?4"),
                        ("Test", "<>", "?1", "?5"),
                        ("Test", "<>", "?1", "?6"),
                        ("Test", "<>", "?1", "?7"),
                        ("Test", "<>", "?1", "?8"),
                        ("Test", "<>", "?1", "?9")
                    ],
                    [
                        ("assert", ("CantBe", ("?x1", "?y1", "?2"))),
                        ("assert", ("CantBe", ("?x1", "?y1", "?3"))),
                        ("assert", ("CantBe", ("?x1", "?y1", "?4"))),
                        ("assert", ("CantBe", ("?x1", "?y1", "?5"))),
                        ("assert", ("CantBe", ("?x1", "?y1", "?6"))),
                        ("assert", ("CantBe", ("?x1", "?y1", "?7"))),
                        ("assert", ("CantBe", ("?x1", "?y1", "?8"))),
                        ("assert", ("CantBe", ("?x1", "?y1", "?9"))),
                    ]
                )
            ),
            False
            )

            self.rbs.net.applyRulesToFacts()
            self.rbs.net.save("sudoku9_canBe.rbs")
            self.rbs.exe.apply()
    
    def solve(self, sudoku):
        for y,s in enumerate(sudoku):
            for x,i in enumerate(s):
                if (i <> None):
                    boxIndex = self.getBoxIndex(x+1, y+1)
                    f = self.rbs.getFact(("Item", (x+1, y+1, i, boxIndex)), apply=False)
                    if(f.ca not in self.rbs.net.activations):
                        self.rbs.net.activations.append(f.ca)

        self.rbs.exe.apply()
