"""

Two Fruit Test 
Fruits:
 1: Banana, 0;
 2: Apple, 0.
Chair:
    1: 2

"""


import nealParams as nealParameters
import pyNN.nest as sim
from rbs import RBS

sim.setup(timestep=nealParameters.DELAY,min_delay=nealParameters.DELAY,max_delay=nealParameters.DELAY, debug=0)

rbs = RBS()

rbs.addRule(
    (
        "eatFruit",
        (
            [
                (True, "monkey-has", ("?type",), "a"),
            ],
            [
                ("assert", ("monkey-ate", ("?type",))),
                ("retract", "a")
            ]            
        )
    )
)

rbs.addRule(
    (
        "monkeyHasFruit",
        (
            [
                (True, "chairAt", ("?pos",), "a"),
                (True, "fruit", ("?type","?pos"),"b")
            ],
            [
                ("assert",("monkey-has", ("?type",))),
                ("retract", "b")
            ]
        )
    )
)

rbs.addRule(
    (   
        "pushChair", 
        (
            # if
            [
                (True,  "fruit", ("?","?pos"), "a"),
                (False, "chairAt", ("?pos",), "b")
            ],
            # then
            [
                ("assert", ("chairAt", ("?pos",))),
                ("retract", "b")
            ]
        )
    )
)

rbs.addFact(("chairAt", (2,)))
rbs.addFact(("fruit",("banana",0)))
rbs.addFact(("fruit",("apple",0)))

sim.run(nealParameters.SIM_LENGTH)

# "################### interns ###############"
"""
for inter in rbs.interns:
    print inter.label
    print inter.get_data().segments[0].spiketrains[0]
"""
# "################### retracts ###############"

for key in rbs.retractions.keys():
    re = rbs.retractions[key]
    re.printSpikes("pkls/Monkey_TwoPlaceFruits/retractions/{}.pkl".format(re.label))

# "################### assertions ###############"

for key in rbs.assertions.keys():
    aa = rbs.assertions[key]
    aa.printSpikes("pkls/Monkey_TwoPlaceFruits/assertions/{}.pkl".format(aa.label))

# "################### facts ###############"

for key in list(rbs.factGroups):
    for f in rbs.factGroups[key]:
        f[0][1].printSpikes("pkls/Monkey_TwoPlaceFruits/facts/{}.pkl".format(f[0][1].label))


sim.end()