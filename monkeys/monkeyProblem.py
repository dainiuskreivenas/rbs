import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

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
        self.rbs.printSpikes()

    
