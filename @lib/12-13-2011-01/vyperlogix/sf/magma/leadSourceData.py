import os, sys, traceback, re

from vyperlogix import misc
from vyperlogix.hash import lists
from vyperlogix.misc import _utils
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

class SalesForceLeadSourceData(SalesForceAbstract):
    def __init__(self, sfQuery):
	super(SalesForceLeadSourceData, self).__init__(sfQuery, object_name='LeadSourceData__c')
	
    def soql_getActivityByLeadOrContact():
        doc = "soql for getActivityByLeadOrContact()"
        def fget(self):
            return "Select l.Contact__c, l.Contact__r.Id, l.CreatedDate, l.Id, l.Lead__c, l.Lead__r.Id, l.Score__c from LeadSourceData__c l WHERE ( (l.Lead__r.Id = '%s') OR (l.Contact__r.Id = '%s') )"
        return locals()
    soql_getActivityByLeadOrContact = property(**soql_getActivityByLeadOrContact())

    def soql_filter_lead_by_CreatedDate():
        doc = "soql for getActivityByLeadOrContact() to filter the Leads by the CreatedDate."
        def fget(self):
            return "(l.CreatedDate > %s)"
        return locals()
    soql_filter_lead_by_CreatedDate = property(**soql_filter_lead_by_CreatedDate())

    def getTodaysActivityByLeadOrContactId(self,id,num_days=0):
	'''num_days can be any valid value expressed as the number of days, the default being 0.'''
	today_iso = _utils.todayForSalesForce_localtime(_utils.days_timedelta(num_days=num_days),begin_at_midnight=True)
	soql = "%s and %s" % (self.soql_getActivityByLeadOrContact,self.soql_filter_lead_by_CreatedDate)
	soql = soql % (id,id,today_iso)
	activities = self.sf_query(soql)
	return activities

    def getActivityByLeadOrContactId(self,id):
	soql = self.soql_getActivityByLeadOrContact % (id,id)
	activities = self.sf_query(soql)
	return activities

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
