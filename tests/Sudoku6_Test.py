

import pyNN.nest as sim
from Sudoku6 import Sudoku6

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

sudoku6 = Sudoku6()

sudoku = [[  1 ,None,  3       ,None,  4 ,None],
          [  4 ,  6 ,None      ,  2 ,  1 ,  3 ],


          [None,  4 ,  6      ,  3 ,None,  1 ],
          [  3 ,None,  2       ,  4 ,  6 ,  5 ],


          [  2 ,None,  1       ,None,  5 ,  4 ],
          [None,  5 ,None      ,  1 ,None,  2 ]]  

sudoku6.activateBoard(sudoku)

sim.run(10000)

for key in list(sudoku6.rbs.factGroups):
    for f in sudoku6.rbs.factGroups[key]:
        print f[0][1].label
        print f[0][1].get_data().segments[0].spiketrains[0]

sim.end()