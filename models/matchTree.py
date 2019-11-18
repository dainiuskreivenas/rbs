#Find a group of facts that are valid for a rule. Hmm
class MatchTree:
    def __init__(self, variables, matches):
        self.variables = variables
        self.matches = matches
        self.label = ""
        indexes = []
        for i,m in enumerate(matches):
            indexes.append(m[0].caIndex)

        for i,m in enumerate(indexes):
            if(i == 0):
                self.label += "{}".format(m)
            else:
                self.label += "-{}".format(m)
