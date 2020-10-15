import os, sys

from vyperlogix.misc import _utils

from vyperlogix.process import Popen

__winscp__ = 'WinSCP'

__program_files__ = [os.sep.join([_utils.GetProgramFiles32(), __winscp__]), _utils.GetProgramFiles32()]

if (_utils.is_x64):
    __program_files__.append(os.sep.join([_utils.GetProgramFiles64(), __winscp__]))
    __program_files__.append(_utils.GetProgramFiles64())

__winSCP__ = '"%s" "root@amazon-svn.vyperlogix.com"'

__commands__ = {}
__commands__[__winSCP__] = "Active session: [1] root@amazon-svn.vyperlogix.com"

def find_winscp():
    global __winSCP__
    for p in __program_files__:
        for top, dirs, files in _utils.walk(p, topdown=True, onerror=None, rejecting_re=None):
            if (top.lower().find(__winscp__.lower()) > -1):
                for f in files:
                    if (f.lower().find(__winscp__.lower()) > -1) and (os.path.splitext(f)[-1].lower() == '.com'):
                        _v_ = __commands__[__winSCP__]
                        del __commands__[__winSCP__]
                        __winSCP__ = __winSCP__ % (os.sep.join([top, f]))
                        __commands__[__winSCP__] = _v_
                        return 

if (__name__ == '__main__'):
    find_winscp()
    s = None
    for k,v in __commands__.iteritems():
        fOut = _utils.stringIO()
        if (s is None):
            s = Popen.Shell([k], shell=None, env=None, isExit=False, isWait=False, isVerbose=False, fOut=fOut)
        print fOut.getvalue()
        pass
    s.doSendWithTail('exit')
