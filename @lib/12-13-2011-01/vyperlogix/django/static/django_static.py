from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseNotModified
from django.shortcuts import render_to_response

import os, sys

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.django import pages

from vyperlogix.django import django_utils

from vyperlogix.hash import lists

try:
    from settings import __title__
except ImportError:
    __title__ = 'Vyper Logix Corp.'

def serve(fullpath,nocache=False):
    import mimetypes
    if (not nocache):
	import rfc822
	import os
	import stat
    
    mimetype = mimetypes.guess_type(fullpath)[0]
    fh = open(fullpath, 'rb')
    try:
	contents = fh.read()
    except:
	contents = ''
    finally:
	fh.close()
    response = HttpResponse(contents, mimetype=mimetype)
    if (not nocache):
	statobj = os.stat(fullpath)
	response["Last-Modified"] = rfc822.formatdate(statobj[stat.ST_MTIME])
    else:
	response["CacheControl"] = 'no-cache'
	response["Cache-Control"] = 'no-cache, no-store'
	response["Expires"] = '-1'
	response["Pragma"] = 'no-cache'
    return response

def normalize1(fname,request):
    return '/'.join([fname.replace(os.sep,'/'),_utils.eat_leading_token_if_empty(request.path,delim='/')]).replace('/uploads/static/','/%s/'%(fname.replace(os.sep,'/').split('/')[-1])).replace('/static/media/','/static/').replace('/',os.sep).replace(os.sep.join(['static','static']),os.sep.join(['static']))

def static(request):
    normalize = lambda fname:'/'.join([fname.replace(os.sep,'/'),_utils.eat_leading_token_if_empty(request.path,delim='/')]).replace('/uploads/static/','/%s/'%(fname.replace(os.sep,'/').split('/')[-1])).replace('/static/media/','/static/').replace('/',os.sep).replace(os.sep.join(['static','static']),os.sep.join(['static']))
    isOkay = django_utils.is_request_okay(request)
    from django.conf import settings
    url_toks = django_utils.parse_url_parms(request)
    if (isOkay):
	fpaths = [normalize(settings.MEDIA_ROOT),normalize(settings.STATIC_ROOT)]
	for fpath in fpaths:
	    if (os.path.exists(fpath)):
		try:
		    return serve(fpath)
		except:
		    try:
			return HttpResponseNotAllowed(pages._render_the_page(request,__title__,'405.html',None,None,context={}))
		    except:
			pass
		    return render_to_response(request, '405.html')
    try:
	return HttpResponseNotFound(pages._render_the_page(request,__title__,'404.html',None,None,context={}))
    except:
	pass
    return render_to_response(request, '404.html')
