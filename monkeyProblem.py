
from rbs import RBS

class MonekyProblem:

    def __init__(self):
        self.rbs = RBS()
        self.rbs.addRule(
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

        self.rbs.addRule(
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

        self.rbs.addRule(
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

    def printSpikes(self, name):
        # "################### retracts ###############"

        for key in self.rbs.retractions.keys():
            re = self.rbs.retractions[key]
            re.printSpikes("pkls/"+name+"/retractions/{}.pkl".format(re.label))

        # "################### assertions ###############"

        for key in self.rbs.assertions.keys():
            aa = self.rbs.assertions[key]
            aa.printSpikes("pkls/"+name+"/assertions/{}.pkl".format(aa.label))

        # "################### facts ###############"

        for key in list(self.rbs.factGroups):
            for f in self.rbs.factGroups[key]:
                f[0][1].printSpikes("pkls/"+name+"/facts/{}.pkl".format(f[0][1].label))

    
