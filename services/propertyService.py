from models.property import Property
from services.unitService import UnitService

class PropertyService(UnitService):
    def __init__(self, fsa, propertiesFile):
        super(PropertyService, self).__init__(fsa, propertiesFile)
        self.__properties = {}

    def fromUnit(self, unit):
        property = None

        if(unit in self.__properties):
            property = self.__properties[unit]
        else:
            propNum = self._structure.getUnitNumber(unit)
            property = Property(propNum)
            self.__properties[unit] = property

        return property