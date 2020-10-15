def grid_handler(request,cls_or_object,func=None):
    '''
    request is the Django Request,
    cls_or_object is the Django Model class or a model object or list of model objects
    func is a callable that takes a row and returns a list of items in the proper order for the grid.'''
    import math
    import simplejson
    
    from vyperlogix.misc import _utils
    
    from vyperlogix.django import django_utils
    from vyperlogix.misc import ObjectTypeName
    
    page = django_utils.get_from_post_or_get(request,'page',default=-1)
    rows = django_utils.get_from_post_or_get(request,'rows',default=-1)
    sidx = django_utils.get_from_post_or_get(request,'sidx',default='')
    sord = django_utils.get_from_post_or_get(request,'sord',default='')

    try:
        if sidx == '' : sidx = 1
    
	symbol_ModelBase = 'django.db.models.base.ModelBase'
	symbol_QuerySet = 'django.db.models.query.QuerySet'
	class_ = ObjectTypeName.typeClassName(cls_or_object)
        if (class_ in [symbol_ModelBase,symbol_QuerySet]):
            try:
                items = cls_or_object.objects.order_by(sidx) if (class_ == symbol_ModelBase) else cls_or_object.order_by(sidx)
                if sord == 'desc':
                    items = misc.reverse(items)
            except Exception, details:
                info_string = _utils.formattedException(details=details)
                print >>sys.stderr, info_string
        elif (isinstance(cls_or_object,list)):
            try:
                items = cls_or_object
            except Exception, details:
                info_string = _utils.formattedException(details=details)
                print >>sys.stderr, info_string
        else:
            try:
                items = [cls_or_object]
            except Exception, details:
                info_string = _utils.formattedException(details=details)
                print >>sys.stderr, info_string
    
	count = len(items)
	total_pages = int(math.ceil(count/rows)) if (count > 0) else 1
	total_pages = total_pages if (total_pages > 0) else 1
    
	if (page > total_pages):
	    page = total_pages
	start = (rows*page)-rows
	
	start = 0 if (start < 0) else start

        cells = [ func(r) if (callable(func)) else r for r in items[start:rows] ]
        results = [ {'cell' : c } for c in cells ]
    except Exception, details:
        results = []
        count = _real_count(results)
        info_string = _utils.formattedException(details=details)
        print >>sys.stderr, info_string

    ret = { 'page' : page,
            'total' : total_pages,
            'records' : count,
	    'rows': results
	    }
    return simplejson.dumps(ret)

