def initIfs(rule, ifs):
    for f in ifs:
        if(f[0] == "test"):
            rule.tests.append(f)
        elif(f[0] == "base"):
            rule.bases.append(f)
        elif(f[0] == "link"):
            rule.links.append(f)
        elif(f[0] == "prime"):
            rule.primes.append(f)
        elif(f[0] == True or f[0] == False):
            rule.conditions.append(f)
        else:
            raise Exception("Invalid rule specification. If option '{}' is not valid.".format(f[0]))

def initThens(rule, thens):
    for t in thens:
        option,item = t
        if(option == "base"):
            rule.baseAssertions.append(item)
        elif(option == "assert"):
            rule.assertions.append(item)
        elif(option == "retract"):
            rule.retractions.append(item)
        elif(option == "prime"):
            rule.primeAssertions.append(item)
        elif(option == "link"):
            rule.linkAssertions.append(item)
        else:
            raise Exception("Invalid rule specification. Then option '{}' is not valid.".format(option))

class Rule:
    def __init__(self, name, ifs, thens):
        self.name = name
        self.baseAssertions = []
        self.primeAssertions = []
        self.linkAssertions = []
        self.assertions = []
        self.retractions = []
        self.tests = []
        self.conditions = []
        self.bases = []
        self.primes = []
        self.links = []
        initIfs(self, ifs)
        initThens(self, thens)