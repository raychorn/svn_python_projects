import sys

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.misc import ObjectTypeName

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

def grid_handler(request,cls_or_object,func,total=None):
    '''
    request is the Django Request,
    cls_or_object is the Django Model class or a model object or list of model objects
    func is a callable that takes a row and returns a list of items in the proper order for the grid.'''
    import simplejson
    
    try:
        page = int(request.POST['page'])
    except Exception, details:
        page = -1
        info_string = _utils.formattedException(details=details)
        print >>sys.stderr, info_string
        
    try:
        rp = int(request.POST['rp'])
    except Exception, details:
        rp = -1
        info_string = _utils.formattedException(details=details)
        print >>sys.stderr, info_string

    try:
        sortname = request.POST['sortname']
    except Exception, details:
        sortname = ''
        info_string = _utils.formattedException(details=details)
        print >>sys.stderr, info_string

    try:
        sortorder = str(request.POST['sortorder']).lower()
    except Exception, details:
        sortorder = ''
        info_string = _utils.formattedException(details=details)
        print >>sys.stderr, info_string

    try:
        query = request.POST['query']
    except Exception, details:
        query = ''
        info_string = _utils.formattedException(details=details)
        print >>sys.stderr, info_string

    try:
        qtype = request.POST['qtype']
    except Exception, details:
        qtype = ''
        info_string = _utils.formattedException(details=details)
        print >>sys.stderr, info_string
        
    try:
        if sortname == '' : sortname = 'name'
        if sortorder == '' : sortorder = '-'
    
        start = (page - 1) * rp

        rows = []
        _real_count = lambda aList:len(aList) if (not str(total).isdigit()) else total
        count = _real_count(rows)
        if (ObjectTypeName.typeClassName(cls_or_object) == 'django.db.models.base.ModelBase'):
            try:
                items = cls_or_object.objects.order_by(sortname)
                if sortorder == 'desc':
                    items = misc.reverse(items)
                if query == '' :
                    rows = items[start:start+rp]
                    count = _real_count(items)
                else :
                    rows = items.filter( qtype + ' =', query.upper() )
                    count = _real_count(items)
            except Exception, details:
                info_string = _utils.formattedException(details=details)
                print >>sys.stderr, info_string
        elif (isinstance(cls_or_object,list)):
            try:
                rows = items = cls_or_object
                count = _real_count(items)
            except Exception, details:
                info_string = _utils.formattedException(details=details)
                print >>sys.stderr, info_string
        else:
            try:
                rows = items = [cls_or_object]
                count = _real_count(items)
            except Exception, details:
                info_string = _utils.formattedException(details=details)
                print >>sys.stderr, info_string
    
        cells = [ func(r) for r in rows ]
        results = [ {'cell' : c } for c in cells ]
    except Exception, details:
        results = []
        count = _real_count(results)
        info_string = _utils.formattedException(details=details)
        print >>sys.stderr, info_string
    
    ret = { 'page' : page,
            'total' : count,
            'rows' : results }
    return simplejson.dumps(ret)
