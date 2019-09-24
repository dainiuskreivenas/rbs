class FactGroupRepository:
    def __init__(self):
        self.groups = {}
    
    def groupExists(self, name):
        return name in self.groups

    def get(self, name = None):
        if(name == None):
            return self.groups.copy()

        if(name not in self.groups):
            return None

        return self.groups[name]

    def addOrGet(self, name):
        group = self.get(name)
        if(group == None):
            group = []
            self.groups[name] = group
        return group
