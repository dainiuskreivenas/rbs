

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

mins = []

for f in sudoku9.rbs.factGroups["Item"]:

    min = 10000
    for t in f[0][1].get_data().segments[0].spiketrains[0].magnitude:
        if(t < min):
            min = t

    mins.append(min)

    hasSpiked = len(f[0][1].get_data().segments[0].spiketrains[0]) > 0
    print "{} - {}".format(f[0][1].label,hasSpiked)

print mins

print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

sim.end()