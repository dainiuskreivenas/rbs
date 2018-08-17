

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


print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

sudoku6.solve(sudoku)
sim.run(1500)

for f in sudoku6.rbs.factGroups["Item"]:
    hasSpiked = len(f[0][1].get_data().segments[0].spiketrains[0]) > 0
    print "{} - {}".format(f[0][1].label,hasSpiked)


print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

sudoku6.solve(sudoku)
sim.run(1500)

for f in sudoku6.rbs.factGroups["Item"]:
    hasSpiked = len(f[0][1].get_data().segments[0].spiketrains[0]) > 0
    print "{} - {}".format(f[0][1].label,hasSpiked)

print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

sim.end()