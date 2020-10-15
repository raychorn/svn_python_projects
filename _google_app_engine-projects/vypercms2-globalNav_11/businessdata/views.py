# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, update_object
from django.template import RequestContext
from google.appengine.ext import db
from mimetypes import guess_type
from myapp.forms import PersonForm
from myapp.models import Contract, File, Person
from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response
from django.contrib.auth.decorators import login_required

from django.template import loader
from django.template import Context

from models import State

import mimetypes

from vyperlogix.misc import _utils
from vyperlogix.django import django_utils

__content__ = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"><title>VyperBusiness v1.0 ERROR</title></head><body>{{ content }}</body></html>'''

__content0__ = '''
<!DOCTYPE html 
     PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
     "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
    dir="ltr"
    xml:lang="en"
    lang="en">
  <head>
    <title>{{ title }}</title>
    <style type="text/css">
        {{ css }}
    </style>
  </head>
  {{ content }}
</html>
'''

__states__ = [{'name':'California','url':'https://businessfilings.sos.ca.gov/defaultbottom.asp','fieldName':'corpname','fieldLen':'47','abbrev':'CA'}]

__mimetype = mimetypes.guess_type('.html')[0]

__development__ = ['unknownlaptop:8888']

def load_and_cache_data_if_necessary():
    numStates = State.all().count()
    if (numStates == 0):
        pass

def default(request,args):
    try:
        s_response = ''
        __error__ = ''

        parms = django_utils.parse_url_parms(request)
        if (parms[0] == 'businessdata'):
            parms = parms[1:]
        url = '/%s' % (str('/'.join(parms)))

        if (parms[0:1] == [u'corpname']): # /corpname/corpname-goes-here/state-abbrev/
            corpname = parms[1]
            stateAbbrev = parms[2]
            return render_to_response(request, 'main.html')
        else:
            try:
                return render_to_response(request, url.replace('/',''))
            except Exception, e:
                cname = request.META['HTTP_HOST']
                return render_to_response(request, '404.html', {'details':'<BR/>'.join(_utils.formattedException(details=e).split('\n')),'HTTP_HOST':cname} if (django_utils._is_(request,__development__)) else {})
        content = t.render(Context(c,autoescape=False))
        return HttpResponse(content,mimetype=__mimetype)
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        mimetype = mimetypes.guess_type('.html')[0]
        return HttpResponse('<font color="red"><small>%s</small></font>'%('<br/>'.join(info_string.split('\n'))), mimetype=mimetype)
