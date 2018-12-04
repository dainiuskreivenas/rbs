
import nealParams

if (nealParams.simulator=="spinnaker"):
    import pyNN.spiNNaker as sim
elif (nealParams.simulator=="nest"):
    import pyNN.nest as sim

from Sudoku6_CanBe import Sudoku6_CanBe
import logging
import numpy as np
import datetime


sim.setup(timestep=2.0,min_delay=2.0,max_delay=2.0, time_scale_factor=40)

logging.info("Setting up the Sudoku Board")

sudoku6 = Sudoku6_CanBe()

sudoku = [[None,  6 ,None      ,None,None,  1 ],
          [None,None,None      ,  4 ,  2 ,None],


          [  1 ,None,None      ,None,None,None],
          [None,None,None      ,None,None,  5 ],


          [None,  4 ,  5       ,None,None,None],
          [  3 ,None,None      ,None,  4 ,None]]

logging.info("Applying a puzzle")
sudoku6.solve(sudoku)

logging.info("Running Simulation")
sim.run(500)

sudoku6.rbs.printSpikes()

print "neuron - {}".format(sudoku6.rbs.net.neuron)
print "synapses - {}".format(len(sudoku6.rbs.net.connections))

data = {}
def getData(population):
    if population.pop.label in data:
        return data[population.pop.label]
    
    d = population.pop.get_data()
    data[population.pop.label] = d

    return d
    

for g in sudoku6.rbs.net.facts:
    for f in sudoku6.rbs.net.facts[g]:
        min = 10000
        pop = sudoku6.rbs.get_population(f.ca[0])
        d = getData(pop)
        st = d.segments[0].spiketrains[f.ca[0]-pop.fromIndex]
        if len(st) > 0:
            min = st.magnitude[0]
        hasSpiked = len(st) > 0
        print "(f-{} - {} {}) - {} - at {}".format(f.index, f.group, f.attributes, hasSpiked, min)

assertionTimes = {}

neurons = []

for l in sudoku6.rbs.net.assertions:
    neuron = sudoku6.rbs.net.assertions[l]
    neurons.append(neuron)

for n in neurons:
    pop = sudoku6.rbs.get_population(n)
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