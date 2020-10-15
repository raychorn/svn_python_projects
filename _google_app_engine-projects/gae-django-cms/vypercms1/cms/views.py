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

from cms.models import *
from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site, RequestSite

from random import choice, sample
from google.appengine.api import memcache

from google.appengine.ext import zipserve
import re

import mimetypes

from settings import TEMPLATE_DIRS,USE_I18N

from vyperlogix.misc import _utils

def EST_time(pub_date):
    pub_date = pub_date.replace(tzinfo=UtcTzinfo())
    return pub_date.astimezone(EstTzinfo())

def get_now_date():
    return EST_time(datetime.datetime.now())

_title = 'Vyper Logix Corp, The 21st Century Python Company'

__product__ = 'Vyper-Menu&trade;'
__version__ = '1.0.0.0'

__content__ = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"><title>{{ title }}</title></head><body>{{ body }}</body></html>'''

__upload_form__ = '''<form enctype="multipart/form-data" action="/upload" method="post">
<input type="file" name="myfile" maxlength="255" size="80"/>
<input type="submit" value="Upload" />
</form>'''

def upload(request) :
    file_contents = request.get('myfile')
    file_name = request.get('filename')
    obj = model.BlobModel()
    obj.blob = db.Blob( file_contents )
    obj.name = file_name
    obj.put()
    
def download(request, id) :
    obj = model.BlobModel.all().filter("id", id).get()
    
def default(request):
    global _title

    try:
        s_response = '';
        t = loader.get_template_from_string(__content__)
        c = {'title':_title,'body':__upload_form__}
        content = t.render(Context(c,autoescape=False))
        return HttpResponse(content,mimetype='text/html')
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        mimetype = mimetypes.guess_type('.html')[0]
        return HttpResponse('<br/>'.join(info_string.split('\n')), mimetype=mimetype)

