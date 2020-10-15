def phaseI(num=1):
    import sys
    
    d = {}
    print >>sys.stderr, 'Begin: Phase I'
    for i in xrange(num):
        d[i] = i
    return d
    