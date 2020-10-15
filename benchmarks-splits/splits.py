def mainBaseline1000():
    for i in xrange(1,1000):
        pass

def mainBaseline10000():
    for i in xrange(1,10000):
        pass

def mainBaseline100000():
    for i in xrange(1,100000):
        pass

def mainBaseline1000000():
    for i in xrange(1,1000000):
        pass

def main1000():
    for i in xrange(1,1000):
        toks = 'one two three four five six seven eight nine ten'.split()

def main2000():
    for i in xrange(1,1000):
        toks = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']

def main10000():
    for i in xrange(1,10000):
        toks = 'one two three four five six seven eight nine ten'.split()

def main20000():
    for i in xrange(1,10000):
        toks = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']

def main100000():
    for i in xrange(1,100000):
        toks = 'one two three four five six seven eight nine ten'.split()

def main200000():
    for i in xrange(1,100000):
        toks = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']

def main1000000():
    for i in xrange(1,1000000):
        toks = 'one two three four five six seven eight nine ten'.split()

def main2000000():
    for i in xrange(1,1000000):
        toks = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']

def lists1100():
    l = []
    for i in xrange(1,100):
        for x in xrange(100):
            l.append(x)

def lists2100():
    l = []
    for i in xrange(1,100):
        [l.append(x) for x in xrange(100)]

def lists11000():
    l = []
    for i in xrange(1,1000):
        for x in xrange(100):
            l.append(x)

def lists21000():
    l = []
    for i in xrange(1,1000):
        [l.append(x) for x in xrange(100)]

def lists110000():
    l = []
    for i in xrange(1,10000):
        for x in xrange(100):
            l.append(x)

def lists210000():
    l = []
    for i in xrange(1,10000):
        [l.append(x) for x in xrange(100)]

def lists1100000():
    l = []
    for i in xrange(1,100000):
        for x in xrange(100):
            l.append(x)

def lists2100000():
    l = []
    for i in xrange(1,100000):
        [l.append(x) for x in xrange(100)]

import hotshot, hotshot.stats
prof = hotshot.Profile("mainBaseline1000.prof")
prof.runcall(mainBaseline1000)
prof.close()
stats = hotshot.stats.load("mainBaseline1000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

import hotshot, hotshot.stats
prof = hotshot.Profile("mainBaseline10000.prof")
prof.runcall(mainBaseline10000)
prof.close()
stats = hotshot.stats.load("mainBaseline10000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

import hotshot, hotshot.stats
prof = hotshot.Profile("mainBaseline100000.prof")
prof.runcall(mainBaseline100000)
prof.close()
stats = hotshot.stats.load("mainBaseline100000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

import hotshot, hotshot.stats
prof = hotshot.Profile("mainBaseline1000000.prof")
prof.runcall(mainBaseline1000000)
prof.close()
stats = hotshot.stats.load("mainBaseline1000000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

import hotshot, hotshot.stats
prof = hotshot.Profile("main1000.prof")
prof.runcall(main1000)
prof.close()
stats = hotshot.stats.load("main1000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

prof = hotshot.Profile("main2000.prof")
prof.runcall(main2000)
prof.close()
stats = hotshot.stats.load("main2000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

import hotshot, hotshot.stats
prof = hotshot.Profile("main10000.prof")
prof.runcall(main10000)
prof.close()
stats = hotshot.stats.load("main10000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

prof = hotshot.Profile("main20000.prof")
prof.runcall(main20000)
prof.close()
stats = hotshot.stats.load("main20000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

import hotshot, hotshot.stats
prof = hotshot.Profile("main100000.prof")
prof.runcall(main100000)
prof.close()
stats = hotshot.stats.load("main100000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

prof = hotshot.Profile("main200000.prof")
prof.runcall(main200000)
prof.close()
stats = hotshot.stats.load("main200000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

import hotshot, hotshot.stats
prof = hotshot.Profile("main1000000.prof")
prof.runcall(main1000000)
prof.close()
stats = hotshot.stats.load("main1000000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

prof = hotshot.Profile("main2000000.prof")
prof.runcall(main2000000)
prof.close()
stats = hotshot.stats.load("main2000000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

prof = hotshot.Profile("lists1100.prof")
prof.runcall(lists1100)
prof.close()
stats = hotshot.stats.load("lists1100.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

prof = hotshot.Profile("lists2100.prof")
prof.runcall(lists2100)
prof.close()
stats = hotshot.stats.load("lists2100.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

prof = hotshot.Profile("lists11000.prof")
prof.runcall(lists11000)
prof.close()
stats = hotshot.stats.load("lists11000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

prof = hotshot.Profile("lists21000.prof")
prof.runcall(lists21000)
prof.close()
stats = hotshot.stats.load("lists21000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

prof = hotshot.Profile("lists110000.prof")
prof.runcall(lists110000)
prof.close()
stats = hotshot.stats.load("lists110000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

prof = hotshot.Profile("lists210000.prof")
prof.runcall(lists210000)
prof.close()
stats = hotshot.stats.load("lists210000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

prof = hotshot.Profile("lists1100000.prof")
prof.runcall(lists1100000)
prof.close()
stats = hotshot.stats.load("lists1100000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

prof = hotshot.Profile("lists2100000.prof")
prof.runcall(lists2100000)
prof.close()
stats = hotshot.stats.load("lists2100000.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

print '='*40

