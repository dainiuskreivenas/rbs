from ..helpers import LabelHelper
from ..models import Assertion

class AssertionRepository:
    def __init__(self, neuronRepository):
        self.__neuronRepository = neuronRepository
        self.__assertions = {}

    def createAssertion(self, match, rule):
        label = LabelHelper.generateRuleLabel(rule, match)

        if(label in self.__assertions):
            return None

        neuronIndex = self.__neuronRepository.addNeuron()
        self.__assertions[label] = Assertion(neuronIndex)

        return self.__assertions[label]

    def get(self):
        return self.__assertions.copy()