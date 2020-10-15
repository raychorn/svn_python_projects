from django import http
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.conf import settings

import os, sys

from vyperlogix.django import django_utils

from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix.js import minify

from vyperlogix.django import pages
from vyperlogix.html import myOOHTML as oohtml

from vyperlogix.django import django_utils

from vyperlogix.products import keys

from vyperlogix.crypto import md5
from vyperlogix.misc import GenPasswd

_root_ = os.path.dirname(__file__)

import random
random.seed()

null_xml = '''<data></data>'''

def getMenuXML(head_tag,body_tag,metadata_tag):
    fname = os.sep.join([settings.MEDIA_ROOT,os.sep.join(['xml','menuItems.xml'])])
    xml = _utils.readFileFrom(fname)
    xml = django_utils.render_from_string(xml,context=Context({'head_tag':head_tag, 'body_tag':body_tag, 'metadata_tag':metadata_tag}))
    return xml

def default(request):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)

    if (url_toks == [u'rest', u'getMenuXML']):
        return HttpResponse(content=getMenuXML('menu','menuitem','meta'),mimetype='text/xml')
    
    return HttpResponse(content=null_xml,mimetype='text/xml')

