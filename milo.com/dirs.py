import os, sys
from vyperlogix.misc import _utils

if (__name__ == '__main__'):
    fpath = sys.argv[1] if (len(sys.argv) > 1) else None
    fpath_out = 'dirs.txt'
    if (os.path.exists(fpath)):
        _bias = os.path.dirname(fpath)
        import re
        svn_regex = re.compile('[._]svn')
        try:
            fout = open(fpath_out,'w')
            print >>fout, 'BEGIN:'
            for top,dirs,files in _utils.walk(fpath,rejecting_re=svn_regex):
                print >>fout, top.replace(_bias,'')
            print >>fout, 'END!'
        except Exception, ex:
            print >>sys.stderr, _utils.formattedException(details=ex)
        fout.flush()
        fout.close()
    pass
