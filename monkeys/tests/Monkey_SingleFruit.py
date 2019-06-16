import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

"""

Single Fruit Test

"""

#import pyNN.spiNNaker as sim
import pyNN.nest as sim

from monkeyProblem import MonekyProblem

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

#mp = MonekyProblem(sim, "spinnaker")
mp = MonekyProblem(sim, "nest")

mp.rbs.addFact(("chairAt", (1,)))
mp.rbs.addFact(("fruit",("banana",0)))

sim.run(200)

mp.printSpikes("Monkey_SingleFruit")

sim.end()