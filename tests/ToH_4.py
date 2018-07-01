"""

Tower of Hanoi 4 disc problem test

"""

import pyNN.nest as sim
from TowerOfHanoi import TowerOfHanoi

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

toh = TowerOfHanoi(4)

sim.run(4000)

toh.printSpikes("TowerOfHanoi_4")

sim.end()