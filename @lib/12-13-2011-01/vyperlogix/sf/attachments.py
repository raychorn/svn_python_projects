from vyperlogix.classes.CooperativeClass import Cooperative

import os, sys, traceback

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName

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
class SalesForceAttachments(SalesForceAbstract):
    def __init__(self, sfQuery):
	super(SalesForceAttachments, self).__init__(sfQuery,object_name='Attachment')

    def getAttachmentByParentId(self,id):
	_names = self.names
	soql = "Select %s from Attachment a WHERE (a.IsDeleted = False) and (a.IsPrivate = False) and (a.ParentId = '%s')" % (', '.join(_names),id)
	return self.sf_query(soql)

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
