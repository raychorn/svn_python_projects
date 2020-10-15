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

def handle_save_data(request,parms,browserAnalysis,__air_id__,__apiMap__):
    d = {}
    
    def get_name_from(aDict):
	name = None
	try:
	    if (aDict.has_key('name')):
		name = aDict['name']
	    elif (aDict.has_key('n')):
		name = aDict['n']
	except Exception, e:
	    pass
	return name
    
    user = get_user(request)
    aUser = request.session['user'] if (request.session.has_key('user')) else None
    if (user._is_active):
	for k,v in request.POST.iteritems():
	    vv = json_to_python(v)
	    try:
		name = None
		if (misc.isList(vv)):
		    for d in vv:
			name = get_name_from(d)
			if (name):
			    break
		else:
		    name = get_name_from(d)
		if (name):
		    types = [aType for aType in models.LogosType.all() if aType.name == name]
		    aType = models.LogosType(user=user,name=name) if (len(types) == 0) else types[0]
		    aType.save()
		    datas = [aData for aData in models.LogosData.all() if aData.aType == aType]
		    aData = models.LogosData(aType=aType) if (len(datas) == 0) else datas[0]
		    aData.data = v
		    aData.save()
	    except Exception, e:
		info_string = _utils.formattedException(details=e)
		d[_error_symbol] = info_string
	    pass
    else:
        d[_error_symbol] = 'Cannot save data because you are not authorized to do so at this time.'
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def handle_get_data(request,parms,browserAnalysis,__air_id__,__apiMap__):
    d = {}
    
    user = get_user(request)
    aUser = request.session['user'] if (request.session.has_key('user')) else None
    if (user._is_active):
	try:
	    types = [aType for aType in models.LogosType.all() if aType.user == user]
	    for aType in types:
		datas = [json_to_python(aData.data) for aData in models.LogosData.all() if aData.aType == aType]
		d[aType.name] = datas
	except Exception, e:
	    info_string = _utils.formattedException(details=e)
	    d[_error_symbol] = info_string
    else:
        d[_error_symbol] = 'Cannot get data because you are not authorized to do so at this time.'
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)
