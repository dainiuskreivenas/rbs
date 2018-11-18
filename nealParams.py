#This the file that's included first.  It selects the parameters for any
#given test.
#There are three ways to run these systems.
#1. On Chris' machine in spinnaker (this is pynn .8beta2)
#2. On Chris' machine in nest 
#So, simulator = spinnaker
#2 simulator = nest

#Select the simulator by changing the import and simulator_name
#simulator = "nest"
simulator = "spinnaker"


printSmall = False #True
#autoRun =  False 
autoRun =  True        #run the environment with an automatic response to
                       #one of the extra actions.
useSpikeServer = True  #In Spinnaker, for at least vision, you can use the
                       #the spikeserver (typically from the environment)
                       #or can it with spike sources.


#INPSIZE = 40
INPSIZE = 20
neuronsPerSubnet = INPSIZE * INPSIZE  #replace neuronsPerSubnet with neuronsPVS
neuronsPerVisionSubnet = INPSIZE * INPSIZE

DELAY = 1.0
#SIM_LENGTH = 200000.0
#SIM_LENGTH = 120000.0
#SIM_LENGTH = 80000.0
#SIM_LENGTH = 30000.0
#SIM_LENGTH = 15000.0
#SIM_LENGTH = 8000.0
#SIM_LENGTH = 3600.0
#SIM_LENGTH = 3000.0
SIM_LENGTH = 200.0
#SIM_LENGTH = 100.0

