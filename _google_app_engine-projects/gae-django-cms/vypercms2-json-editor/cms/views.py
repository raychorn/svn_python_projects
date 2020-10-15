# -*- coding: utf-8 -*-
import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, update_object
from google.appengine.ext import db
from mimetypes import guess_type
from django.template import loader
from django.template import Context

from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site, RequestSite

from random import choice, sample
from google.appengine.api import memcache

import models

from google.appengine.ext import zipserve
import re

import mimetypes

from settings import TEMPLATE_DIRS,USE_I18N

from vyperlogix.misc import _utils
from vyperlogix.django import django_utils

def EST_time(pub_date):
    pub_date = pub_date.replace(tzinfo=UtcTzinfo())
    return pub_date.astimezone(EstTzinfo())

def get_now_date():
    return EST_time(datetime.datetime.now())

_title = 'Vyper Logix Corp, The 21st Century Python Company'

__product__ = 'Vyper-JSON&trade;'
__version__ = '1.0.0.0'

__content__ = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"><title>{{ title }}</title></head><body>{{ body }}</body></html>'''

__upload_form__ = '''<form enctype="multipart/form-data" action="/upload/" method="post" target="_top">
<NOBR><input type="file" name="myfile" maxlength="255" size="120"/>
<input type="submit" value="Upload" /></NOBR>
</form>'''

__delete_form__ = '''<a href="/delete/" target="_top">Delete All</a>'''

__refresh_form__ = '''<a href="/" target="_top">Refresh</a>'''

def upload(request) :
    import uuid
    import base64
    from vyperlogix.misc import _utils
    
    aStream = _utils.stringIO()

    aFile = request.FILES['myfile']
    if (aFile.content_type == 'application/x-shockwave-flash'):
        for aChunk in aFile.chunks():
            b64 = base64.b64encode(aChunk)
            aStream.write(b64)
    else:
        aStream.write(aFile.readlines())
    blob = db.Blob( aStream.getvalue() )
    obj = models.BlobModel(bid=str(uuid.uuid4()),blob=blob,name=aFile.name,type=aFile.content_type,size=aFile.size)
    obj.put()
    
def download(bid) :
    blob = models.BlobModel.all().filter("bid", bid).get()
    return blob
    
def downloads() :
    blobs = models.BlobModel.all()
    return blobs

def delete_downloads() :
    blobs = downloads()
    for aBlob in blobs.__iter__():
        aBlob.delete()

def render_downloads_from(_blobs):
    from vyperlogix.html import myOOHTML
    rows = []
    for aBlob in _blobs.__iter__():
        rows.append(myOOHTML.renderAnchor('/fetch/%s/'%(aBlob.bid),'%s (%s, %s)'%(aBlob.name,aBlob.type,aBlob.size)))
    oo = myOOHTML.HtmlCycler()
    oo.html_simple_table(rows)
    t = myOOHTML.render_BR() + myOOHTML.render_BR() + myOOHTML.render_BR() + oo.toHtml()
    return t
    
def render_delete_all():
    from vyperlogix.html import myOOHTML
    t = myOOHTML.render_BR() + myOOHTML.render_BR() + __delete_form__
    return t
    
def render_refresh_list():
    from vyperlogix.html import myOOHTML
    t = myOOHTML.render_BR() + myOOHTML.render_BR() + __refresh_form__
    return t
    
def render_error_notice_from(errMsg):
    from vyperlogix.html import myOOHTML
    t = myOOHTML.render_P(errMsg,styles="color=red")
    return t
    
def default(request):
    try:
        __error__ = ''
        
        parms = django_utils.parse_url_parms(request)
        isUpload = (len(parms) > 0) and (parms[0] == 'upload')
        isDelete = (len(parms) > 0) and (parms[0] == 'delete')
        isFetch = (len(parms) > 0) and (parms[0] == 'fetch')
        if (django_utils.is_method_post(request)):
            if (isUpload):
                upload(request)
            pass
        elif (isDelete):
            delete_downloads()
        elif (isFetch):
            bid = parms[-1]
            anItem = download(bid)
            if (anItem):
                pass
            else:
                __error__ = 'Invalid download id given. Cannot retrieve the requested item.'
        __error__ = 'Invalid download id given. Cannot retrieve the requested item.'
        blobs = downloads()
        s_response = '';
        t = loader.get_template_from_string(__content__)
        c = {'title':'%s %s (%s)'%(__product__,__version__,_title),'body':__upload_form__+render_error_notice_from(__error__)+render_refresh_list()+render_delete_all()+render_downloads_from(blobs)}
        content = t.render(Context(c,autoescape=False))
        return HttpResponse(content,mimetype='text/html')
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        mimetype = mimetypes.guess_type('.html')[0]
        return HttpResponse('<font color="red"><small>%s</small></font>'%('<br/>'.join(info_string.split('\n'))), mimetype=mimetype)

