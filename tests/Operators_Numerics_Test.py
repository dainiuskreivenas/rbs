"""

Operators Tests for numerical

"""


import pyNN.nest as sim
from rbs import RBS

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

rbs = RBS()

rbs.addRule(
    (
        "test",
        (
            [
                (True, "item", ("?number","?number2"), "r1"),
                ("Test", "=", "?number", "?number2")
            ],
            [
                ("assert", ("equal", ("?number","?number2"))),
                ("retract", "r1")
            ]
        )
    )
)

rbs.addRule(
    (
        "test1",
        (
            [
                (True, "item2", ("?number","?number2"), "r1"),
                ("Test", "<>", "?number", "?number2")
            ],
            [
                ("assert", ("not equal", ("?number","?number2"))),
                ("retract", "r1")
            ]
        )
    )
)

rbs.addRule(
    (
        "test2",
        (
            [
                (True, "item3", ("?number","?number2"), "r1"),
                ("Test", ">", "?number", "?number2")
            ],
            [
                ("assert", ("more", ("?number","?number2"))),
                ("retract", "r1")
            ]
        )
    )
)

rbs.addRule(
    (
        "test3",
        (
            [
                (True, "item4", ("?number","?number2"), "r1"),
                ("Test", "<", "?number", "?number2")
            ],
            [
                ("assert", ("less", ("?number","?number2"))),
                ("retract", "r1")
            ]
        )
    )
)

rbs.addFact(("item", (1,1)))

rbs.addFact(("item2", (1,2)))

rbs.addFact(("item3", (2,1)))

rbs.addFact(("item4", (1,2)))

sim.run(200)

# "################### retracts ###############"

for key in rbs.retractions.keys():
    re = rbs.retractions[key]
    re.printSpikes("pkls/Operators_Numerics_Tests/retractions/{}.pkl".format(re.label))

# "################### assertions ###############"

for key in rbs.assertions.keys():
    aa = rbs.assertions[key]
    aa.printSpikes("pkls/Operators_Numerics_Tests/assertions/{}.pkl".format(aa.label))


# "################### facts ###############"

for key in list(rbs.factGroups):
    for f in rbs.factGroups[key]:
        f[0][1].printSpikes("pkls/Operators_Numerics_Tests/facts/{}.pkl".format(f[0][1].label))

sim.end()