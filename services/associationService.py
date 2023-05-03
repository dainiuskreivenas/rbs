import sys
import os
sys.path.append(os.getcwd() + '/..')
from rbs.lib.readAssocFile import AssocReaderClass

class AssociationService:
    def __init__(self, assocFile):
        self.__associations = AssocReaderClass()
        self.__associations.readAssocFile(assocFile)

    def getAssociations(self):
        return self.__associations