import os,sys
from vyperlogix.misc.ObjectTypeName import typeClassName

__introspect__ = lambda o:['%s --> %s'%(a,type(o.__getattribute__(a))) for a in dir(o)]

__describe__ = lambda something,delim:'%s --> %s' % (typeClassName(something),delim.join(__introspect__(something)))

def introspect(something,fout=sys.stderr,delim='\n'):
    print >> fout, '='*40
    print >> fout, 'BEGIN: %s' % (something)
    print >> fout, '-'*40
    print >> fout, __describe__(something,delim)
    print >> fout, '-'*40
    try:
        for item in something:
            if (item):
                print >> fout, '%s --> %s' % (item,__describe__(something,delim))
    except:
        pass
    print >> fout, 'END!!!'
    print >> fout, '='*40

