from ..models import Connection

class ConnectionsService:
    def __init__(self, connectionsRepository, internService):
        self.connectionsRepository = connectionsRepository
        self.internService = internService

        ### State to State
        self.ON = 0
        self.HALF_ON = 1
        self.OFF = 2
        self.HALF_OFF = 3

        ### State to Neuron
        self.ON_ONE = 4
        self.HALF_ON_ONE = 5

        ### Neuron to State
        self.ONE_ON = 6
        self.ONE_HALF_ON = 7
        self.ONE_OFF = 8
        self.ONE_HALF_OFF = 9

        ### Neuron to Neuron
        self.ONE_ON_ONE = 10
        self.ONE_HALF_ON_ONE = 11
        self.ONE_OFF_ONE = 12
        self.ONE_HALF_ON_ONE = 13


    def neuronAndCaTurnOnNeuron(self, fromNeuron, fromCa, toNeuron):
        self.__neuronHalfTurnOnNeuron(fromNeuron,toNeuron)
        self.caHalfTurnsOnNeuron(fromCa, toNeuron)

    def neuronHalfTurnOnCa(self, neuron, ca):
        self.__neuronHalfTurnOnCa(neuron, ca)

    def neuronTurnsOnCa(self, neuron, ca):
        self.__neuronTurnsOnCa(neuron, ca)

    def neuronTurnsOnAssociationCA(self, neuron, ca):
        self.__neuronTurnsOnCa(neuron, ca)

    def neuronTurnsOffAssociationCA(self, neuron, ca):
        self.__neuronTurnsOffCa(neuron, ca)

    def neuronTurnsOffCA(self, neuron, ca):
        self.__neuronTurnsOffCa(neuron, ca)

    def twoCaTurnOnNeuron(self, fromOne, fromTwo, toNeuron):
        self.caHalfTurnsOnNeuron(fromOne, toNeuron)
        self.caHalfTurnsOnNeuron(fromTwo, toNeuron)

    def caHalfTurnsOnNeuron(self, fromCa, toNeuron):
        self.__caToNeuron(fromCa, toNeuron, self.HALF_ON_ONE)

    def caTurnsOnNeuron(self, fromCa, toNeuron):
        self.__caToNeuron(fromCa, toNeuron, self.ON_ONE)

    def connectCorrelatedLink(self, ca, amCA):
        self.__caToCa(ca, amCA, self.ON)
        self.__caToCa(amCA, ca, self.ON)

    def connectQueryableLink(self, ca, amCA):
        self.__caToCa(amCA, ca, self.ON)

    def connectStimulatedLink(self, ca, amCA):
        self.__caToCa(ca, amCA, self.ON)

    def connectPrimeToAssociationCA(self, ca, amCA):
        self.__caToCa(ca, amCA, self.HALF_ON)

    def __neuronHalfTurnOnNeuron(self, fromNeuron, toNeuron):
        self.__neuronToNeuron(fromNeuron, toNeuron, self.ONE_HALF_ON_ONE)

    def __neuronTurnsOffCa(self, neuron, ca):
        self.__neuronToCa(neuron, ca, self.ONE_OFF)
    
    def __neuronTurnsOnCa(self, neuron, ca):
        self.__neuronToCa(neuron, ca, self.ONE_ON)

    def __neuronHalfTurnOnCa(self, neuron, ca):
        self.__neuronToCa(neuron, ca, self.ONE_HALF_ON)

    def __neuronToCa(self, neuron, ca, connectionType):
        self.connectionsRepository.add(Connection(neuron, ca, connectionType))

    def __neuronToNeuron(self, fromNueron, toNeuron, connectionType):
        self.connectionsRepository.add(Connection(fromNueron, toNeuron, connectionType))

    def __caToCa(self, fromCa, toCa, connectionType):
        self.connectionsRepository.add(Connection(fromCa, toCa, connectionType))

    def __caToNeuron(self, ca, neuron, connectionType):
        self.connectionsRepository.add(Connection(ca, neuron, connectionType))