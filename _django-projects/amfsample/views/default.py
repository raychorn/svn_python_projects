from django import http
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed

import os, sys

from vyperlogix.django import django_utils

from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix.js import minify

from vyperlogix.django import pages
from vyperlogix.html import myOOHTML as oohtml

from vyperlogix.django import django_utils

from vyperlogix.products import keys

#from models import User, UserActivity

from vyperlogix.django import forms
from vyperlogix.django.forms import form_as_html

from vyperlogix.crypto import md5
from vyperlogix.misc import GenPasswd

_root_ = os.path.dirname(__file__)

def default(request):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    
    dname = os.path.join(os.path.dirname(_root_),'static','flex')
    files = [os.path.join(dname,f) for f in os.listdir(dname) if (os.path.splitext(f)[-1] == '.html')]
    
    if (len(files) > 0):
        _content = _utils.readFileFrom(files[0],noCRs=True)
        return HttpResponse(content=_content)
    
    return HttpResponseNotFound(content='<b>Cannot find the static content file.</b>')

