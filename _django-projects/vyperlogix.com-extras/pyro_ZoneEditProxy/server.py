__copyright__ = """\
(c). Copyright 1990-2020, Vyper Logix Corp., 

              All Rights Reserved.

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

__version__ = '''4.1.0'''

import os, sys
import time

import Pyro.naming
import Pyro.core
from Pyro import config as Pyro_config
from Pyro.errors import PyroError,NamingError

from vyperlogix.crypto import Encryptors

from vyperlogix.zones.dns import ZoneEdit
from vyperlogix.zones.dns import ZoneEditProxy

from vyperlogix.hash import lists
from vyperlogix.misc import _utils

from vyperlogix.misc import ObjectTypeName

from vyperlogix.daemon.daemon import EchoLog

from vyperlogix.django import django_utils

from vyperlogix.misc import threadpool

_logging_Q_ = threadpool.ThreadQueue(100)

_isRunningLocal = (_utils.isBeingDebugged) or (django_utils._cname in ['undefined3','ubuntu4.web20082'])

from config import ACCEPTED_ID

isZoneProxy = lambda obj:(ObjectTypeName.typeClassName(obj).find('.ZoneProxy') > -1)

from vyperlogix.decorators.synchronized import synchronized
from threading import Lock
myLock = Lock()

class ZoneEditProxy(Pyro.core.ObjBase):
    '''
    the sfdc cannot be returned to the caller because it cannot be pickled.
    '''
    def __init__(self, isLogging=True):
	self.__isLogging__ = isLogging
	self.__zo__ = None
        Pyro.core.ObjBase.__init__(self)
        
    def isLogging():
        doc = "isLogging"
        def fget(self):
            return self.__isLogging__
        return locals()
    isLogging = property(**isLogging())
    
    def zones(self):
	pass

    def login(self,username,password):
	pass

def main(host):
    _root_ = os.path.dirname(os.path.abspath(os.sep.join(['.',sys.argv[0]])) if (os.path.dirname(sys.argv[0]) == '') else sys.argv[0])
    
    LOGFILE = os.sep.join([_root_,'logs','pyro_server_%s.log' % (_utils.timeStampLocalTimeForFileName())])
    _utils.makeDirs(LOGFILE)
    
    print >>sys.stderr, 'LOGFILE is "%s".' % (LOGFILE)

    sys.stdout = EchoLog(open(LOGFILE,'a'),fOut=sys.stderr)
    
    if (_isVerbose):
	print 'sys.stdout=%s' % (str(sys.stdout))    
    
    Pyro_config.PYRO_COMPRESSION = 1
    Pyro_config.PYRO_CHECKSUM = 1
    Pyro_config.PYRO_SOCK_KEEPALIVE = 1
    Pyro_config.PYRO_MAXCONNECTIONS = Pyro_config.PYRO_TCP_LISTEN_BACKLOG = 1024
    Pyro_config.PYRO_MULTITHREADED = 1
    
    # initialize the server
    Pyro.core.initServer()
    
    ident = ACCEPTED_ID(__version__)
    
    # locate the NS
    print 'Searching Naming Service...'
    locator = Pyro.naming.NameServerLocator(identification=ident)
    try:
	ns_URI = locator.detectNS(host=host.split(':')[0],port=int(host.split(':')[-1]),trace=1)
	print 'Found Name Server at "%s".' % (ns_URI)
    except Exception, e:
	info_string = _utils.formattedException(details=e)
	print info_string
	sys.exit(1)
    try:
	ns = locator.getNS(host=host.split(':')[0],port=int(host.split(':')[-1]),trace=1)
    except Exception, e:
	info_string = _utils.formattedException(details=e)
	print info_string
	sys.exit(1)
    
    try:
	ns.createGroup(":ZoneEditProxy")
    except NamingError:
	pass
    
    daemon = Pyro.core.Daemon()
    daemon.useNameServer(ns)
    daemon.hostname = '0.0.0.0'
    daemon.setAllowedIdentifications([ident])
    
    # connect new instance, but using persistent mode
    daemon.connectPersistent(ZoneEditProxy(isLogging=_isLogging),':ZoneEditProxy.version_%s' % (__version__.replace('.','_')))
    
    # enter the service loop.
    print 'Server started.'
    daemon.requestLoop()

if (__name__ == '__main__'):
    from vyperlogix.misc import Args
    from vyperlogix.misc import PrettyPrint

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--host=?':'host:port for name server.',
	    '--nopsyco':'do not load Psyco when this option is used.',
	    '--production':'act as though we are running in a production mode without certain profiling actions.',
	    '--logging':'log certain actions in a log file.',
	    }
    _argsObj = Args.Args(args)
    _progName = _argsObj.programName

    _isVerbose = False
    try:
	if _argsObj.booleans.has_key('isVerbose'):
	    _isVerbose = _argsObj.booleans['isVerbose']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print >>sys.stderr, info_string
	_isVerbose = False
	    
    if (_isVerbose):
	print '_argsObj=(%s)' % str(_argsObj)

    _isHelp = False
    try:
	if _argsObj.booleans.has_key('isHelp'):
	    _isHelp = _argsObj.booleans['isHelp']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print >>sys.stderr, info_string
	_isHelp = False
	    
    _isNopsyco = False
    try:
	if _argsObj.booleans.has_key('isNopsyco'):
	    _isNopsyco = _argsObj.booleans['isNopsyco']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print >>sys.stderr, info_string
	_isNopsyco = False
	    
    _isProduction = False
    try:
	if _argsObj.booleans.has_key('isProduction'):
	    _isProduction = _argsObj.booleans['isProduction']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print >>sys.stderr, info_string
	_isProduction = False
	    
    _isLogging = False
    try:
	if _argsObj.booleans.has_key('isLogging'):
	    _isLogging = _argsObj.booleans['isLogging']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print >>sys.stderr, info_string
	_isLogging = False
	    
    _host = '127.0.0.1:8888'
    try:
	if _argsObj.arguments.has_key('host'):
	    _host = _argsObj.arguments['host']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print >>sys.stderr, info_string
	    
    if (_isHelp):
	ppArgs()
	
    if (not _isNopsyco):
	from vyperlogix.misc import _psyco
	_psyco.importPsycoIfPossible(func=main)
	
    if (_isProduction):
	_isRunningLocal = False
	
    main(_host)
