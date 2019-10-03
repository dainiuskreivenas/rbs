class RulesRepository:
    def __init__(self):
        self.rules = {}

    def addRule(self, rule):
        self.rules[rule.name] = rule

    def get(self):
        return self.rules.copy()