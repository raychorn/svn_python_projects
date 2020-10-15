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
import os,sys

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.process import Popen
from vyperlogix.hash.lists import HashedFuzzyLists2

from vyperlogix.classes import CooperativeClass

class Symlink(CooperativeClass.Cooperative):
    def __init__(self,srce,folder,alias,isDebugging=False):
        self.__srce__ = srce
        self.__alias__ = alias
        self.__folder__ = folder
        self.__isDebugging__ = isDebugging if (misc.isBoolean(isDebugging)) else False
        if (_utils.isUsingLinux) or (_utils.isUsingMacOSX):
            self.__command__ = 'ln -s %s %s'
            _cmd_ = self.__command__ % (self.__srce__,os.sep.join([self.__folder__,self.__alias__]))
            print 'DEBUG: %s' % (_cmd_)
            self.__shell__(_cmd_)
        elif (_utils.isUsingWindows):
            import win32file
            win32file.CreateSymbolicLink(self.__srce__,os.sep.join([self.__folder__,self.__alias__]),1)
            
    def __callback__(self,data):
        if (self.__isDebugging__):
            print '<<%s>>' % (data)

    def __shell__(self,cmd,isExit=True,isWait=False,isVerbose=True):
        _isExit=isExit
        _isWait=isWait
        if (self.__isDebugging__):
            print '%s.1 --> cmd=%s, isExit=%s, isWait=%s, isVerbose=%s' % (misc.funcName(),cmd,_isExit,_isWait,isVerbose)
        s = Popen.Shell(cmd, shell=None, env=None, isExit=_isExit, isWait=_isWait, isVerbose=isVerbose, fOut=self.__callback__)
        return

    def srce():
        doc = "get the source."
        def fget(self):
            return len(self.__srce__)
        return locals()
    srce = property(**srce())

    def alias():
        doc = "get the alias."
        def fget(self):
            return len(self.__alias__)
        return locals()
    alias = property(**alias())

    def folder():
        doc = "get the folder."
        def fget(self):
            return len(self.__folder__)
        return locals()
    folder = property(**folder())

################################################################################################

if (__name__ == "__main__"):
    if (_utils.isUsingLinux):
        __ip__ = 'google.com'
    else:
        __ip__ = 'rackspace.vyperlogix.com'

    t = TraceRoute(__ip__,isDebugging=True)
    print 'There %s %d hop%s.' % ('are' if (t.hops > 1) else 'is',t.hops,'s' if (t.hops > 1) else '')