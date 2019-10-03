"""

Test for numerical decrementation of Asserted Fact values

"""

import pyNN.nest as sim
from .. import RuleBasedSystemBuilder
from .. import FSAHelperFunctions
from .. import NealCoverFunctions

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

simName = "nest"
neal = NealCoverFunctions(simName, sim)
fsa = FSAHelperFunctions(simName, sim, neal)
rbs = RuleBasedSystemBuilder(sim, simName, fsa).build()

rbs.addRule(
        "test",
            [
                (True, "item", ("?number","?number2"), "r1")
            ],
            [
                ("assert", ("difference", (("-", "?number", 1),"?number2"))),
                ("retract", "r1")
            ]    
)

rbs.addRule(
        "test1",
        
            [
                (True, "difference", ("?number","?number2"), "r1")
            ],
            [
                ("assert", ("diffOfdifference", (("-", "?number", "?number2"),))),
                ("retract", "r1")
            ]
)

rbs.addFact("item", (10,5))

neal.nealApplyProjections()

sim.run(50)

rbs.printSpikes()

sim.end()