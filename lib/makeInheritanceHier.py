"""
Create an neural topology that has an inheritance hierarchy.
In PyNN/python the topology can be accessed via this class.

Invoke by creating the class, then calling createNeuralInheritanceHierarcy 
with an inheritance hierarchy specified in python (readInheritanceClass is one
way).
"""
class NeuralInheritanceClass:
    #constants
    neuronsPerCA = 10
    intraCAWeight = 0.0085 # .01 is hot (every 4 ms) .005 doesn't go #replaced with fsa state weights
    hierWeight = 0.0012 #replaced with half fsa connections undone 
    primeWeight = 0.017#0.016-0.015 three levels of hier in 75 ms#.02 too big

    #class variables
    numCAs = -1
    cells = None
    
    def __init__(self, simName,sim,neal,spinnVersion,fsa):
        self.simName = simName
        self.sim = sim
        self.neal = neal
        self.spinnVersion = spinnVersion
        self.fsa = fsa

    def createNeurons(self,numNeurons):
        self.cells = self.sim.Population(numNeurons,self.sim.IF_cond_exp, 
                                    self.fsa.CELL_PARAMS)

    def setRecord(self):
        self.cells.record(['spikes'])

    #Make a binary CA for each unit
    def makeCAs(self):
        for CA in range (0,self.numCAs):
            self.fsa.makeCA(self.cells,CA)

    #make a hierarchical relationship for each isA pair passed in
    def makeHiersFromHier(self,pythonHier):
        isAPairs = pythonHier.isARelationships
        numberPairs = len(isAPairs)
        for pairNumber in range (0,numberPairs):
            subCatName = isAPairs[pairNumber][0]
            superCatName = isAPairs[pairNumber][1]
            subCatNumber = pythonHier.getUnitNumber(subCatName)
            superCatNumber = pythonHier.getUnitNumber(superCatName)
            #print(subCatName,superCatName,subCatNumber,superCatNumber)
            #make one hierarchical relations as a half CA connection
            self.fsa.stateHalfTurnsOnState(self.cells,subCatNumber,
                                           self.cells,superCatNumber)

    #--Main way to create the heirarchy topology
    def createNeuralInheritanceHierarchy(self,inheritanceStructure):
        self.numCAs = inheritanceStructure.numberUnits 
        numberNeurons = self.numCAs * self.neuronsPerCA
        self.createNeurons(numberNeurons)
        self.setRecord()
        self.makeCAs()
        self.makeHiersFromHier(inheritanceStructure)

    #---Test code.
    #Set up spike generators to start each unit, then stop them.
    #When run, each unit should persist, but only that unit 
    #should.
    def makeGenerator(self,genTime):
        genTimes = genTime
        genTimeArray = {'spike_times': [genTimes]}
        spikeGen=self.sim.Population(1,self.sim.SpikeSourceArray,genTimeArray)
        return spikeGen

    #now stop all of the units after each individual unit is tested.
    def createStopAll(self,stopTimes):
        stopTimeArray = {'spike_times': [stopTimes]}
        stopSpikeGen=self.sim.Population(1,self.sim.SpikeSourceArray,
                                         stopTimeArray)
        for unit in range (0,self.numCAs): #numCAs is numUnits
            self.fsa.turnOffStateFromSpikeSource(stopSpikeGen,self.cells,unit)

    def createTestAllUnits(self,firstTestStart):
        oneTestDuration = 100.0
        stopTimes = []
        for unit in range (0,self.numCAs): #numCAs is numUnits
            startTime = 25.0 + (unit*oneTestDuration)+firstTestStart
            generator = self.makeGenerator([startTime])
            self.fsa.turnOnStateFromSpikeSource(generator,self.cells,unit)
            lastTime =(((unit+1)*oneTestDuration)+firstTestStart)
            stopTimes = stopTimes + [lastTime]

        self.createStopAll(stopTimes)
        return lastTime

    #Create a spikeGen that primes all of the units numTests times.
    #Connect it to all of the units.
    def createTestPrimeAllUnits(self,firstTestStart,numTests):
        oneTestDuration = 100.0
        timeBetweenSteps = 5.0
        numberPrimeSteps = 10
        for primeEpoch in range (0,self.numCAs): #numCAs is numUnits
            startTime = 25.0 + (primeEpoch*oneTestDuration)+firstTestStart
            primeTimes = []
            for primeStep in range (0,numberPrimeSteps): 
                primeTimes = primeTimes + [startTime + 
                                           (timeBetweenSteps*primeStep)]
            generator = self.makeGenerator(primeTimes)

            #self.connectGeneratorToPrimeUnit(generator,unit)
            for unit in range (0,self.numCAs): #numCAs is numUnits
                self.fsa.stimulateStateFromSpikeSource(generator,self.cells,
                                                       unit,self.primeWeight)
        return firstTestStart + (self.numCAs*oneTestDuration)

    #Create spikeGens and synapses to connect all the units
    #to be tested, and to spread up the hierarchy.
    def createTestAllInheritanceUnits(self,firstTestStart):
        testFullTime = self.createTestPrimeAllUnits(firstTestStart,self.numCAs)
        #this assumes that both of the functions have the same testduration.
        otherTestFullTime = self.createTestAllUnits(firstTestStart)
        print("bob", testFullTime, otherTestFullTime)
        return otherTestFullTime

    #This is a test to see if some neurons are firing.
    def createSimpleTest(self):
        primeTimes = [5]
        primeArray = {'spike_times': [primeTimes]}
        generator=self.sim.Population(1,self.sim.SpikeSourceArray,primeArray)

        self.fsa.turnOnStateFromSpikeSource(generator,self.cells,0)

    def printInheritanceHier(self,fileName):
        self.cells.printSpikes(fileName)
