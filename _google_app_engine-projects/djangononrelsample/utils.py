from vyperlogix import misc

def __context__(request,data=None):
    __data__ = {
        "url": request.META.get('PATH_INFO','/'),
        "siteurl":"http://www.vyperlogix.com",
        "sitename": "VyperLogix Site&trade;",
        "services": "VyperLogix",
        "company": "VyperLogix",
        "sitename2": "The VyperLogix Site&trade;"
    }
    if (misc.isDict(data)):
        for k,v in data.iteritems():
            __data__[k] = v
    return __data__

