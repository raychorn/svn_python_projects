from vyperlogix.process import Popen

from vyperlogix import misc
from vyperlogix.misc import _utils

import os,sys

if (__name__ == '__main__'):
    gcc = _utils.findUsingPath(r"@PATH@/gcc (2).exe")
    if (misc.isStringValid(gcc)) and (os.path.exists(gcc)) and (gcc.lower().find('gcc.exe') == -1):
        args = [a for a in sys.argv[1:] if (str(a).lower().find('cygwin') == -1)]
        _cmd_ = '%s %s' % (gcc,' '.join(args))
        fOut = open(os.path.abspath('./gcc-report.txt'),'w+')
        print >>fOut, '%s' % (_cmd_)
        fOut.flush()
        fOut.close()
        Popen.Shell(_cmd_, shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=sys.stdout)
    else:
        print >> sys.stderr, 'WARNING: Cannot find gcc anywhere !!!'


