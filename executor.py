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
        neuralHierarchyTopology,
        logger):
        self.__simulator = simulator
        self.__fsa = fsa
        self.__sim = sim
        self.__neuronRepository = neuronRepository
        self.__connectionsRepository = connectionsRepository
        self.__activationsRepository = activationsRepository
        self.__neuralHierarchyTopology = neuralHierarchyTopology
        self.__logger = logger
        self.__connections = 0
        self.__populations = []
        self.__neuron = 0
        self.__actived = 0

    def apply(self): 
        self.__logger.writeDebug("Populating network")
        self.__populate()
        self.__logger.writeDebug("Making connections")
        self.__connect()
        self.__logger.writeDebug("Setting activations")
        self.__activate()

    def get_data(self):
        data = {}
        for pop in self.__populations:
            data[pop.pop.label] = pop.pop.get_data()
        return data

    def get_population(self, index):
        for pop in self.__populations:
            if(pop.fromIndex <= index and pop.toIndex > index):
                return pop
        return None

    def __populate(self):
        addNeurons = 0
        neuron = self.__neuronRepository.getNeuron() + 1

        if(self.__neuron == 0):
            self.__neuron += neuron
            addNeurons = self.__neuron
        else:
            addNeurons = neuron - self.__neuron
            self.__neuron += addNeurons

        if(addNeurons > 0):
            self.__logger.writeDebug("New Neurons: {}".format(addNeurons))
            population = Population(self.__sim, self.__fsa, addNeurons, self.__neuron - addNeurons)
            self.__populations.append(population)

    def __connect(self):
        connections = None

        allConnections = self.__connectionsRepository.getConnections()

        if(self.__connections == 0):
            connections = allConnections[:]
            self.__connections = len(connections)
        else:
            start = self.__connections-1
            connections = allConnections[start:]
            self.__connections += len(connections)

        if(len(connections) > 0):
            self.__logger.writeDebug("New Connections: {}".format(len(connections)))
            allC = [self.__getConnection(c) for c in connections]
            allC.sort(key=itemgetter(0,1,3))
            groups = groupby(allC,key=itemgetter(0,1,3))
            
            for key,data in groups:               
                items = [item[2] for item in data]
                if(self.__simulator == "nest" or key[2] == "excitatory"):
                    conn = self.__sim.FromListConnector(items)
                    self.__sim.Projection(key[0],key[1], conn, receptor_type="excitatory")
                else:
                    conn = self.__sim.FromListConnector(items)
                    self.__sim.Projection(key[0],key[1], conn, receptor_type="inhibitory")   

    def __activate(self):
        activate = []

        allActivations = self.__activationsRepository.get()

        if(self.__actived == 0):
            activate = allActivations
        else:
            activate = allActivations[self.__actived:]

        if(len(activate) > 0):
            self.__logger.writeDebug("Activation CA's: {}".format(len(activate)))
            spikeTimes = {'spike_times': [[self.__sim.get_current_time()+5]]}
            spikeGen = self.__sim.Population(1, self.__sim.SpikeSourceArray, spikeTimes)
            for a in activate:
                population = None
                for pop in self.__populations:
                    if(pop.fromIndex <= a[0] and pop.toIndex > a[0]):
                        population = pop
                        break

                self.__fsa.turnOnStateFromSpikeSource(spikeGen, population.pop, a[0]-population.fromIndex)
                self.__actived += 1

    def __getConnection(self, conn):
        fromPop = None
        toPop = None

        fromN = conn[0]
        toN = conn[1]
        mode = conn[4]

        if(mode in [0, 1, 2]):
            for pop in self.__populations:
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
            pTo = self.__neuralHierarchyTopology.cells
            connector = (conn[0]-fromPop.fromIndex,conn[1],conn[2],conn[3])
        elif(mode == 2): # From Inheritance to Network
            pFrom = self.__neuralHierarchyTopology.cells
            pTo = toPop.pop
            connector = (conn[0],conn[1]-toPop.fromIndex,conn[2],conn[3])
        else: # Within Inheritance
            pFrom = self.__neuralHierarchyTopology.cells
            pTo = self.__neuralHierarchyTopology.cells
            connector = (conn[0],conn[1],conn[2],conn[3])

        connType = "excitatory"
        
        if(conn[2] < 0):
            connType = "inhibitory"
            if(self.__simulator == "spinnaker"):
                connector = (conn[0],conn[1],conn[2]*-1,conn[3])
        
        return (
            pFrom,
            pTo,
            connector,
            connType
        )