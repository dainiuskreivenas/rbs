"""
Read in a file terminated by @@@ or association triples.  Fill
the association structure; this is a triple association.
"""
class AssocReaderClass:
    #instance variables
    assocs = []
    numberAssocs = -1

    #--Functions for reading in the assocs
    #read lines until you get one starting with an @
    #each of these is a primitive unit in the hierarchy
    def readAssocs(self,handle):
        assocListDone = False
        while (not assocListDone):
            line = handle.readline()
            self.numberAssocs += 1
            if (line[0]=='@'):
                assocListDone = True
            else:
                assoc = line.strip()
                assocTuple = assoc.split(" ")
                #base = assocTuple[0]
                #relationship = assocTuple[1]
                #property = assocTuple[2]
                self.assocs = self.assocs + [assocTuple]

    #---top level functions
    def createAssocViaRead(self,fileName):
        fileHandle = open(fileName, 'r')
        self.readAssocs(fileHandle)
        fileHandle.close()

    def readAssocFile(self,fileName):
        inputFileName = fileName+".txt"
        self.createAssocViaRead(inputFileName)
