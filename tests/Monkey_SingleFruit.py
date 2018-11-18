"""

Single Fruit Test

"""

import nealParams

if (nealParams.simulator=="spinnaker"):
    import pyNN.spiNNaker as sim
elif (nealParams.simulator=="nest"):
    import pyNN.nest as sim

from monkeyProblem import MonekyProblem

sim.setup(timestep=nealParams.DELAY,min_delay=nealParams.DELAY,max_delay=nealParams.DELAY, debug=0)

mp = MonekyProblem()

mp.rbs.addFact(("chairAt", (1,)))
mp.rbs.addFact(("fruit",("banana",0)))

sim.run(nealParams.SIM_LENGTH)

mp.printSpikes("Monkey_SingleFruit")

sim.end()