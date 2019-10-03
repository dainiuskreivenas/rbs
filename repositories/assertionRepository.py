from ..helpers import LabelHelper

class AssertionRepository:
    def __init__(self, neuronRepository):
        self.__neuronRepository = neuronRepository
        self.__assertions = {}

    def createAssertion(self, match, rule):
        label = LabelHelper.generateRuleLabel(rule, match)

        if(label in self.__assertions):
            return None

        rulePop = self.__neuronRepository.addNeuron()
        self.__assertions[label] = rulePop

        return rulePop

    def get(self):
        return self.__assertions.copy()