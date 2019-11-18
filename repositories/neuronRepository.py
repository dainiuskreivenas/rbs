class NeuronRepository:
    def __init__(self):
        self.__caIndexes = -1
        self.__neuron = -1

    def addNeuron(self):
        self.__neuron += 1
        return self.__neuron

    def addCA(self):
        self.__caIndexes += 1
        return self.__caIndexes

    def getCAs(self):
        return self.__caIndexes

    def getNeuron(self):
        return self.__neuron
