import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

#import pyNN.spiNNaker as sim
import pyNN.nest as sim

from LanguageParser import LanguageParser

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

#parser = LanguageParser(sim, "spinnaker")
parser = LanguageParser(sim, "nest")

parser.parseSentence("I saw the dog")

sim.run(200)

parser.rbs.printSpikes()

sim.end()