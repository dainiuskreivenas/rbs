class ActivationsRepository:
    def __init__(self):
        self.__activations = []

    def add(self, pop):
        self.__activations.append(pop)

    def get(self):
        return list(self.__activations)