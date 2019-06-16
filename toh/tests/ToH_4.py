"""

Tower of Hanoi 4 disc problem test

"""
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

#import pyNN.spiNNaker as sim
import pyNN.nest as sim

from TowerOfHanoi import TowerOfHanoi

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

#toh = TowerOfHanoi(sim, "spinnaker", 4)
toh = TowerOfHanoi(sim, "nest", 4)

sim.run(4000)

toh.printSpikes("TowerOfHanoi_4")

sim.end()