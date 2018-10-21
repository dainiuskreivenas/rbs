"""

Single Fruit Test

"""


import nealParams as nealParameters
import pyNN.nest as sim
from rbs import RBS

sim.setup(timestep=nealParameters.DELAY,min_delay=nealParameters.DELAY,max_delay=nealParameters.DELAY, debug=0)

rbs = RBS()

rbs.addRule(
    (
        "MonkeyCanReach",
        (
            [
                (True, "MonkeyCanReach", ("?type",),"b")
            ],
            [
                ("assert",("MonkeyGrab", ("?type",))),
                ("retract", "b")
            ]
        )
    )
)

rbs.addFact(("MonkeyCanReach",("banana",)))

sim.run(100)

print "assertions"
for a in rbs.assertions:
    pop = rbs.assertions[a]

    for i, st in enumerate(pop.get_data().segments[0].spiketrains):
        for d in st.magnitude:
            print "{} {}".format(i, d)

add = 10

for g in rbs.factGroups:
    for f in rbs.factGroups[g]:
        add = add + 10
        pop = f[0][1]
        print pop.label
        for i, st in enumerate(pop.get_data().segments[0].spiketrains):
            for d in st.magnitude:
                print "{} {}".format(i+add, d)


sim.end()