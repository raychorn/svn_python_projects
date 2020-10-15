import os, sys
from vyperlogix.misc import _psyco
from shove.cache.db import DbCache

if (__name__ == '__main__'):
    _psyco.importPsycoIfPossible()
    
    print >>sys.stderr, __file__

    import phaseI
    d = phaseI.phaseI()
        
    import phaseII
    d = phaseII.phaseII(d)
        
    def open_dbx(fname):
        return DbCache('sqlite:///')
    
    def close_dbx(dbx):
        pass
    
    import phaseIII
    fname = phaseIII.phaseIII(d,open_dbx,close_dbx)

    #dbx = open_dbx(fname)
    #for k,v in dbx.iteritems():
        #print '%s, %s' % (k,v[-1]['dt'])
    #close_dbx(dbx)

    pass

