from constants import *

class SequentialRuleGenerator:
    def caFromUnit(self, net, unit):
        unit = net.inheritanceStructure.getUnitNumber(unit)
        start = (unit * net.fsa.CA_SIZE)
        return range(start, start + 10)

    def getCas(self, net, match, isAs):
        ca = []
        for m in match:
            ca.append((m[0].ca, CONNECTION_NETWORK))
        
        for a in isAs:
            ca.append((self.caFromUnit(net, a[1]), CONNECTION_INHERITANCE_NETWORK))
        return ca

    def setupActivations(self, net, match, isAs, ruleNeuron):
        length = len(match) + len(isAs)
        ca = self.getCas(net, match, isAs)
    
        if length == 1:
            net.caTurnsOnNeuron(ca[0][0], ruleNeuron, ca[0][1])
        elif length == 2:
            net.twoCaTurnOnNeuron(ca[0][0], ca[1][0], ruleNeuron, ca[0][1], ca[1][1])
        else:
            index = 0

            pop1 = ca[index][0]
            conn1 = ca[index][1]
            pop2 = ca[index+1][0]
            conn2 = ca[index+1][1]

            intermediate = net.addTwoStateIntermediate(pop1,pop2,conn1,conn2)
            while(index < length-2):
                pop3 = ca[index+2][0]
                conn3 = ca[index+2][1]
                if(index == len(match)-3):
                    net.neuronAndCaTurnOnNeuron(intermediate, pop3, ruleNeuron, CONNECTION_NETWORK, conn3)
                else:
                    intermediate = net.addNeuronAndStateIntermediate(intermediate, pop3, CONNECTION_NETWORK, conn3)

                index = index + 1