class SequentialRuleGenerator:
    def __init__(self, connectionsService, internService):
        self.__connectionsService = connectionsService
        self.__internService = internService

    def setupActivations(self, net, ca, ruleNeuron):
        length = len(ca)

        if length == 1:
            self.__connectionsService.caTurnsOnNeuron(ca[0], ruleNeuron)
        elif length == 2:
            self.__connectionsService.twoCaTurnOnNeuron(ca[0], ca[1], ruleNeuron)
        else:
            index = 0
            pop1 = ca[index]
            pop2 = ca[index+1]

            intermediate = self.__internService.createIntern()
            self.__connectionsService.twoCaTurnOnNeuron(pop1, pop2, intermediate)
            while(index < length-2):
                pop3 = ca[index+2]
                if(index == len(ca)-3):
                    self.__connectionsService.neuronAndCaTurnOnNeuron(intermediate, pop3, ruleNeuron)
                else:
                    tempIntermediate = self.__internService.createIntern()
                    self.__connectionsService.neuronAndCaTurnOnNeuron(intermediate, pop3, tempIntermediate)
                    intermediate = tempIntermediate


                index = index + 1