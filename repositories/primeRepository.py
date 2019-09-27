class PrimeRepository:
    def __init__(self, neuronRepository, connectionsService, association):
        self.neuronRepository = neuronRepository
        self.connectionsService = connectionsService
        self.association = association
        self.primes = {}

    def addOrGet(self, prime):
        if(prime in self.primes):
            ca = self.primes[prime]
        else:
            ca = self.neuronRepository.addCA()
            self.primes[prime] = ca

            if(prime == "base"):
                baseService = self.association.getBaseService()
                for u in baseService.getInheritance().units:
                    amCa = baseService.caFromUnit(u)
                    self.connectionsService.connectPrimeToAssociationCA(ca, amCa)
            if(prime == "property"):
                propertyService = self.association.getPropertyService()
                for u in propertyService.getStructure().units:
                    amCa = propertyService.caFromUnit(u)
                    self.connectionsService.connectPrimeToAssociationCA(ca, amCa)
            if(prime == "relationship"):
                relationshipService = self.association.getRelationshipService()
                for u in relationshipService.getStructure().units:
                    amCa = relationshipService.caFromUnit(u)
                    self.connectionsService.connectPrimeToAssociationCA(ca, amCa)

        return ca

    def get(self):
        return self.primes.copy()
    