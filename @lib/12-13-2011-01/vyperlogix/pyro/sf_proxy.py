from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName

from vyperlogix.classes.SmartObject import PyroSmartObject

from vyperlogix.classes.MagicObject import MagicObject2

from vyperlogix.misc import _utils

from vyperlogix.hash import lists

from vyperlogix.daemon.daemon import BackgroundLog

from vyperlogix.decorators.memoized_duration import MemoizeStrictForDuration

import Pyro.naming, Pyro.core
import Pyro.errors
from Pyro import config as Pyro_config

import sys
import time

_isRunningLocal = (_utils.isBeingDebugged) or (_utils.getComputerName().lower() in ['rhorn-lap.ad.magma-da.com','undefined3'])

sys.stdout = BackgroundLog(fOut=sys.stdout)

__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

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

class SalesForceProxy(MagicObject2):
    '''This object knows how to interface with a Pyro Server when interfacing with SalesForce using a single sign-on for SF.'''
    def __init__(self,__version__,__func__):
        '''__version__ is the version for the Pyro Server and NS Authentication to ensure the client can connect to the server.'''
        if (_isRunningLocal):
	    _beginTime = time.time()
	    
	Pyro_config.PYRO_COMPRESSION = 1
	Pyro_config.PYRO_CHECKSUM = 1
	Pyro_config.PYRO_SOCK_KEEPALIVE = 1
	Pyro_config.PYRO_MULTITHREADED = 1
	
        Pyro.core.initClient()
        ident = __func__(__version__)

        locator = Pyro.naming.NameServerLocator(identification=ident)
        print '%s :: Searching Naming Service...' % (ObjectTypeName.objectSignature(self))
        ns = locator.getNS()

        print '%s :: Naming Service found at %s port %s'  % (ObjectTypeName.objectSignature(self),ns.URI.address,ns.URI.port)

        print '%s :: Binding to Remote Object.' % (ObjectTypeName.objectSignature(self))
        try:
            URI = ns.resolve(':SalesForceProxy.version_%s' % (__version__.replace('.','_')))
            print '%s :: URI: %s' % (ObjectTypeName.objectSignature(self),URI)
        except Pyro.core.PyroError,x:
            print '%s :: Couldn\'t bind object, nameserver says: %s' % (ObjectTypeName.objectSignature(self),x)
            raise SystemExit

        self.__proxy__ = Pyro.core.getProxyForURI(URI)
        self.__proxy__._setIdentification(ident)
        
        self.__reset_magic__()

        if (_isRunningLocal):
	    _endTime = time.time()
	    _et = _endTime - _beginTime
	    _rate = 1.0 / _et if (_et != 0) else 1.0
	    print '(%2.4f, %4.2f reqs/sec) "%s"' % (_et,_rate,ObjectTypeName.objectSignature(self))
	
    @MemoizeStrictForDuration(timeout=60,isDebug=False)
    def get_objects(self,s):
	try:
	    objs = eval(s)
	except Exception, _details:
	    objs = []
	    info_string = _utils.formattedException(details=_details)
	    print >>sys.stderr, info_string
	return objs
    
    def __call__(self,*args,**kwargs):
        '''
        Automatically redirect all unknown methods to the underlying Pyro Proxy object.
        Builds a request in the format of: contacts.getPortalContactByEmail('rhorn@magma-da.com')
            that is turned into: request_objects('contacts.getPortalContactByEmail("%s")' % (contact_username))
        '''
        m = super(MagicObject2, self).__call__(*args,**kwargs)[1:]
        if (len(m[0]) > 1):
            isExecute = (m[0][-1] == 'execute') and (len(args) == 0) and (len(kwargs) == 0)
            if (isExecute):
                s = 'self.proxy.request_objects(\'%s.%s\')' % (m[0][0],m[0][1])
            else:
                s = 'self.proxy.request_objects(\'%s.%s(%s)\')' % (m[0][0],m[0][1],_utils.args(*args,**kwargs))
        else:
            s = 'self.proxy.%s(%s)' % (m[0][0],_utils.args(*args,**kwargs))
	lastError = 'n/a'
	objs = self.get_objects(s)
	if (isinstance(objs,tuple)):
	    objs = list(objs)
	    lastError = objs[-1]
	    objs = objs[0]
        if (_isRunningLocal):
            print '"%s" --> %s' % (s,objs if (not misc.isString(objs)) else '"%s"' % (objs))
        self.__reset_magic__()
	if (not isinstance(objs,list)) and (not isinstance(objs,tuple)) and (not lists.isDict(objs)):
	    return objs
        return self.asSmartObjects(objs), lastError

    def proxy():
        doc = "proxy"
        def fget(self):
            return self.__proxy__
        return locals()
    proxy = property(**proxy())

    def asSmartObjects(self,objects):
        from vyperlogix.hash import lists
        items = []
        if (isinstance(objects,list)) or (isinstance(objects,tuple)):
            for obj in objects:
                items.append(PyroSmartObject(obj) if (lists.isDict(obj)) else obj)
	elif (lists.isDict(objects)):
	    items.append(objects)
        return items
