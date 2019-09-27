class SequentialRuleGenerator:
    def __init__(self, connectionsService, neuronRepository):
        self.__connectionsService = connectionsService
        self.__neuronRepository = neuronRepository

    def setupActivations(self, net, ca, ruleNeuron):
        length = len(ca)

        if length == 1:
            self.__connectionsService.caTurnsOnNeuron(ca[0][0], ruleNeuron, ca[0][1])
        elif length == 2:
            self.__connectionsService.twoCaTurnOnNeuron(ca[0][0], ca[1][0], ruleNeuron, ca[0][1], ca[1][1])
        else:
            index = 0
            pop1 = ca[index][0]
            pop2 = ca[index+1][0]
            conn1 = ca[index][1]
            conn2 = ca[index+1][1]
            intermediate = self.__neuronRepository.addTwoStateIntermediate(pop1, pop2, conn1, conn2)
            while(index < length-2):
                pop3 = ca[index+2][0]
                conn3 = ca[index+2][1]
                if(index == len(ca)-3):
                    self.__connectionsService.neuronAndCaTurnOnNeuron(intermediate, pop3, ruleNeuron, self.__connectionsService.CONNECTION_NETWORK, conn3)
                else:
                    intermediate = self.__neuronRepository.addNeuronAndStateIntermediate(intermediate, pop3, self.__connectionsService.CONNECTION_NETWORK, conn3)

                index = index + 1