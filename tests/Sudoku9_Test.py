

import nealParams as nealParameters
if (nealParameters.simulator=="spinnaker"):
    import pyNN.spiNNaker as sim
elif (nealParameters.simulator=="nest"):
    import pyNN.nest as sim

from Sudoku9 import Sudoku9
import time
import datetime


sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

sudoku9 = Sudoku9()

sudoku = [[None,  2 ,None,         7 ,  5 ,None,        6 ,None,  1 ],
          [  1 ,  8 ,  3 ,         6 ,None,  2 ,        5 ,  4 ,None],
          [  6 ,None,  7 ,         4 ,  3 ,  1 ,        8 ,  2 ,  9 ],
                           
                           
          [  2 ,  6 ,None,         9 ,None,  3 ,        7 ,  5 ,  4 ],
          [None,  4 ,  9 ,         5 ,  2 ,  6 ,      None,None,  3 ],
          [  3 ,  1 ,  5 ,         8 ,  4 ,  7 ,        9 ,  6 ,None],
                     
                     
          [  8 ,  9 ,  6 ,         2 ,None,  4 ,      None,  1 ,  5 ],
          [  4 ,None,  1 ,       None,  8 ,  5 ,        2 ,  9 ,  6 ],
          [  5 ,None,  2 ,         1 ,  6 ,None,        4 ,  7 ,  8 ]]

print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

sudoku9.solve(sudoku)
sim.run(5000)

data = {}
def getData(population):
    if population.pop.label in data:
        return data[population.pop.label]
    
    d = population.pop.get_data()
    data[population.pop.lalbe] = d

    return d
    
for g in sudoku9.rbs.net.facts:
    for f in sudoku9.rbs.net.facts[g]:
        min = 10000
        pop = sudoku9.rbs.get_population(f.ca[0])
        data = getData(pop)
        st = data.segments[0].spiketrains[f.ca[0]-pop.fromIndex]
        if len(st) > 0:
            min = st.magnitude[0]
        hasSpiked = len(st) > 0
        print "(f-{} - {} {}) - {} - at {}".format(f.index, f.group, f.attributes, hasSpiked, min)

print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

sim.end()