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

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.process import Popen
from vyperlogix.hash.lists import HashedFuzzyLists2

from vyperlogix.classes import CooperativeClass

class TraceRoute(CooperativeClass.Cooperative):
    def __init__(self,ip_or_domain,isDebugging=False):
        self.__ip__ = ip_or_domain
        self.__lines__ = []
        self.__command__ = None
        self.__isDebugging__ = isDebugging if (misc.isBoolean(isDebugging)) else False
        if (_utils.isUsingWindows):
            self.__command__ = 'tracert'
            _cmd_ = '%s %s' % (self.__command__,self.__ip__)
            print 'DEBUG: %s' % (_cmd_)
            self.__shell__(_cmd_)
        else:
            self.__command__ = 'traceroute'
            _cmd_ = '%s %s' % (self.__command__,self.__ip__)
            print 'DEBUG: %s' % (_cmd_)
            self.__shell__(_cmd_)

    def __callback__(self,data):
        if (self.__isDebugging__):
            print '<<%s>>' % (data)
        _data_ = str(data).strip()
        if (len(_data_) > 0):
            lines = _data_.split('\r\n')
            if (len(lines) == 1):
                lines = _data_.split('\n')
            if (self.__isDebugging__):
                print '{{%s}}' % (lines)
            for i in xrange(len(lines),0,-1):
                aLine = lines[i-1]
                toks = aLine.split()
                _cnt = 0
                for t in toks:
                    if (len(_utils.numerics_only(t)) > 0):
                        _cnt += 1
                if (_cnt >= 4):
                    self.__lines__.append(toks)
                    if (self.__isDebugging__):
                        print self.__lines__[-1]

    def __shell__(self,cmd,isExit=True,isWait=False,isVerbose=True):
        misc.removeAll(self.__lines__)
        _isExit=isExit
        _isWait=isWait
        if (self.__isDebugging__):
            print '%s.1 --> cmd=%s, isExit=%s, isWait=%s, isVerbose=%s' % (misc.funcName(),cmd,_isExit,_isWait,isVerbose)
        s = Popen.Shell(cmd, shell=None, env=None, isExit=_isExit, isWait=_isWait, isVerbose=isVerbose, fOut=self.__callback__)
        if (self.__isDebugging__):
            n = len(self.__lines__)
            print '%d hop%s' % (n,'s' if (n > 1) else '')
        return

    def hops():
        doc = "get the number of hops from the last traceroute command."
        def fget(self):
            return len(self.__lines__)
        return locals()
    hops = property(**hops())

################################################################################################

if (__name__ == "__main__"):
    if (_utils.isUsingLinux):
        __ip__ = 'google.com'
    else:
        __ip__ = 'rackspace.vyperlogix.com'

    t = TraceRoute(__ip__,isDebugging=True)
    print 'There %s %d hop%s.' % ('are' if (t.hops > 1) else 'is',t.hops,'s' if (t.hops > 1) else '')