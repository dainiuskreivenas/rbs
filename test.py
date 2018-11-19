

import numpy as np
from operator import itemgetter
from itertools import groupby





def getSomething(x):
    return x * 5


def f3(l):
    nl = []
    for item in map(getSomething, l):
        nl.append(item)
    return nl


l = range(1,10)

print f3(l)



