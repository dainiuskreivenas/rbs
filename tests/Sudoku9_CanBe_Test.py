

import pyNN.nest as sim
from Sudoku9_CanBe import Sudoku9
import time
import datetime


sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)


print "Start"
print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


sudoku9 = Sudoku9()


"""
sudoku = [[None,  2 ,None,         7 ,  5 ,None,        6 ,None,  1 ],
          [  1 ,  8 ,  3 ,         6 ,None,  2 ,        5 ,  4 ,None],
          [  6 ,None,  7 ,         4 ,  3 ,  1 ,        8 ,  2 ,  9 ],
                           
                           
          [  2 ,  6 ,None,         9 ,None,  3 ,        7 ,  5 ,  4 ],
          [None,  4 ,  9 ,         5 ,  2 ,  6 ,      None,None,  3 ],
          [  3 ,  1 ,  5 ,         8 ,  4 ,  7 ,        9 ,  6 ,None],
                     
                     
          [  8 ,  9 ,  6 ,         2 ,None,  4 ,      None,  1 ,  5 ],
          [  4 ,None,  1 ,       None,  8 ,  5 ,        2 ,  9 ,  6 ],
          [  5 ,None,  2 ,         1 ,  6 ,None,        4 ,  7 ,  8 ]]
"""

sudoku = [[None,None,  7 ,         6 ,None,None,      None,None,  1 ],
          [None,None,None,         2 ,None,None,        5 ,  3 ,None],
          [None,None,None,       None,  8 ,  3 ,      None,  9 ,  7 ],
                           
                           
          [  1 ,None,None,         3 ,None,  5 ,      None,None,  8 ],
          [  4 ,  9 ,None,       None,None,  8 ,        1 ,None,None],
          [None,None,  2 ,       None,None,None,      None,  7 ,  6 ],
                     
                     
          [None,  8 ,None,       None,None,  2 ,        4 ,None,None],
          [  3 ,None,None,         4 ,  1 ,None,      None,None,None],
          [  5 ,  6 ,None,       None,None,None,      None,None,  9 ]]        

print "Solve"
print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

sudoku9.solve(sudoku)
sim.run(500)

print "neuron - {}".format(sudoku9.rbs.net.neuron)
print "synapses - {}".format(len(sudoku9.rbs.net.connections))

print "GetData"
print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

for g in sudoku9.rbs.net.facts:
    for f in sudoku9.rbs.net.facts[g]:
        min = 10000
        data = sudoku9.rbs.exe.assembly[f.ca[0]:f.ca[9]].get_data()
        if len(data.segments[0].spiketrains[0]) > 0:
            min = data.segments[0].spiketrains[0].magnitude[0]
        hasSpiked = len(data.segments[0].spiketrains[0]) > 0
        print "(f-{} - {} {}) - {} - at {}".format(f.index, f.group, f.attributes, hasSpiked, min)

assertionTimes = {}
neurons = []

for l in sudoku9.rbs.net.assertions:
    neuron = sudoku9.rbs.net.assertions[l]
    neurons.append(neuron)

pop = sudoku9.rbs.exe.assembly[neurons]

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