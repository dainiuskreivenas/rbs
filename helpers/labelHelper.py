from variableHelper import VariableHelper

class LabelHelper:
    @staticmethod
    def generateRuleLabel(rule, match):
        variables = match.variables

        label = getIndexLabel(match.matches)
        
        assertion = addAssertions("", variables, rule.assertions)
        assertion = addBaseAssertions(assertion, variables, rule.baseAssertions)
        assertion = addPrimeAssertions(assertion, variables, rule.primeAssertions)
        assertion = addLinkAssertions(assertion, variables, rule.linkAssertions)

        retratction = getRetractionsLabel(rule, match)

        return "{}{}{}".format(label, assertion, retratction)

def getIndexLabel(matches):
    indexes = []
    for m in matches:
        indexes.append(m[0].index)
    indexes.sort()

    label = ""
    for i,m in enumerate(indexes):
        if(i == 0):
            label = "{}".format(m)
        else:
            label += "{} and {}".format(label, m)
            
    return label

def getRetractionsLabel(rule, match):
    retractions = rule.retractions
    bases = rule.bases
    primes = rule.primes
    links = rule.links

    variables = match.variables

    if(len(retractions) == 0):
        return ""

    text = " <= "

    for i,a in enumerate(retractions):
        lbl = getLabelFromMatches(match.matches, a)


        if(lbl == None):
            for b in bases:
                if(b[2] == a):
                    val = b[1]
                    if(val[0] == "?"):
                        val = variables[val]
                    lbl = "({}, {})".format(b[0], val)
                    break
        if(lbl == None):
            for p in primes:
                if(p[2] == a):
                    lbl = "({}, {})".format(p[0], p[1])
                    break
                
        if(lbl == None):
            for l in links:
                if(l[2] == a):
                    
                    val = l[1]
                    if(val[1][0] == "?"):
                        val = (val[0], variables[val[1]], val[2])
                    lbl = "({}, {})".format(l[0], val)
                    break

        if(i == 0):
            text += lbl
        else:
            text += " and {}".format(lbl)
    
    return text

def getLabelFromMatches(matches, retraction):
    lbl = None
    for m in matches:
        if m[1] == retraction:
            lbl = "({}, {})".format(m[0].group, m[0].attributes)
            break
    return lbl

def addLinkAssertions(text, variables, linkAssertions):
    if(len(linkAssertions) == 0):
        return text

    text = appendNextAssertion(text)

    textAdded = False
    for l in linkAssertions:
        val = l
        if(val[1][0] == "?"):
            val = (val[0], variables[val[1]],val[2])
        lbl = "(link, {})".format(val)
        if(textAdded):
            text += " and {}".format(lbl)
        else:
            text += lbl
            textAdded = True

    return text

def addPrimeAssertions(text, variables, primeAssertions):
    if(len(primeAssertions) == 0):
        return text

    text = appendNextAssertion(text)

    textAdded = False
    for p in primeAssertions:
        lbl = "{}".format(("prime", p))

        if(textAdded):
            text += " and {}".format(lbl)
        else:
            text += lbl
            textAdded = True

    return text

def addBaseAssertions(text, variables, baseAssertions):
    if(len(baseAssertions) == 0):
        return text
    
    text = appendNextAssertion(text)

    textAdded = False
    for a in baseAssertions:
        val = a
        if(val[0] == "?"):
            val = variables[a]               
        lbl = "{}".format(("base", val))

        if(textAdded):
            text += " and {}".format(lbl)
        else:
            text += lbl
            textAdded = True
    
    return text
        
def addAssertions(text, variables, assertions):
    if(len(assertions) == 0):
        return text
    
    text = appendNextAssertion(text)

    textAdded = False
    for assertion in assertions:
        label = getLabelFromAssertion(variables, assertion)

        if(textAdded):
            text += " and {}".format(label)
        else:
            text += label
            textAdded = True

    return text

def getLabelFromAssertion(variables, assertion):
    properties = assertion[1]
    newProps = []
    for p in properties:
        prop = VariableHelper.extractValue(p, variables)
        newProps.append(prop)
    text = "{}".format((assertion[0],tuple(newProps)))
    return text

def appendNextAssertion(text):
    if(text == ""):
        text += " => "
    else:
        text += " and "
    
    return text
