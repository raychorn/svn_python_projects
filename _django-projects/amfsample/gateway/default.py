import os,sys

from vyperlogix import misc
from vyperlogix.misc import _utils

def default(request,*args):
    from datetime import datetime
    dname = os.path.dirname(__file__)
    while (dname.split(os.sep)[-1] != 'django'):
        dname = os.path.dirname(dname)
    fname = os.path.join(dname,'amf_log_%s.txt' % (_utils.timeStampForFileName()))
    fOut = open(fname,mode='a')
    try:
        for anArg in args:
            print >>fOut, '%s :: anArg=%s' % (misc.funcName(),str(anArg))
    finally:
        fOut.flush()
        fOut.close()
    return datetime.now()
