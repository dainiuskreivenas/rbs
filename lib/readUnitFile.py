"""
Read in from a file a list of units terminated by @@@@@.
Thease are stored into the units array.
"""
class UnitReaderClass:
    #instance variables
    units = []
    numberUnits = -1

    #--Functions for reading in the units
    #read lines until you get one starting with an @
    #each of these is a primitive unit in the hierarchy
    def readUnits(self,handle):
        unitListDone = False
        while (not unitListDone):
            line = handle.readline()
            if (line[0]=='@'):
                unitListDone = True
            else:
                unitName = line.strip() #take off the \n
                self.units = self.units + [unitName]
    
    def inUnits(self,checkUnit):
        done = False
        unitListOffset = 0
        while (not done):
            if (checkUnit == self.units[unitListOffset]):
                return True
            unitListOffset = unitListOffset + 1
            if (unitListOffset == self.numberUnits):
                done = True
        return False

    def getUnitNumber(self,checkUnit):
        for resultUnit in range (0,self.numberUnits):
            if (checkUnit == self.units[resultUnit]):
                return resultUnit
        print "error ", checkUnit , " not in unit array"


    #---top level functions
    def createViaRead(self,fileName):
        fileHandle = open(fileName, 'r')
        self.readUnits(fileHandle)
        self.numberUnits = len(self.units)
        fileHandle.close()

    def readUnitFile(self,fileName):
        inputFileName = fileName+".txt"
        self.createViaRead(inputFileName)

