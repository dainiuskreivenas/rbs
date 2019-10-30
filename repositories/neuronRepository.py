class NeuronRepository:
    def __init__(self):
        self.caIndexes = -1
        self.neuron = -1

    def addNeuron(self):
        self.neuron += 1
        return self.neuron

    def addCA(self):
        self.caIndexes += 1
        return self.caIndexes

    def getCAs(self):
        return self.caIndexes

    def getNeuron(self):
        return self.neuron