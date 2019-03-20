import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

"""

Two Fruit Test 
Fruits:
 1: Banana, 0;
 2: Banana, 1.
Chair:
    1: 2

"""

import nealParams as nealParameters
if (nealParameters.simulator=="spinnaker"):
    import pyNN.spiNNaker as sim
elif (nealParameters.simulator=="nest"):
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