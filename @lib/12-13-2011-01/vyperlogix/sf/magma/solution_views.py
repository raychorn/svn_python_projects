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

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

class SalesForceMoltenSolutionViews(SalesForceAbstract):
    def __init__(self, sfQuery):
	super(SalesForceMoltenSolutionViews, self).__init__(sfQuery, object_name='Molten_Solution_Views__c')
	
    def getSolutionsViews(self,num_days=30):
	today_iso = _utils.todayForSalesForce_localtime(_utils.days_timedelta(num_days=num_days),begin_at_midnight=True)
	soql = "Select m.Contact__c, m.Contact__r.AccountId, m.Contact__r.Id, m.Created_At__c, m.Id, m.IsDeleted, m.Solution__c, m.Solution__r.Account_Name__c, m.Solution__r.Id, m.Solution__r.IsDeleted, m.Solution__r.IsPublished, m.Solution__r.SolutionName from Molten_Solution_Views__c m WHERE (m.Created_At__c > %s)" % (today_iso)
	views = self.sf_query(soql)
	return views

    def new_schema(self,Contact__c,Created_At__c,Solution__c):
	'''This method builds a schema that can be used to make a new instance of this object via a Factory.'''
	return {'Contact__c': Contact__c,
		'Created_At__c': Created_At__c,
		'Solution__c': Solution__c
		}

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
