from vyperlogix.classes.CooperativeClass import Cooperative

import os, sys, traceback

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName

try:
    from cStringIO import StringIO as StringIO
except:
    from StringIO import StringIO as StringIO

from vyperlogix.sf.abstract import SalesForceAbstract

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

class SalesForceCases(SalesForceAbstract):
    def __init__(self, sfQuery):
	super(SalesForceCases, self).__init__(sfQuery,object_name='Case')

    def getCasesOwnedBy(self,ownerid,recordTypeId=None):
	_names = self.names
	soql = "Select %s from Case c where (c.OwnerId = '%s') and (c.IsClosed = False) and (c.IsDeleted = False)" % (', '.join(_names),ownerid)
	if (recordTypeId is not None):
	    soql += " and (c.RecordTypeId = '%s')" % (recordTypeId)
	return self.sf_query(soql)

    def getCasesForContactById(self,contactid,recordTypeId=None):
	_names = self.names
	soql = "Select %s from Case c where (c.ContactId = '%s') and (c.IsClosed = False) and (c.IsDeleted = False)" % (', '.join(_names),contactid)
	if (recordTypeId is not None):
	    soql += " and (c.RecordTypeId = '%s')" % (recordTypeId)
	return self.sf_query(soql)

    def getAllCasesForContactById(self,contactid,recordTypeId=None):
	_names = self.names
	soql = "Select %s from Case c where (c.ContactId = '%s') and (c.IsDeleted = False)" % (', '.join(_names),contactid)
	if (recordTypeId is not None):
	    soql += " and (c.RecordTypeId = '%s')" % (recordTypeId)
	return self.sf_query(soql)

    def getCasesForMoltenContacts(self,recordTypeId=None):
	_names = self.names
	soql = "Select %s, c.Contact.ContactStatus__c from Case c where (c.Contact.ContactStatus__c = 'Active') and (c.IsDeleted = False)" % (', '.join(_names))
	if (recordTypeId is not None):
	    soql += " and (c.RecordTypeId = '%s')" % (recordTypeId)
	return self.sf_query(soql)

    def getCasesById(self,id,names=[]):
	_names = self._names(names)
	soql = "Select %s from Case c where (c.Id = '%s') and (c.IsClosed = False) and (c.IsDeleted = False)" % (', '.join(_names),id)
	return self.sf_query(soql)

    def getAllCasesWithOldCCList(self):
	soql = "Select c.CaseNumber, c.CC__c, c.CC_List_1__r.Email, c.CC_Name_2__r.Email, c.CC_Name_3__r.Email, c.CC_Name_4__r.Email, c.Id, c.IsClosed from Case c WHERE c.IsClosed = false and (c.CC_List_1__r.Email != null or c.CC_Name_2__r.Email != null or c.CC_Name_3__r.Email != null or c.CC_Name_4__r.Email != null)"
	return self.sf_query(soql)

    def getAllCasesById(self,id,names=[]):
	_names = self._names(names)
	soql = "Select %s from Case c where (c.Id = '%s')" % (', '.join(_names),id)
	return self.sf_query(soql)

    def getCasesByAccountId(self,account_id,recordTypeId=None):
	'''account_id can be either a single id or a list of id values.'''
	_names = self.names
	soql = "Select %s from Case c where %s and (c.IsClosed = False) and (c.IsDeleted = False)" % (', '.join(_names),"(c.AccountId = '%s')" % (account_id) if (not isinstance(account_id,list)) else '(c.AccountId in (%s))' % (','.join(["'%s'" % (id) for id in account_id])))
	if (recordTypeId is not None):
	    soql += " and (c.RecordTypeId = '%s')" % (recordTypeId)
	return self.sf_query(soql)

    def getAllCasesByAccountId(self,account_id,names=[],recordTypeId=None):
	'''account_id can be either a single id or a list of id values.'''
	_names = self._names(names)
	soql = "Select %s from Case c where %s" % (', '.join(_names),"(c.AccountId = '%s')" % (account_id) if (not isinstance(account_id,list)) else '(c.AccountId in (%s))' % (','.join(["'%s'" % (id) for id in account_id])))
	if (recordTypeId is not None):
	    soql += " and (c.RecordTypeId = '%s')" % (recordTypeId)
	return self.sf_query(soql)

    def getAllCasesCountByAccountId(self,account_id,recordTypeId=None):
	'''account_id can be either a single id or a list of id values.'''
	soql = "Select COUNT() from Case c where %s" % ("(c.AccountId = '%s')" % (account_id) if (not isinstance(account_id,list)) else '(c.AccountId in (%s))' % (','.join(["'%s'" % (id) for id in account_id])))
	if (recordTypeId is not None):
	    soql += " and (c.RecordTypeId = '%s')" % (recordTypeId)
	return self.sf_query(soql)

    def getSupportCasesByAccountId(self,account_id,recordTypeId=None):
	'''account_id can be either a single id or a list of id values.'''
	_names = self.names
	soql = "Select %s from Case c where %s and (c.IsClosed = False) and (c.IsDeleted = False)" % (', '.join(_names),"(c.AccountId = '%s')" % (account_id) if (not isinstance(account_id,list)) else '(c.AccountId in (%s))' % (','.join(["'%s'" % (id) for id in account_id])))
	if (recordTypeId is not None):
	    soql += " and (c.RecordTypeId = '%s')" % (recordTypeId)
	return self.sf_query(soql)

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
