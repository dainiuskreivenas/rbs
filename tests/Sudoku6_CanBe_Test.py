
import nealParams

if (nealParams.simulator=="spinnaker"):
    import pyNN.spiNNaker as sim
elif (nealParams.simulator=="nest"):
    import pyNN.nest as sim

from Sudoku6_CanBe import Sudoku6_CanBe
import time
import numpy as np
import datetime


sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0)

print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

sudoku6 = Sudoku6_CanBe()

sudoku = [[None,  6 ,None      ,None,None,  1 ],
          [None,None,None      ,  4 ,  2 ,None],


          [  1 ,None,None      ,None,None,None],
          [None,None,None      ,None,None,  5 ],


          [None,  4 ,  5       ,None,None,None],
          [  3 ,None,None      ,None,  4 ,None]]

print "Beginning To Solve the Puzzle"
sudoku6.solve(sudoku)

print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

sim.run(200)

print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

print "neuron - {}".format(sudoku6.rbs.net.neuron)
print "synapses - {}".format(len(sudoku6.rbs.net.connections))


data = {}
def getData(population):
    if population.pop.label in data:
        return data[population.pop.label]
    
    d = population.pop.get_data()
    data[population.pop.lalbe] = d

    return d
    

for g in sudoku6.rbs.net.facts:
    for f in sudoku6.rbs.net.facts[g]:
        min = 10000
        pop = sudoku6.rbs.get_population(f.ca[0])
        data = getData(pop)
        st = data.segments[0].spiketrains[f.ca[0]-pop.fromIndex]
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
    data = getData(pop)

    for spikes in data.segments[0].spiketrains[n - pop.fromIndex]:
        hasSpiked = len(spikes) > 0
        if(hasSpiked):
            t = spikes.magnitude[0]
            if (t in assertionTimes):
                assertionTimes[t] += 1
            else:
                assertionTimes[t] = 1
        break

for t in assertionTimes:
    print "{} - {}".format(t,assertionTimes[t])

print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

sim.end()