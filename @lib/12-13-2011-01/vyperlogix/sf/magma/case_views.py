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

class SalesForceMoltenCaseViews(SalesForceAbstract):
    def __init__(self, sfQuery):
	super(SalesForceMoltenCaseViews, self).__init__(sfQuery, object_name='Molten_Case_Views__c')
	
    def getCaseViews(self):
	soql = "Select m.Contact__c, m.Created_At__c, m.Id, m.SupportCase__c from Molten_Case_Views__c m"
	return self.sf_query(soql)

    def new_schema(self,Contact__c,Created_At__c,SupportCase__c):
	'''This method builds a schema that can be used to make a new instance of this object via a Factory.'''
	return {'Contact__c': Contact__c,
		'Created_At__c': Created_At__c,
		'SupportCase__c': SupportCase__c
		}

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
