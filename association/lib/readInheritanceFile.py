"""
Read in an inheritance file and fill the individual items in
the hierarchy and the isa pairs.  Access these via the methods 
in this class.

Invoke by creating the class, then calling
readInheritanceFile(fileName) with an assumed .txt suffix
"""

class InheritanceReaderClass:
    #instance variables
    units = []
    numberUnits = -1
    isARelationships = []
    numberIsAs = -1

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

    #--Functions for reading in the isAs
    #read lines until you get one starting with an @
    #each line should be three tuple of A isA B
    #report error if it's not a threeTuple, if A or B is not in units and 
    #isA is not isA
    def readIsAs(self,handle):
        relationshipListDone = False
        while (not relationshipListDone):
            line = handle.readline()
            if (line[0]=='@'):
                relationshipListDone = True
            else:
                stringTriplet = line.split(' ')
                if (len(stringTriplet) != 3):
                    print "error ", line, " wrong length"
                if (stringTriplet[1] != "isA"):
                    print "error ", line, " only handling isA now"
                subCatName = stringTriplet[0]
                superCatName = stringTriplet[2]
                superCatName = superCatName.strip()
                #Check sub and supercat in units
                if (not self.inUnits(subCatName)):
                    print "error ", subCatName, " not a unit"
                if (not self.inUnits(superCatName)):
                    print "error ", superCatName, " not a unit"

                self.isARelationships = self.isARelationships + [
                    [subCatName,superCatName]]

    #---top level functions
    def createViaRead(self,fileName):
        fileHandle = open(fileName, 'r')
        self.readUnits(fileHandle)
        self.numberUnits = len(self.units)
        self.readIsAs(fileHandle)
        self.numberIsAs = len(self.isARelationships)
        fileHandle.close()

    def readInheritanceFile(self,fileName):
        inputFileName = fileName+".txt"
        self.createViaRead(inputFileName)

