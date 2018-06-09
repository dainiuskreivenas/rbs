import nealParams as nealParameters
if (nealParameters.simulator=="spinnaker"):
    import pyNN.spiNNaker as sim
elif (nealParameters.simulator=="nest"):
    import pyNN.nest as sim
    import cPickle as pickle


#Functions to isolate differences between different list synapse constructors
class NealCoverFunctions:
    def __init__(self, simName):
        """
        self.DELAY = 1.0
        self.simulator = simName
        if self.simulator == "nest":
            exec("from nest import *")
        elif self.simulator == 'spinnaker':
            exec("from pyNN.spiNNaker import *")

        else: print "bad simulator in nealFunctions"
        """

    def nealProjection(self,preNeurons,postNeurons, connectorList,inhExc):
        connList = sim.FromListConnector(connectorList)
        if (nealParameters.simulator=="spinnaker"):
            sim.Projection(preNeurons, postNeurons, connList,target=inhExc)   
        elif (nealParameters.simulator=="nest"):
            sim.Projection(preNeurons, postNeurons, connList) 

        else: print "bad simulator nealProjection"

