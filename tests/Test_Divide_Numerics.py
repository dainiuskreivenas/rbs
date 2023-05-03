"""

Test for numerical incrementation within Test Condition

"""
import sys
import os
sys.path.append(os.getcwd() + '/..')
import pyNN.nest as sim
from rbs.narcBuilder import NeuralCognitiveArchitectureBuilder
from rbs.stateMachineClass import FSAHelperFunctions
from rbs.nealCoverClass import NealCoverFunctions

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

#rbs = RBS(sim, "spinnaker")
simName = "nest"
neal = NealCoverFunctions(simName, sim)
fsa = FSAHelperFunctions(simName, sim, neal)
narc = NeuralCognitiveArchitectureBuilder(simName, sim, fsa, neal).build()

narc.addRule(
    
        "test",
        
            [
                (True, "item", ("?number","?number2"), "r1"),
                ("test", "<", ("/", "?number", 2), "?number2")
            ],
            [
                ("assert", ("less", ("?number","?number2"))),
                ("retract", "r1")
            ]
        
    
)

narc.addFact("item", (6,4))

narc.apply()

sim.run(50)

narc.printSpikes()

sim.end()