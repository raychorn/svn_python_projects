import os, sys
from vyperlogix.misc import _psyco
from shove import Shove

if (__name__ == '__main__'):
    _psyco.importPsycoIfPossible()
    
    print >>sys.stderr, __file__

    import phaseI
    d = phaseI.phaseI()
        
    import phaseII
    d = phaseII.phaseII(d)
        
    def open_dbx(fname):
        return Shove('bsddb://' + fname, compressed=True)
    
    def close_dbx(dbx):
        dbx.close()
    
    import phaseIII
    fname = phaseIII.phaseIII(d,open_dbx,close_dbx)

    _msg = '%s' % os.lstat(fname)
    print >>sys.stdout, _msg
    print >>sys.stderr, _msg
        
    dbx = open_dbx(fname)
    for k,v in dbx.iteritems():
        print '%s, %s' % (k,v[-1]['dt'])
    close_dbx(dbx)

    pass

