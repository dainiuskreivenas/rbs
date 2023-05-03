import sys
import os
sys.path.append(os.getcwd() + '/..')
from rbs.models.intern import Intern

class InternService:
    def __init__(self, neuronRepository, internRepository):
        self.__neuronRepository = neuronRepository
        self.__internRepository = internRepository

    def createIntern(self):
        neuronIndex = self.__neuronRepository.addNeuron()
        intern = Intern(neuronIndex)
        self.__internRepository.add(intern)
        return intern
