class FactRepository:
    def __init__(self, factGroupRepository, neuronRepository, activationsRepository):
        self.factGroupRepository = factGroupRepository
        self.neuronRepository = neuronRepository
        self.activationsRepository = activationsRepository

    def addFact(self, fact, active):
        group = self.factGroupRepository.addOrGet(fact.group)
        
        fact.caIndex = self.neuronRepository.addCA()
        group.append(fact)

        if(active):
            self.activationsRepository.add(fact.caIndex)

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