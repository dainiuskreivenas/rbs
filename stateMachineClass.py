#This is the class for construcing State Machines.  The individual CAs 
#(both inputs and states) run at 5 ms.  See the notes for running faster or 
#slower. 
#There are test functions at the end. 
#Note that to externally activate a CA State, you should only send
#excitatory connections to the first 8 neurons.
#Using the nealNRPCover so no nealParams
#import nealParams as nealParameters

import numpy as np

from nealCoverClass import NealCoverFunctions

class FSAHelperFunctions:
    #def __init__(self, simName,sim,neal,spinnVersion):
    #changed for rbs backward compatability
    def __init__(self, sim, simName, neal=None,spinnVersion = None):
        self.simName = simName
        self.sim = sim
        if neal is None:
            self.neal = NealCoverFunctions(sim, simName)
            self.neal.DELAY = 1
            self.ONE_NEURON_STARTS_CA_WEIGHT = 0.08
            self.HALF_ON_ONE_WEIGHT = .00088
            self.ONE_HALF_ON_ONE_WEIGHT = 0.008
        else :
            self.neal = neal
        if spinnVersion is None:
            self.spinnVersion = -1
        else:
            self.spinnVersion = spinnVersion
        self.initParams()

    #FSA Parmaeters
    def initParams(self):
        self.CA_SIZE = 10  #This will (almost certainly) not work with a 
                     #different sized CA.
        self.CA_INHIBS = 2

        self.INPUT_WEIGHT = 0.12
        self.HALF_INPUT_WEIGHT = 0.08
        self.INTRA_CA_TO_INHIB_WEIGHT = 0.002
        #if (self.simName=="spinnaker"):
            #if you over inhib on my spinnaker, it fires.
        self.INTRA_CA_FROM_INHIB_WEIGHT = 0.15 
        self.CA_STOPS_CA_WEIGHT = 0.15
        self.ONE_NEURON_STOPS_CA_WEIGHT = 1.0
        #elif (self.simName=="nest"): Nov 2018
        #    self.INTRA_CA_FROM_INHIB_WEIGHT = -0.15 
        #    self.CA_STOPS_CA_WEIGHT = -0.15
        #    self.ONE_NEURON_STOPS_CA_WEIGHT = -1.0

        if (self.simName =="spinnaker"):
            self.INTRA_CA_WEIGHT = 0.025
        elif (self.simName == "nest"):
            self.INTRA_CA_WEIGHT = 0.022 
        self.FULL_ON_WEIGHT = 0.01 
        self.FULL_ON_WEIGHT_SLOW = 0.0022
        self.HALF_ON_WEIGHT = 0.0012
        self.STATE_TO_ONE_WEIGHT = .01

        if (self.simName == 'nest'):
            self.CELL_PARAMS = {'v_thresh':-48.0, 'v_reset' : -70.0, 
                                'tau_refrac': 2.0 , 'tau_syn_E': 5.0,  
                                'tau_syn_I' : 5.0, 
                                'v_rest' : -65.0,'i_offset':0.0}
        elif (self.simName == 'spinnaker'):
            self.CELL_PARAMS = {'v_thresh':-48.0, 'v_reset' : -70.0, 
                                'tau_refrac': 2.0 , 'tau_syn_E': 5.0,  
                                'tau_syn_I': 5.0, #bug2 fix
                                'v_rest' : -65.0,'i_offset':0.0}



    #--------Finite State Automata Functions ------------
    #states can be turned and off by a spikeSource, and can be stimulate or
                   #inhibited by one.
    #states can be turned on and off by a neuron, and can stimulate or inhibit
                    #one
    #states can stimulate or inhibit neurons

    #states can be turned on and off by a state, and can stimulate or inhibit
                    #them.  States can also slow turn on other states, and
                    #half turn them on


    #---Functions that turn on states by one item
    #-- Function to ignite a state from a spike source
    #-- Uses INPUT_WEIGHT
    #use this when your using a spikesource
    def turnOnStateFromSpikeSource(self,spikeSource, toNeurons, toCA):
        connector = []
        for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            toNeuron = toOffset + (toCA*self.CA_SIZE)
            connector = connector + [(0,toNeuron,self.INPUT_WEIGHT,
                                      self.neal.DELAY)]
        self.neal.nealProjection(spikeSource, toNeurons, connector,'excitatory')

    #undone new for cogmap on January 30th 2019.  Need to add to tests and
    #propagate through.  (This should be seemless as it's unused elsewhere)
    def halfTurnOnStateFromSpikeSource(self,spikeSource, toNeurons, toCA):
        connector = []
        for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            toNeuron = toOffset + (toCA*self.CA_SIZE)
            connector = connector + [(0,toNeuron,self.HALF_INPUT_WEIGHT,
                                      self.neal.DELAY)]
        self.neal.nealProjection(spikeSource, toNeurons, connector,'excitatory')

    def turnOffStateFromSpikeSource(self,spikeSource, toNeurons, toCA):
        connector = []
        for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            toNeuron = toOffset + (toCA*self.CA_SIZE)
            connector = connector + [(0,toNeuron,
                        self.ONE_NEURON_STOPS_CA_WEIGHT,self.neal.DELAY)]
        self.neal.nealProjection(spikeSource, toNeurons, connector,'inhibitory')

    def stimulateStateFromSpikeSource(self,spikeSource, toNeurons, toCA, weight):
        connector = []
        for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            toNeuron = toOffset + (toCA*self.CA_SIZE)
            connector = connector + [(0,toNeuron,weight,
                                      self.neal.DELAY)]
        self.neal.nealProjection(spikeSource, toNeurons, connector,'excitatory')

    def inhibitStateFromSpikeSource(self,spikeSource, toNeurons, toCA, weight):
        connector = []
        for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            toNeuron = toOffset + (toCA*self.CA_SIZE)
            connector = connector + [(0,toNeuron,weight,
                                      self.neal.DELAY)]
        self.neal.nealProjection(spikeSource, toNeurons, connector,'inhibitory')

    #---states can be turned on and off by a neuron, and can stimulate or 
    #inhibit one.
    #def turnOnStateFromOneNeuron(self,fromNeurons,fromNeuron, toNeurons, toCA):
    def oneNeuronTurnsOnState(self,fromNeurons,fromNeuron, toNeurons, toCA):
        connector = []
        for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            toNeuron = toOffset + (toCA*self.CA_SIZE)
            connector = connector + [(fromNeuron,toNeuron,self.INPUT_WEIGHT,
                                      self.neal.DELAY)]
        self.neal.nealProjection(fromNeurons, toNeurons, connector,'excitatory')

    def oneNeuronTurnsOffState(self,fromNeurons, fromNeuron, toNeurons, toCA):
        connector = []
        for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            toNeuron = toOffset + (toCA*self.CA_SIZE)
            connector = connector + [(fromNeuron,toNeuron,
                                      self.ONE_NEURON_STOPS_CA_WEIGHT,
                                      self.neal.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'inhibitory')

    def oneNeuronStimulatesState(self,fromNeurons,fromNeuron, toNeurons, toCA, 
                                weight):
        connector = []
        for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            toNeuron = toOffset + (toCA*self.CA_SIZE)
            connector = connector + [(fromNeuron,toNeuron,weight,
                                      self.neal.DELAY)]
        self.neal.nealProjection(fromNeurons, toNeurons, connector,'excitatory')

    def oneNeuronInhibitsState(self,fromNeurons,fromNeuron, toNeurons, toCA, 
                               weight):
        connector = []
        for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            toNeuron = toOffset + (toCA*self.CA_SIZE)
            connector = connector + [(fromNeuron,toNeuron,weight,
                                      self.neal.DELAY)]
        self.neal.nealProjection(fromNeurons, toNeurons, connector,'inhibitory')


    #states can stimulate or inhibit neurons
    def stateTurnsOnOneNeuron(self,fromNeurons,fromCA,toNeurons,toNeuron):
        connector = []
        #uses STATE_TO_ONE_WEIGHT
        for fromOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            fromNeuron = fromOffset + (fromCA*self.CA_SIZE)
            connector=connector+[(fromNeuron,toNeuron,
                                  self.STATE_TO_ONE_WEIGHT,
                                  self.neal.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'excitatory')

    def stateStimulatesOneNeuron(self,fromNeurons,fromCA,toNeurons,toNeuron,
                                 weight):
        connector = []
        for fromOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            fromNeuron = fromOffset + (fromCA*self.CA_SIZE)
            connector=connector+[(fromNeuron,toNeuron,weight,
                                  self.neal.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'excitatory')


    def stateInhibitsOneNeuron(self,fromNeurons,fromCA,toNeurons,toNeuron, 
                              weight):
        connector = []
        for fromOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            fromNeuron = fromOffset + (fromCA*self.CA_SIZE)
            connector=connector+[(fromNeuron,toNeuron,weight,
                                  self.neal.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'inhibitory')

    #states can be turned on and off by a state, and can stimulate or inhibit
                    #them.  States can also slow turn on other states, and
                    #half turn them on

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
                                          self.neal.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'excitatory')

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
                                          self.neal.DELAY)]

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
                                              self.neal.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'inhibitory')

    #--Functions when two inputs are needed to turn on a third
    #-- Two states are needed to turn on a third.  
    #-- This connects one of the inputs to the the third.
    #-- Uses HALFs_ON_WEIGHT
    def stateHalfTurnsOnState(self,fromNeurons,fromCA,toNeurons,toCA):
        connector = []
        #uses HALF_ON_WEIGHT
        for fromOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            fromNeuron = fromOffset + (fromCA*self.CA_SIZE)
            for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
                toNeuron = toOffset + (toCA*self.CA_SIZE)
                connector=connector+[(fromNeuron,toNeuron,
                                          self.HALF_ON_WEIGHT,
                                          self.neal.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'excitatory')

    def stateStimulatesState(self,fromNeurons,fromCA,toNeurons,toCA,weight):
        connector = []
        for fromOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            fromNeuron = fromOffset + (fromCA*self.CA_SIZE)
            for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
                toNeuron = toOffset + (toCA*self.CA_SIZE)
                connector=connector+[(fromNeuron,toNeuron,
                    weight, self.neal.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'excitatory')

    def stateInhibitsState(self,fromNeurons, fromCA, toNeurons, toCA, wt):
        connector = []
        for fromOffset in range (0,self.CA_SIZE):
            fromNeuron = fromOffset + (fromCA*self.CA_SIZE)
            for toOffset in range (0,self.CA_SIZE):
                toNeuron = toOffset + (toCA*self.CA_SIZE)
                connector = connector + [(fromNeuron,toNeuron,
                                              wt,self.neal.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'inhibitory')



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
                        self.INTRA_CA_WEIGHT, self.neal.DELAY)]

        self.neal.nealProjection(neurons,neurons,connector,'excitatory')

        #excitatory turn on inhibitory
        connector = []
        for fromOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
            fromNeuron = fromOffset + (CA*self.CA_SIZE)
            for toOffset in range (self.CA_SIZE-self.CA_INHIBS,self.CA_SIZE):
                toNeuron = toOffset + (CA*self.CA_SIZE)
                connector = connector + [(fromNeuron,toNeuron,
                        self.INTRA_CA_TO_INHIB_WEIGHT, self.neal.DELAY)]

        self.neal.nealProjection(neurons,neurons,connector,'excitatory')

        #inhibitory slows excitatory 
        connector = []
        for fromOffset in range (self.CA_SIZE-self.CA_INHIBS,self.CA_SIZE):
            fromNeuron = fromOffset + (CA*self.CA_SIZE)
            for toOffset in range (0,self.CA_SIZE-self.CA_INHIBS):
                toNeuron = toOffset + (CA*self.CA_SIZE)
                connector = connector + [(fromNeuron,toNeuron,
                        self.INTRA_CA_FROM_INHIB_WEIGHT, self.neal.DELAY)]

        self.neal.nealProjection(neurons,neurons,connector,'inhibitory')

    def nopMakeCA(self,neurons, CA):
        connector = []
        fromNeuron = CA
        toNeuron = CA + 1
        connector = connector + [(fromNeuron,toNeuron, 1.2, self.neal.DELAY)]

        self.neal.nealProjection(neurons,neurons,connector,'excitatory')
        
#------test functions
    #initialize the simulator. 
    def testInit(self):
        #print "spin" or nest
        self.sim.setup(timestep=self.neal.DELAY,
                    min_delay=self.neal.DELAY,
                    max_delay=self.neal.DELAY, debug=0)


    def testCreateTwoInputs(self):
        inputSpikeTimes0 = [10.0]
        inputSpikeTimes1 = [50.0]
        spikeArray0 = {'spike_times': [inputSpikeTimes0]}
        spikeGen0=self.sim.Population(1,self.sim.SpikeSourceArray,spikeArray0,
                                   label='inputSpikes_0')
        spikeArray1 = {'spike_times': [inputSpikeTimes1]}
        spikeGen1=self.sim.Population(1, self.sim.SpikeSourceArray, spikeArray1,
                                   label='inputSpikes_1')

        return [spikeGen0,spikeGen1]

    def testCreateNeurons(self):
        if (self.simName == 'nest'):
            numNeurons = self.CA_SIZE * 3
        elif (self.simName == 'spinnaker'):
            numNeurons = 100
        
        cells=self.sim.Population(numNeurons,self.sim.IF_cond_exp,self.CELL_PARAMS)

        return cells

    def testSetupRecording(self,cells):
        if  ((self.neal.simulator == 'nest') or 
             ((self.neal.simulator == 'spinnaker') and (self.neal.spinnVersion == 8))):
            cells.record({'spikes','v'})
        elif ((self.neal.simulator == 'spinnaker') and (self.neal.spinnVersion == 7)):
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
        self.sim.run(duration)

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
        if  ((self.neal.simulator == 'nest') or 
             ((self.neal.simulator == 'spinnaker') and (self.neal.spinnVersion == 8))):
            simCells.printSpikes('temp.pkl')
        elif ((self.neal.simulator == 'spinnaker') and (self.neal.spinnVersion == 7)):
            simCells.printSpikes('temp.sp')

