from vyperlogix.profiling import profilehooks

@profilehooks.profile
def test1():
    foo = xrange(0,1000000)
    bar = [n**2 for n in foo]
    return bar

@profilehooks.profile
def test2():
    def pow(n):
        return n**2
    foo = xrange(0,1000000)
    bar = map(pow,foo)
    return bar

@profilehooks.profile
def test3():
    foo = xrange(0,1000000)
    bar = map(lambda pow:pow**2,foo)
    return bar

def main():
    print 'test1()'
    test1()
    
    print 'test2()'
    test2()
    
    print 'test3()'
    test3()

import lib._psyco
lib._psyco.importPsycoIfPossible(main)

main()
