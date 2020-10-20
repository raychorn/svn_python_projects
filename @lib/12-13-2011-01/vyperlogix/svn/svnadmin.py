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

class SVNAdminShell(CooperativeClass.Cooperative):
    def __init__(self,callback=None,isDebugging=False,onExit=None,svnadmin=None,sysout=sys.stderr):
	self.__sysout__ = sysout
	self.__isDebugging__ = isDebugging
	self.__callback__ = callback
	self.__onExit__ = onExit
	self.__svnadmin__ = _utils.findUsingPath(r"@SVN_BINDIR@/svnadmin.exe") if ((not misc.isStringValid(svnadmin)) or (not os.path.exists(svnadmin)) or (not os.path.isfile(svnadmin))) else svnadmin
	self.__data__ = []

    def verify(self,top,callback=None):
	if (misc.isStringValid(self.__svnadmin__)) and (os.path.exists(self.__svnadmin__)):
	    from vyperlogix.os.shell import Shell
	    self.__data__ = []
	    if (self.__isDebugging__):
		print >> self.__sysout__, 'DEBUG: callback=%s' % (str(callback))
	    if (callable(callback)):
		self.__callback__ = callback
	    if (self.__isDebugging__):
		print >> self.__sysout__, 'DEBUG: self.__callback__=%s' % (str(self.__callback__))
	    def callback1(data):
		import re
		_re_ = re.compile(r"\*\s(?P<action>Verified)\srevision\s(?P<number>.*[0-9])\.")
		toks = str(data).split(os.linesep)
		matches = [(tt is not None) for tt in [_re_.match(t) for t in toks]]
		if (self.__isDebugging__):
		    print >> self.__sysout__, 'DEBUG: matches=%s' % (str(matches))
		if (any(matches)):
		    for match in matches:
			self.__data__.append(m.groupdict())
		    if (self.__isDebugging__):
			print >> self.__sysout__, 'DEBUG: self.__callback__=%s' % (str(self.__callback__))
		    if (callable(self.__callback__)):
			try:
			    self.__callback__(self)
			except Exception, ex:
			    info_string = _utils.formattedException(details=ex)
			    print >> self.__sysout__, info_string
	    def onExit():
		if (callable(self.__onExit__)):
		    try:
			self.__onExit__(self)
		    except Exception, ex:
			info_string = _utils.formattedException(details=ex)
			print >> self.__sysout__, info_string
	    if (misc.isStringValid(top)) and (os.path.exists(top)) and (os.path.isdir(top)):
		self.__command__ = '"%s" verify %s' % (self.__svnadmin__,top)
		if (self.__isDebugging__):
		    print >> self.__sysout__, 'DEBUG: %s' % (self.__command__)
		self.__shell__ = Shell(self.__command__,callback=callback1,isDebugging=False,isExit=True,isWait=False,onExit=onExit)
	    else:
		print >> self.__sysout__, 'ERROR: Missing (top) "%s" !!!' % (top)
	else:
	    print >> self.__sysout__, 'ERROR: Missing (svnadmin) "%s" !!!' % (self.__svnadmin__)

    def svnadmin():
        doc = "get the svnadmin executable fully qualified path."
        def fget(self):
            return self.__svnadmin__
        return locals()
    svnadmin = property(**svnadmin())

    def data():
        doc = "get the data."
        def fget(self):
            return self.__data__
        return locals()
    data = property(**data())

    def callback():
        doc = "set/get the calllback."
        def fget(self):
            return self.__callback__
        def fset(self,callback):
	    if (callable(callback)):
		self.__callback__ = callback
        return locals()
    callback = property(**callback())

################################################################################################

if (__name__ == "__main__"):
    def __callback__(s3):
	print 'BEGIN:'
	for f in s3.files:
	    print f
	print 'END !'
    s = S3Shell('__vyperlogix_svn_backups__','AKIAI52A6BTLWZHHDLCA','E6HT0b8BkiN71ey+iZZxMUhVTPqbHCCdNfhtfgIv',callback=__callback__,s3exe='J:/@Vyper Logix Corp/@Projects/python-projects/svnHotBackups/s3.exe')
    s.list()
    
    # s3 put __vyperlogix_svn_backups__/testing/ "J:/@Vyper Logix Corp/@Projects/python-projects/svnHotBackups/To-Do.txt" /key:AKIAI52A6BTLWZHHDLCA /secret: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 /nogui
    
    # s3 
