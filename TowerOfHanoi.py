"""

Tower of Hanoi expert system.
Usage new instance pass in number of discs. Run a simulation.

"""

from rbs import RBS

class TowerOfHanoi:
    def __init__(self, discNum):
        self.rbs = RBS()

        self.rbs.addRule(
            (
                "ToH",
                (
                    [
                        (True, "ToH", ("?d",), "r1"),            
                    ],
                    [
                        ("assert", ("tower", ("A",))),
                        ("assert", ("tower", ("B",))),
                        ("assert", ("tower", ("C",))),
                        ("assert", ("stackTop", (0,))),
                        ("assert", ("stack", (0, "goal", 1, "?d", "A", "C"))),
                        ("assert", ("addDisk", ("?d", "A"))),
                        ("retract", "r1")
                    ]
                )
            )
        )

        self.rbs.addRule(
            (
                "addDisk",
                (
                    [
                        (True, "addDisk", ("?d","?from"), "a"),
                        ("Test", ">", "?d", 1)
                    ],
                    [
                        ("retract", "a"),
                        ("assert", ("diskAt", ("?d", "?from"))),
                        ("assert", ("addDisk", (("-", "?d", 1),"?from")))
                    ]
                )
            )
        )

        self.rbs.addRule(
            (
                "addFinalDisk",
                (
                    [
                        (True, "addDisk", ("?d","?from"), "a"),
                        ("Test", "=", "?d", 1)
                    ],
                    [
                        ("retract", "a"),
                        ("assert", ("diskAt", ("?d", "?from")))
                    ]
                )
            )
        )

        self.rbs.addRule(
            (
                "GoalToGoals",
                (
                    [
                        (True, "stack", ("?t", "goal", "?topDisc", "?bottomDisc", "?from", "?to"), "g"),
                        (True, "stackTop", ("?t",), "st"),
                        (True, "tower", ("?from",), "towerFrom"),
                        (True, "tower", ("?to",), "towerTo"),
                        (True, "tower", ("?other",), "towerOther"),
                        ("Test", "<>", "?from", "?other"),
                        ("Test", "<>", "?to", "?other"),
                        ("Test", "<", ("+", "?topDisc", 1), "?bottomDisc"),
                    ],
                    [
                        ("retract", "g"),
                        ("retract", "st"),
                        ("assert", ("stackTop",(("+","?t",2),))),
                        ("assert", ("stack", ("?t", "goal", "?topDisc", ("-", "?bottomDisc", 1), "?other", "?to"))),
                        ("assert", ("stack", (("+", "?t", 1), "move", "?bottomDisc", "?from", "?to"))),
                        ("assert", ("stack", (("+", "?t", 2), "goal", "?topDisc", ("-", "?bottomDisc", 1), "?from", "?other")))
                    ]
                )
            )
        )

        self.rbs.addRule(
            (
                "GoalToMoves",
                (
                    [
                        (True, "stack", ("?t", "goal", "?topDisc", "?bottomDisc", "?from", "?to"), "g"),
                        (True, "stackTop", ("?t",), "st"),
                        (True, "tower", ("?from",), "towerFrom"),
                        (True, "tower", ("?to",), "towerTo"),
                        (True, "tower", ("?other",), "towerOther"),
                        ("Test", "<>", "?from", "?other"),
                        ("Test", "<>", "?to", "?other"),
                        ("Test", "=", ("+", "?topDisc", 1), "?bottomDisc"),
                    ],
                    [
                        ("retract", "g"),
                        ("retract", "st"),
                        ("assert", ("stackTop",(("+", "?t", 2),))),
                        ("assert", ("stack", ("?t", "move", "?topDisc", "?other", "?to"))),
                        ("assert", ("stack", (("+", "?t", 1), "move", "?bottomDisc", "?from", "?to"))),
                        ("assert", ("stack", (("+", "?t", 2), "move", "?topDisc", "?from", "?other")))
                    ]
                )
            )
        )

        self.rbs.addRule(
            (
                "MakeMove",
                (
                    [
                        (True, "stack", ("?t","move","?disc","?from","?to"), "g"),
                        (True, "stackTop", ("?t",), "st"),
                        (True, "diskAt", ("?disc","?from"), "d")
                    ],
                    [
                        ("retract", "g"),
                        ("retract", "d"),
                        ("retract", "st"),
                        ("assert", ("diskAt",("?disc","?to"))),
                        ("assert", ("stackTop",(("-","?t",1),)))
                    ]
                )
            )
        )

        self.rbs.addFact(("ToH",(discNum,)))

    def printSpikes(self, name):
        # "################### interns ###############"

        for inter in self.rbs.interns:
            inter.printSpikes("pkls/"+name+"/interns/{}.pkl".format(inter.label))


        # "################### assertions ###############"

        for key in self.rbs.assertions.keys():
            aa = self.rbs.assertions[key]
            aa.printSpikes("pkls/"+name+"/assertions/{}.pkl".format(aa.label))

        # "################### assertions ###############"

        for key in list(self.rbs.factGroups):
            for f in self.rbs.factGroups[key]:
                f[0][1].printSpikes("pkls/"+name+"/facts/{}.pkl".format(f[0][1].label))
