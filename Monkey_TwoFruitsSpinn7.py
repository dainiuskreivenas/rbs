import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

"""

Two Fruit Test 
Fruits:
 1: Banana, 0;
 2: Apple, 1.
Chair:
    1: 2

"""

import pyNN.spiNNaker as sim
#import pyNN.nest as sim
from monkeyProblem import MonekyProblem

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

mp = MonekyProblem(sim, "spinnaker",7)
#mp = MonekyProblem(sim, "nest")

mp.rbs.addFact(("chairAt", (2,)))
mp.rbs.addFact(("fruit",("banana",0)))
mp.rbs.addFact(("fruit",("apple",1)))

mp.rbs.neal.nealApplyProjections()
sim.run(200)

mp.printSpikes("Monkey_TwoFruits")
mp.rbs.printAllSpikes()

sim.end()



