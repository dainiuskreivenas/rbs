import logging
from operator import itemgetter
from itertools import groupby
from models import *
from constants import ConnectionTypes

class Executor:
    def __init__(self, 
        sim, 
        simulator, 
        fsa,
        neal,
        spinnVersion,
        neuronRepository, 
        connectionsRepository, 
        activationsRepository,
        associationTopology,
        logger):
        self.__simulator = simulator
        self.__fsa = fsa
        self.__neal = neal
        self.__sim = sim
        self.__spinnVersion = spinnVersion
        self.__neuronRepository = neuronRepository
        self.__connectionsRepository = connectionsRepository
        self.__activationsRepository = activationsRepository
        self.__associationTopology = associationTopology
        self.__logger = logger
        self.connections = 0
        self.__neuronPopulations = []
        self.neuron = 0
        self.__caPopulations = []
        self.__ca = 0
        self.__actived = 0

    def apply(self): 
        self.__logger.writeDebug("Populating network")
        self.__populate()
        self.__logger.writeDebug("Making connections")
        self.__connect()
        self.__logger.writeDebug("Setting activations")
        self.__activate()
        self.__logger.writeDebug("NEAL apply")
        self.__neal.nealApplyProjections()

    def get_neuron_data(self):
        data = {}
        for pop in self.__neuronPopulations:
            data[pop.pop.label] = pop.pop.get_data()
        return data

    def get_ca_data(self):
        data = {}
        for pop in self.__caPopulations:
            data[pop.pop.label] = pop.pop.get_data()
        return data

    def getPopulationFromCA(self, caIndex):
        for pop in self.__caPopulations:
            if (pop.fromIndex <= caIndex and pop.toIndex >= caIndex):
                return pop
        return None

    def getPopulationFromNeuron(self, neuronIndex):
        for pop in self.__neuronPopulations:
            if (pop.fromIndex <= neuronIndex and pop.toIndex >= neuronIndex):
                return pop
        return None

    def __populate(self):
        self.__populateNeurons()
        self.__populateCAs()

    def __populateCAs(self):
        addCAs = 0
        ca = self.__neuronRepository.getCAs() + 1

        if(self.__ca == 0):
            self.__ca += ca
            addCAs = self.__ca
        else:
            addCAs = ca - self.__ca
            self.__ca += addCAs

        if(addCAs > 0):
            self.__logger.writeDebug("New CAs: {}".format(addCAs))

            pop = self.__sim.Population(addCAs * self.__fsa.CA_SIZE, self.__sim.IF_cond_exp, self.__fsa.CELL_PARAMS)
            pop.record("spikes")

            population = Population(pop, self.__ca - addCAs, self.__ca)

            self.__caPopulations.append(population)

            for i in range(self.__ca - addCAs, self.__ca):
                self.__fsa.makeCA(population.pop, i)

    def __populateNeurons(self):
        addNeurons = 0
        neuron = self.__neuronRepository.getNeuron() + 1

        if(self.neuron == 0):
            self.neuron += neuron
            addNeurons = self.neuron
        else:
            addNeurons = neuron - self.neuron
            self.neuron += addNeurons

        if(addNeurons > 0):
            self.__logger.writeDebug("New Neurons: {}".format(addNeurons))

            pop = self.__sim.Population(addNeurons, self.__sim.IF_cond_exp, self.__fsa.CELL_PARAMS)
            pop.record("spikes")
            
            population = Population(pop, self.neuron - addNeurons, self.neuron)

            self.__neuronPopulations.append(population)

    def __connect(self):
        connections = None

        allConnections = self.__connectionsRepository.getConnections()

        if(self.connections == 0):
            connections = allConnections[:]
            self.connections = len(connections)
        else:
            start = self.connections-1
            connections = allConnections[start:]
            self.connections += len(connections)

        if(len(connections) > 0):
            self.__logger.writeDebug("New Connections: {}".format(len(connections)))

            for connection in connections:
                fromPopulation, sourceIndex = self.__getNeurons(connection.source)
                toPopulation, targetIndex = self.__getNeurons(connection.target)
                connectMethod = None

                if(connection.connectionType == ConnectionTypes.ON):
                    connectMethod = self.__fsa.stateTurnsOnState
                elif(connection.connectionType == ConnectionTypes.HALF_ON):
                    connectMethod = self.__fsa.stateHalfTurnsOnState
                elif(connection.connectionType == ConnectionTypes.OFF):
                    connectMethod = self.__fsa.stateTurnsOffState
                elif(connection.connectionType == ConnectionTypes.HALF_OFF):
                    connectMethod = self.__fsa.stateHalfTurnsOffState
                elif(connection.connectionType == ConnectionTypes.ON_ONE):
                    connectMethod = self.__fsa.stateTurnsOnOneNeuron
                elif(connection.connectionType == ConnectionTypes.HALF_ON_ONE):
                    connectMethod = self.__fsa.stateHalfTurnsOnOneNueron
                elif(connection.connectionType == ConnectionTypes.ONE_ON):
                    connectMethod = self.__fsa.oneNeuronTurnsOnState
                elif(connection.connectionType == ConnectionTypes.ONE_HALF_ON):
                    connectMethod = self.__fsa.oneNeuronHalfTurnsOnState
                elif(connection.connectionType == ConnectionTypes.ONE_OFF):
                    connectMethod = self.__fsa.oneNeuronTurnsOffState
                elif(connection.connectionType == ConnectionTypes.ONE_HALF_OFF):
                    connectMethod = self.__fsa.oneNeuronHalfTurnsOffState
                elif(connection.connectionType == ConnectionTypes.ONE_ON_ONE):
                    connectMethod = self.__fsa.oneNeuronTurnsOnOneNeuron
                elif(connection.connectionType == ConnectionTypes.ONE_HALF_ON_ONE):
                    connectMethod = self.__fsa.oneNeuronHalfTurnsOnOneNeuron

                connectMethod(fromPopulation, sourceIndex, toPopulation, targetIndex)

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
                for pop in self.__caPopulations:
                    if(pop.fromIndex <= a and pop.toIndex >= a):
                        population = pop
                        break

                self.__fsa.turnOnStateFromSpikeSource(spikeGen, population.pop, a-population.fromIndex)
                self.__actived += 1

    def __getPopulationAndIndexFromCA(self, caIndex):
        population = self.getPopulationFromCA(caIndex)        
        return (population.pop, caIndex - population.fromIndex)

    def __getPopulationAndIndexFromNeuron(self, neuronIndex):
        population = self.getPopulationFromNeuron(neuronIndex)
        return (population.pop, neuronIndex - population.fromIndex)

    def __getNeurons(self, item):
        population = None
        index = None

        if(isinstance(item, Fact)):
            population, index = self.__getPopulationAndIndexFromCA(item.caIndex)
        elif(isinstance(item, Assertion)):
            population, index = self.__getPopulationAndIndexFromNeuron(item.neuronIndex)
        elif(isinstance(item, Intern)):
            population, index = self.__getPopulationAndIndexFromNeuron(item.neuronIndex)
        elif(isinstance(item, Base)):
            index = item.unitNumber
            population = self.__associationTopology.neuralHierarchyTopology.cells
        elif(isinstance(item, Link)):
            population, index = self.__getPopulationAndIndexFromCA(item.caIndex)
        elif(isinstance(item, Prime)):
            population, index = self.__getPopulationAndIndexFromCA(item.caIndex)
        elif(isinstance(item, Property)):
            index = item.unitNumber
            population = self.__associationTopology.propertyCells
        elif(isinstance(item, Relationship)):
            index = item.unitNumber
            population = self.__associationTopology.relationCells

        return (population, index)