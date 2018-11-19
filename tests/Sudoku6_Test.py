

import nealParams

if (nealParams.simulator=="spinnaker"):
    import pyNN.spiNNaker as sim
elif (nealParams.simulator=="nest"):
    import pyNN.nest as sim

from Sudoku6 import Sudoku6
import time
import datetime


sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, time_scale_factor=5)


sudoku6 = Sudoku6()

sudoku = [[  1 ,None,  3       ,None,  4 ,None],
          [  4 ,  6 ,None      ,  2 ,  1 ,  3 ],


          [None,  4 ,  6      ,  3 ,None,  1 ],
          [  3 ,None,  2       ,  4 ,  6 ,  5 ],


          [  2 ,None,  1       ,None,  5 ,  4 ],
          [None,  5 ,None      ,  1 ,None,  2 ]]

"""
sudoku = [[None,  3 ,  6       ,  1 ,  2 ,None],
          [  1 ,  2 ,None      ,  6 ,None,  3 ],


          [  6 ,  1 ,  4       ,None,  5 ,  2 ],
          [  2 ,None,  3       ,  4 ,  1 ,None],


          [None,  4 ,None      ,  5 ,None,  1 ],
          [  5 ,None,  1       ,None,  3 ,  4 ]]


sudoku = [[  2 ,None,  5        ,  3 ,  1 ,None],
          [None,  3 ,  1        ,  2 ,None,  5 ],


          [  4 ,  5 ,None       ,  6 ,  3 ,None],
          [  3 ,  1 ,  6        ,None,  5 ,  2 ],


          [None,None,  3        ,  1 ,  2 ,  4 ],
          [  1 ,  2 ,  4        ,None,None,  3 ]]
"""

print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

sudoku6.solve(sudoku)
print "{}".format(len(sudoku6.rbs.exe.populations))
sim.run(100)

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
        print "(f-{} - {} {}) - {} - at {}".format(f.index, f.group, f.attributes, f.ca, min)


print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

sim.end()