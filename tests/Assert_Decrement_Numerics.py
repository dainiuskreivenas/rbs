"""

Test for numerical decrementation of Asserted Fact values

"""
import sys
import os
sys.path.append(os.getcwd() + '/..')
import pyNN.nest as sim
from rbs.narcBuilder import NeuralCognitiveArchitectureBuilder
from rbs.stateMachineClass import FSAHelperFunctions
from rbs.nealCoverClass import NealCoverFunctions

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
                ("assert", ("difference", (("-", "?number", 1),"?number2"))),
                ("retract", "r1")
            ]    
)

narc.addRule(
        "test1",
        
            [
                (True, "difference", ("?number","?number2"), "r1")
            ],
            [
                ("assert", ("diffOfdifference", (("-", "?number", "?number2"),))),
                ("retract", "r1")
            ]
)

narc.addFact("item", (10,5))

narc.apply()

sim.run(50)

narc.printSpikes()

sim.end()