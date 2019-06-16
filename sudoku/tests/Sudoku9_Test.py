import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

#import pyNN.spiNNaker as sim
import pyNN.nest as sim

from Sudoku9 import Sudoku9
import logging
import time
import datetime


sim.setup(timestep=2.0,min_delay=2.0,max_delay=2.0, time_scale_factor=40)

logging.info("Setting up the Sudoku Board")

#sudoku9 = Sudoku9(sim, "spinnaker", True)
sudoku9 = Sudoku9(sim, "nest", True)


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

logging.info("Applying a puzzle")
sudoku9.solve(sudoku)

logging.info("Running Simulation")
sim.run(500)

print "neuron - {}".format(sudoku9.rbs.net.neuron)
print "synapses - {}".format(len(sudoku9.rbs.net.connections))

data = {}
def getData(population):
    if population.pop.label in data:
        return data[population.pop.label]
    
    d = population.pop.get_data()
    data[population.pop.label] = d

    return d
    

for g in sudoku9.rbs.net.facts:
    for f in sudoku9.rbs.net.facts[g]:
        min = 10000
        pop = sudoku9.rbs.get_population(f.ca[0])
        d = getData(pop)
        st = d.segments[0].spiketrains[f.ca[0]-pop.fromIndex]
        if len(st) > 0:
            min = st.magnitude[0]
        hasSpiked = len(st) > 0
        print "(f-{} - {} {}) - {} - at {}".format(f.index, f.group, f.attributes, hasSpiked, min)

assertionTimes = {}

neurons = []

for l in sudoku9.rbs.net.assertions:
    neuron = sudoku9.rbs.net.assertions[l]
    neurons.append(neuron)

for n in neurons:
    pop = sudoku9.rbs.get_population(n)
    d = getData(pop)
    index = n - pop.fromIndex

    t = d.segments[0].spiketrains[index]
    if(len(t.magnitude) > 0):
        if (t.magnitude[0] in assertionTimes):
            assertionTimes[t.magnitude[0]] += 1
        else:
            assertionTimes[t.magnitude[0]] = 1

times = []
for t in assertionTimes:
    times.append(t)
    
times.sort()
for t in times:
    print "{} - {}".format(t,assertionTimes[t])

logging.info("End")

sim.end()