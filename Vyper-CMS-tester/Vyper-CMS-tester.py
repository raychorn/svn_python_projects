import os, sys, re
import datetime
import random

from vyperlogix.products import keys

from vyperlogix import misc
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.misc import _utils

from vyperlogix.hash import lists

import logging

from vyperlogix.daemon.daemon import Log
from vyperlogix.daemon.daemon import CustomLog
from vyperlogix.logging import standardLogging

################################################################

from vyperlogix.classes import CooperativeClass

import urllib
import mechanize, urllib2
from vyperlogix.url import _urllib2

import BeautifulSoup

__copyright__ = """\
(c). Copyright 1990-2014, Vyper Logix Corp., All Rights Reserved.

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

class VyperCMS(CooperativeClass.Cooperative):
    def __init__(self):
	self._url = 'http://www.vyperlogix.com/'
	self.url = '%sauth/' % (self._url)
    
	self.browser = mechanize.Browser(
	    factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True)
	    )
	self.browser.set_handle_robots(False)
	#self.browser.add_password(self.url, username, password)

    def register(self):
	pass
    
from vyperlogix.classes.MagicObject import MagicObject2

class VyperCMSProxy(MagicObject2):
    '''
    This object holds onto a ZoneEdit object that interfaces with ZoneEdit.Com.
    '''
    def __init__(self,_proxy):
	self.__proxy__ = _proxy
	
    def proxy():
	doc = "proxy"
	def fget(self):
	    return self.__proxy__
	return locals()
    proxy = property(**proxy())
	
    def __call__(self,*args,**kwargs):
	s = 'self.proxy.%s(*args,**kwargs)' % (self.n.pop())
	try:
	    objects = eval(s)
	except Exception, details:
	    objects = None
	    info_string = _utils.formattedException(details=details)
	return objects if (objects is not None) else self

def main(logging,username,password,target):
    proxy = VyperCMSProxy(VyperCMS())
    proxy.firstname('Tom').lastname('Hanks').email_address('Tom.Hanks@vyperlogix.com').state('California').country('United States').register()

if (__name__ == '__main__'):
    from vyperlogix.misc import Args
    from vyperlogix.misc import PrettyPrint

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--cwd=?':'the path the program runs from, defaults to the path the program runs from.',
	    '--username=?':'Username for the PYPI Account',
	    '--password=?':'Password for the PYPI Account',
	    '--zone=?':'the target Zone name.',
	    '--logging=?':'[logging.INFO,logging.WARNING,logging.ERROR,logging.DEBUG]',
	    '--console_logging=?':'[logging.INFO,logging.WARNING,logging.ERROR,logging.DEBUG]'}
    _argsObj = Args.Args(args)

    _progName = _argsObj.programName
    _isVerbose = True
    try:
	if _argsObj.booleans.has_key('isVerbose'):
	    _isVerbose = _argsObj.booleans['isVerbose']
    except Exception, e:
	info_string = _utils.formattedException(details=e)
	logging.warning(info_string)
	_isVerbose = False
	
    _isHelp = False
    try:
	if _argsObj.booleans.has_key('isHelp'):
	    _isHelp = _argsObj.booleans['isHelp']
    except:
	pass
    
    if (_isHelp):
	ppArgs()

    try:
	_username = str(_argsObj.arguments['username']) if _argsObj.arguments.has_key('username') else _username
	username = _username
    except:
	username = _username
	
    try:
	_password = str(_argsObj.arguments['password']) if _argsObj.arguments.has_key('password') else _password
	password = _password
    except:
	password = _password
	
    __cwd__ = os.path.dirname(sys.argv[0])
    try:
	__cwd = _argsObj.arguments['cwd'] if _argsObj.arguments.has_key('cwd') else __cwd__
	if (len(__cwd) == 0) or (not os.path.exists(__cwd)):
	    if (os.environ.has_key('cwd')):
		__cwd = os.environ['cwd']
	__cwd__ = __cwd
    except:
	pass
    _cwd = __cwd__
    
    _zone = ''
    try:
	_zone = _argsObj.arguments['zone'] if _argsObj.arguments.has_key('zone') else ''
    except:
	pass
    
    _logging = logging.WARNING
    try:
	_logging = eval(_argsObj.arguments['logging']) if _argsObj.arguments.has_key('logging') else False
    except:
	_logging = logging.WARNING
	
    _console_logging = logging.WARNING
    try:
	_console_logging = eval(_argsObj.arguments['console_logging']) if _argsObj.arguments.has_key('console_logging') else False
    except:
	_console_logging = logging.WARNING

    name = _utils.getProgramName()
    fpath=_cwd
    _log_path = _utils.safely_mkdir_logs(fpath=fpath)
    _log_path = _utils.safely_mkdir(fpath=_log_path,dirname=_utils.timeStampLocalTimeForFileName(delimiters=('_'),format=_utils.formatDate_MMDDYYYY_dashes()))
    _data_path = _utils.safely_mkdir(fpath=fpath,dirname='dbx')

    logFileName = os.sep.join([_log_path,'%s.log' % (name)])

    print '(%s) :: logFileName=%s' % (_utils.timeStampLocalTime(),logFileName)

    _stdOut = open(os.sep.join([_log_path,'stdout.txt']),'w')
    _stdErr = open(os.sep.join([_log_path,'stderr.txt']),'w')
    _stdLogging = open(logFileName,'w')

    if (not _utils.isBeingDebugged):
	sys.stdout = Log(_stdOut)
	sys.stderr = Log(_stdErr)
    _logLogging = CustomLog(_stdLogging)

    standardLogging.standardLogging(logFileName,_level=_logging,console_level=_console_logging,isVerbose=_isVerbose)

    _logLogging.logging = logging # echos the log back to the standard logging...
    logging = _logLogging # replace the default logging with our own custom logging...

    main(logging,username,password,_zone)
