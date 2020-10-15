from vyperlogix import oodb
import os, sys
from vyperlogix.misc import _psyco

def main():
    print >>sys.stderr, __file__

    import phaseI
    d = phaseI.phaseI(100)
        
    import phaseII
    d = phaseII.phaseII(d)
        
    def open_dbx(fname):
        dbx = oodb.PickledFastHash2(fname,method=oodb.PickleMethods.useCerealizer)
        return dbx
    
    def close_dbx(dbx):
        dbx.sync()
        dbx.close()
    
    import phaseIII
    fname = phaseIII.phaseIII(d,open_dbx,close_dbx)

    _msg = '%s' % os.lstat(fname)
    print >>sys.stdout, _msg
    print >>sys.stderr, _msg
        
    dbx = open_dbx(fname)
    for k,v in dbx.iteritems():
        #print >>sys.stderr, '%s=%s' % (k,v)
        pass
    close_dbx(dbx)

    pass

if (__name__ == '__main__'):
    _psyco.importPsycoIfPossible(func=main)
    
    main()
