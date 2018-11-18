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

    def nealProjection(self,preNeurons,postNeurons, connectorList, type="excitatory"):
        if (nealParameters.simulator=="spinnaker"):
            connList = sim.FromListConnector(connectorList)
            sim.Projection(preNeurons, postNeurons, connList, receptor_type=type)
        elif (nealParameters.simulator=="nest"):
            connList = sim.FromListConnector(connectorList)
            sim.Projection(preNeurons, postNeurons, connList) 
        else: print "bad simulator nealProjection"

