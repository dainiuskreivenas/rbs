import logging
from operator import itemgetter
from itertools import groupby
from contracts.population import Population

class Executor:
    def __init__(self, 
        sim, 
        simulator, 
        fsa, 
        neuronRepository, 
        connectionsRepository, 
        activationsRepository,
        debug = False):
        self.simulator = simulator
        self.fsa = fsa
        self.sim = sim
        self.neuronRepository = neuronRepository
        self.connectionsRepository = connectionsRepository
        self.activationsRepository = activationsRepository
        self.debug = debug

    def useAssociationTopology(self, topology):
        self.neuralHierarchyTopology = topology
        return self

    def build(self):
        self.connections = 0
        self.populations = []
        self.neuron = 0
        self.actived = 0
        return self

    def getConnection(self, conn):
        fromPop = None
        toPop = None

        fromN = conn[0]
        toN = conn[1]
        mode = conn[4]

        if(mode in [0, 1, 2]):
            for pop in self.populations:
                if(fromN >= pop.fromIndex and fromN < pop.toIndex and (mode in [0, 1])):
                    fromPop = pop
                    if(toPop != None):
                        break
                if(toN >= pop.fromIndex and toN < pop.toIndex and (mode in [0, 2])):
                    toPop = pop
                    if(fromPop != None):
                        break
        
        if(mode == 0): # Within Network
            pFrom = fromPop.pop
            pTo = toPop.pop
            connector = (conn[0]-fromPop.fromIndex,conn[1]-toPop.fromIndex,conn[2],conn[3])
        elif(mode == 1): # From Network to Inheritance
            pFrom = fromPop.pop
            pTo = self.neuralHierarchyTopology.cells
            connector = (conn[0]-fromPop.fromIndex,conn[1],conn[2],conn[3])
        elif(mode == 2): # From Inheritance to Network
            pFrom = self.neuralHierarchyTopology.cells
            pTo = toPop.pop
            connector = (conn[0],conn[1]-toPop.fromIndex,conn[2],conn[3])
        else: # Within Inheritance
            pFrom = self.neuralHierarchyTopology.cells
            pTo = self.neuralHierarchyTopology.cells
            connector = (conn[0],conn[1],conn[2],conn[3])

        connType = "excitatory"
        
        if(conn[2] < 0):
            connType = "inhibitory"
            if(self.simulator == "spinnaker"):
                connector = (conn[0],conn[1],conn[2]*-1,conn[3])
        
        return (
            pFrom,
            pTo,
            connector,
            connType
        )

    def populate(self):
        addNeurons = 0
        neuron = self.neuronRepository.getNeuron() + 1

        if(self.neuron == 0):
            self.neuron += neuron
            addNeurons = self.neuron
        else:
            addNeurons = neuron - self.neuron
            self.neuron += addNeurons

        if(addNeurons > 0):
            self.writeDebug("New Neurons: {}".format(addNeurons))
            population = Population(self.sim, self.fsa, addNeurons, self.neuron - addNeurons)
            self.populations.append(population)

    def connect(self):
        connections = None

        allConnections = self.connectionsRepository.getConnections()

        if(self.connections == 0):
            connections = allConnections[:]
            self.connections = len(connections)
        else:
            start = self.connections-1
            connections = allConnections[start:]
            self.connections += len(connections)

        if(len(connections) > 0):
            self.writeDebug("New Connections: {}".format(len(connections)))
            allC = [self.getConnection(c) for c in connections]
            allC.sort(key=itemgetter(0,1,3))
            groups = groupby(allC,key=itemgetter(0,1,3))
            
            for key,data in groups:               
                items = [item[2] for item in data]
                if(self.simulator == "nest" or key[2] == "excitatory"):
                    conn = self.sim.FromListConnector(items)
                    self.sim.Projection(key[0],key[1], conn, receptor_type="excitatory")
                else:
                    conn = self.sim.FromListConnector(items)
                    self.sim.Projection(key[0],key[1], conn, receptor_type="inhibitory")   

    def activate(self):
        activate = []

        allActivations = self.activationsRepository.get()

        if(self.actived == 0):
            activate = allActivations
        else:
            activate = allActivations[self.actived:]

        if(len(activate) > 0):
            self.writeDebug("Activation CA's: {}".format(len(activate)))
            spikeTimes = {'spike_times': [[self.sim.get_current_time()+5]]}
            spikeGen = self.sim.Population(1, self.sim.SpikeSourceArray, spikeTimes)
            for a in activate:
                population = None
                for pop in self.populations:
                    if(pop.fromIndex <= a[0] and pop.toIndex > a[0]):
                        population = pop
                        break

                self.fsa.turnOnStateFromSpikeSource(spikeGen, population.pop, a[0]-population.fromIndex)
                self.actived += 1

    def writeDebug(self, msg):
        if(self.debug):
            logging.info(msg)

    def apply(self): 
        self.writeDebug("Populating network")
        self.populate()
        self.writeDebug("Making connections")
        self.connect()
        self.writeDebug("Setting activations")
        self.activate()