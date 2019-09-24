class VariableHelper:      
    @staticmethod
    def extractVariables(var, found, precon):
        for i,prop in enumerate(precon):
            if(isinstance(prop, str) and len(prop) > 1 and prop[0] == "?" and prop not in var):
                var[prop] = found.attributes[i]
        return var

    @staticmethod
    def extractValue(item, match):
        if(isinstance(item, tuple)):
            c = item[0]
            left = item[1]
            right = item[2]
            if(isinstance(left, str) and left[0] == "?"):
                left = match[left]
            
            if(isinstance(right, str) and right[0] == "?"):
                right = match[right]

            if(c == "+"):
                value = left + right
            elif(c == "-"):
                value = left - right
            elif(c == "*"):
                value = left * right
            elif(c == "/"):
                value = left / right
        else:
            if(isinstance(item, str) and item[0] == "?"):
                if(item in match):
                    value = match[item]
                else:
                    value = None
            else:
                value = item
        
        return value

    @staticmethod
    def testVariables(item, var):
        op = item[1]
        left = VariableHelper.extractValue(item[2], var)
        right = VariableHelper.extractValue(item[3], var)

        if(left == None):
            return True
        if(right == None):
            return True

        if(op == ">"):
            return left > right
        elif(op == "<"):
            return left < right
        elif(op == "=" or op == "=="):
            return left == right
        elif(op == "<>" or op == "!="):
            return left != right
        else:
            return False