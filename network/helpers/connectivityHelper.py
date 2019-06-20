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
                connector = connector + [(fromNeuron, toNeuron, intraCaWeight, 1.0)]
    #excitatory turn on inhibitory
    for fromNeuron in range (start,start + caSize - caInhibs):
        for toNeuron in range (start + caSize - caInhibs,start + caSize):
            connector = connector + [(fromNeuron, toNeuron, intraCaToInhibWeight, 1.0)]
    #inhibitory slows excitatory 
    for fromNeuron in range (start + caSize - caInhibs, start + caSize):
        for toNeuron in range (start,start+caSize-caInhibs):
            connector = connector + [(fromNeuron, toNeuron, intraCaFromInhibWeight, 1.0)]
    connections += connector

def caToNeuron(connections, caSize, caInhibs, ca, neuron, weight):
    for n in range(ca[0], ca[caSize-caInhibs]):
        connections.append((n,neuron,weight,1.0))

def caToCa(connections, caSize, caInhibs, fromCa, toCa, weight):
    for n in range(fromCa[0], fromCa[caSize-caInhibs]):
        for m in range(toCa[0], toCa[caSize-caInhibs]):
            connections.append((n,m,weight,1.0))

def neuronToCa(connections, caSize, caInhibs, neuron, ca, weight):
    for n in range(ca[0], ca[caSize-caInhibs]):
        connections.append((neuron,n,weight,1.0))

def neuronToNeruon(connections, fromNeruon, toNeuron, weight):
    connections.append((fromNeruon,toNeuron,weight,1.0))