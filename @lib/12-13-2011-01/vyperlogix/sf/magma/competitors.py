from vyperlogix.classes.CooperativeClass import Cooperative

import os, sys, traceback, re

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.misc import ObjectTypeName

try:
    from cStringIO import StringIO as StringIO
except:
    from StringIO import StringIO as StringIO

from vyperlogix.sf.abstract import SalesForceAbstract

class SalesForceMagmaCompetitors(SalesForceAbstract):
    def __init__(self, sfQuery):
	super(SalesForceMagmaCompetitors, self).__init__(sfQuery)
	self.__className__ = 'Magma_Competitor__c'

    def className():
        doc = "className"
        def fget(self):
            return self.__className__
        return locals()
    className = property(**className())
    
    def getCompetitorsList(self):
	soql = "Select m.Company_Name__c, m.CreatedById, m.CreatedDate, m.Id, m.LastModifiedById, m.LastModifiedDate from Magma_Competitor__c m"
	return self.sf_query(soql)
    
    def getCompetitorByName(self,name):
	soql = "Select m.Company_Name__c, m.CreatedById, m.CreatedDate, m.Id, m.LastModifiedById, m.LastModifiedDate from Magma_Competitor__c m WHERE m.Company_Name__c = '%s'" % (name)
	return self.sf_query(soql)
    
    def deleteCompetitorsByName(self,names):
	ids = []
	info_string = ''
	try:
	    names = names if (isinstance(names,list)) else [names]
	    for name in names:
		recs = self.getCompetitorByName(name)
		if (recs is not None):
		    for rec in recs:
			ids.append(rec['Id'])
	    from vyperlogix.sf.delete import deleteSalesForceObjects
	    deleteSalesForceObjects(self.sfQuery.sfdc, ids)
	except Exception, details:
	    info_string = _utils.formattedException(details=details)
	    print >>sys.stderr, info_string
	return info_string
    
    def newCompetitor(self,data):
	from pyax.sobject.classfactory import ClassFactory
	aCompetitor = ClassFactory(self.sfQuery.sfdc, self.className)

	saveResults = self.sfQuery.sfdc.create(aCompetitor, [data])
	if (saveResults[0].has_key('errors')):
	    info_string = 'Failed to create %s from %s!' % (self.className,data)
	    print >>sys.stderr, info_string
	else:
	    info_string = 'Created %s from %s!' % (self.className,data)
	    print >>sys.stdout, info_string
	return info_string
