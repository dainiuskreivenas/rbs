"""

Test for numerical multiplication of Asserted Fact values

"""

import pyNN.nest as sim
from .. import NeuralCognitiveArchitectureBuilder
from .. import FSAHelperFunctions
from .. import NealCoverFunctions

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

simName = "nest"
neal = NealCoverFunctions(simName, sim)
fsa = FSAHelperFunctions(simName, sim, neal)
narc = NeuralCognitiveArchitectureBuilder(simName, sim, fsa, neal).build()

narc.addRule(
    
        "test",
        
            [
                (True, "item", ("?number","?number2"), "r1")
            ],
            [
                ("assert", ("mutiplyOf2", (("*", "?number", 2),"?number2"))),
                ("retract", "r1")
            ]
        
    
)

narc.addRule(
   
        "test1",
        
            [
                (True, "mutiplyOf2", ("?number","?number2"), "r1")
            ],
            [
                ("assert", ("mutiplyOfAttr", (("*", "?number", "?number2"),))),
                ("retract", "r1")
            ]
)

narc.addFact("item", (2,4))

narc.apply()

sim.run(50)

narc.printSpikes()

sim.end()