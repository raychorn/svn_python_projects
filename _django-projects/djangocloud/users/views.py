from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, update_object
from django.template import RequestContext
from mimetypes import guess_type
from django.contrib.auth.decorators import login_required

from users.registration import RegistrationProfile

from django.contrib.auth import get_user, login, logout

from django.template import loader, Template, TemplateDoesNotExist
from django.template import Context
from django.conf import settings

import models

import re
import logging
import mimetypes

from datetime import datetime,timedelta

import uuid
import urllib

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.django import django_utils
from vyperlogix.misc import ObjectTypeName
from vyperlogix.hash import lists
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.classes.SmartObject import SmartObject, SmartFuzzyObject

from vyperlogix.classes.CooperativeClass import Cooperative

from django.contrib.sitemaps.views import sitemap
from vyperlogix.feeds import feedparser

from vyperlogix.html import myOOHTML

from g import dict_to_json, today

from vyperlogix.django.common.API.api import API

__mimetype = mimetypes.guess_type('.html')[0]
__jsonMimetype = 'application/json'
__xmlMimetype = mimetypes.guess_type('.xml')[0]
__textMimetype = 'text/plain'

_user_symbol = 'user'

_error_symbol = 'ERROR'
_isLoggedIn_symbol = 'isLoggedIn'
_user_symbol = 'USER'
_message_symbol = 'MSG'

