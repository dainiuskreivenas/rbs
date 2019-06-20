import logging
from operator import itemgetter
from itertools import groupby
from contracts.population import Population

class Executor:
    def __init__(self, sim, simulator, fsa, net, debug = False):
        self.simulator = simulator
        self.fsa = fsa
        self.sim = sim
        self.net = net
        self.connections = 0
        self.populations = []
        self.neuron = 0
        self.actived = 0
        self.debug = debug

    def getConnection(self, conn):
        fromPop = None
        toPop = None

        fromN = conn[0]
        toN = conn[1]


        for pop in self.populations:
            rng = range(pop.fromIndex, pop.toIndex)
            if(fromN in rng):
                fromPop = pop
                if(toPop != None):
                    break
            if(toN in rng):
                toPop = pop
                if(fromPop != None):
                    break
        
        connector = (conn[0]-fromPop.fromIndex,conn[1]-toPop.fromIndex,conn[2],conn[3])
        connType = "excitatory"
        
        if(conn[2] < 0):
            connType = "inhibitory"
            if(self.simulator == "spinnaker"):
                connector = (conn[0],conn[1],conn[2]*-1,conn[3])
        
        return (
            fromPop.pop,
            toPop.pop,
            connector,
            connType
        )

    def populate(self):
        addNeurons = 0
        if(self.neuron == 0):
            self.neuron += self.net.neuron + 1
            addNeurons = self.neuron
        else:
            addNeurons = self.net.neuron + 1 - self.neuron
            self.neuron += addNeurons

        if(addNeurons > 0):
            self.writeDebug("New Neurons: {}".format(addNeurons))
            population = Population(self.sim, self.fsa, addNeurons, self.neuron - addNeurons)
            self.populations.append(population)

    def connect(self):
        connections = None
        if(self.connections == 0):
            connections = self.net.connections[:]
            self.connections = len(connections)
        else:
            start = self.connections-1
            connections = self.net.connections[start:]
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
        if(self.actived == 0):
            activate = self.net.activations
        else:
            activate = self.net.activations[self.actived:]

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