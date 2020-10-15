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
import os

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.process import Popen
from vyperlogix.hash.lists import HashedFuzzyLists2

from vyperlogix.classes import CooperativeClass

__header__ = 'Active Internet connections (only servers)'.split()

__LISTEN__ = 'LISTEN'
__State__ = 'State'
__LocalAddress__ = 'Local Address'
__port__ = 'port'

class NetStat(CooperativeClass.Cooperative):
    def __init__(self,isDebugging=False):
        self.__lines__ = []
	self.__listeners__ = []
	self.__ports__ = []
	self.has_header = False
	self.header = None
        self.__command__ = None
        self.__isDebugging__ = isDebugging if (misc.isBoolean(isDebugging)) else False
        if (_utils.isUsingWindows):
	    self.__command__ = 'netstat -a'
	    print 'DEBUG: %s' % (self.__command__)
	    self.__shell__(self.__command__)

	    #lines = _utils.read_lines_simple('J:/@Deployments/@@TEMPLATE@@/netstat.txt','r')
	    #for aLine in lines:
		#self.__callback__(aLine)
        else:
            self.__command__ = 'netstat -lnptu'
            print 'DEBUG: %s' % (self.__command__)
            self.__shell__(self.__command__)

    def __callback__(self,data):
        if (self.__isDebugging__):
            print '<<%s>>' % (data)
	lines = data.split(os.linesep)
	if (self.__isDebugging__):
	    print 'lines=%d\n%s' % (len(lines),'\n'.join(lines))
	for aLine in lines:
	    toks = aLine.split()
	    if (not self.has_header) and (toks == __header__):
		self.has_header = True
		continue
	    if (self.has_header):
		if (self.header is None):
		    if (_utils.isUsingWindows):
			patterns = ['Local'.lower(),'Foreign'.lower(),'State'.lower()]
		    else:
			patterns = ['Local'.lower(),'Foreign'.lower(),'PID/Program'.lower()]
		    for i in xrange(0,len(toks)):
			if (i < len(toks)) and (str(toks[i]).lower() in patterns):
			    toks[i] = ' '.join(toks[i:i+2])
			    del toks[i+1]
		    self.header = toks
		else:
		    d = {}
		    for i in xrange(0,len(toks)):
			d[self.header[i]] = toks[i]
		    if (d.has_key(__LocalAddress__)):
			d[__port__] = int(d[__LocalAddress__].split(':')[-1])
			self.__ports__.append(d[__port__])
			self.__ports__ = list(set(self.__ports__))
			misc.sort(self.__ports__)
		    self.__lines__.append(d)
		    if (d.has_key(__State__)) and (d[__State__] == __LISTEN__):
			self.__listeners__.append(d)
		pass
	    pass

    def __shell__(self,cmd,isExit=False,isWait=True,isVerbose=True):
        misc.removeAll(self.__lines__)
        _isExit=isExit
        _isWait=isWait
        if (self.__isDebugging__):
            print '%s.1 --> cmd=%s, isExit=%s, isWait=%s, isVerbose=%s' % (misc.funcName(),cmd,_isExit,_isWait,isVerbose)
        s = Popen.Shell(cmd, shell=None, env=None, isExit=_isExit, isWait=_isWait, isVerbose=isVerbose, fOut=self.__callback__)
        return

    def ports():
        doc = "get the ports with listeners."
        def fget(self):
            return self.__ports__
        return locals()
    ports = property(**ports())

    def lines():
        doc = "get the lines."
        def fget(self):
            return self.__lines__
        return locals()
    lines = property(**lines())

    def listeners():
        doc = "get the lines with listeners."
        def fget(self):
            return self.__listeners__
        return locals()
    listeners = property(**listeners())

################################################################################################

if (__name__ == "__main__"):
    n = NetStat(isDebugging=True)
    print 'The ports are\n\t%s' % ('\n\t'.join(n.ports))
    print 'The listeners are\n\t%s' % ('\n\t'.join(n.listeners))
    