def create_admin_user(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    from g import make_admin_user
    make_admin_user()
    _user = User.objects.get(username=_admin_username)
    ignore = ['_entity','_parent','_password']
    valueOf = lambda v:_utils.getAsSimpleDateStr(v,str(_utils.formatDjangoDateTimeStr())) if (ObjectTypeName.typeClassName(v) == 'datetime.datetime') else str(v) if (v != None) else None
    d = dict([(str(k),valueOf(v)) for k,v in _user.__dict__.iteritems() if (k not in ignore) and (v)])
    d[_air_version_symbol] = air_version[__air_id__]
    if (d[_air_version_symbol] == None):
	d[_api_symbol] = __apiMap__.asMap(noIgnore=True)
    d[_isLoggedIn_symbol] = _user.is_active and _user.is_authenticated() and (not _user.is_anonymous())
    d['REMOTE_ADDR'] = django_utils.get_from_META(request,'REMOTE_ADDR','')
    uname = str(_user)
    u = {
        'id':_user.id, 
        'is_active':_user.is_active, 
        'is_anonymous':_user.is_anonymous(),
        'is_authenticated':_user.is_authenticated(),
        'is_staff':_user.is_staff,
        'is_superuser':_user.is_superuser if (settings.IS_PRODUCTION_SERVER) else (_user.username == settings.SUPER_USER),
        'username':_user.username,
        #'groups':_user._get_groups(),
        #'permissions':_user._get_user_permissions(),
        'name':uname if (len(uname) > 0) else str(_user.username.split('@')[0]).capitalize()
    }
    handle_geolocation(request)
    u = get_starbucks_data(u,_user,__air_id__,parms)
    d[_user_symbol] = u
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def rest_handle_user_passwordChange(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    d = {}
    _user = get_user(request)
    try:
        username = django_utils.get_from_post(request,'username',default=None)
        password = django_utils.get_from_post(request,'password',default=None)
        password2 = django_utils.get_from_post(request,'password2',default=None)
        if username and password and password2:
            if (len(username) > 0):
                if (len(password) > 0) and (len(password2) > 0):
                    if (password == password2):
                        users = User.objects.filter(email=username.lower())
                        if users.count() > 0:
			    _user = users[0]
			    try:
				from users.registration import RegistrationManager
				rm = RegistrationManager()
				_error_symbol2 = _error_symbol+'2'
				__is__ = rm.reactivate_user(_user.email,password=password,data=d,error_symbol=_error_symbol2)
				if (not __is__):
				    d[_error_symbol] = 'WARNING: Cannot Reset your Password because you have no Registration(s) for this site.\nPlease Register again.'
				elif (d.has_key(_error_symbol2) and d[_error_symbol2]):
				    d[_error_symbol] = 'Your Account ReActivation Email has NOT been sent. (%s)' % (d[_error_symbol2])
				else:
				    d[_error_symbol] = 'Your Account ReActivation Email has been sent.'
			    except Exception, e:
				d[_error_symbol] = 'ERROR: %s' % (str(e))
                    else:
                        d[_error_symbol] = 'Invalid Password Change... Passwords do not match, please try again..'
                else:
                    d[_error_symbol] = 'Invalid Password Change... Passwords must both be something rather than one or the other being nothing, please try again..'
            else:
                d[_error_symbol] = 'Invalid Password Change... User name must be your email address, please try again.'
    except Exception, e:
        d[_error_symbol] = 'ERROR: %s' % (str(e))
    uname = str(_user)
    u = {
        'id':_user.id, 
        'is_active':_user.is_active, 
        'is_anonymous':_user.is_anonymous(),
        'is_authenticated':_user.is_authenticated(),
        'is_staff':_user.is_staff,
        'is_superuser':_user.is_superuser if (settings.IS_PRODUCTION_SERVER) else (_user.username == settings.SUPER_USER),
        'username':_user.username,
        'name':uname if (len(uname) > 0) else str(_user.username.split('@')[0]).capitalize()
    }
    json = dict_to_json(d)
    request.session[_error_symbol] = d[_error_symbol]
    request.session.save()
    return HttpResponseRedirect('/')

def rest_handle_user_register(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    d = {}
    _user = get_user(request)
    try:
        username = django_utils.get_from_post(request,'username',default=None)
        password = django_utils.get_from_post(request,'password',default=None)
        password2 = django_utils.get_from_post(request,'password2',default=None)
        fullname = django_utils.get_from_post(request,'fullname',default=None)
	first_name = django_utils.get_from_post(request,'first_name',default=None)
	last_name = django_utils.get_from_post(request,'last_name',default=None)
        if username and password and password2:
            if (len(username) > 0):
                if (len(password) > 0) and (len(password2) > 0):
                    if (password == password2):
			registrations = [aRegistration for aRegistration in RegistrationProfile.objects.all() if (aRegistration.user.username == username.lower())]
			if (len(registrations) > 0):
                            d[_error_symbol] = 'Invalid Registration, User Name already taken...  Please try again with a more unique User Name...'
                        else:
			    from users.registration import RegistrationManager
			    rm = RegistrationManager()
			    new_user = rm.create_inactive_user( username=username,
			                                        password=password,
			                                        email=username,
			                                        first_name='' if (first_name is None) else first_name if (fullname is None) else fullname.split()[0],
			                                        last_name='' if (last_name is None) else last_name if (fullname is None) else ' '.join(fullname.split()[1:]),
			                                        air_id=__air_id__,
			                                        domain_override=request.get_host() if (not settings.IS_PRODUCTION_SERVER) else ''
			                                        )
                            if new_user is None:
                                d[_error_symbol] = 'Invalid Registration, cannot complete your Registration at this time...'
                            else:
                                isRegisterComplete = True
                    else:
                        d[_error_symbol] = 'Invalid Registration... Passwords do not match, please try again..'
                else:
                    d[_error_symbol] = 'Invalid Registration... Passwords must both be something rather than one or the other being nothing, please try again..'
            else:
                d[_error_symbol] = 'Invalid Registration... User name must be your email address, please try again.'
    except Exception, e:
        d[_error_symbol] = 'ERROR: %s' % (str(e))
    uname = str(_user)
    u = {
        'id':_user.id, 
        'is_active':_user.is_active, 
        'is_anonymous':_user.is_anonymous(),
        'is_authenticated':_user.is_authenticated(),
        'is_staff':_user.is_staff,
        'is_superuser':_user.is_superuser if (settings.IS_PRODUCTION_SERVER) else (_user.username == settings.SUPER_USER),
        'username':_user.username,
        #'groups':_user._get_groups(),
        #'permissions':_user._get_user_permissions(),
        'name':uname if (len(uname) > 0) else str(_user.username.split('@')[0]).capitalize()
    }
    json = dict_to_json(d)
    request.session[_error_symbol] = d[_error_symbol]
    request.session.save()
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def rest_handle_get_user(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    _user = get_user(request)
    ignore = ['_entity','_parent','_password']
    valueOf = lambda v:_utils.getAsSimpleDateStr(v,str(_utils.formatDjangoDateTimeStr())) if (ObjectTypeName.typeClassName(v) == 'datetime.datetime') else str(v) if (v != None) else None
    d = dict([(str(k),valueOf(v)) for k,v in _user.__dict__.iteritems() if (k not in ignore) and (v)])
    d[_air_version_symbol] = air_version[__air_id__]
    if (d[_air_version_symbol] == None):
	d[_api_symbol] = __apiMap__.asMap(noIgnore=True)
    d[_isLoggedIn_symbol] = _user.is_active and _user.is_authenticated() and (not _user.is_anonymous())
    d['REMOTE_ADDR'] = django_utils.get_from_META(request,'REMOTE_ADDR','')
    uname = str(_user)
    u = {
        'id':_user.id, 
        'is_active':_user.is_active, 
        'is_anonymous':_user.is_anonymous(),
        'is_authenticated':_user.is_authenticated(),
        'is_staff':_user.is_staff,
        'is_superuser':_user.is_superuser if (settings.IS_PRODUCTION_SERVER) else (_user.username == settings.SUPER_USER),
        'username':_user.username,
        #'groups':_user._get_groups(),
        #'permissions':_user._get_user_permissions(),
        'name':uname if (len(uname) > 0) else str(_user.username.split('@')[0]).capitalize()
    }
    handle_geolocation(request)
    d[_user_symbol] = u
    json = dict_to_json(d)
    request.session[_error_symbol] = d[_error_symbol]
    request.session.save()
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def rest_handle_user_login(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    d = {}
    u = {}
    _user = get_user(request)
    isLoginComplete = False
    try:
        from django.contrib.auth import authenticate
        username = django_utils.get_from_post(request,'username',default=None)
        password = django_utils.get_from_post(request,'password',default=None)
        if username and password:
            _user_ = authenticate(username=username, password=password)
            if (_user_ is None) or (not _user_.check_password(password)):
                d[_error_symbol] = 'Invalid Login...'
            else:
                _user = _user_
		d[_isLoggedIn_symbol] = _user.is_active and _user.is_authenticated()
		if (d[_isLoggedIn_symbol]):
		    login(request,_user_)
		    isLoginComplete = True
		else:
		    isLoginComplete = False
		uname = str(_user)
		u = {
	            'id':_user.id, 
	            'session_key':request.session.session_key,
	            'is_active':_user.is_active, 
	            'is_anonymous':_user.is_anonymous(),
	            'is_authenticated':_user.is_authenticated(),
	            'is_staff':_user.is_staff,
	            'is_superuser':_user.is_superuser if (settings.IS_PRODUCTION_SERVER) else (_user.username == settings.SUPER_USER),
	            'username':_user.username,
	            'name':uname if (len(uname) > 0) else str(_user.username.split('@')[0]).capitalize()
	        }
		u['data'] = d
		request.session['user'] = u
		request.session.save()
		return HttpResponseRedirect('/')
    except Exception, e:
	d[_error_symbol] = _utils.formattedException(details=e)
	d[_isLoggedIn_symbol] = False
    return HttpResponseRedirect('/')

def handle_go_login(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    d = {}
    _user = get_user(request)
    user = request.session.get('user',_user)
    _error_ = request.session.get('_error_symbol',None)
    _is_ = (not user.is_anonymous()) and user.get('is_active',False) and user.get('is_authenticated',False)
    data[_error_symbol] = _error_
    try:
	del request.session[_error_symbol]
    except:
	pass
    request.session.save()
    return HttpResponseRedirect('/')

def handle_go_logout(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    d = {}
    _user = get_user(request)
    user = request.session.get('user',_user)
    _error_ = request.session.get('_error_symbol',None)
    data[_error_symbol] = _error_
    try:
	del request.session['user']
    except:
	pass
    logout(request)
    request.session.save()
    return HttpResponseRedirect('/')

def handle_go_home(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    d = {}
    _user = get_user(request)
    user = request.session.get('user',_user)
    _error_ = request.session.get(_error_symbol,None)
    if (_error_):
	del request.session[_error_symbol]
    request.session.save()
    return HttpResponseRedirect('/')

def handle_user_activation(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    from users.registration import RegistrationManager
    d = {}
    activation_key = django_utils.get_from_post(request,'x',django_utils.get_from_get(request,'x',''))
    rm = RegistrationManager()
    try:
	username,password,activation_key = rm.decode_activation_key(activation_key)
	isActivated = RegistrationProfile.objects.activate_user(username,password,activation_key)
    except:
	isActivated = False
    if (not isActivated): # this line may look funny but it works... leave it alone.
        d[_error_symbol] = 'Invalid Activation... You must Register or Reset your Password to get a new Activation Code.'
    else:
	d[_error_symbol] = 'Activation is Complete... You may Login to continue.'
    if (request.method.upper() == 'POST'):
	json = dict_to_json(d)
	return HttpResponse(content=json,mimetype=__jsonMimetype)
    request.session[_error_symbol] = d[_error_symbol]
    request.session.save()
    return HttpResponseRedirect('/')

