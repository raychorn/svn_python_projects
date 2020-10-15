import sys

s = 'Z:\python projects\@lib;Z:\python projects\_pyax-0.9.7.2-py2.5'
toks = s.split(';')
reversed(toks)
for t in toks:
    sys.path.insert(0,t)

from vyperlogix import misc
from vyperlogix.analysis import ioTimeAnalysis

def strstr(s,t):
    '''Returns a positive number if t is found in s.'''
    n = len(t)
    for i in xrange(0,len(s)-n):
        if (s[i:i+n] == t):
            return i
    return -1

def strstr_optimized(s,t):
    '''Returns a positive number if t is found in s.'''
    n = len(t)
    m = n
    for i in xrange(0,len(s)-n):
        if (s[i:m] == t):
            return i
        else:
            m += 1
    return -1

def strstr_split(s,t):
    '''Returns a positive number if t is found in s using split().'''
    toks = s.split(t)
    return len(toks[0]) if (toks[0] != s) else -1

def find1(args):
    s,t = args
    for i in xrange(0,1000000):
        i = s.find(t)

def strstr1(args):
    s,t = args
    for i in xrange(0,1000000):
        j = strstr(s,t)

def strstr1_optimized(args):
    s,t = args
    for i in xrange(0,1000000):
        j = strstr_optimized(s,t)

def strstr1_split(args):
    s,t = args
    for i in xrange(0,1000000):
        j = strstr_split(s,t)

def main():
    s = 'aaaaca'
    t = 'aac'
    i = s.find(t)
    print i
    j = strstr(s,t)
    print j
    j2 = strstr_optimized(s,t)
    print j2
    k = strstr_split(s,t)
    print k
    
    ioTimeAnalysis.runWithAnalysis(func=find1,args=[s,t])
    
    ioTimeAnalysis.runWithAnalysis(func=strstr1,args=[s,t])

    ioTimeAnalysis.runWithAnalysis(func=strstr1_optimized,args=[s,t])

    ioTimeAnalysis.runWithAnalysis(func=strstr1_split,args=[s,t])

if (__name__ == '__main__'):
    from vyperlogix.misc._psyco import *
    importPsycoIfPossible(func=main,isVerbose=True)
    
    main()
    