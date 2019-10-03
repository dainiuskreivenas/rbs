class ConnectionsService:
    def __init__(self, fsa, connectionsRepository):
        self.__fsa = fsa
        self.connectionsRepository = connectionsRepository

        self.CONNECTION_NETWORK = 0
        self.CONNECTION_NETWORK_INHERITANCE = 1
        self.CONNECTION_INHERITANCE_NETWORK = 2
        self.CONNECTION_INHERITANCE = 3

    def neuronAndCaTurnOnNeuron(self, fromNeuron, fromCa, toNeuron, neuronConnectionType, caConnectionType):
        self.__neuronHalfTurnOnNeuron(fromNeuron,toNeuron, neuronConnectionType)
        self.caHalfTurnsOnNeuron(fromCa, toNeuron, caConnectionType)

    def neuronHalfTurnOnCa(self, neuron, ca):
        self.__neuronHalfTurnOnCa(neuron, ca, self.CONNECTION_NETWORK)

    def neuronTurnsOnCa(self, neuron, ca):
        self.__neuronTurnsOnCa(neuron, ca, self.CONNECTION_NETWORK)

    def neuronTurnsOnAssociationCA(self, neuron, ca):
        self.__neuronTurnsOnCa(neuron, ca, self.CONNECTION_NETWORK_INHERITANCE)

    def neuronTurnsOffAssociationCA(self, neuron, ca):
        self.__neuronTurnsOffCa(neuron, ca, self.CONNECTION_NETWORK_INHERITANCE)

    def neuronTurnsOffCA(self, neuron, ca):
        self.__neuronTurnsOffCa(neuron, ca, self.CONNECTION_NETWORK)

    def twoCaTurnOnNeuron(self, fromOne, fromTwo, toNeuron, firstConnectionType, secondConnectionType):
        self.caHalfTurnsOnNeuron(fromOne, toNeuron, firstConnectionType)
        self.caHalfTurnsOnNeuron(fromTwo, toNeuron, secondConnectionType)

    def caHalfTurnsOnNeuron(self, fromCa, toNeuron, connectionType):
        self.__caToNeuron(fromCa, toNeuron, self.__fsa.HALF_ON_WEIGHT, connectionType)

    def caTurnsOnNeuron(self, fromCa, toNeuron, connectionType):
        self.__caToNeuron(fromCa, toNeuron, self.__fsa.STATE_TO_ONE_WEIGHT, connectionType)

    def connectCorrelatedLink(self, ca, amCA):
        self.__caToCa(ca, amCA, self.__fsa.FULL_ON_WEIGHT, self.CONNECTION_NETWORK_INHERITANCE)
        self.__caToCa(amCA, ca, self.__fsa.FULL_ON_WEIGHT, self.CONNECTION_INHERITANCE_NETWORK)

    def connectQueryableLink(self, ca, amCA):
        self.__caToCa(amCA, ca, self.__fsa.FULL_ON_WEIGHT, self.CONNECTION_INHERITANCE_NETWORK)

    def connectStimulatedLink(self, ca, amCA):
        self.__caToCa(ca, amCA, self.__fsa.FULL_ON_WEIGHT, self.CONNECTION_NETWORK_INHERITANCE)

    def connectPrimeToAssociationCA(self, ca, amCA):
        self.__caToCa(ca, amCA, self.__fsa.HALF_ON_WEIGHT, self.CONNECTION_NETWORK_INHERITANCE)

    def makeCA(self, start):
        connector = []
        #excitatory turn each other on
        for fromNeuron in range (start,start+(self.__fsa.CA_SIZE-self.__fsa.CA_INHIBS)):
            for toNeuron in range (start,start+(self.__fsa.CA_SIZE-self.__fsa.CA_INHIBS)):
                if (fromNeuron != toNeuron):
                    connector = connector + [(fromNeuron, toNeuron, self.__fsa.INTRA_CA_WEIGHT, 1.0, 0)]
        #excitatory turn on inhibitory
        for fromNeuron in range (start,start + self.__fsa.CA_SIZE - self.__fsa.CA_INHIBS):
            for toNeuron in range (start + self.__fsa.CA_SIZE - self.__fsa.CA_INHIBS,start + self.__fsa.CA_SIZE):
                connector = connector + [(fromNeuron, toNeuron, self.__fsa.INTRA_CA_TO_INHIB_WEIGHT, 1.0, 0)]
        #inhibitory slows excitatory 
        for fromNeuron in range (start + self.__fsa.CA_SIZE - self.__fsa.CA_INHIBS, start + self.__fsa.CA_SIZE):
            for toNeuron in range (start,start+self.__fsa.CA_SIZE-self.__fsa.CA_INHIBS):
                connector = connector + [(fromNeuron, toNeuron, self.__fsa.INTRA_CA_FROM_INHIB_WEIGHT, 1.0, 0)]
        
        self.connectionsRepository.addRange(connector)

    def __neuronHalfTurnOnNeuron(self, fromNeuron, toNeuron, connectionType):
        self.__neuronToNeuron(fromNeuron, toNeuron, self.__fsa.ONE_HALF_ON_ONE_WEIGHT, connectionType)

    def __neuronTurnsOffCa(self, neuron, ca, connectionType):
        self.__neuronToCa(neuron, ca, self.__fsa.RBS_ONE_NEURON_STOPS_CA_WEIGHT, connectionType)
    
    def __neuronTurnsOnCa(self, neuron, ca, connectionType):
        self.__neuronToCa(neuron, ca, self.__fsa.INPUT_WEIGHT, connectionType)

    def __neuronHalfTurnOnCa(self, neuron, ca, connectionType):
        self.__neuronToCa(neuron, ca, self.__fsa.HALF_ON_WEIGHT, connectionType)

    def __neuronToCa(self, neuron, ca, weight, connectionType):
        for n in range(ca[0], ca[self.__fsa.CA_SIZE-self.__fsa.CA_INHIBS]):
            self.connectionsRepository.add((neuron,n,weight,1.0,connectionType))

    def __neuronToNeuron(self, fromNueron, toNeuron, weight, connectionType):
        self.connectionsRepository.add((fromNueron, toNeuron, weight, 1.0, connectionType))

    def __caToCa(self, fromCa, toCa, weight, connectionType):
        for n in range(fromCa[0], fromCa[self.__fsa.CA_SIZE-self.__fsa.CA_INHIBS]):
            for m in range(toCa[0], toCa[self.__fsa.CA_SIZE-self.__fsa.CA_INHIBS]):
                self.connectionsRepository.add((n,m,weight,1.0,connectionType))

    def __caToNeuron(self, ca, neuron, weight, connectionType):
        for n in range(ca[0], ca[self.__fsa.CA_SIZE-self.__fsa.CA_INHIBS]):
            self.connectionsRepository.add((n,neuron,weight,1.0,connectionType))