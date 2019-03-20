import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

"""

Single Fruit Test
    Fruit:
        1. Banana, 0
    Chair:
        1. 0

"""

import nealParams

if (nealParams.simulator=="spinnaker"):
    import pyNN.spiNNaker as sim
elif (nealParams.simulator=="nest"):
    import pyNN.nest as sim
from monkeyProblem import MonekyProblem


sim.setup(timestep=nealParams.DELAY,min_delay=nealParams.DELAY,max_delay=nealParams.DELAY, debug=0)

mp = MonekyProblem()

mp.rbs.addFact(("chairAt", (0,)))
mp.rbs.addFact(("fruit",("banana",0)))

sim.run(nealParams.SIM_LENGTH)

mp.printSpikes("Monkey_SingleWithChair")

sim.end()



