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
        return Shove('memory://', compressed=True)
    
    def close_dbx(dbx):
        try:
            dbx.close()
        except:
            pass
    
    import phaseIII
    fname = phaseIII.phaseIII(d,open_dbx,close_dbx)

    if (os.path.exists(fname)):
        _msg = '%s' % os.lstat(fname)
        print >>sys.stdout, _msg
        print >>sys.stderr, _msg
        
    dbx = open_dbx(fname)
    try:
        for k,v in dbx.iteritems():
            print '%s, %s' % (k,v[-1]['dt'])
    except:
        print >>sys.stderr, 'ERROR: Cannot iterate over the items in the dbx.'
    close_dbx(dbx)

    pass

