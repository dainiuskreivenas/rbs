from ..lib import UnitReaderClass

class UnitService:
    def __init__(self, fsa, unitFile):
        self.__fsa = fsa
        self.__structure = UnitReaderClass()
        self.__structure.readUnitFile(unitFile)
    
    def test(self, prop, variables):
        unit = prop
        if(unit[0] == "?"):
            if(unit not in variables):
                return True
            else:
                unit = variables[prop]
        return self.__structure.inUnits(unit)

    def caFromUnit(self, unit):
        unit = self.__structure.getUnitNumber(unit)
        start = (unit * self.__fsa.CA_SIZE)
        return range(start, start + 10)

    def getStructure(self):
        return self.__structure