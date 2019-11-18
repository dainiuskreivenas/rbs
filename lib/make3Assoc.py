"""
This creates a three way association topology.  One of the types
is the base type (typically a node in a semantic net).  The other
two are the same but one is named relation and the other property.
If you turn two on, the third should come on.  You should also be
able to get the (base) to spread up the inheritance hierarchy.

Testing is weak.  It has only been tested in nest.
"""

import pickle
from ..stateMachineClass import FSAHelperFunctions
from makeInheritanceHier import NeuralInheritanceClass

class NeuralThreeAssocClass:
    #class variables
    numPropertyCAs = -1
    numRelationshipCAs = -1
    neuralHierarchyTopology = None
    baseStructure = None
    propStructure = None
    relStructure = None

    def __init__(self, simName,sim,neal,spinnVersion,fsa):
        self.simName = simName
        self.sim = sim
        self.neal = neal
        self.spinnVersion = spinnVersion
        self.fsa = fsa

    def createNeurons(self,numPropertyNeurons,numRelationNeurons):
        self.propertyCells = self.sim.Population(numPropertyNeurons,
                    self.sim.IF_cond_exp,self.fsa.CELL_PARAMS)
        self.relationCells = self.sim.Population(numRelationNeurons,
                    self.sim.IF_cond_exp, self.fsa.CELL_PARAMS)

    def setRecord(self):
        self.propertyCells.record(['spikes'])
        self.relationCells.record(['spikes'])

    #Make a binary CA for each unit
    def makeCAs(self):
        for CA in range (0,self.numPropertyCAs):
            self.fsa.makeCA(self.propertyCells,CA)
        for CA in range (0,self.numRelationCAs):
            self.fsa.makeCA(self.relationCells,CA)
    
    #main function
    def createBaseNet(self,baseNodeStructure):
        self.baseStructure = baseNodeStructure
        self.neuralHierarchyTopology = NeuralInheritanceClass(self.simName,
                self.sim,self.neal,self.spinnVersion,self.fsa)
        self.neuralHierarchyTopology.createNeuralInheritanceHierarchy(
            baseNodeStructure)

    def createAssociationTopology(self,propertyStructure,relationStructure):
        self.propStructure = propertyStructure
        self.relStructure = relationStructure
        self.numPropertyCAs = propertyStructure.numberUnits 
        numberPropertyNeurons = self.numPropertyCAs * self.fsa.CA_SIZE
        self.numRelationCAs = relationStructure.numberUnits 
        numberRelationNeurons = self.numRelationCAs * self.fsa.CA_SIZE
        self.createNeurons(numberPropertyNeurons,numberRelationNeurons)
        self.setRecord()
        self.makeCAs()

    #Add synapses that make a 2/3 CA.
    def addThreeAssoc(self,assocTuple):
        base = assocTuple[0]
        relation = assocTuple[1]
        property = assocTuple[2]
        baseNum = self.baseStructure.getUnitNumber(base)
        propertyNum = self.propStructure.getUnitNumber(property)
        relationNum = self.relStructure.getUnitNumber(relation)
        #print assocTuple
        #print baseNum,propertyNum,relationNum

        self.fsa.stateHalfTurnsOnState(self.neuralHierarchyTopology.cells,
                                       baseNum,self.propertyCells,propertyNum)
        self.fsa.stateHalfTurnsOnState(self.neuralHierarchyTopology.cells,
                                       baseNum,self.relationCells,relationNum)

        self.fsa.stateHalfTurnsOnState(self.propertyCells,propertyNum,
                                self.neuralHierarchyTopology.cells,baseNum)
        self.fsa.stateHalfTurnsOnState(self.propertyCells,propertyNum,
                                       self.relationCells,relationNum)

        self.fsa.stateHalfTurnsOnState(self.relationCells,relationNum,
                                self.neuralHierarchyTopology.cells,baseNum)
        self.fsa.stateHalfTurnsOnState(self.relationCells,relationNum,
                                       self.propertyCells,propertyNum)

    def addAssociations(self,assocStructure):
        print assocStructure.numberAssocs
        for assocNum in range (0,assocStructure.numberAssocs):
            self.addThreeAssoc(assocStructure.assocs[assocNum])


    #-print function
    def printSpikes(self):
        self.propertyCells.printSpikes("testProps.pkl")
        self.relationCells.printSpikes("testRels.pkl")
        self.neuralHierarchyTopology.cells.printSpikes("test3.pkl")


    def printPklSpikes(self,inFileName,outFileName):
        outFileHandle = open(outFileName,'w')
        inFileHandle = open(inFileName)
        neoObj = pickle.load(inFileHandle)
        segments = neoObj.segments
        segment = segments[0]
        spikeTrains = segment.spiketrains
        neurons = len(spikeTrains)
        for neuronNum in range (0,neurons):
            if (len(spikeTrains[neuronNum])>0):
                spikes = spikeTrains[neuronNum]
                for spike in range (0,len(spikes)):
                    #outFileHandle.print(neuronNum, spikes[spike])
                    outString = str(neuronNum) + " " + str(spikes[spike]) +"\n";
                    outFileHandle.write(outString)
        inFileHandle.close()
        outFileHandle.flush()
        outFileHandle.close()

    def printSpikes(self,fileName):
        if ((self.simName =="spinnaker") and (self.spinnVersion == 7)):
            suffix = ".sp"
        elif ((self.simName =="nest") or
              ((self.simName =="spinnaker") and (self.spinnVersion == 8))):
            suffix = ".pkl"

        basePklFile = "results/"+fileName +"Bases" + suffix
        #baseSpFile = "results/"+fileName +"Bases.sp"
        self.neuralHierarchyTopology.cells.printSpikes(basePklFile)
        #self.printPklSpikes(basePklFile,baseSpFile)
        propPklFile = "results/"+fileName +"Props"+ suffix
        self.propertyCells.printSpikes(propPklFile)
        relPklFile = "results/"+fileName +"Rels"+ suffix
        self.relationCells.printSpikes(relPklFile)

    #--test functions
    #Set up spike generators to start each unit, then stop them.
    #When run, each unit should persist, but only that unit 
    #should.
    def makeGenerator(self,genTime):
        genTimes = genTime
        genTimeArray = {'spike_times': [genTimes]}
        spikeGen=self.sim.Population(1,self.sim.SpikeSourceArray,genTimeArray)
        return spikeGen

    #now stop all of the units after each individual unit is tested.
    def createStopAll(self,stopTimes,cells,numUnits):
        stopTimeArray = {'spike_times': [stopTimes]}
        stopSpikeGen=self.sim.Population(1,self.sim.SpikeSourceArray,
                                         stopTimeArray)
        for unit in range (0,numUnits): 
            self.fsa.turnOffStateFromSpikeSource(stopSpikeGen,cells,unit)

    def createSimpleTest(self):
        primeTimes = [5]
        primeArray = {'spike_times': [primeTimes]}
        generator=self.sim.Population(1,self.sim.SpikeSourceArray,primeArray)
        
        self.fsa.turnOnStateFromSpikeSource(generator,self.propertyCells,1)
        self.fsa.turnOnStateFromSpikeSource(generator,self.relationCells,2)
        self.neuralHierarchyTopology.createSimpleTest()

    #call this with 0-3 items to be stimulated (but typically two)
    def createTwoTest(self,baseNum,propNum,relNum):
        primeTimes = [5]
        primeArray = {'spike_times': [primeTimes]}
        generator=self.sim.Population(1,self.sim.SpikeSourceArray,primeArray)
        
        if (baseNum >= 0):
            self.fsa.turnOnStateFromSpikeSource(generator,
                        self.neuralHierarchyTopology.cells,baseNum)
        if (propNum >= 0):
            self.fsa.turnOnStateFromSpikeSource(generator,self.propertyCells,
                                                propNum)
        if (relNum >= 0):
            self.fsa.turnOnStateFromSpikeSource(generator,self.relationCells,
                                                relNum)

    def createTestPrimeAllBaseUnits(self,firstTestStart,hierarchy):
        primeWeight = 0.014#0.017
        oneTestDuration = 100.0
        timeBetweenSteps = 5.0
        numberPrimeSteps = 10
        for primeEpoch in range (0,hierarchy.numCAs): 
            startTime = 25.0 + (primeEpoch*oneTestDuration)+firstTestStart
            primeTimes = []
            for primeStep in range (0,numberPrimeSteps): 
                primeTimes = primeTimes + [startTime + 
                                           (timeBetweenSteps*primeStep)]
            generator = self.makeGenerator(primeTimes)

            for unit in range (0,hierarchy.numCAs): #numCAs is numUnits
                self.fsa.stimulateStateFromSpikeSource(generator,hierarchy.cells,
                                                       unit,primeWeight)
        return firstTestStart + (hierarchy.numCAs*oneTestDuration)

    #call this with 0-3 items to be stimulated (but typically two)
    def createTwoPrimeTest(self,baseNum,propNum,relNum):
        primeTimes = [5]
        primeArray = {'spike_times': [primeTimes]}
        generator=self.sim.Population(1,self.sim.SpikeSourceArray,primeArray)
        
        if (baseNum >= 0):
            self.fsa.turnOnStateFromSpikeSource(generator,
                        self.neuralHierarchyTopology.cells,baseNum)
            self.createTestPrimeAllBaseUnits(5.0,self.neuralHierarchyTopology)

        if (propNum >= 0):
            self.fsa.turnOnStateFromSpikeSource(generator,self.propertyCells,
                                                propNum)
        if (relNum >= 0):
            self.fsa.turnOnStateFromSpikeSource(generator,self.relationCells,
                                                relNum)

    #call this with 0-3 items to be stimulated (but typically two) 
    def createTwoPrimeTestPoisson(self,baseNum,propNum,relNum):
        PoissonParameters = {'duration': 200.0, 'start': 0.0, 'rate': 200.0} # rate = 200 Hz  
        generator=self.sim.Population(1,self.sim.SpikeSourcePoisson,PoissonParameters)
        
        if (baseNum >= 0):
            self.fsa.turnOnStateFromSpikeSource(generator,
                        self.neuralHierarchyTopology.cells,baseNum)
            self.createTestPrimeAllBaseUnits(5.0,self.neuralHierarchyTopology)

        if (propNum >= 0):
            self.fsa.turnOnStateFromSpikeSource(generator,self.propertyCells,
                                                propNum)
        if (relNum >= 0):
            self.fsa.turnOnStateFromSpikeSource(generator,self.relationCells,
                                                relNum)



    def createTestAllUnits(self,firstTestStart,cells,numUnits):
        print numUnits
        oneTestDuration = 100.0
        stopTimes = []
        for unit in range (0,numUnits): 
            startTime = 25.0 + (unit*oneTestDuration)+firstTestStart
            generator = self.makeGenerator([startTime])
            self.fsa.turnOnStateFromSpikeSource(generator,cells,unit)
            lastTime =(((unit+1)*oneTestDuration)+firstTestStart)
            stopTimes = stopTimes + [lastTime]

        print stopTimes
        self.createStopAll(stopTimes,cells,numUnits)
        return lastTime

    def createUnitTests(self):
        baseUnitTime = self.neuralHierarchyTopology.createTestAllUnits(0.0)
        propUnitTime = self.createTestAllUnits(baseUnitTime,self.propertyCells,
                                               self.numPropertyCAs)
        relUnitTime = self.createTestAllUnits(propUnitTime,self.relationCells,
                                               self.numRelationCAs)


        print baseUnitTime,propUnitTime,relUnitTime
        return relUnitTime
