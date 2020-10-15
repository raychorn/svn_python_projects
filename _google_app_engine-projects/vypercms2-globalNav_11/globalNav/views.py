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

import re

import mimetypes

from settings import TEMPLATE_DIRS,USE_I18N

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc import _utils
from vyperlogix.django import django_utils

from vyperlogix.enum.Enum import Enum

__mimetype = 'html/text'

_title = 'Vyper Logix Corp, The 21st Century Python Company'

__product__ = 'Vyper-Menu&trade;'
__version__ = '1.0.0.0'

__content__ = '''{{ content }}'''

__isCrossDomain_xml__ = '''
<?xml version="1.0"?>
<!DOCTYPE cross-domain-policy SYSTEM "http://www.adobe.com/xml/dtds/cross-domain-policy.dtd">

<cross-domain-policy>
	<site-control permitted-cross-domain-policies="all"/>
	<allow-access-from domain="*" secure="false"/>
	<allow-http-request-headers-from domain="*" headers="*" secure="false"/>
</cross-domain-policy>
'''

class MenuStates(Enum):
    loggedIn = 'loggedIn'
    loggedOut = 'loggedOut'
    
is_menu_state_logged_in = lambda e:e.value == MenuStates.loggedIn.value
is_menu_state_logged_out = lambda e:e.value == MenuStates.loggedOut.value

def python_to_json(obj):
    from django.utils import simplejson
    
    json = simplejson.dumps(obj)
    
    return json.replace('\n','')

def delete_states():
    states = models.State.all()
    for aState in states.__iter__():
        aState.delete()

def get_state(state_handle):
    state_handle = state_handle.value if (ObjectTypeName.typeClassName(state_handle) == 'vyperlogix.enum.Enum.EnumInstance') else state_handle
    #delete_states()
    states = models.State.all()
    if (states.count() != 2):
        aState = models.State(state='loggedIn')
        aState.save()
        aState = models.State(state='loggedOut')
        aState.save()
        states = models.State.all()
    return states.filter('state',state_handle)

def delete_users():
    users = models.User.all()
    for aUser in users.__iter__():
        aUser.delete()

def delete_menus():
    menus = models.Json.all()
    for aMenu in menus.__iter__():
        aMenu.delete()

def get_user_account(user_handle):
    toks = user_handle.split(',')
    try:
        _name, _password = toks
    except:
        _name, _password = ('raychorn','password')
    #delete_users()
    users = models.User.all()
    if (users.count() < 1):
        aUser = models.User(uid=_name,name='Ray Horn',password=_password)
        aUser.save()
        users = models.User.all()
    return users.filter('uid',_name).filter('password',_password)

def restGetMenuCount(request,parms):
    s_response = ''
    states = get_state(MenuStates(parms[-3]).value)
    users = get_user_account(parms[-2])
    is_returning_json = (parms[-1] == 'json')
    num = 0
    if (users.count() > 0) and (states.count() > 0):
        num = models.Json.all().filter('user',users[0]).filter('state',states[0]).count()
    data = {'count':num}
    s_response = python_to_json(data)
    return s_response

def restGetMenus(request,parms):
    s_response = ''
    users = get_user_account(parms[-2])
    states = get_state(MenuStates(parms[-3]).value)
    menus = []
    if (users.count() > 0) and (states.count() > 0):
        selections = models.Menu.all().filter('user',users[0]).filter('state',states[0])
        aUuid = selections[0].json.uuid if (selections.count() > 0) else ''
        menus = [{'name':aMenu.name + ' Modified by: Ray Horn on mm-dd-yyyy HH:MM:SS PM','state':aMenu.state.state,'uuid':aMenu.uuid,'selected':'true' if (aMenu.uuid == aUuid) else 'false'} for aMenu in models.Json.all().filter('user',users[0]).filter('state',states[0]).order('name')]
    names = {}
    for aMenu in menus:
        names[aMenu['name']] = aMenu
    menus = [names[k] for k in misc.sort(names.keys())]
    s_response = python_to_json(menus)
    return s_response

