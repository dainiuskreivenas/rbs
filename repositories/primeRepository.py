from ..models.prime import Prime

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
            primeObject = self.__primes[prime]
        else:
            caIndex = self.__neuronRepository.addCA()
            primeObject = Prime(caIndex)
            self.__primes[prime] = primeObject

            if(prime == "base"):
                for u in self.__baseService.getInheritance().units:
                    amCa = self.__baseService.fromUnit(u)
                    self.__connectionsService.connectPrimeToAssociationCA(primeObject, amCa)
            if(prime == "property"):
                for u in self.__propertyService.getStructure().units:
                    amCa = self.__propertyService.fromUnit(u)
                    self.__connectionsService.connectPrimeToAssociationCA(primeObject, amCa)
            if(prime == "relationship"):
                for u in self.__relationshipService.getStructure().units:
                    amCa = self.__relationshipService.fromUnit(u)
                    self.__connectionsService.connectPrimeToAssociationCA(primeObject, amCa)

        return primeObject

    def get(self):
        return self.__primes.copy()
    