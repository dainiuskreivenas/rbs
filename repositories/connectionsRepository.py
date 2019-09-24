class ConnectionsRepository:
    def __init__(self):
        self.__connections = []

    def add(self, connection):
        self.__connections.append(connection)

    def addRange(self, connections):
        self.__connections += connections

    def getConnections(self):
        return list(self.__connections)
