"""

Operators Tests for numerical

"""
import pyNN.nest as sim
from .. import RuleBasedSystemBuilder
from .. import FSAHelperFunctions
from .. import NealCoverFunctions

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

#rbs = RBS(sim, "spinnaker")
simName = "nest"
neal = NealCoverFunctions(simName, sim)
fsa = FSAHelperFunctions(simName, sim, neal)
rbs = RuleBasedSystemBuilder(sim, simName, fsa).build()

rbs.addRule(
    
        "test",
        
            [
                (True, "item", ("?number","?number2"), "r1"),
                ("test", "=", "?number", "?number2")
            ],
            [
                ("assert", ("equal", ("?number","?number2"))),
                ("retract", "r1")
            ]
        
    
)

rbs.addRule(
    
        "test1",
        
            [
                (True, "item2", ("?number","?number2"), "r1"),
                ("test", "<>", "?number", "?number2")
            ],
            [
                ("assert", ("not equal", ("?number","?number2"))),
                ("retract", "r1")
            ]
        
    
)

rbs.addRule(
    
        "test2",
        
            [
                (True, "item3", ("?number","?number2"), "r1"),
                ("test", ">", "?number", "?number2")
            ],
            [
                ("assert", ("more", ("?number","?number2"))),
                ("retract", "r1")
            ]
        
    
)

rbs.addRule(
    
        "test3",
        
            [
                (True, "item4", ("?number","?number2"), "r1"),
                ("test", "<", "?number", "?number2")
            ],
            [
                ("assert", ("less", ("?number","?number2"))),
                ("retract", "r1")
            ]
        
    
)

rbs.addFact("item", (1,1))

rbs.addFact("item2", (1,2))

rbs.addFact("item3", (2,1))

rbs.addFact("item4", (1,2))

neal.nealApplyProjections()

sim.run(200)

rbs.printSpikes()

sim.end()