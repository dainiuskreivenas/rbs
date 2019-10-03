class PrimeRepository:
    def __init__(self, neuronRepository, connectionsService, baseService, propertyService, relationshipService):
        self.__neuronRepository = neuronRepository
        self.__connectionsService = connectionsService
        self.__baseService = baseService
        self.__propertyService = propertyService
        self.__relationshipService = relationshipService
        self.__primes = {}

    def addOrGet(self, prime):
        if(prime in self.__primes):
            ca = self.__primes[prime]
        else:
            ca = self.__neuronRepository.addCA()
            self.__primes[prime] = ca

            if(prime == "base"):
                for u in self.__baseService.getInheritance().units:
                    amCa = self.__baseService.caFromUnit(u)
                    self.__connectionsService.connectPrimeToAssociationCA(ca, amCa)
            if(prime == "property"):
                for u in self.__propertyService.getStructure().units:
                    amCa = self.__propertyService.caFromUnit(u)
                    self.__connectionsService.connectPrimeToAssociationCA(ca, amCa)
            if(prime == "relationship"):
                for u in self.__relationshipService.getStructure().units:
                    amCa = self.__relationshipService.caFromUnit(u)
                    self.__connectionsService.connectPrimeToAssociationCA(ca, amCa)

        return ca

    def get(self):
        return self.__primes.copy()
    