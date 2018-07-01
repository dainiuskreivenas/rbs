"""

Two Fruit Test 
Fruits:
 1: Banana, 0;
 2: Banana, 1.
Chair:
    1: 2

"""

import nealParams as nealParameters
import pyNN.nest as sim
from monkeyProblem import MonekyProblem

sim.setup(timestep=nealParameters.DELAY,min_delay=nealParameters.DELAY,max_delay=nealParameters.DELAY, debug=0)

mp = MonekyProblem()

mp.rbs.addFact(("chairAt", (2,)))
mp.rbs.addFact(("fruit",("banana",0)))
mp.rbs.addFact(("fruit",("banana",1)))

sim.run(nealParameters.SIM_LENGTH)

mp.printSpikes("Monkey_TwoSameFruits")

sim.end()