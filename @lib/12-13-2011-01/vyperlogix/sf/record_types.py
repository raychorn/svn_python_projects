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

class SalesForceRecordTypes(SalesForceAbstract):
    def __init__(self, sfQuery):
	super(SalesForceRecordTypes, self).__init__(sfQuery)

    def getRecordTypes(self):
	soql = "Select r.BusinessProcessId, r.Description, r.Id, r.Name, r.SobjectType from RecordType r"
	return self.sf_query(soql)

    def getCaseRecordTypes(self,rtype=None):
	'''rtype is one of the available case types or None to get all the types.'''
	soql = "Select r.BusinessProcessId, r.Description, r.Id, r.Name, r.SobjectType from RecordType r WHERE (r.SobjectType = 'Case')"
	if (rtype is not None):
	    soql += " and (r.Name = '%s')" % (rtype)
	return self.sf_query(soql)

    def getMoltenRecordTypes(self,rtype=None):
	'''rtype is one of the available case types or None to get all the types.'''
	soql = "Select r.BusinessProcessId, r.Description, r.Id, r.Name, r.SobjectType from RecordType r WHERE (r.SobjectType = 'MoltenPost__c')"
	if (rtype is not None):
	    soql += " and (r.Name = '%s')" % (rtype)
	return self.sf_query(soql)

    def getMoltenPostArticlesRecordTypes(self,rtype='Articles'):
	'''rtype is one of the available case types or None to get all the types.'''
	return self.getMoltenRecordTypes(rtype=rtype)

    def getMoltenTipsRecordTypes(self,rtype='Tips'):
	'''rtype is one of the available case types or None to get all the types.'''
	return self.getMoltenRecordTypes(rtype=rtype)

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
