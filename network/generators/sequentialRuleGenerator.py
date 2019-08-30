from constants import *

class SequentialRuleGenerator:

    def setupActivations(self, net, ca, ruleNeuron):
        length = len(ca)

        if length == 1:
            net.caTurnsOnNeuron(ca[0][0], ruleNeuron, ca[0][1])
        elif length == 2:
            net.twoCaTurnOnNeuron(ca[0][0], ca[1][0], ruleNeuron, ca[0][1], ca[1][1])
        else:
            index = 0
            pop1 = ca[index][0]
            pop2 = ca[index+1][0]
            conn1 = ca[index][1]
            conn2 = ca[index+1][1]
            intermediate = net.addTwoStateIntermediate(pop1, pop2, conn1, conn2)
            while(index < length-2):
                pop3 = ca[index+2][0]
                conn3 = ca[index+2][1]
                if(index == len(ca)-3):
                    net.neuronAndCaTurnOnNeuron(intermediate, pop3, ruleNeuron, CONNECTION_NETWORK, conn3)
                else:
                    intermediate = net.addNeuronAndStateIntermediate(intermediate, pop3, CONNECTION_NETWORK, conn3)

                index = index + 1