from ..lib import InheritanceReaderClass

class BaseService:
    def __init__(self, fsa, basesFile):
        self.__fsa = fsa
        self.__inheritance = InheritanceReaderClass()
        self.__inheritance.readInheritanceFile(basesFile)

    def caFromUnit(self, unit):
        unit = self.__inheritance.getUnitNumber(unit)
        start = (unit * self.__fsa.CA_SIZE)
        return range(start, start + 10)

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