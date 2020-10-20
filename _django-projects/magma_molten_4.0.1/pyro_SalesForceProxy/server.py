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

import sys
import Pyro.naming
import Pyro.core
from Pyro.errors import PyroError,NamingError

from config import ACCEPTED_ID

from vyperlogix.wx.pyax import SalesForceLoginModel
from vyperlogix.sf.sf import SalesForceQuery
from vyperlogix.sf.users import SalesForceUsers

from maglib.salesforce.auth import magma_molten_passphrase
from maglib.salesforce.auth import CredentialTypes
from maglib.salesforce.cred import credentials

from vyperlogix.classes.MagicObject import MagicObject2

from vyperlogix.hash import lists
from vyperlogix.misc import _utils

from vyperlogix.misc import ObjectTypeName

__version__ = '''4.0.1'''

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
	    for obj in objects:
		d = lists.HashedLists2(obj)
		d['__className__'] = ObjectTypeName.typeClassName(obj)
		items.append(d.asDict())
	return items
	
class SalesForceProxy(Pyro.core.ObjBase):
    '''
    the sfdc cannot be returned to the caller because it cannot be pickled.
    '''
    def __init__(self):
	self.__sf_login_model__ = SalesForceLoginModel.SalesForceLoginModel()
	cred = credentials(magma_molten_passphrase,using_set=CredentialTypes.Magma_Production)
	endpts = self.end_points()
	endpt = [e[-1] for e in endpts if (e[0].find('www.') > -1)][0]
	self.__is_logged_in__ = self.login(cred['username'],cred['password'],endpt)
	self.__sfQuery__ = None
	if (self.__is_logged_in__):
	    self.__sfQuery__ = SalesForceQuery(self.sf_login_model)
	self.__sf_object_cache__ = lists.HashedLists2() # key is the object type and valus is the proxy object that handles requests for objects
        Pyro.core.ObjBase.__init__(self)
        
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
	    if (self.is_logged_in):
		if (self.__sf_object_cache__['users'] is None):
		    self.__sf_object_cache__['users'] = SalesForceObjectProxy(SalesForceUsers(self.sfQuery))
            return self.__sf_object_cache__['users']
        return locals()
    users = property(**users())

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

def main():
    # initialize the server
    Pyro.core.initServer()
    
    # locate the NS
    print 'Searching Naming Service...'
    locator = Pyro.naming.NameServerLocator(identification=ACCEPTED_ID) # note the ident string
    ns = locator.getNS()
    
    try:
	ns.createGroup(":SalesForceProxy")
    except NamingError:
	pass
    
    daemon = Pyro.core.Daemon()
    daemon.useNameServer(ns)
    daemon.setAllowedIdentifications([ACCEPTED_ID])
    
    # connect new instance, but using persistent mode
    daemon.connectPersistent(SalesForceProxy(),':SalesForceProxy.version_%s' % (__version__.replace('.','_')))
    
    # enter the service loop.
    print 'Server started.'
    daemon.requestLoop()

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)
    main()
