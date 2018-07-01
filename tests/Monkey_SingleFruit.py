"""

Single Fruit Test

"""

import nealParams as nealParameters
import pyNN.nest as sim
from monkeyProblem import MonekyProblem

sim.setup(timestep=nealParameters.DELAY,min_delay=nealParameters.DELAY,max_delay=nealParameters.DELAY, debug=0)

mp = MonekyProblem()

mp.rbs.addFact(("chairAt", (1,)))
mp.rbs.addFact(("fruit",("banana",0)))

sim.run(nealParameters.SIM_LENGTH)

mp.printSpikes("Monkey_SingleFruit")

sim.end()