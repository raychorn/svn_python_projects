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
from django.contrib.auth import get_user

from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response
from django.contrib.auth.decorators import login_required

from random import choice, sample
from google.appengine.api import memcache

from vyperlogix.google.gae import unique

import models

import re

import mimetypes

import logging

from settings import TEMPLATE_DIRS,USE_I18N

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc import _utils
from vyperlogix.django import django_utils

from users.g import json_to_python, dict_to_json
from users.views import __jsonMimetype

def handle_get_random_data1000(request,parms,browserAnalysis,__air_id__,__apiMap__):
    d = {}
    
    user = get_user(request)
    aUser = request.session['user'] if (request.session.has_key('user')) else None
    if (user._is_active):
	try:
	    import random, uuid
	    random.seed()
	    
	    _count = django_utils.get_from_post(request,'points',100)
	    _guid = django_utils.get_from_post(request,'guid',str(uuid.uuid4))
	    data = []
	    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
	    for i in xrange(_count):
		data.append({'m':random.choice(months), 'p':random.randrange(100,stop=5000,step=100), 'x':random.randrange(100,stop=5000,step=100), '$':random.randrange(100,stop=5000,step=100)})
	    d['data'] = data
	    d['count'] = _count
	    d['guid'] = _guid
	except Exception, e:
	    info_string = _utils.formattedException(details=e)
	    d[_error_symbol] = info_string
    else:
        d[_error_symbol] = 'Cannot get data because you are not authorized to do so at this time.'
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def handle_get_usage_data(request,parms,browserAnalysis,__air_id__,__apiMap__):
    d = {}
    
    user = get_user(request)
    aUser = request.session['user'] if (request.session.has_key('user')) else None
    if (user._is_active):
	try:
	    d['count'] = 0
	    usages = [aUsage for aUsage in models.TestData.all() if aUsage.user == user]
	    for aUsage in usages:
		d['count'] = aUsage.count
	except Exception, e:
	    info_string = _utils.formattedException(details=e)
	    d[_error_symbol] = info_string
    else:
        d[_error_symbol] = 'Cannot get usage data because you are not authorized to do so at this time.'
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def handle_set_usage_data(request,parms,browserAnalysis,__air_id__,__apiMap__):
    d = {}
    
    user = get_user(request)
    aUser = request.session['user'] if (request.session.has_key('user')) else None
    if (user._is_active):
	try:
	    _count = django_utils.get_from_post(request,'count',0)
	    usages = [aUsage for aUsage in models.TestData.all() if aUsage.user == user]
	    aUsage = models.TestData(user=user,count=_count) if (len(usages) == 0) else usages[0]
	    aUsage.count = _count
	    aUsage.save()
	except Exception, e:
	    info_string = _utils.formattedException(details=e)
	    d[_error_symbol] = info_string
    else:
        d[_error_symbol] = 'Cannot set usage data because you are not authorized to do so at this time.'
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)
