class ParallelRuleGenerator:
    def setupActivations(self, net, match, ruleNeuron):
        if len(match) == 1:
            net.caTurnsOnNeuron(match[0][0].ca, ruleNeuron)
        elif (len(match) == 2):
            net.twoCaTurnOnNeuron(match[0][0].ca, match[1][0].ca, ruleNeuron)
        else:
            index = 0

            pop1 = match[index][0].ca
            pop2 = match[index+1][0].ca

            intermediate = net.addTwoStateIntermediate(pop1,pop2)
            while(index < len(match)-2):
                pop3 = match[index+2][0].ca
                if(index == len(match)-3):
                    net.neuronAndCaTurnOnNeuron(intermediate, pop3, ruleNeuron)
                else:
                    inter2 = net.addNeuronAndStateIntermediate(intermediate, pop3)
                    intermediate = inter2

                index = index + 1