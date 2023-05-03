from ..lib.readUnitFile import UnitReaderClass

class UnitService(object):
    def __init__(self, fsa, unitFile):
        self.__fsa = fsa
        self._structure = UnitReaderClass()
        self._structure.readUnitFile(unitFile)
    
    def test(self, prop, variables):
        unit = prop
        if(unit[0] == "?"):
            if(unit not in variables):
                return True
            else:
                unit = variables[prop]
        return self._structure.inUnits(unit)

    def getStructure(self):
        return self._structure