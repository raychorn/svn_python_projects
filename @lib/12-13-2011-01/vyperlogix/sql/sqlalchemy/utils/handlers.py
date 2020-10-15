from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.sql.sqlalchemy import SQLAgent

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

def handle_items(qry,callback=None,asSmartObject=False):
    items = []
    num_items = qry.count()
    num_items_part = num_items / 100
    num_items_part = num_items_part if (num_items_part > 0) else num_items
    for i in xrange(num_items):
        item = SQLAgent.instance_as_SmartObject(qry[i]) if (asSmartObject == True) else qry[i]
        items.append(item)
        if (i > 0) and ((i % num_items_part) == 0):
            print '%d of %d.' % (i,num_items)
            if (callable(callback)):
                try:
                    callback(items,i,num_items)
                finally:
                    items = []
    if (len(items) > 0):
        if (callable(callback)):
            try:
                callback(items,num_items,num_items)
            finally:
                items = []
    return items
