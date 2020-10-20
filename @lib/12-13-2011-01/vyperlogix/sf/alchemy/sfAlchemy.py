# SalesForce Alchemy - provides an ORM-type interface for SalesForce via pyax and pyax_utils.

import os, sys
import random

from vyperlogix.classes.MagicObject import MagicObject2

from vyperlogix.sf.sf import SalesForceQuery
from vyperlogix.sf.abstract import SalesForceAbstract
from vyperlogix.wx.pyax.SalesForceLoginModel import SalesForceLoginModel

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix.daemon.daemon import Log

from vyperlogix.classes.SmartObject import SmartFuzzyObject

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

class SalesForceObjectException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)
        
class SalesForceFieldException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)
        
class SalesForceParmException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)
        
class SalesForceOrderByException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)
        
class SalesForceAlchemy(MagicObject2,SalesForceAbstract):
    def __init__(self,username=None,password=None,token=None):
	# Note: SalesForceAbstract.__init__() appears below where it should... never mind about doing anything about it here.
        self.__username__ = username
        self.__password__ = password
        self.__token__ = token
        self.__endPoint__ = None
        self.__sfLoginModel__ = None
        self.__api_version__ = 14
        self.__types__ = lists.HashedFuzzyLists2()
        self.__objectStack__ = []
        self.__fieldsStack__ = []
        self.__filterStack__ = []
        self.__orderByStack__ = []
        self.__quoted__ = lambda val:"'" if (not str(val).isdigit()) else ''
	
        self.__reset_magic__() # This is basically the init method for MagicObject2...
        
    def __tokenize_password__(self):
        if (misc.isString(self.__token__)):
            self.__password__ = str(self.__password__) + self.__token__
            self.__token__ = None

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
            return self.__sfLoginModel__.lastError
        return locals()
    lastError = property(**lastError())

    def isLoggedIn():
        doc = "isLoggedIn property"
        def fget(self):
            return self.__sfLoginModel__.isLoggedIn
        return locals()
    isLoggedIn = property(**isLoggedIn())
    
    def __make_soql__(self):
        where_clause = []
        while (len(self.__filterStack__) > 0):
            aFilter = self.__filterStack__.pop()[0]
	    aClause = ' and '.join(['%s.%s=%s%s%s' % (self.object_prefix,k,self.__quoted__(v),v,self.__quoted__(v)) for k,v in aFilter.iteritems()])
	    if (len(aClause) > 0):
		where_clause.append()
	if (len(where_clause) > 0):
	    where_clause = ['(%s)' % (where) for where in where_clause]
        order_by_clause = []
        while (len(self.__orderByStack__) > 0):
            item = self.__orderByStack__.pop()[0]
            if (item in self.description.fieldnames):
                order_by_clause.append('%s.%s' % (self.object_prefix,item))
                break
            else:
                raise SalesForceOrderByException('Cannot use the field named "%s" in an ORDER BY clause for SalesForce Object named "%s".' % (item,self.object_name))
	if (len(order_by_clause) == 1):
	    order_by_clause.insert(0,'')
        from_clause = ' FROM %s %s%s' % (self.object_name,self.object_prefix,' WHERE %s' % (' and '.join(where_clause)) if (len(where_clause) > 0) else '')
        soql = 'SELECT %s%s%s' % (', '.join(self.names),from_clause,' ORDER BY '.join(order_by_clause) if (len(order_by_clause) > 0) else '')
        soql_count = 'SELECT COUNT()%s' % (from_clause)
        return soql,soql_count
    
    def __getattr__(self,name):
        t = self.__types__[name]
        if (t is not None):
            self.__objectStack__.append(t)
            return self
        return super(SalesForceAlchemy, self).__getattr__(name)
    
    def __call__(self,*args,**kwargs):
        super(SalesForceAlchemy, self).__call__(*args,**kwargs)
        n = self.n.pop()
        a = list(args)
        a.append(kwargs)
        if (n == 'endPoint'):
            self.__endPoint__ = a
        elif (n == 'login'):
            self.__tokenize_password__()
            self.__sfLoginModel__ = SalesForceLoginModel(username=self.__username__,password=self.__password__)
            if (isinstance(self.__endPoint__,list)):
                self.__sfLoginModel__.api_version = self.__api_version__
                self.__endPoint__ = self.__endPoint__[0] if (len(self.__endPoint__) > 0) else 'www.salesforce.com'
            if (self.__endPoint__.find('://') == -1):
                self.__endPoint__ = self.__sfLoginModel__.get_endpoint(end_point=self.__endPoint__)
            self.__sfLoginModel__.perform_login(end_point=self.__endPoint__)
            if (self.isLoggedIn):
                for t in self.__sfLoginModel__.sfdc.describe_global_response['types']:
                    self.__types__[t] = t
		#self.__sfQuery__ = SalesForceQuery(self.__sfLoginModel__)
		SalesForceAbstract.__init__(self, SalesForceQuery(self.__sfLoginModel__))
        elif (n == 'username'):
            self.__username__ = a[0] if (len(a) > 0) else ''
        elif (n == 'password'):
            self.__password__ = a[0] if (len(a) > 0) else ''
        elif (n == 'token'):
            self.__token__ = a[0] if (len(a) > 0) else ''
        elif (n == 'fields'):
            self.__fieldsStack__.append(a)
        elif (n == 'filter'):
            self.__filterStack__.append(a)
        elif (n == 'order_by'):
            self.__orderByStack__.append(a)
        elif (n == 'all') or (n == 'count'):
            try:
                object_name = self.__objectStack__.pop()
            except IndexError:
                raise SalesForceObjectException("Required Object Name was not present.  Object Name must appear like this (sf.case.fields('*').filter(Id='value-of-Id').order_by('Name').all()) with each Object Name being present in the target SalesForce Org.")
	    fieldsStack_copy = misc.copy(self.__fieldsStack__)
	    filterStack_copy = misc.copy(self.__filterStack__)
	    orderByStack_copy = misc.copy(self.__orderByStack__)
            self.object_name = object_name
	    self.canonicalizeNames(self.__fieldsStack__)
            soql,soql_count = self.__make_soql__()
            results_count = self.sf_query(soql_count)
	    if (n == 'count'):
		if (kwargs.has_key('debug')) and (kwargs['debug']):
		    return soql,soql_count,results_count[0]
		else:
		    return results_count[0]
	    else:
		_callback = None
		if (kwargs.has_key('callback')) and (callable(kwargs['callback'])):
		    _callback = kwargs['callback']
		if (int(results_count[0].size[0]) > 1):
		    f = self.fields_by_(name='idlookup',value='true')
		    if (f is not None):
			l = [_f for _f in f if (_f.has_key('name')) and (_f['name'].find('Id') > -1)]
			if (len(l) == 0):
			    l = random.choice(f)
			l = l[0] if (isinstance(l,list)) and (len(l) > 0) else l
			self.__filterStack__ = filterStack_copy
			self.__orderByStack__ = orderByStack_copy
			self.namesCanonicalized([l['name']])
			soql,soql_count = self.__make_soql__()
			records = self.sf_query(soql)
			for rec in records:
			    self.__fieldsStack__ = fieldsStack_copy
			    self.__filterStack__ = filterStack_copy
			    self.__orderByStack__ = orderByStack_copy
			    self.canonicalizeNames(self.__fieldsStack__)
			    pass
			pass
		    pass
		elif (kwargs.has_key('debug')) and (kwargs['debug']):
		    return soql,soql_count,results_count[0]
		else:
		    records = self.sf_query(soql)
		    if (callable(_callback)):
			for rec in records:
			    _callback(rec)
		    return records
        self.__reset_magic__()
        return self
