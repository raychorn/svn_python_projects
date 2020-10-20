__copyright__ = """\
(c). Copyright 1990-2020, Vyper Logix Corp., 

              All Rights Reserved.

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

__version__ = '''4.1.0'''

import os, sys
import time

import Pyro.naming
import Pyro.core
from Pyro import config as Pyro_config
from Pyro.errors import PyroError,NamingError

from vyperlogix.crypto import Encryptors

from vyperlogix.wx.pyax import SalesForceLoginModel
from vyperlogix.sf.sf import SalesForceQuery

from vyperlogix.sf.users import SalesForceUsers
from vyperlogix.sf.contacts import SalesForceContacts
from vyperlogix.sf.accounts import SalesForceAccounts
from vyperlogix.sf.record_types import SalesForceRecordTypes
from vyperlogix.sf.cases import SalesForceCases
from vyperlogix.sf.solutions import SalesForceSolutions
from vyperlogix.sf.attachments import SalesForceAttachments

from vyperlogix.sf.magma.molten_posts import SalesForceMoltenPosts

from vyperlogix.sf.accounts import MagmaAccountTree

from maglib.salesforce.auth import magma_molten_passphrase
from maglib.salesforce.auth import CredentialTypes
from maglib.salesforce.cred import credentials

from vyperlogix.classes.MagicObject import MagicObject2

from vyperlogix.hash import lists
from vyperlogix.misc import _utils

from vyperlogix.misc import ObjectTypeName

from vyperlogix.daemon.daemon import EchoLog

from vyperlogix.misc import threadpool

_logging_Q_ = threadpool.ThreadQueue(100)

_isRunningLocal = (_utils.isBeingDebugged) or (_utils.getComputerName().lower() in ['misha-lap.ad.magma-da.com','undefined3'])

from config import ACCEPTED_ID

isSalesForceObjectProxy = lambda obj:(ObjectTypeName.typeClassName(obj).find('.SalesForceObjectProxy') > -1)

class SalesForceObjectProxy(MagicObject2):
    '''
    This object holds onto a SalesForceAbstract subclass that returns objects as well as a cache (dict) that knows
    how to get SmartObject instances from each unique object Id that comes from SalesForce via pyax.
    
    The notion of an Object Cache may not be all that useful because some objects based on the type of SOQL should
    probably not be cached while others should.
    
    For now the object cache is not being used until a better use case scenario can be found where it makes sense to use it.
    '''
    def __init__(self,sf_proxy):
	self.__sf_proxy__ = sf_proxy
	self.__object_cache__ = lists.HashedLists2()
	
    def sf_proxy():
	doc = "sf_proxy"
	def fget(self):
	    return self.__sf_proxy__
	return locals()
    sf_proxy = property(**sf_proxy())
	
    def object_cache():
	doc = "object_cache"
	def fget(self):
	    return self.__object_cache__
	return locals()
    object_cache = property(**object_cache())
    
    def sf_proxy_do_cached(aMethod):
	pass
	
    def __call__(self,*args,**kwargs):
	s = 'self.sf_proxy.%s(*args,**kwargs)' % (self.n[0])
	try:
	    objects = eval(s)
	except Exception, details:
	    objects = None
	    info_string = _utils.formattedException(details=details)
	items = []
	if (objects is not None):
	    objects = objects if (isinstance(objects,list)) else list(objects) if (isinstance(objects,tuple)) else [objects]
	    for obj in objects:
		if (lists.isDict(obj)):
		    d = lists.HashedLists2(obj)
		    d['__className__'] = ObjectTypeName.typeClassName(obj)
		    items.append(d.asDict())
		else:
		    items.append(obj)
	return items
	
@threadpool.threadify(_logging_Q_)
def do_some_profiling(bt,et,spec,objects,fOut=sys.stdout):
    from vyperlogix.decorators.synchronized import synchronized
    from threading import Lock
    myLock = Lock()
    
    @synchronized(myLock)
    def _do_some_profiling(bt,et,spec,objects,fOut):
	_et = et - bt
	_rate = 1.0 / _et if (_et != 0) else 1.0
	if (_isVerbose):
	    print >>fOut, 'fOut=%s' % (str(fOut))
	print >>fOut, '(%2.4f, %4.2f reqs/sec) "%s" --> %s' % (_et,_rate,spec,objects if (not isinstance(objects,str)) else '"%s"' % (objects))
	
    _do_some_profiling(bt,et,spec,objects,fOut)

class SalesForceProxy(Pyro.core.ObjBase):
    '''
    the sfdc cannot be returned to the caller because it cannot be pickled.
    '''
    def __init__(self, isLogging=True):
	self.__sf_login_model__ = SalesForceLoginModel.SalesForceLoginModel()
	cred = credentials(magma_molten_passphrase,using_set=CredentialTypes.Magma_Production)
	endpts = self.end_points()
	endpt = [e[-1] for e in endpts if (e[0].find('www.') > -1)][0]
	self.__is_logged_in__ = self.login(cred['username'],cred['password'],endpt)
	self.__sfQuery__ = None
	if (self.__is_logged_in__):
	    self.__sfQuery__ = SalesForceQuery(self.sf_login_model)
	self.__isLogging__ = isLogging
        Pyro.core.ObjBase.__init__(self)
        
    def isLogging():
        doc = "isLogging"
        def fget(self):
            return self.__isLogging__
        return locals()
    isLogging = property(**isLogging())
    
    def is_logged_in():
        doc = "is_logged_in"
        def fget(self):
            return self.__is_logged_in__
        return locals()
    is_logged_in = property(**is_logged_in())
    
    def sf_login_model():
        doc = "sf_login_model"
        def fget(self):
            return self.__sf_login_model__
        return locals()
    sf_login_model = property(**sf_login_model())

    def sfQuery():
        doc = "sfQuery"
        def fget(self):
            return self.__sfQuery__
        return locals()
    sfQuery = property(**sfQuery())
    
    def users():
        doc = "users"
        def fget(self):
            return SalesForceObjectProxy(SalesForceUsers(self.sfQuery))
        return locals()
    users = property(**users())

    def contacts():
        doc = "contacts"
        def fget(self):
            return SalesForceObjectProxy(SalesForceContacts(self.sfQuery))
        return locals()
    contacts = property(**contacts())

    def accounts():
        doc = "accounts"
        def fget(self):
            return SalesForceObjectProxy(SalesForceAccounts(self.sfQuery))
        return locals()
    accounts = property(**accounts())

    def recordTypes():
        doc = "recordTypes"
        def fget(self):
            return SalesForceObjectProxy(SalesForceRecordTypes(self.sfQuery))
        return locals()
    recordTypes = property(**recordTypes())

    def cases():
        doc = "cases"
        def fget(self):
            return SalesForceObjectProxy(SalesForceCases(self.sfQuery))
        return locals()
    cases = property(**cases())

    def solutions():
        doc = "solutions"
        def fget(self):
            return SalesForceObjectProxy(SalesForceSolutions(self.sfQuery))
        return locals()
    solutions = property(**solutions())
    
    def attachments():
        doc = "attachments"
        def fget(self):
            return SalesForceObjectProxy(SalesForceAttachments(self.sfQuery))
        return locals()
    attachments = property(**attachments())

    def moltenPosts():
        doc = "moltenPosts"
        def fget(self):
            return SalesForceObjectProxy(SalesForceMoltenPosts(self.sfQuery))
        return locals()
    moltenPosts = property(**moltenPosts())

    def end_points(self):
	servers = []
	for k,v in self.__sf_login_model__.sfServers.iteritems():
	    _endpoint = self.__sf_login_model__.get_endpoint(v)
	    if (isinstance(v,list)):
		v.append(_endpoint)
	    else:
		v = [v,_endpoint]
	    servers += [v]
	return servers

    def login(self,username,password,endpoint):
	self.sf_login_model.username = username
	self.sf_login_model.password = password
	self.sf_login_model.perform_login(endpoint)
	success = self.sf_login_model.isLoggedIn
	return success

    def isLoggedIn(self):
        return self.is_logged_in

    def getAllActiveUsers(self):
	self.users.__start__()
	objects = self.users.getAllActiveUsers()
	return objects

    def getMagmaAccountTree(self, accountId, role):
	from maglib.molten import roles
	anAccount = self.accounts.sf_proxy.getAccountById(accountId)[0]
	tree = self.accounts.sf_proxy._getAccountTree(anAccount)
	mat = MagmaAccountTree(self.sfQuery,accountId,role=roles.role_from_molten(role),tree=tree)
	return mat.accounts.asPythonDict()

    def request_objects(self,spec):
	'''spec is something like "contacts.getPortalContactByEmail('rhorn@magma-da.com')".'''
        if (self.isLogging):
	    _beginTime = time.time()
	toks = spec.split('(')
	toks2 = toks[0].split('.')
	object_spec = toks2[0]
	s1 = 'self.%s.__start__()' % (object_spec)
	try:
	    eval(s1)
	except:
	    pass
	if (len(toks) == 1):
	    s2 = 'self.%s' % (spec if (len(toks2) > 1) else object_spec)
	    s3 = ''
	else:
	    s2 = 'self.%s' % (object_spec)
	    s3 = spec.replace('%s.' % (object_spec),'')
	try:
	    objects = eval(s2)
	except:
	    objects = None
	proxy = None
	if (len(s3) > 0):
	    proxy = objects
	    s4 = 'proxy.%s' % (s3)
	    try:
		objects = eval(s4)
	    except:
		objects = []
	    s5 = 'proxy.sf_proxy.lastError'
	    try:
		lastError = eval(s5)
	    except:
		lastError = 'n/a'
	if (isSalesForceObjectProxy(objects)):
	    toks2 = toks2[1:]
	    for t in toks2:
		objects = eval('objects%s.%s' % ('.sf_proxy' if isSalesForceObjectProxy(objects) else '',t))
        if (self.isLogging):
	    _endTime = time.time()
	    do_some_profiling(_beginTime,_endTime,s2,objects,fOut=sys.stdout)
	return objects, lastError

def main():
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
    locator = Pyro.naming.NameServerLocator(identification=ident) # note the ident string
    ns_URI = locator.detectNS()
    print 'Found Name Server at "%s".' % (ns_URI)
    ns = locator.getNS()
    
    try:
	ns.createGroup(":SalesForceProxy")
    except NamingError:
	pass
    
    daemon = Pyro.core.Daemon()
    daemon.useNameServer(ns)
    if (sys.platform != 'win32'): # Linux requires the following options...
	daemon.hostname = '0.0.0.0' # tide.magma-da.com requires the hostname to be 0.0.0.0 (cannot be 127.0.0.1) otherwise the server and client cannot find the Name Server...
    daemon.setAllowedIdentifications([ident])
    
    # connect new instance, but using persistent mode
    daemon.connectPersistent(SalesForceProxy(isLogging=_isLogging),':SalesForceProxy.version_%s' % (__version__.replace('.','_')))
    
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
	    
    if (_isHelp):
	ppArgs()
	
    if (not _isNopsyco):
	from vyperlogix.misc import _psyco
	_psyco.importPsycoIfPossible(func=main)
	
    if (_isProduction):
	_isRunningLocal = False
	
    main()
