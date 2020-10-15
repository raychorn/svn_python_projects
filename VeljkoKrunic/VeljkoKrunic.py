#List 1: a, b, c
#List 2: a, d

#If Union return a,b, c, d
#If Intersection return a
def __sort__(l):
    l = list(l)
    l.sort()
    return l

dummy = lambda x:list(x)

def func1_union(a,b,func=dummy):
    sA = set(a)
    sB = set(b)
    return func(sA.union(sB))

def func1_intersection(a,b,func=dummy):
    sA = set(a)
    sB = set(b)
    return func(sA.intersection(sB))

def __func1_union__(a,b,func=dummy):
    result = {}
    for aa in a:
        result[aa] = aa
    for bb in b:
        result[bb] = bb
    return func(result.keys())

def __func1_intersection__(a,b,func=dummy):
    result = {}
    foo = {}
    for aa in a:
        foo[aa] = aa
    for bb in b:
        if (foo.has_key(bb)):
            result[bb] = bb
    return func(result.keys())

if (__name__ == '__main__'):
    a = ['a', 'b', 'c']
    b = ['a', 'd']
    cU = func1_union(a,b)
    cI = func1_intersection(a,b)
    print cU
    print cI
    cU = func1_union(a,b,func=__sort__)
    cI = func1_intersection(a,b,func=__sort__)
    print cU
    print cI
    print '='*40
    cU = __func1_union__(a,b)
    cI = __func1_intersection__(a,b)
    print cU
    print cI
    cU = __func1_union__(a,b,func=__sort__)
    cI = __func1_intersection__(a,b,func=__sort__)
    print cU
    print cI
