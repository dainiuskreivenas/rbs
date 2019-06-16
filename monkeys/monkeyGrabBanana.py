"""

Single Fruit Test

"""
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

#import pyNN.spiNNaker as sim
import pyNN.nest as sim

from rbs import RBS

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

#rbs = RBS(sim, "spinnaker")
rbs = RBS(sim, "nest")

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