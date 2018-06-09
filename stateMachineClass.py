#This is the class for construcing State Machines.  The individual CAs 
#(both inputs and states) run at 5 ms.  See the notes for running faster or 
#slower. 
#There are test functions at the end. 
#Note that to externally activate a CA State, you should only send
#excitatory connections to the first 8 neurons.

import nealParams as nealParameters

if (nealParameters.simulator=="spinnaker"):
    import pyNN.spiNNaker as sim
elif (nealParameters.simulator=="nest"):
    import pyNN.nest as sim
    import cPickle as pickle

import numpy as np

from nealCoverClass import NealCoverFunctions

class FSAHelperFunctions:
    def __init__(self, simName):
        self.simulator = simName
        self.neal = NealCoverFunctions(self.simulator)
        self.initParams()

    #FSA Parmaeters
    def initParams(self):
        self.CA_SIZE = 10  #This will (almost certainly) not work with a 
                     #different sized CA.
        self.CA_INHIBS = 2

        self.INPUT_WEIGHT = 0.1
        self.INTRA_CA_TO_INHIB_WEIGHT = 0.001 
        if (nealParameters.simulator=="spinnaker"):
            #if you over inhib on my spinnaker, it fires.
            self.INTRA_CA_FROM_INHIB_WEIGHT = 0.1  
            self.CA_STOPS_CA_WEIGHT = 0.15
            self.ONE_NEURON_STOPS_CA_WEIGHT = 1.0
        elif (nealParameters.simulator=="nest"):
            self.INTRA_CA_FROM_INHIB_WEIGHT = -0.1  
            self.CA_STOPS_CA_WEIGHT = -0.15
            self.ONE_NEURON_STOPS_CA_WEIGHT = -1.0

        self.INTRA_CA_WEIGHT = 0.016 
        self.FULL_ON_WEIGHT = 0.01 
        #self.FULL_ON_WEIGHT_SLOW = 0.002
        self.FULL_ON_WEIGHT_SLOW = 0.0015
        self.HALF_ON_WEIGHT = 0.0008
        self.STATE_TO_ONE_WEIGHT = .002

        if (nealParameters.simulator == 'nest'):
            self.CELL_PARAMS = {'v_thresh':-53.0, 'v_reset' : -70.0, 
                                'tau_refrac': 2.0 , 'tau_syn_E': 5.0,  
                                #'e_rev_I': -100.0, 
                                #'tau_syn_I': 1.0, #bug2 fix
                                #'tau_syn_I': 0.1,
                                'v_rest' : -65.0,'i_offset':0.0}
        elif (nealParameters.simulator == 'spinnaker'):
            self.CELL_PARAMS = {'v_thresh':-55.0, 'v_reset' : -70.0, 
                                'tau_refrac': 2.0 , 'tau_syn_E': 5.0,  
                                #'e_rev_I': -100.0, 
                                'tau_syn_I': 5.0, #bug2 fix
                                #'tau_syn_I': 0.1,
                                'v_rest' : -65.0,'i_offset':0.0}



    #--------Finite State Automata Functions ------------
    #---Functions that turn on states by one item

    #-- Function to ignite a state from a spike source
    #-- Uses INPUT_WEIGHT
    #use this when your using a spikesource
    def turnOnStateFromSpikeSource(self,spikeSource, toNeurons, toCA):
        connector = []
        for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            toNeuron = toOffset + (toCA*self.CA_SIZE)
            connector = connector + [(0,toNeuron,self.INPUT_WEIGHT,
                                      nealParameters.DELAY)]
        self.neal.nealProjection(spikeSource, toNeurons, connector,'excitatory')

    def stimulateStateFromSpikeSource(self,spikeSource, toNeurons, toCA, weight):
        connector = []
        for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            toNeuron = toOffset + (toCA*self.CA_SIZE)
            connector = connector + [(0,toNeuron,weight,
                                      nealParameters.DELAY)]
        self.neal.nealProjection(spikeSource, toNeurons, connector,'excitatory')

    def turnOnStateFromOneNeuron(self,fromNeurons,fromNeuron, toNeurons, toCA):
        connector = []
        for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            toNeuron = toOffset + (toCA*self.CA_SIZE)
            connector = connector + [(fromNeuron,toNeuron,self.INPUT_WEIGHT,
                                      nealParameters.DELAY)]
        self.neal.nealProjection(fromNeurons, toNeurons, connector,'excitatory')

    def oneNeuronStimulatesState(self,fromNeurons,fromNeuron, toNeurons, toCA, 
                                weight):
        connector = []
        for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            toNeuron = toOffset + (toCA*self.CA_SIZE)
            connector = connector + [(fromNeuron,toNeuron,weight,
                                      nealParameters.DELAY)]
        self.neal.nealProjection(fromNeurons, toNeurons, connector,'excitatory')


    #Function to turn on one state from another
    #Call with fromPopulation, fromCA, toPopulation and toCA
    def stateTurnsOnState(self,fromNeurons,fromCA,toNeurons,toCA):
        connector = []
        #uses FULL_ON_WEIGHT
        for fromOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            fromNeuron = fromOffset + (fromCA*self.CA_SIZE)
            for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
                toNeuron = toOffset + (toCA*self.CA_SIZE)
                connector=connector+[(fromNeuron,toNeuron,
                                          self.FULL_ON_WEIGHT,
                                          nealParameters.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'excitatory')

    #undone not in tests.
    #When stateTurnsOnState and the preState remains on, the post
    #state runs hot.
    def stateTurnsOnStateSlow(self,fromNeurons,fromCA,toNeurons,toCA):
        connector = []
        #uses FULL_ON_WEIGHT_SLOW
        for fromOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            fromNeuron = fromOffset + (fromCA*self.CA_SIZE)
            for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
                toNeuron = toOffset + (toCA*self.CA_SIZE)
                connector=connector+[(fromNeuron,toNeuron,
                                          self.FULL_ON_WEIGHT_SLOW,
                                          nealParameters.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'excitatory')

    def stateTurnsOnOneNeuron(self,fromNeurons,fromCA,toNeurons,toNeuron):
        connector = []
        #uses FULL_ON_WEIGHT
        for fromOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            fromNeuron = fromOffset + (fromCA*self.CA_SIZE)
            connector=connector+[(fromNeuron,toNeuron,
                                  self.STATE_TO_ONE_WEIGHT,
                                  nealParameters.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'excitatory')


    #---Create a CA that will persistently fire.
    #-- Assumes neurons in the same population
    #-- Uses INTRA_CA_WEIGHT
    def makeCA(self,neurons, CA):
        #print 'makeCA
        connector = []
        #excitatory turn each other on
        for fromOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            fromNeuron = fromOffset + (CA*self.CA_SIZE)
            for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
                toNeuron = toOffset + (CA*self.CA_SIZE)
                if (toNeuron != fromNeuron):
                    connector = connector + [(fromNeuron,toNeuron,
                        self.INTRA_CA_WEIGHT, nealParameters.DELAY)]

        self.neal.nealProjection(neurons,neurons,connector,'excitatory')

        #excitatory turn on inhibitory
        connector = []
        for fromOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            fromNeuron = fromOffset + (CA*self.CA_SIZE)
            for toOffset in range (self.CA_SIZE-self.CA_INHIBS,self.CA_SIZE):
                toNeuron = toOffset + (CA*self.CA_SIZE)
                connector = connector + [(fromNeuron,toNeuron,
                        self.INTRA_CA_TO_INHIB_WEIGHT, nealParameters.DELAY)]

        self.neal.nealProjection(neurons,neurons,connector,'excitatory')

        #inhibitory slows excitatory 
        connector = []
        for fromOffset in range (self.CA_SIZE-self.CA_INHIBS,self.CA_SIZE):
            fromNeuron = fromOffset + (CA*self.CA_SIZE)
            for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
                toNeuron = toOffset + (CA*self.CA_SIZE)
                connector = connector + [(fromNeuron,toNeuron,
                        self.INTRA_CA_FROM_INHIB_WEIGHT, nealParameters.DELAY)]

        self.neal.nealProjection(neurons,neurons,connector,'inhibitory')


    #--Functions when two inputs are needed to turn on a third
    #-- Two states are needed to turn on a third.  
    #-- This connects one of the inputs to the the third.
    #-- Uses HALF_ON_WEIGHT
    def stateHalfTurnsOnState(self,fromNeurons,fromCA,toNeurons,toCA):
        connector = []
        #uses HALF_ON_WEIGHT
        for fromOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            fromNeuron = fromOffset + (fromCA*self.CA_SIZE)
            for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
                toNeuron = toOffset + (toCA*self.CA_SIZE)
                connector=connector+[(fromNeuron,toNeuron,
                                          self.HALF_ON_WEIGHT,
                                          nealParameters.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'excitatory')

    def stateStimulatesState(self,fromNeurons,fromCA,toNeurons,toCA,weight):
        connector = []
        for fromOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            fromNeuron = fromOffset + (fromCA*self.CA_SIZE)
            for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
                toNeuron = toOffset + (toCA*self.CA_SIZE)
                connector=connector+[(fromNeuron,toNeuron,
                    weight, nealParameters.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'excitatory')

    #---- One State or other set of neurons turns off another
    #-- Uses CA_STOPS_CA_WEIGHT
    def stateTurnsOffState(self,fromNeurons, fromCA, toNeurons, toCA):
        connector = []
        for fromOffset in range (0,self.CA_SIZE):
            fromNeuron = fromOffset + (fromCA*self.CA_SIZE)
            for toOffset in range (0,self.CA_SIZE):
                toNeuron = toOffset + (toCA*self.CA_SIZE)
                connector = connector + [(fromNeuron,toNeuron,
                                              self.CA_STOPS_CA_WEIGHT,
                                              nealParameters.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'inhibitory')

    #undone need a test for this.
    def stateInhibitsState(self,fromNeurons, fromCA, toNeurons, toCA, wt):
        connector = []
        for fromOffset in range (0,self.CA_SIZE):
            fromNeuron = fromOffset + (fromCA*self.CA_SIZE)
            for toOffset in range (0,self.CA_SIZE):
                toNeuron = toOffset + (toCA*self.CA_SIZE)
                connector = connector + [(fromNeuron,toNeuron,
                                              wt,nealParameters.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'inhibitory')

    def oneNeuronTurnsOffState(self,fromNeurons, fromNeuron, toNeurons, toCA):
        connector = []
        for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            toNeuron = toOffset + (toCA*self.CA_SIZE)
            connector = connector + [(fromNeuron,toNeuron,
                                      self.ONE_NEURON_STOPS_CA_WEIGHT,
                                      nealParameters.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'inhibitory')


#------test functions
    #initialize the simulator. 
    def testInit(self):
        #print "spin" or nest
        sim.setup(timestep=nealParameters.DELAY,
                    min_delay=nealParameters.DELAY,
                    max_delay=nealParameters.DELAY, debug=0)


    def testCreateTwoInputs(self):
        inputSpikeTimes0 = [10.0]
        inputSpikeTimes1 = [50.0]
        spikeArray0 = {'spike_times': [inputSpikeTimes0]}
        spikeGen0=sim.Population(1,sim.SpikeSourceArray,spikeArray0,
                                   label='inputSpikes_0')
        spikeArray1 = {'spike_times': [inputSpikeTimes1]}
        spikeGen1=sim.Population(1, sim.SpikeSourceArray, spikeArray1,
                                   label='inputSpikes_1')

        return [spikeGen0,spikeGen1]

    def testCreateNeurons(self):
        if (nealParameters.simulator == 'nest'):
            numNeurons = self.CA_SIZE * 3
        elif (nealParameters.simulator == 'spinnaker'):
            numNeurons = 100
        
        cells=sim.Population(numNeurons,sim.IF_cond_exp,self.CELL_PARAMS)

        return cells

    def testSetupRecording(self,cells):
        if (nealParameters.simulator == 'nest'):
            cells.record({'spikes','v'})
        elif (nealParameters.simulator == 'spinnaker'):
            cells.record()

    def test3StateFSA(self, firstSpikeGenerator, secondSpikeGenerator,
                      stateCells):
        #Build the FSA
        self.turnOnStateFromSpikeSource(firstSpikeGenerator,stateCells,0)
        self.turnOnStateFromSpikeSource(secondSpikeGenerator,stateCells,1)
        self.makeCA(stateCells,0)
        self.makeCA(stateCells,1)
        self.makeCA(stateCells,2)
        self.stateHalfTurnsOnState(stateCells,0,stateCells,2)
        self.stateTurnsOffState(stateCells,2,stateCells,0)
        #comment below out to check state 0 alone does not turn on state 2
        self.stateHalfTurnsOnState(stateCells,1,stateCells,2)
        self.stateTurnsOffState(stateCells,2,stateCells,1)

    def testRunFSA(self,duration):
        sim.run(duration)

    def testPrintPklSpikes(self,fileName):
        fileHandle = open(fileName)
        neoObj = pickle.load(fileHandle)
        segments = neoObj.segments
        segment = segments[0]
        spikeTrains = segment.spiketrains
        neurons = len(spikeTrains)
        for neuronNum in range (0,neurons):
            if (len(spikeTrains[neuronNum])>0):
                spikes = spikeTrains[neuronNum]
                for spike in range (0,len(spikes)):
                    print neuronNum, spikes[spike]
        fileHandle.close()
    

    def testPrintResults(self,simCells):
        #print
        if  (nealParameters.simulator == 'nest'):
            simCells.printSpikes('temp.pkl')
            self.testPrintPklSpikes('temp.pkl')
        elif (nealParameters.simulator == 'spinnaker'):
            simCells.printSpikes('temp.sp')
