class NeuronRepository:
    def __init__(self, connectionsService):
        self.connectionsService = connectionsService
        self.neuron = -1
        self.interns = []

    def addNeuron(self):
        self.neuron += 1
        return self.neuron

    def addCA(self):
        start = self.neuron + 1
        self.neuron += 10

        self.connectionsService.makeCA(start)

        return range(start, self.neuron+1)

    def addNeuronAndStateIntermediate(self, pop1, pop2, neuronConnectionType, caConnectionType):
        intermediate = self.addNeuron()
        self.connectionsService.neuronAndCaTurnOnNeuron(pop1, pop2, intermediate, neuronConnectionType, caConnectionType)
        self.interns.append(intermediate)
        return intermediate

    def addTwoStateIntermediate(self, pop1, pop2, firstConnectionType, secondConnectionType):
        intermediate = self.addNeuron()
        self.connectionsService.twoCaTurnOnNeuron(pop1,pop2,intermediate, firstConnectionType, secondConnectionType)
        self.interns.append(intermediate)
        return intermediate

    def getNeuron(self):
        return self.neuron

    def getInterns(self):
        return list(self.interns)