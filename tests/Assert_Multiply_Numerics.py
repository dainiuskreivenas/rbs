"""

Test for numerical multiplication of Asserted Fact values

"""

#import pyNN.spiNNaker as sim
import pyNN.nest as sim
from rbs import RuleBasedSystem as RBS

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

#rbs = RBS(sim, "spinnaker")
rbs = RBS(sim, "nest")

rbs.addRule(
    (
        "test",
        (
            [
                (True, "item", ("?number","?number2"), "r1")
            ],
            [
                ("assert", ("mutiplyOf2", (("*", "?number", 2),"?number2"))),
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
                (True, "mutiplyOf2", ("?number","?number2"), "r1")
            ],
            [
                ("assert", ("mutiplyOfAttr", (("*", "?number", "?number2"),))),
                ("retract", "r1")
            ]
        )
    ) 
)

rbs.addFact(("item", (2,4)))

sim.run(50)

rbs.printSpikes()

sim.end()