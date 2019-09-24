class ActivationsRepository:
    def __init__(self):
        self.__activations = []

    def add(self, ca):
        self.__activations.append(ca)

    def get(self):
        return list(self.__activations)