def restNewMenu(request,parms):
    name = parms[-5]
    uuid = parms[-4]
    states = get_state(MenuStates(parms[-3]).value)
    users = get_user_account(parms[-2])
    _content = ''
    if (users.count() > 0) and (states.count() > 0):
        if (request.POST.has_key('data')) and (len(request.POST['data']) > 0):
            _json = request.POST['data']
            if ( (isinstance(_json,str)) or (isinstance(_json,unicode)) ) and (states.count() > 0):
                aMenu = models.Json(name=name,json=_json,state=states[0],uuid=uuid,user=users[0])
                aMenu.save()
                _content = aMenu.json
    return _content

def restGetMenu(request,parms):
    users = get_user_account(parms[-2])
    states = get_state(MenuStates(parms[-3]).value)
    uuid = parms[-4]
    _content = ''
    if (users.count() > 0) and (states.count() > 0):
        menus = models.Json.all().filter('uuid',uuid).filter('user',users[0]).filter('state',states[0])
        if (menus.count() > 0):
            aMenu = menus[0]
            _content = aMenu.json
    return _content

def restSetMenuSelection(request,parms):
    value = {'success':True}
    s_response = python_to_json(value)
    return s_response

def restSetMenu(request,parms):
    try:
        users = get_user_account(parms[-2])
        states = get_state(MenuStates(parms[-3]).value)
        uuid = parms[-4]
        status = {'success':False,'uuid':uuid}
        if (users.count() > 0) and (states.count() > 0):
            menus = models.Json.all().filter('uuid',uuid).filter('user',users[0]).filter('state',states[0])
            if (menus.count() > 0):
                aMenu = menus[0]
                aMenu.json = request.POST['data']
                aMenu.save()
                status['success'] = True
    except Exception, e:
        status['success'] = False
    s_response = python_to_json(status)
    return s_response

def default(request):
    try:
        s_response = ''
        __error__ = ''
        
        parms = django_utils.parse_url_parms(request)
        isRestGetMenuCount = (len(parms) > 0) and (parms[0:4] == [u'rest', u'get', u'menu', u'count'])
        isRestGetMenus = (len(parms) > 0) and (parms[0:3] == [u'rest', u'get', u'menus'])
        isRestNewMenus = (len(parms) > 0) and (parms[0:3] == [u'rest', u'new', u'menu'])
        isRestGetMenu = (len(parms) > 0) and (parms[0:3] == [u'rest', u'get', u'menu'])
        isRestSetMenuSelection = (len(parms) > 0) and (parms[0:3] == [u'rest', u'set', u'menu-selection'])
        isRestSetMenu = (len(parms) > 0) and (parms[0:3] == [u'rest', u'set', u'menu'])
        isRestDeleteMenus = (len(parms) > 0) and (parms[0:3] == [u'delete', u'menus'])
        isRestDeleteMenus = (len(parms) > 0) and (parms[0:3] == [u'delete', u'menus'])
        isCrossDomain_xml = (len(parms) > 0) and (parms[0:1] == [u'crossdomain.xml'])

        if (isRestGetMenuCount):
            s_response = restGetMenuCount(request,parms)
        elif (isRestGetMenus):
            s_response = restGetMenus(request,parms)
        elif (isRestNewMenus):
            s_response = restNewMenu(request,parms)
        elif (isRestGetMenu):
            s_response = restGetMenu(request,parms)
        elif (isRestSetMenuSelection):
            s_response = restSetMenuSelection(request,parms)
        elif (isRestSetMenu):
            s_response = restSetMenu(request,parms)
        elif (isRestDeleteMenus):
            delete_menus()
        elif (isCrossDomain_xml):
            mimetype = mimetypes.guess_type('.xml')[0]
            return HttpResponse(__isCrossDomain_xml__, mimetype=mimetype)
        else:
            __error__ = 'INVALID Request.'
            data = {'success':False,'message':__error__}
            s_response = python_to_json(data)
        t = loader.get_template_from_string(__content__)
        c = {'content':s_response}
        content = t.render(Context(c,autoescape=False))
        return HttpResponse(content,mimetype=__mimetype)
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        mimetype = mimetypes.guess_type('.html')[0]
        return HttpResponse('<font color="red"><small>%s</small></font>'%('<br/>'.join(info_string.split('\n'))), mimetype=mimetype)

