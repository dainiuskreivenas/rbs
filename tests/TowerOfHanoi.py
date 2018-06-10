"""

Test for numerical Decrement within Test condition

"""


import pyNN.nest as sim
from rbs import RBS

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

rbs = RBS()

rbs.addRule(
    (
        "ToH",
        (
            [
                (True, "ToH", ("?d",), "r1"),            
            ],
            [
                ("assert", ("tower", (1,))),
                ("assert", ("tower", (2,))),
                ("assert", ("tower", (3,))),
                ("assert", ("stackTop", (0,))),
                ("assert", ("stack", (0, "goal", 1, "?d", 1, 3))),
                ("assert", ("addDisk", ("?d", 1))),
                ("retract", "r1")
            ]
        )
    )
)

rbs.addRule(
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

rbs.addRule(
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

rbs.addRule(
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

rbs.addRule(
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

rbs.addRule(
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

rbs.addFact(("ToH",(4,)))

sim.run(1200)

for key in list(rbs.factGroups):
    for f in rbs.factGroups[key]:
        f[0][1].printSpikes("pkls/TowerOfHanoi/facts/{}.pkl".format(f[0][1].label))

sim.end()