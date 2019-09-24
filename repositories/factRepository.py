class FactRepository:
    def __init__(self, factGroupRepository, neuronRepository, activationsRepository):
        self.factGroupRepository = factGroupRepository
        self.neuronRepository = neuronRepository
        self.activationsRepository = activationsRepository
        self.__factIndex = 0
        self.__activations = []

    def addFact(self, fact, active):
        group = self.factGroupRepository.addOrGet(fact.group)
        fact.ca = self.neuronRepository.addCA()
        self.__factIndex += 1
        fact.index = self.__factIndex
        group.append(fact)

        if(active):
            self.activationsRepository.add(fact.ca)

        return fact

    def getFact(self, fact):
        group = self.factGroupRepository.addOrGet(fact.group)

        found = None
        for f in group:
            match = True
            for i,p in enumerate(f.attributes):
                if(p != fact.attributes[i]):
                    match = False
                    break
            if(match):
                found = f
        
        if(found == None):
            found = self.addFact(fact, False)
        
        return found

    def getActivations(self):
        return list(self.__activations)