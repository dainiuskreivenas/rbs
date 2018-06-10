"""

Test for numerical Decrement within Test condition

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
                ("Test", "<", ("-", "?number", 1), "?number2")
            ],
            [
                ("assert", ("less", ("?number","?number2"))),
                ("retract", "r1")
            ]
        )
    )
)

rbs.addFact(("item", (2,2)))

sim.run(50)

for key in list(rbs.factGroups):
    for f in rbs.factGroups[key]:
        f[0][1].printSpikes("pkls/Test_Decrement_Numerics/facts/{}.pkl".format(f[0][1].label))

sim.end()