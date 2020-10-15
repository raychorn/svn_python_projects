import sys

from vyperlogix.misc import _utils

from vyperlogix.sql.sqlalchemy import SQLAgent

def get_qry_by_parts(qry,callback=None):
    items = []
    try:
        num_items = qry.count()
        one_percent = (num_items / 100)
        if (one_percent < 200):
            one_percent = 200
        num_items_part = one_percent if (num_items > 10000) else num_items
        for i in xrange(num_items):
            item = SQLAgent.instance_as_SmartObject(qry[i])
            items.append(item)
            if (i > 0) and ((i % num_items_part) == 0):
                if (callable(callback)):
                    try:
                        callback(items)
                    finally:
                        items = []
        if (len(items) > 0):
            if (callable(callback)):
                try:
                    callback(items)
                finally:
                    items = []
    except Exception, details:
        print >>sys.stderr, _utils.formattedException(details=details)
    return items

