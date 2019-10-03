class Rule:
    def __init__(self, name, ifs, thens):
        self.name = name
        self.baseAssertions = []
        self.primeAssertions = []
        self.linkAssertions = []
        self.propertyAssertions = []
        self.relationshipAssertions = []
        self.assertions = []
        self.retractions = []
        self.tests = []
        self.conditions = []
        self.bases = []
        self.primes = []
        self.links = []
        self.properties = []
        self.relationships = []

        self.__initIfs(ifs)
        self.__initThens(thens)

    def __initIfs(self, ifs):
        for f in ifs:
            if(f[0] == "test"):
                self.tests.append(f)
            elif(f[0] == "base"):
                self.bases.append(f)
            elif(f[0] == "link"):
                self.links.append(f)
            elif(f[0] == "prime"):
                self.primes.append(f)
            elif(f[0] == "property"):
                self.properties.append(f)
            elif(f[0] == "relationship"):
                self.relationships.append(f)
            elif(f[0] == True or f[0] == False):
                self.conditions.append(f)
            else:
                error = "Invalid rule specification. If option '{}' is not valid.".format(f[0])
                raise Exception(error)

    def __initThens(self, thens):
        for t in thens:
            option,item = t
            if(option == "base"):
                self.baseAssertions.append(item)
            elif(option == "assert"):
                self.assertions.append(item)
            elif(option == "retract"):
                self.retractions.append(item)
            elif(option == "prime"):
                self.primeAssertions.append(item)
            elif(option == "link"):
                self.linkAssertions.append(item)
            elif(option == "property"):
                self.propertyAssertions.append(item)
            elif(option == "relationship"):
                self.relationshipAssertions.append(item)
            else:
                error = "Invalid rule specification. Then option '{}' is not valid.".format(option)
                raise Exception(error)