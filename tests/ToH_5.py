"""

Tower of Hanoi 5 disc problem test

"""

import pyNN.nest as sim
from TowerOfHanoi import TowerOfHanoi

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

toh = TowerOfHanoi(5)

sim.run(5000)

toh.printSpikes("TowerOfHanoi_5")

sim.end()