# Maxime Biais <http://www.biais.org/blog>

import hotshot, hotshot.stats
 
def profileit(printlines=1):
    def _my(func):
        def _func(*args, **kargs):
            prof = hotshot.Profile("profiling.data")
            res = prof.runcall(func, *args, **kargs)
            prof.close()
            stats = hotshot.stats.load("profiling.data")
            stats.strip_dirs()
            stats.sort_stats('time', 'calls')
            print ">>>---- Begin profiling print"
            stats.print_stats(printlines)
            print ">>>---- End profiling print"
            return res
        return _func
    return _my

if __name__ == '__main__':
    from random import random
    def mip():
        return random()
    @profileit(20)
    def mop():
        a = 0
        for i in xrange(1000):
            a += mip()
        return a
    print mop()
