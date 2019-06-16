#Functions to isolate differences between different list synapse constructors
class NealCoverFunctions:
    def __init__(self, sim, simName):
        self.sim = sim
        self.simulator = simName

    def nealProjection(self,preNeurons,postNeurons, connectorList, type="excitatory"):
        if (self.simulator=="spinnaker"):
            connList = self.sim.FromListConnector(connectorList)
            self.sim.Projection(preNeurons, postNeurons, connList, receptor_type=type)
        elif (self.simulator=="nest"):
            connList = self.sim.FromListConnector(connectorList)
            self.sim.Projection(preNeurons, postNeurons, connList) 
        else: print "bad simulator nealProjection"

