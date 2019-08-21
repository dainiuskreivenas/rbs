from constants import *

class SequentialRuleGenerator:

    def setupActivations(self, net, ca, ruleNeuron):
        length = len(ca)

        if length == 1:
            net.caTurnsOnNeuron(ca[0], ruleNeuron, CONNECTION_NETWORK)
        elif length == 2:
            net.twoCaTurnOnNeuron(ca[0], ca[1], ruleNeuron, CONNECTION_NETWORK, CONNECTION_NETWORK)
        else:
            index = 0
            pop1 = ca[index]
            pop2 = ca[index+1]
            intermediate = net.addTwoStateIntermediate(pop1, pop2, CONNECTION_NETWORK, CONNECTION_NETWORK)
            while(index < length-2):
                pop3 = ca[index+2]
                if(index == len(ca)-3):
                    net.neuronAndCaTurnOnNeuron(intermediate, pop3, ruleNeuron, CONNECTION_NETWORK, CONNECTION_NETWORK)
                else:
                    intermediate = net.addNeuronAndStateIntermediate(intermediate, pop3, CONNECTION_NETWORK, CONNECTION_NETWORK)

                index = index + 1