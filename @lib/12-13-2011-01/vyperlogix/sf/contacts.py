from vyperlogix.classes.CooperativeClass import Cooperative

import os, sys, traceback

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName

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

class SalesForceContacts(SalesForceAbstract):
    def __init__(self, sfQuery):
	super(SalesForceContacts, self).__init__(sfQuery,object_name='Contact')

    def getContactById(self,id):
	_names = self.names
	soql = "Select %s from Contact c where c.Id = '%s'" % (', '.join(_names),id)
	return self.sf_query(soql)

    def getSortedPortalContacts(self):
	soql = "Select Id, AccountId, ContactStatus__c from Contact where (ContactStatus__c = 'Active') and (AccountId != NULL) ORDER BY AccountId"
	return self.sf_query(soql)

    def getPortalContacts(self,for_accounts=[],callback=None,limit=None):
	soql = "Select Id, AccountId, ContactStatus__c from Contact where (ContactStatus__c = 'Active')"
	if (misc.isList(for_accounts)):
	    soql += " and (AccountId in (%s))" % (','.join(["'%s'" % (id) for id in for_accounts if (misc.isString(id))]))
	else:
	    soql += " and (AccountId != NULL)"
	if (limit is not None):
	    soql += ' LIMIT %s' % (limit)
	return self.sf_query(soql,callback=callback)

    def getPortalContactsCount(self,for_accounts=[]):
	soql = "Select COUNT() from Contact c where (c.ContactStatus__c = 'Active')"
	if (misc.isList(for_accounts)):
	    soql += " and (AccountId in (%s))" % (','.join(["'%s'" % (id) for id in for_accounts if (misc.isString(id))]))
	else:
	    soql += " and (AccountId != NULL)"
	return self.sf_query(soql)

    def getPortalContactByEmail(self,email):
	_names = self.names
	soql = "Select %s from Contact c where (c.Email = '%s') and (c.ContactStatus__c = 'Active')" % (', '.join(_names),email)
	return self.sf_query(soql)

    def getContactsByEmail(self,email):
	_names = self.names
	soql = "Select %s from Contact c where (c.Email = '%s')" % (', '.join(_names),email)
	return self.sf_query(soql)

    def getContactsByFuzzyEmail(self,email):
	from vyperlogix.mail import validateEmail
	_names = self.names
	toks = validateEmail.parseEmail(email)
	soql = "Select %s from Contact c where (c.Email like '%%%s%%')" % (', '.join(_names),toks[-1])
	return self.sf_query(soql)

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
