#Functions to isolate differences between different list synapse constructors
#Note that you should only have one nealCoverClass in an entire system.
#It's current primary function is to store projection lists.  You 
#need to store them all and before the run is started apply 
#nealApplyProjections.
class NealCoverFunctions:
    projections = []
    
    def __init__(self, simName,sim,spinnVersion):
        self.DELAY = 1.0
        self.simulator = simName
        self.sim = sim
        self.spinnVersion = spinnVersion

    def nealProjection(self,preNeurons,postNeurons, connectorList,inhExc):
        newProjection = [preNeurons,postNeurons,inhExc,connectorList]
        self.projections.append(newProjection)

    def sameProjectionType(self,projectionA,projectionB):
        if ((projectionA[0] == projectionB[0]) and # pre Neurons 
            (projectionA[1] == projectionB[1]) and # post Neurons
            (projectionA[2] == projectionB[2])):    # inh or exc
            return True
        return False

    #collect the projections into projections that are pre post and type
    #specific.  Write those out in one fromList
    def nealApplyProjections(self):
        while (len(self.projections) > 0):
            projectionNumber = 0
            #get the first projection and collect all projections like it
            firstProjection = self.projections[0]
            connList = firstProjection[3]
            self.projections.remove(firstProjection)
            while (projectionNumber < len(self.projections)):
                if (self.sameProjectionType(self.projections[projectionNumber],
                           firstProjection)):
                    connList = connList + self.projections[projectionNumber][3]
                    #print projectionNumber,len(connList)
                    self.projections.remove(self.projections[projectionNumber])
                else:
                    projectionNumber = projectionNumber + 1
                    
            #actually put out the projections
            fromListConnector = self.sim.FromListConnector(connList)
            preNeurons = firstProjection[0]
            postNeurons = firstProjection[1]
            inhExc = firstProjection[2]
            if ((self.simulator=="spinnaker") and (self.spinnVersion==7)):
                self.sim.Projection(preNeurons, postNeurons, fromListConnector,
                                   target=inhExc)
            elif ((self.simulator=="nest") or
              ((self.simulator=="spinnaker") and (self.spinnVersion==8))):
                    self.sim.Projection(preNeurons, postNeurons, fromListConnector,
                                   receptor_type=inhExc)
            
            else: print "bad simulator nealProjection"

        
