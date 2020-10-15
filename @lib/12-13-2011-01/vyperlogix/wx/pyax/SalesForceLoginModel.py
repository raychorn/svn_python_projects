from vyperlogix.classes.CooperativeClass import Cooperative
from vyperlogix.lists.ListWrapper import ListWrapper

import os, sys, traceback

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

from pyax.connection import Connection
from pyax.exceptions import ApiFault

try:
    from cStringIO import StringIO as StringIO
except:
    from StringIO import StringIO as StringIO

class SalesForceLoginModel(Cooperative):
    def __init__(self, username='', password='', callback_developers_check=None, api_version='14.0'):
        self.__username__ = username
        self.__password__ = password
        self.__sfdc__ = None
        self.__isStaging__ = True
	self.__lastError__ = ''
	self.__stagUsernamePolicy__ = True
	self.__callback_developers_check__ = callback_developers_check
	self.__api_version__ = '14.0' if (not isinstance(api_version, str)) else api_version

	from vyperlogix.sf.context import getSalesForceContext
	
	self.__sfContext__ = getSalesForceContext()
	self.__sfServers__ = self.sfContext.get__login_servers()
	
    def __str__(self):
	return 'username is "%s", password is "%s", sfdc is "%s", isStaging is "%s", sfServers is "%s", login_endpoint is "%s".' % (self.username,self.password,str(self.sfdc),self.isStaging,self.sfServers,self.sfContext.login_endpoint)
	
    def is_running_securely_for_developers():
        doc = "is_running_securely_for_developers property"
        def fget(self):
	    val = False
	    if (callable(self.__callback_developers_check__)):
		try:
		    val = self.__callback_developers_check__()
		except Exception, details:
		    print _utils.formattedException(details=details)
            return val
        return locals()
    is_running_securely_for_developers = property(**is_running_securely_for_developers())

    def api_version():
        doc = "api_version - default is 14.0 however any valid value works so long as SalesForce supports it."
        def fget(self):
            return self.__api_version__
        def fset(self, api_version):
            self.__api_version__ = _utils.only_float_digits(str(api_version))
        return locals()
    api_version = property(**api_version())

    def lastError():
        doc = "lastError property"
        def fget(self):
            return self.__lastError__
        return locals()
    lastError = property(**lastError())

    def stagUsernamePolicy():
        doc = "stagUsernamePolicy property - True means the username must have .stag on the end otherwise not."
        def fget(self):
            return self.__stagUsernamePolicy__
        def fset(self, stagUsernamePolicy):
            self.__stagUsernamePolicy__ = stagUsernamePolicy
        return locals()
    stagUsernamePolicy = property(**stagUsernamePolicy())

    def isStaging():
        doc = "username property"
        def fget(self):
            return self.__isStaging__
        def fset(self, isStaging):
            self.__isStaging__ = isStaging
        return locals()
    isStaging = property(**isStaging())

    def sfContext():
        doc = "sfContext property"
        def fget(self):
            return self.__sfContext__
        return locals()
    sfContext = property(**sfContext())
    
    def sfServers():
        doc = "sfServers property"
        def fget(self):
            return self.__sfServers__
        return locals()
    sfServers = property(**sfServers())

    def username():
        doc = "username property"
        def fget(self):
            return self.__username__
        def fset(self, username):
            self.__username__ = username
        return locals()
    username = property(**username())

    def password():
        doc = "password property"
        def fget(self):
            return self.__password__
        def fset(self, password):
            self.__password__ = password
        return locals()
    password = property(**password())

    def sfdc():
        doc = "sfdc property"
        def fget(self):
            return self.__sfdc__
        return locals()
    sfdc = property(**sfdc())

    def current_endpoint():
        doc = "end-point property for the currently logged-in session"
        def fget(self):
            return self.__sfdc__.endpoint
        return locals()
    current_endpoint = property(**current_endpoint())

    def isLoggedIn():
        doc = "isLoggedIn property"
        def fget(self):
	    isUsernameValid = misc.isString(self.username)
	    isPasswordValid = misc.isString(self.password)
	    isSFDCValid = (self.sfdc is not None) and (ObjectTypeName.typeClassName(self.sfdc).find('pyax.connection.Connection') > -1)
            return (isUsernameValid) and (isPasswordValid) and (isSFDCValid)
        return locals()
    isLoggedIn = property(**isLoggedIn())
    
    def get_endpoint(self,end_point='test.salesforce.com',isVerbose=False):
	endPt = self.sfContext.endpoint
	if (len(end_point) > 0):
	    endPt = self.sfContext.login_endpoint.replace(self.sfServers['production'],end_point)
	toks = endPt.split('/')
	v = _utils._float(toks[-1])
	if ('%02.1f' % (v) == toks[-1]):
	    toks[-1] = self.api_version
	    endPt = '/'.join(toks)
	if (isVerbose):
	    print '(%s) :: self.sfContext.login_endpoint is "%s" for "%s".' % (ObjectTypeName.objectSignature(self),endPt,end_point)
	return endPt
	    
    def perform_login(self,end_point='https://test.salesforce.com/services/Soap/u/14.0',isVerbose=False):
	self.sfContext.login_endpoint = end_point
	try:
	    self.__lastError__ = ''
	    if (isVerbose):
		print '(%s) :: self.username is "%s".' % (ObjectTypeName.objectSignature(self),self.username)
	    if (self.is_running_securely_for_developers):
		print 'self.password is "%s".' % (self.password)
	    if (isVerbose):
		print '(%s) :: self.sfContext.login_endpoint is "%s".' % (ObjectTypeName.objectSignature(self),self.sfContext.login_endpoint)
	    self.__sfdc__ = Connection.connect(self.username, self.password, context=self.sfContext)
	    if (isVerbose):
		print '(%s) :: self.__sfdc__ is "%s".' % (ObjectTypeName.objectSignature(self),self.__sfdc__)
	except Exception, details:
	    info_string = _utils.formattedException(details=details)
	    self.__lastError__ = info_string
	    try:
		del self.__sfdc__
	    finally:
		self.__sfdc__ = None
	    
    def perform_login_appropriately(self):
	if (self.isStaging):
	    self.perform_login(end_point=self.get_endpoint(self.sfServers['sandbox']))
	else:
	    self.perform_login(end_point=self.get_endpoint(self.sfServers['production']))
    
    def use_default_assignment_rule():
        doc = "use_default_assignment_rule property"
        def fget(self):
            return self.sfdc.context.use_default_assignment_rule
        def fset(self, aBool):
            self.sfdc.context.use_default_assignment_rule = aBool
        return locals()
    use_default_assignment_rule = property(**use_default_assignment_rule())
