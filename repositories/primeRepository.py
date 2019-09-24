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
            for u in self.association.inheritance.units:
                amCa = self.association.caFromUnit(u)
                self.connectionsService.connectPrimeToAssociationCA(ca, amCa)

        return ca

    def get(self):
        return self.primes.copy()
    