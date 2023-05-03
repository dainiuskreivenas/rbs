import sys
import os
sys.path.append(os.getcwd() + '/..')
from rbs.models.relationship import Relationship
from rbs.services.unitService import UnitService

class RelationshipService(UnitService):
    def __init__(self, fsa, relationshipsFile):
        super(RelationshipService, self).__init__(fsa, relationshipsFile)
        self.__relationships = {}

    def fromUnit(self, unit):
        relationship = None

        if(unit in self.__relationships):
            relationship = self.__relationships[unit]
        else:
            propNum = self._structure.getUnitNumber(unit)
            relationship = Relationship(propNum)
            self.__relationships[unit] = relationship
            
        return relationship
