#This is the class for construcing State Machines.  The individual CAs 
#(both inputs and states) run at 5 ms.  See the notes for running faster or 
#slower. 
#There are test functions at the end. 
#Note that to externally activate a CA State, you should only send
#excitatory connections to the first 8 neurons.

import nealParams as nealParameters
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
     
        #----- removed the spinnaker switch controlled in rbs.exe
        self.INTRA_CA_FROM_INHIB_WEIGHT = -0.1
        self.CA_STOPS_CA_WEIGHT = -0.15
        self.ONE_NEURON_STOPS_CA_WEIGHT = -1.0

        self.ONE_NEURON_STARTS_CA_WEIGHT = 0.08
        self.INTRA_CA_WEIGHT = 0.016 
        
        #---- STATE to ? WEIGHTS
        self.FULL_ON_WEIGHT = 0.01
        self.STATE_TO_ONE_WEIGHT = 0.01

        self.FULL_ON_WEIGHT_SLOW = 0.0015
        
        self.HALF_ON_WEIGHT = 0.0008
        self.HALF_ON_ONE_WEIGHT = .0008

        #---- NEURON to ? WEIGHTS
        self.ONE_HALF_ON_WEIGHT = 0.007
        self.ONE_HALF_ON_ONE_WEIGHT = 0.03
        
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

    #---Create a CA that will persistently fire.
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
                w = self.INTRA_CA_FROM_INHIB_WEIGHT
                if(self.simulator == "spinnaker"):
                    w = w*-1
                connector = connector + [(fromNeuron,toNeuron, w, nealParameters.DELAY)]
        
        self.neal.nealProjection(neurons,neurons,connector,'inhibitory')

    #--------Finite State Automata Functions ------------

    #-------- Turns On Functions

    #-------- SPIKE GENERATOR FUCNTION
    def turnOnStateFromSpikeSource(self,spikeSource, toNeurons, toCA):
        connector = []
        for toNeuron in range (toCA,toCA+self.CA_SIZE-self.CA_INHIBS):
            connector = connector + [(0,toNeuron,self.INPUT_WEIGHT,
                                      nealParameters.DELAY)]
        self.neal.nealProjection(spikeSource, toNeurons, connector,'excitatory')

################ NEURON METHODS #################
    def oneNeuronStimulatesState(self,fromNeurons, fromNeuron, toNeurons, toCA, weight):
        connector = []
        for toNeuron in range (0,self.CA_SIZE-self.CA_INHIBS):
            connector = connector + [(fromNeuron,toNeuron,weight,nealParameters.DELAY)]

        self.neal.nealProjection(fromNeurons, toNeurons, connector,'excitatory')

    def oneNueronStimulatesNeuron(self, fromNeurons,fromCA,toNeurons,toCA,weight):
        connector = [(fromCA, toCA, weight, nealParameters.DELAY)]
        self.neal.nealProjection(fromNeurons,toNeurons,connector,'excitatory')

    #-------- ONE TURNS ON ?
    def oneNeuronTurnsOnState(self,fromNeurons,fromNeuron, toNeurons, toCA):
        self.oneNeuronStimulatesState(fromNeurons, fromNeuron, toNeurons, toCA, self.ONE_NEURON_STARTS_CA_WEIGHT)

    def oneNeuronTurnsOnOneNeuron(self,fromNeurons,fromCA,toNeurons,toCA):
        self.oneNueronStimulatesNeuron(fromNeurons,fromCA,toNeurons,toCA, self.INPUT_WEIGHT)

    #-------- ONE HALF TURNS ON ?
    def oneNeuronHalfTurnsOnOneNeuron(self,fromNeurons,fromCA,toNeurons,toCA):
        self.oneNueronStimulatesNeuron(fromNeurons,fromCA,toNeurons,toCA, self.ONE_HALF_ON_ONE_WEIGHT)

    def oneNeuronHalfTurnsOnState(self,fromNeurons,fromCA,toNeurons,toCA):
        self.oneNeuronStimulatesState(fromNeurons,fromCA,toNeurons,toCA,self.ONE_HALF_ON_WEIGHT)

    #-------- ONE TURNS OFF ?
    def oneNeuronTurnsOffState(self,fromNeurons, fromNeuron, toNeurons, toCA):
        connector = []
        for toNeuron in range (toCA,toCA+self.CA_SIZE-self.CA_INHIBS):
            w = self.ONE_NEURON_STOPS_CA_WEIGHT
            if(self.simulator == "spinnaker"):
                w = w*-1
            connector = connector + [(fromNeuron,toNeuron,w,nealParameters.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'inhibitory')

################ STATE METHODS #################
    def stateStimulatesState(self,fromNeurons,fromCA,toNeurons,toCA,weight):
        connector = []
        for fromNeuron in range (fromCA, fromCA+self.CA_SIZE-self.CA_INHIBS):
            for toNeuron in range (toCA, toCA+self.CA_SIZE-self.CA_INHIBS):
                connector=connector+[(fromNeuron,toNeuron,weight,nealParameters.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'excitatory')

    def stateInhibitsState(self,fromNeurons,fromCA,toNeurons,toCA,weight):
        connector = []
        for fromNeuron in range (fromCA, fromCA+self.CA_SIZE-self.CA_INHIBS):
            for toNeuron in range (toCA, toCA+self.CA_SIZE-self.CA_INHIBS):
                w = weight
                if(self.simulator == "spinnaker"):
                    w = w*-1
                connector=connector+[(fromNeuron,toNeuron,w,nealParameters.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'inhibitory')

    def stateStimulatesNeuron(self,fromNeurons,fromCA,toNeurons,toNeuron,weight):
        connector = []
        for fromNeuron in range (0,self.CA_SIZE-self.CA_INHIBS):
            connector=connector+[(fromNeuron,toNeuron,weight,nealParameters.DELAY)]

        self.neal.nealProjection(fromNeurons,toNeurons,connector,'excitatory')

    #-------- STATE TURNS ON ?
    def stateTurnsOnState(self,fromNeurons,fromCA,toNeurons,toCA):
        self.stateStimulatesState(fromNeurons,fromCA, toNeurons, toCA, self.FULL_ON_WEIGHT)

    def stateTurnsOnStateSlow(self,fromNeurons,fromCA,toNeurons,toCA):
        self.stateStimulatesState(fromNeurons,fromCA, toNeurons, toCA, self.FULL_ON_WEIGHT_SLOW)

    def stateTurnsOnOneNeuron(self,fromNeurons,fromCA,toNeurons,toNeuron):
        self.stateStimulatesNeuron(fromNeurons,fromCA,toNeurons,toNeuron,self.STATE_TO_ONE_WEIGHT)

    #-------- STATE TURNS OFF ?
    def stateTurnsOffState(self,fromNeurons, fromCA, toNeurons, toCA):
        self.stateInhibitsState(fromNeurons, fromCA, toNeurons, toCA, self.CA_STOPS_CA_WEIGHT)

    #-------- STATE HALF TURNS ON ?
    def stateHalfTurnsOnState(self,fromNeurons,fromCA,toNeurons,toCA):
        self.stateStimulatesState(fromNeurons,fromCA, toNeurons, toCA, self.HALF_ON_WEIGHT)

    def stateHalfTurnsOnOneNueron(self,fromNeurons,fromCA,toNeurons,toNeuron):
        self.stateStimulatesNeuron(fromNeurons,fromCA,toNeurons,toNeuron,self.HALF_ON_ONE_WEIGHT)