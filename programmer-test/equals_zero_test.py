
__list__ = [1, 2, 3, 0, 4, 0, 0, -1, 1, -2, 2]

if (__name__ == '__main__'):
    results = []
    for i in xrange(0, len(__list__)-1):
        val = __list__[i] + __list__[i+1]
        if (val == 0):
            print 'PASSES: %s and %s == %s' % (__list__[i], __list__[i+1], val)
            results.append(tuple([__list__[i], __list__[i+1]]))
        else:
            print 'FAILS:  %s and %s == %s' % (__list__[i], __list__[i+1], val)
    print results
