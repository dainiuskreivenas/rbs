
import pyNN.nest as sim
from LanguageParser import LanguageParser 

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)

parser = LanguageParser()

parser.parseSentence("I saw the dog")

sim.run(200)

for key in list(parser.rbs.factGroups):
    for f in parser.rbs.factGroups[key]:
        f[0][1].printSpikes("pkls/parse_I_saw_the_dog/facts/{}.pkl".format(f[0][1].label))

sim.end()