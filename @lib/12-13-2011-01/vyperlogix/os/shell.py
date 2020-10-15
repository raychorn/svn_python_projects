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

class Shell(CooperativeClass.Cooperative):
    def __init__(self,command,callback=None,isWait=False,isExit=True,isDebugging=False,onExit=None):
        self.__command__ = command
	self.__callback__ = callback
	self.__onExit__ = onExit
        self.__isDebugging__ = isDebugging if (misc.isBoolean(isDebugging)) else False
	print 'DEBUG: %s' % (self.__command__)
	self.__shell__(self.__command__,isWait=isWait,isExit=isExit)

    def __callback__(self,data):
        if (self.__isDebugging__):
            print '<<%s>>' % (data)
	if (callable(self.__callback__)):
	    try:
		self.__callback__(data)
	    except Exception, ex:
		info_string = _utils.formattedException(details=ex)
		print >> sys.stderr, info_string

    def __shell__(self,cmd,isExit=True,isWait=False,isVerbose=True):
	if (callable(self.__callback__)):
	    try:
		self.__callback__(None)
	    except Exception, ex:
		info_string = _utils.formattedException(details=ex)
		print >> sys.stderr, info_string
        _isExit=isExit
        _isWait=isWait
        if (self.__isDebugging__):
            print '%s.1 --> cmd=%s, isExit=%s, isWait=%s, isVerbose=%s' % (misc.funcName(),cmd,_isExit,_isWait,isVerbose)
        s = Popen.Shell(cmd, shell=None, env=None, isExit=_isExit, isWait=_isWait, isVerbose=isVerbose, fOut=self.__callback__, onExit=self.__onExit__)
        return

    def command():
        doc = "get the command."
        def fget(self):
            return self.__command__
        return locals()
    command = property(**command())

    def callback():
        doc = "get the callback."
        def fget(self):
            return self.__callback__
        return locals()
    callback = property(**callback())

################################################################################################

if (__name__ == "__main__"):
    s = Shell(isDebugging=True)
    print 'The command is "%s".' % (s.command)