from vyperlogix.classes.CooperativeClass import Cooperative

import os, sys, traceback

from vyperlogix import misc
from vyperlogix.misc import _utils
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

class SalesForceSolutions(SalesForceAbstract):
    def __init__(self, sfQuery):
	super(SalesForceSolutions, self).__init__(sfQuery,object_name='Solution')

    def getNewSolutions(self,num_days=30,limit=5):
	num_days = int(num_days) if (str(num_days).isdigit()) else num_days
	limit = int(limit) if (str(limit).isdigit()) else limit
	today_iso = _utils.todayForSalesForce_localtime(_utils.days_timedelta(num_days=num_days),begin_at_midnight=True)
	try:
	    limit = int(str(limit))
	except:
	    limit = 5
	soql = "Select s.Id, s.Account_Name__c, s.IsDeleted, s.IsPublished, s.LastModifiedDate, s.Portal_Account_Name__c, s.Published_Date__c, s.Question_Problem__c, s.Region__c, s.SME_Reviewer__c, s.Solution_Answer__c, s.Solution_Type__c, s.Solution_Workaround__c, s.SolutionName, s.SolutionNote, s.SolutionNumber, s.Special_Build__c, s.Status from Solution s WHERE (s.Status = 'Published') AND (s.IsDeleted = False) AND (s.LastModifiedDate > %s) ORDER BY s.LastModifiedDate DESC LIMIT %d" % (today_iso,limit)
	solutions = self.sf_query(soql)
	return solutions

    def getNewSolutionsCount(self,num_days=30):
	num_days = int(num_days) if (str(num_days).isdigit()) else num_days
	today_iso = _utils.todayForSalesForce_localtime(_utils.days_timedelta(num_days=num_days),begin_at_midnight=True)
	soql = "Select COUNT() from Solution s WHERE (s.Status = 'Published') AND (s.IsDeleted = False) AND (s.LastModifiedDate > %s)" % (today_iso)
	solutions = self.sf_query(soql)
	count = [item for item in solutions if (str(item).isdigit())][0]
	return count

    def getSolutionsViewsFrequencies(self,num_days=30):
	from vyperlogix.sf.magma.solution_views import SalesForceMoltenSolutionViews
	sf_solution_views = SalesForceMoltenSolutionViews(self.sfQuery)

	num_days = int(num_days) if (str(num_days).isdigit()) else num_days
	
	d = lists.HashedLists()
	views = sf_solution_views.getSolutionsViews(num_days=num_days)
	try:
	    for view in views:
		if (view.has_key('Solution__c')):
		    d[view['Solution__c']] = view
	except:
	    pass
	d_freqs = lists.HashedLists()
	for k,v in d.iteritems():
	    d_freqs[len(v)] = k
	l_freqs = misc.sort(d_freqs.keys())
	return (l_freqs,d_freqs,d)

    def getSpecificSolutions(self,solutions=[]):
	solutions = []
	if (len(solutions) > 0):
	    soql = "Select %s from Solution s WHERE (s.Status = 'Published') AND (s.IsDeleted = False) AND (s.Id in (%s))" % (', '.join(self.names),','.join(["'%s'" % (item) for item in solutions]))
	    solutions = self.sf_query(soql)
	return solutions

    def getCustomHomePagesForAccount(self,account_id):
	soql = "Select %s from Solution s WHERE (s.Status = 'Published') AND (s.IsDeleted = False) AND (s.Portal_Account_Name__c = '%s')" % (', '.join(self.names),account_id)
	solutions = self.sf_query(soql)
	return solutions

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
