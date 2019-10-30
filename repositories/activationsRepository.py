class ActivationsRepository:
    def __init__(self):
        self.__activations = []

    def add(self, caIndex):
        self.__activations.append(caIndex)

    def get(self):
        return list(self.__activations)