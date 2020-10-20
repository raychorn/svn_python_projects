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

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

class SalesForceMoltenPosts(SalesForceAbstract):
    def __init__(self, sfQuery):
	super(SalesForceMoltenPosts, self).__init__(sfQuery, object_name='MoltenPost__c')
	
    def new_schema(self,Name,Page__c,Valid_From__c,Valid_To__c):
	'''This method builds a schema that can be used to make a new instance of this object via a Factory.'''
	return {'Name': Name,
		'Page__c': Page__c,
		'Valid_From__c': Valid_From__c,
		'Valid_To__c': Valid_To__c
		}

    def getMoltenPostsByRecordTypeId(self,record_type_id):
	soql = "Select m.body__c, m.Id, m.Name, m.Page__c, m.RecordTypeId, m.Valid_From__c, m.Valid_To__c, m.LastModifiedDate from MoltenPost__c m WHERE (m.RecordTypeId = '%s')" % (record_type_id)
	return self.sf_query(soql)

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
