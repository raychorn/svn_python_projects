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

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
class SalesForceUsers(SalesForceAbstract):
    def __init__(self, sfQuery):
	super(SalesForceUsers, self).__init__(sfQuery,object_name='User')

    def getUserById(self,id):
	soql = "Select u.Email, u.FirstName, u.Id, u.LastName, u.Name from User u where u.Id = '%s'" % (id)
	return self.sf_query(soql)

    def getAllActiveUsers(self):
	soql = "Select u.Email, u.FirstName, u.Id, u.LastName, u.Name, u.IsActive from User u where u.IsActive = true"
	return self.sf_query(soql)

    def getAllMagmaUsers(self):
	soql = "Select u.Email, u.FirstName, u.Id, u.LastName, u.Name, u.IsActive from User u where u.IsActive = true and u.Email LIKE '%@magma%'"
	return self.sf_query(soql)

    def getUserByEmail(self,email,related_to=[]):
	'''related_to is a list of object names to which the parent object is related, related objects will be queried along with the parent.'''
	names = self.names
	related_to = related_to if (isinstance(related_to,list)) else [related_to] if (related_to is not None) else []
	related_names = self.get_related_names(related_to)
	_related_names = []
	for _names in related_names:
	    _related_names += _names
	soql = "Select %s from %s %s where u.Email = '%s'" % (', '.join(names+_related_names),self.object_name,self.object_prefix,email)
	return self.sf_query(soql)

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
