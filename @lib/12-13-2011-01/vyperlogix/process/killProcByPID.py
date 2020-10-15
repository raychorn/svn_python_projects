__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

import os, sys
from vyperlogix import misc

def killProcByPID(pid,isVerbose=False):
    info_string = ''
    if (isVerbose):
        print >>sys.stderr, '(%s) :: sys.platform is "%s".' % (misc.funcName(),sys.platform)
    if (sys.platform == 'win32'):
        def kill(pid):
            info_string = ''
            from vyperlogix.win import WinProcesses
            p = WinProcesses.WinProcesses()
            proc_handle = p.openProcessTerminateForPID(pid)
            if (isVerbose):
                print >>sys.stderr, '(%s) :: proc_handle is "%s".' % (misc.funcName(),proc_handle)
            if (proc_handle):
                try:
                    import win32api
                    win32api.TerminateProcess(proc_handle, -1)
                except Exception, details:
                    from vyperlogix.misc import _utils
                    info_string += _utils.formattedException(details=details)
                    try:
                        import ctypes
                        ctypes.windll.kernel32.TerminateProcess(proc_handle, -1)
                    except Exception, details:
                        from vyperlogix.misc import _utils
                        info_string += _utils.formattedException(details=details)
                        print >>sys.stderr, 'ERROR: Cannot Kill the process with pid of %s due to a system error.' % (pid)
                        print >>sys.stderr, info_string
                finally:
                    p.closeProcessHandle(proc_handle)
        if (isVerbose):
            print >>sys.stderr, '(%s) :: kill(%d).' % (misc.funcName(),pid)
        kill(pid)
    else:
        try:
            os.kill(pid)
        except Exception, details:
            from vyperlogix.misc import _utils
            info_string += _utils.formattedException(details=details)
            print >>sys.stderr, 'ERROR: Cannot kill the process !'
            print >>sys.stderr, info_string
    if (isVerbose):
        print >>sys.stderr, '(%s) :: info_string is "%s".' % (misc.funcName(),info_string)

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
