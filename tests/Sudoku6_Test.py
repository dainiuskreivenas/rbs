

import pyNN.nest as sim
from Sudoku6 import Sudoku6
import time
import datetime


sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

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
sim.run(500)

data = sudoku6.rbs.get_data()
for f in sudoku6.rbs.net.facts["Item"]:
    min = 10000
    for t in data.segments[0].spiketrains[f.ca[0]].magnitude:
        if(t < min):
            min = t
    hasSpiked = len(data.segments[0].spiketrains[f.ca[0]]) > 0
    print "(f-{} - {} {}) - {} - at {}".format(f.index, f.group, f.attributes,hasSpiked,min)


print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

sim.end()