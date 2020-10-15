#!/usr/bin/env python
import scramblelib
import sys

def deScrambleFile(fname):
    scramblelib.scrambleFile(fname,0)

if ( (len(sys.argv) == 1) or (sys.argv[1] == '--help') ):
        print '--help ... displays this help text'
        print '--profile to use the profiler'
        print '--input=some_file_name'
elif (sys.argv[1].find('--profile') > -1):
    import cProfile
    cProfile.run("deScrambleFile('reports_production.sql.scrambled')")
elif (sys.argv[1].find('--input=') > -1):
    toks = splitToksFrom(sys.argv[1],'=')
    if (len(toks) == 2):
        deScrambleFile(toks[1])
    