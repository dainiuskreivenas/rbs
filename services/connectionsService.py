import sys
import os
sys.path.append(os.getcwd() + '/..')
from rbs.models.connection import Connection
from rbs.constants.connectionTypes import ConnectionTypes

class ConnectionsService:
    def __init__(self, connectionsRepository, internService):
        self.connectionsRepository = connectionsRepository
        self.internService = internService

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
        self.__caToNeuron(fromCa, toNeuron, ConnectionTypes.HALF_ON_ONE)

    def caTurnsOnNeuron(self, fromCa, toNeuron):
        self.__caToNeuron(fromCa, toNeuron, ConnectionTypes.ON_ONE)

    def connectCorrelatedLink(self, ca, amCA):
        self.__caToCa(ca, amCA, ConnectionTypes.ON)
        self.__caToCa(amCA, ca, ConnectionTypes.ON)

    def connectQueryableLink(self, ca, amCA):
        self.__caToCa(amCA, ca, ConnectionTypes.ON)

    def connectStimulatedLink(self, ca, amCA):
        self.__caToCa(ca, amCA, ConnectionTypes.ON)

    def connectPrimeToAssociationCA(self, ca, amCA):
        self.__caToCa(ca, amCA, ConnectionTypes.HALF_ON)

    def __neuronHalfTurnOnNeuron(self, fromNeuron, toNeuron):
        self.__neuronToNeuron(fromNeuron, toNeuron, ConnectionTypes.ONE_HALF_ON_ONE)

    def __neuronTurnsOffCa(self, neuron, ca):
        self.__neuronToCa(neuron, ca, ConnectionTypes.ONE_OFF)
    
    def __neuronTurnsOnCa(self, neuron, ca):
        self.__neuronToCa(neuron, ca, ConnectionTypes.ONE_ON)

    def __neuronHalfTurnOnCa(self, neuron, ca):
        self.__neuronToCa(neuron, ca, ConnectionTypes.ONE_HALF_ON)

    def __neuronToCa(self, neuron, ca, connectionType):
        self.connectionsRepository.add(Connection(neuron, ca, connectionType))

    def __neuronToNeuron(self, fromNueron, toNeuron, connectionType):
        self.connectionsRepository.add(Connection(fromNueron, toNeuron, connectionType))

    def __caToCa(self, fromCa, toCa, connectionType):
        self.connectionsRepository.add(Connection(fromCa, toCa, connectionType))

    def __caToNeuron(self, ca, neuron, connectionType):
        self.connectionsRepository.add(Connection(ca, neuron, connectionType))