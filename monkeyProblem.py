from rbs import RuleBasedSystem as RBS

class MonekyProblem:

    def __init__(self, sim, simulator):
        self.rbs = \
            RBS(sim, simulator) \
                .build(200)

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
        self.rbs.printSpikes()

    
