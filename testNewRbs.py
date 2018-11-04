import pyNN.nest as sim
import nealParams as nealParameters
import pickle
from rbs import RBS

sim.setup(timestep=nealParameters.DELAY,min_delay=nealParameters.DELAY,max_delay=nealParameters.DELAY, debug=0)



rbs = RBS()

rbs.addFact(
    (
        "MonkeyReach", ("banana",)
    )
)

rbs.addRule((
    "MonkeyGrab",
    (
        [
            (True, "MonkeyReach", ("?x",), "1")
        ],
        [
            ("assert", ("MonkeyHas", ("?x",))),
            ("retract", "1")
        ]
    )
))

rbs.addRule((
    "MonkeyEat",
    (
        [
            (True, "MonkeyHas", ("?x",), "1")
        ],
        [
            ("retract", "1")
        ]
    )
))

rbs.net.save("test.pkl")


rbs = RBS(fromFile="test.pkl")

sim.run(30)

rbs.addFact(
    (
        "MonkeyReach", ("apple",)
    )
)

sim.run(30)

rbs.exe.printSpikes()
