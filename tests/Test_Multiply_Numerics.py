"""

Test for numerical incrementation within Test Condition

"""

import nealParams as nealParameters
if (nealParameters.simulator=="spinnaker"):
    import pyNN.spiNNaker as sim
elif (nealParameters.simulator=="nest"):
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
                ("Test", "<", ("*", "?number", 2), "?number2")
            ],
            [
                ("assert", ("less", ("?number","?number2"))),
                ("retract", "r1")
            ]
        )
    )
)

rbs.addFact(("item", (2,5)))

sim.run(50)

rbs.printSpikes()

sim.end()