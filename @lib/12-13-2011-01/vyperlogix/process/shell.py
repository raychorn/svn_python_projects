__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
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
from vyperlogix.http import downloadFileFromURL

from vyperlogix.classes import CooperativeClass

class SmartShell(CooperativeClass.Cooperative):
    def __init__(self,command=None,callback=None,isDebugging=False,onExit=None,sysout=sys.stderr):
	self.__sysout__ = sysout
	self.__isDebugging__ = isDebugging
	self.__command__ = command
	    
    def execute(self,command=None,callback=None,onExit=None,isExit=True,isWait=False):
	if (command):
	    self.__command__ = command

	try:
	    import subprocess
	    have_subprocess = 1
	except ImportError:
	    have_subprocess = 0

	if (self.__isDebugging__):
	    print >> self.__sysout__, 'DEBUG: %s' % (self.__command__)

	tp = _utils.tempFile('shell')
	if (not os.path.exists(tp)):
	    os.makedirs(tp)
	tf = '%s%sdoscommand.cmd' % (tp,os.sep)
	fOut = open(tf,'w')
	print >> fOut, '@echo off\n'
	print >> fOut, '%s' % (self.__command__)
	fOut.flush()
	fOut.close()
	
	if have_subprocess:
	    p = subprocess.Popen([tf],
		                 stdin=subprocess.PIPE,
		                 stdout=subprocess.PIPE,
		                 stderr=subprocess.PIPE)
	    infile, outfile, errfile = p.stdin, p.stdout, p.stderr
	else:
	    infile, outfile, errfile = os.popen3(tf)
    
	stdout_lines = outfile.readlines()
	stderr_lines = errfile.readlines()
	outfile.close()
	infile.close()
	errfile.close()
	
	print >> self.__sysout__, ''.join(stdout_lines+stderr_lines)

    def command():
        doc = "get the command."
        def fget(self):
            return self.__command__
        def fset(self,command):
	    self.__command__ = command
        return locals()
    command = property(**command())

    def sysout():
        doc = "get the sysout."
        def fget(self):
            return self.__sysout__
        def fset(self,sysout):
	    self.__sysout__ = sysout
        return locals()
    sysout = property(**sysout())

    def callback():
        doc = "set/get the calllback."
        def fget(self):
            return None
        def fset(self,callback):
	    if (callable(callback)):
		pass
        return locals()
    callback = property(**callback())

    def isDebugging():
        doc = "get the isDebugging."
        def fget(self):
            return self.__isDebugging__
        def fset(self,isDebugging):
	    self.__isDebugging__ = isDebugging if (isDebugging) else False
        return locals()
    isDebugging = property(**isDebugging())

    def onExit():
        doc = "get the onExit."
        def fget(self):
            return None
        def fset(self,onExit):
	    if (callable(onExit)):
		pass
        return locals()
    onExit = property(**onExit())

################################################################################################

if (__name__ == "__main__"):
    def __callback__(ss,data=None):
	if (data) and (misc.isString(data)) and (len(data) > 0):
	    print 'BEGIN:'
	    print 'data=%s' % (data)
	    print 'END !'
    def __onExit__(ss):
	print 'BEGIN:'
	print 'END !'
    ss = SmartShell('dir c:\\',callback=__callback__,isDebugging=True,onExit=__onExit__,sysout=sys.stdout)
    ss.execute()
