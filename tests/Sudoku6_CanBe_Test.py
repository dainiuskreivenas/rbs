

import pyNN.nest as sim
from Sudoku6_CanBe import Sudoku6_CanBe
import time
import numpy as np
import datetime


sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)


print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

sudoku6 = Sudoku6_CanBe()

sudoku = [[None,  6 ,None      ,None,None,  1 ],
          [None,None,None      ,  4 ,  2 ,None],


          [  1 ,None,None      ,None,None,None],
          [None,None,None      ,None,None,  5 ],


          [None,  4 ,  5       ,None,None,None],
          [  3 ,None,None      ,None,  4 ,None]]

sudoku6.solve(sudoku)

print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

sim.run(200)

print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

"""
for g in sudoku6.rbs.net.facts:
    for f in sudoku6.rbs.net.facts[g]:
        min = 10000
        data = sudoku6.rbs.exe.assembly[f.ca[0]:f.ca[9]].get_data()
        if len(data.segments[0].spiketrains[0]) > 0:
            min = data.segments[0].spiketrains[0].magnitude[0]
        hasSpiked = len(data.segments[0].spiketrains[0]) > 0
        print "(f-{} - {} {}) - {} - at {}".format(f.index, f.group, f.attributes, hasSpiked, min)
"""

assertionTimes = {}

neurons = []

for l in sudoku6.rbs.net.assertions:
    neuron = sudoku6.rbs.net.assertions[l]
    neurons.append(neuron)

pop = sudoku6.rbs.exe.assembly[neurons]
print pop

data = pop.get_data()
for spikes in data.segments[0].spiketrains:
    hasSpiked = len(spikes) > 0
    if(hasSpiked):
        t = spikes.magnitude[0]
        if (t in assertionTimes):
            assertionTimes[t] += 1
        else:
            assertionTimes[t] = 1

for t in assertionTimes:
    print "{} - {}".format(t,assertionTimes[t])

print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

sim.end()