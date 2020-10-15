#!/usr/bin/env python
import scramblelib
import sys
import psyco

def scrambleFile(fname):
    #scramblelib.scrambleFile(fname,1)
    #scramblelib._scrambleFile(fname,1)
    scramblelib.__scrambleFile(fname,1)

if (__name__ == '__main__'):
    psyco.bind(scrambleFile)
    #psyco.full()
    #psyco.log()
    #psyco.profile()
    if ( (len(sys.argv) == 1) or (sys.argv[1] == '--help') ):
        print '--help ... displays this help text'
        print '--profile to use the profiler'
        print '--input=some_file_name'
    elif (sys.argv[1].find('--profile') > -1):
        import cProfile
        cProfile.run("scrambleFile('reports_production.sql')")
    elif (sys.argv[1].find('--input=') > -1):
        toks = sys.argv[1].split('=')
        if (len(toks) == 2):
            scrambleFile(toks[1])
    
    
