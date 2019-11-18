"""
Connection holds reference to the source object (Fact, Assertion, Intern, Base, Link, Prime, Property, Relationship)
and the target object, also the connectionType (TurnOn, TurnOff, HalfTurnOn, HalfTurnOff) between them.
"""
class Connection:
    def __init__(self, source, target, connectionType):
        self.source = source
        self.target = target
        self.connectionType = connectionType