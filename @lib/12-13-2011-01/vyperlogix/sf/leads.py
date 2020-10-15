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

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

class SalesForceLeads(SalesForceAbstract):
    def __init__(self, sfQuery):
	super(SalesForceLeads, self).__init__(sfQuery,object_name='Lead')
	self.__d_LeadSourceData__c = None
	self.__flds_LeadSourceData__c = None

    def d_LeadSourceData__c():
        doc = "d_LeadSourceData__c property"
        def fget(self):
	    if (self.__d_LeadSourceData__c is None):
		self.__d_LeadSourceData__c = self.sfQuery.sfdc.describeSObject('LeadSourceData__c')
	    return self.__d_LeadSourceData__c
        return locals()
    d_LeadSourceData__c = property(**d_LeadSourceData__c())
    
    def flds_LeadSourceData__c():
        doc = "flds_LeadSourceData__c property"
        def fget(self):
	    if (self.__flds_LeadSourceData__c is None):
		self.__flds_LeadSourceData__c = self.d_LeadSourceData__c.metadata['fields']
	    return self.__flds_LeadSourceData__c
        return locals()
    flds_LeadSourceData__c = property(**flds_LeadSourceData__c())
    
    def soql_leads_fields():
        doc = "soql_leads_fields property"
        def fget(self):
	    return 'l.Email, l.Id, l.ConvertedDate, l.ConvertedContactId, l.LeadSource, l.RecordTypeId, l.OwnerId, l.City, l.Company, l.FirstName, l.LastName, l.PostalCode, l.State, l.Street, l.ConvertedContact.AccountId, l.ConvertedContact.Email, l.ConvertedContact.FirstName, l.ConvertedContact.Id, l.ConvertedContact.LastName, l.ConvertedContact.LeadSource, l.ConvertedContact.MailingCity, l.ConvertedContact.MailingCountry, l.ConvertedContact.MailingPostalCode, l.ConvertedContact.MailingState, l.ConvertedContact.MailingStreet, l.ConvertedContact.MobilePhone, l.ConvertedContact.OwnerId, l.ConvertedContact.Portal_Password__c, l.ConvertedContact.Portal_Privilege__c, l.ConvertedContact.Portal_Username__c, l.ConvertedContact.RecordTypeId'
        return locals()
    soql_leads_fields = property(**soql_leads_fields())
    
    def getLeadRecordTypes(self):
	soql = "Select r.Id, r.Name, r.SobjectType from RecordType r WHERE r.SobjectType = 'Lead' and r.Name = 'Sales Lead' ORDER BY r.Name"
	return self.sf_query(soql)
    
    def getLeadSourceTypes(self):
	soql = "Select l.Id, l.Name from LeadSourceType__c l"
	return self.sf_query(soql)
    
    def recordTypes(self):
	from vyperlogix.hash import lists
	d_recordTypes = lists.HashedLists2()
	r = self.getLeadRecordTypes()
	if (r):
	    d_recordTypes = lists.HashedLists2(dict([(t['Id'],t['Name']) for t in r if (t.has_key('Id'))]))
	return d_recordTypes
    
    def leadTypes(self):
	from vyperlogix.hash import lists
	d_leadTypes = lists.HashedLists2()
	r = self.getLeadSourceTypes()
	if (r):
	    d_leadTypes = lists.HashedLists2(dict([(t['Id'],t['Name']) for t in r if (t.has_key('Id'))]))
	return d_leadTypes
	
    def leadSources(self):
	from vyperlogix.hash import lists
	d_Lead = self.sfQuery.sfdc.describeSObject('Lead')
	flds_Lead = d_Lead.metadata['fields']
	d_LeadSources = lists.HashedLists2()
	if (flds_Lead.has_key('LeadSource')):
	    d_LeadSources = lists.HashedLists2(flds_Lead['LeadSource']['picklistValues'])
	    l_retire = []
	    for k,v in d_LeadSources.iteritems():
		if (v['active'] == False):
		    l_retire.append(k)
	    for k in l_retire:
		del d_LeadSources[k]
	return d_LeadSources

    def leadSourceDescriptions(self):
	from vyperlogix.hash import lists
	d_LeadSourceData_Descriptions = lists.HashedLists2()
	if (self.flds_LeadSourceData__c.has_key('Description__c')):
	    d_LeadSourceData_Descriptions = lists.HashedLists2(self.flds_LeadSourceData__c['Description__c']['picklistValues'])
	return d_LeadSourceData_Descriptions

    def leadSourceTypes(self):
	from vyperlogix.hash import lists
	d_LeadSourceData_Types = lists.HashedLists2()
	if (self.flds_LeadSourceData__c.has_key('Type__c')):
	    d_LeadSourceData_Types = lists.HashedLists2(self.flds_LeadSourceData__c['Type__c']['picklistValues'])
	    l_retire = []
	    for k,v in d_LeadSourceData_Types.iteritems():
		if (v['label'].find(' did not ') > -1) or (v['value'].find(' did not ') > -1):
		    l_retire.append(k)
	    #for k in l_retire:
		#del d_LeadSourceData_Types[k]
	return d_LeadSourceData_Types

    def getLeadsByEmail(self,email):
	soql = "Select %s from Lead l where l.Email = '%s'" % (self.soql_leads_fields,email)
	return self.sf_query(soql)

    def getLeadOwnerById(self,id):
	from vyperlogix.sf.users import SalesForceUsers
	users = SalesForceUsers(self.sfQuery)
	return users.getUserById(id)

    def getLeadSourceDataById(self,id):
	soql = "Select l.Applications__c, l.Contact__c, l.Date__c, l.Description__c, l.Id, l.Lead__c, l.Notes__c, l.Score__c, l.Source__c, l.Type__c from LeadSourceData__c l where l.Id = '%s'" % (id)
	return self.sf_query(soql)

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
