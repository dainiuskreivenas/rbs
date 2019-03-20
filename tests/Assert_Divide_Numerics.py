"""

Test for numerical division of Asserted Fact values

"""


import nealParams

if (nealParams.simulator=="spinnaker"):
    import pyNN.spiNNaker as sim
elif (nealParams.simulator=="nest"):
    import pyNN.nest as sim
from rbs import RBS

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

rbs = RBS()

rbs.addRule(
    (
        "test",
        (
            [
                (True, "item", ("?number","?number2"), "r1")
            ],
            [
                ("assert", ("divisionOf2", (("/", "?number", 2),"?number2"))),
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
                (True, "divisionOf2", ("?number","?number2"), "r1")
            ],
            [
                ("assert", ("divisionOfAttr", (("/", "?number", "?number2"),))),
                ("retract", "r1")
            ]
        )
    ) 
)

rbs.addFact(("item", (16,4)))

sim.run(50)

rbs.printSpikes()

sim.end()