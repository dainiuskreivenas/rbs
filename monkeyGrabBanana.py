"""

Single Fruit Test

"""

import nealParams as nealParameters
if (nealParameters.simulator=="spinnaker"):
    import pyNN.spiNNaker as sim
elif (nealParameters.simulator=="nest"):
    import pyNN.nest as sim

from rbs import RBS

sim.setup(timestep=nealParameters.DELAY,min_delay=nealParameters.DELAY,max_delay=nealParameters.DELAY, debug=0)

rbs = RBS()

rbs.addRule(
    (
        "MonkeyCanReach",
        (
            [
                (True, "MonkeyCanReach", ("?type",),"b")
            ],
            [
                ("assert",("MonkeyGrab", ("?type",))),
                ("retract", "b")
            ]
        )
    )
)

rbs.addFact(("MonkeyCanReach",("banana",)))

sim.run(50)

rbs.printSpikes()

sim.end()