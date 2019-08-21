class Rule:
    def __init__(self, name, ifs, thens):
        self.name = name
        self.ifs = ifs
        self.thens = thens

    def extract(self):
        assertions = []
        retractions = []
        tests = []
        bases = []
        conditions = []

        for t in self.thens:
            option,item = t
            if(option == "assert"):
                assertions.append(item)
            elif(option == "retract"):
                retractions.append(item)

        for f in self.ifs:
            if(f[0] == "Test"):
                tests.append(f)
            elif(f[0] == "Base"):
                bases.append(f)
            else:
                conditions.append(f)
        
        return conditions,tests,bases,assertions,retractions