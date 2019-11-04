class InternRepository:
    def __init__(self):
        self.__interns = []

    def add(self, intern):
        self.__interns.append(intern)

    def get(self):
        return list(self.__interns)