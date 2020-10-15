import os, sys, traceback, re

from vyperlogix import misc
from vyperlogix.hash import lists
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

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

class SalesForceAssets(SalesForceAbstract):
    def __init__(self, sfQuery):
	super(SalesForceAssets, self).__init__(sfQuery,object_name='Asset')

    def getCurrentAssets(self):
        windowIsoDateTime = self.today()
	soql = "Select a.AccountId, a.ContactId, a.Current_Start_Date__c, a.Current_End_Date__c, a.Name, a.Id, a.Status from Asset a WHERE (a.Current_Start_Date__c < %s) and (a.Current_End_Date__c > %s) ORDER BY a.Current_Start_Date__c, a.Current_End_Date__c" % (windowIsoDateTime,windowIsoDateTime)
	return self.sf_query(soql)
    
    def getAccountContacts(self,accountId,reExclude_AccountName=None):
	_contacts = []
	if (accountId is not None) and (len(accountId) > 0):
	    soql = "Select c.Email, c.FirstName, c.Full_Name__c, c.HasOptedOutOfEmail, c.Id, c.LastName, c.MailingCity, c.MailingCountry, c.MailingPostalCode, c.MailingState, c.MailingStreet, c.OtherCity, c.OtherCountry, c.OtherPhone, c.OtherPostalCode, c.OtherState, c.OtherStreet from Contact c WHERE (c.HasOptedOutOfEmail = False) and (c.AccountId = '%s')" % (accountId)
	    contacts = self.sf_query(soql)
	    if (contacts):
		for c in contacts:
		    d = lists.HashedLists2(c)
		    _contacts.append(d)
	return _contacts
    
    def getAssetContacts(self,accountId):
	_contacts = []
	if (accountId is not None) and (len(accountId) > 0):
	    soql = "Select a.Id, a.Name, a.OwnerId, a.Owner.City, a.Owner.ContactId, a.Owner.User_Contact_Id__c, a.Owner.CompanyName, a.Owner.Email, a.Owner.FirstName, a.Owner.Id, a.Owner.LastName, a.Owner.MobilePhone, a.Owner.Name, a.Owner.Phone, a.Owner.PostalCode, a.Owner.State, a.Owner.Street, a.Owner.Title from Account a WHERE (a.Id = '%s')" % (accountId)
	    accounts = self.sf_query(soql)
	    if (accounts):
		for acct in accounts:
		    if (acct['Owner']['User_Contact_Id__c'] is not None) and (len(acct['Owner']['User_Contact_Id__c']) > 0):
			soql = "Select c.Email, c.FirstName, c.Full_Name__c, c.HasOptedOutOfEmail, c.Id, c.LastName, c.MailingCity, c.MailingCountry, c.MailingPostalCode, c.MailingState, c.MailingStreet, c.OtherCity, c.OtherCountry, c.OtherPhone, c.OtherPostalCode, c.OtherState, c.OtherStreet from Contact c WHERE (c.HasOptedOutOfEmail = False) and (c.Id = '%s')" % (acct['Owner']['User_Contact_Id__c'])
			contacts = self.sf_query(soql)
			if (contacts):
			    for c in contacts:
				d = lists.HashedLists2(c)
				d['CompanyName'] = acct['Owner']['CompanyName']
				_contacts.append(d)
	return _contacts

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
