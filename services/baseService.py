import sys
import os
sys.path.append(os.getcwd() + '/..')
from rbs.lib.readInheritanceFile import InheritanceReaderClass
from rbs.models.base import Base

class BaseService:
    def __init__(self, fsa, basesFile):
        self.__fsa = fsa
        self.__inheritance = InheritanceReaderClass()
        self.__inheritance.readInheritanceFile(basesFile)
        self.__bases = {}

    def fromUnit(self, unit):
        base = None

        if(unit in self.__bases):
            base = self.__bases[unit]
        else:
            unitNumber = self.__inheritance.getUnitNumber(unit)
            base = Base(unitNumber)
            self.__bases[unit] = base
            
        return base

    def test(self, base, variables):
        unit = base
        if(unit[0] == "?"):
            if(unit not in variables):
                return True
            else:
                unit = variables[base]
        return self.__inheritance.inUnits(unit)

    def getInheritance(self):
        return self.__inheritance