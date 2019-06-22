"""

Helper class for making connections

connectionTypes:

0 = within network
1 = from network to inheritance
2 = from inheritance to network
3 = within inheritance

"""

def makeCA(connections,
    caSize,
    caInhibs,
    start, 
    intraCaWeight,
    intraCaToInhibWeight, 
    intraCaFromInhibWeight):
    connector = []
    #excitatory turn each other on
    for fromNeuron in range (start,start+(caSize-caInhibs)):
        for toNeuron in range (start,start+(caSize-caInhibs)):
            if (fromNeuron != toNeuron):
                connector = connector + [(fromNeuron, toNeuron, intraCaWeight, 1.0, 0)]
    #excitatory turn on inhibitory
    for fromNeuron in range (start,start + caSize - caInhibs):
        for toNeuron in range (start + caSize - caInhibs,start + caSize):
            connector = connector + [(fromNeuron, toNeuron, intraCaToInhibWeight, 1.0, 0)]
    #inhibitory slows excitatory 
    for fromNeuron in range (start + caSize - caInhibs, start + caSize):
        for toNeuron in range (start,start+caSize-caInhibs):
            connector = connector + [(fromNeuron, toNeuron, intraCaFromInhibWeight, 1.0, 0)]
    connections += connector

def caToNeuron(connections, caSize, caInhibs, ca, neuron, weight, connectionType):
    for n in range(ca[0], ca[caSize-caInhibs]):
        connections.append((n,neuron,weight,1.0,connectionType))

def caToCa(connections, caSize, caInhibs, fromCa, toCa, weight, connectionType):
    for n in range(fromCa[0], fromCa[caSize-caInhibs]):
        for m in range(toCa[0], toCa[caSize-caInhibs]):
            connections.append((n,m,weight,1.0,connectionType))

def neuronToCa(connections, caSize, caInhibs, neuron, ca, weight, connectionType):
    for n in range(ca[0], ca[caSize-caInhibs]):
        connections.append((neuron,n,weight,1.0,connectionType))

def neuronToNeruon(connections, fromNeruon, toNeuron, weight, connectionType):
    connections.append((fromNeruon,toNeuron,weight,1.0,connectionType))