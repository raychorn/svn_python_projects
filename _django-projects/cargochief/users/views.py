from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, update_object
from django.template import RequestContext
from mimetypes import guess_type
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user, login

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

def create_admin_user(request,parms,browserAnalysis,__air_id__,__apiMap__):
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

def rest_handle_user_register(request,parms,browserAnalysis,__air_id__,__apiMap__):
    d = {}
    _user = get_user(request)
    try:
        username = django_utils.get_from_post(request,'username',default=None)
        password = django_utils.get_from_post(request,'password',default=None)
        password2 = django_utils.get_from_post(request,'password2',default=None)
        fullname = django_utils.get_from_post(request,'fullname',default=None)
        if username and password and password2:
            if (len(username) > 0):
                if (len(password) > 0) and (len(password2) > 0):
                    if (password == password2):
                        users = User.objects.filter(email=username.lower())
                        if users.count() > 0:
                            d[_error_symbol] = 'Invalid Registration, User Name already taken...  Please try again with a more unique User Name...'
                        else:
                            new_user = utils.RegistrationProfile.objects.create_inactive_user(username=username,
                                                                                               password=password,
                                                                                               email=username,
                                                                                               first_name='' if (fullname is None) else fullname.split()[0],
                                                                                               last_name='' if (fullname is None) else ' '.join(fullname.split()[1:]),
			                                                                       air_id=__air_id__,
			                                                                       domain_override=request.get_host() if (not settings.IS_PRODUCTION_SERVER) else ''
                                                                                               )
                            if new_user is None:
                                d[_error_symbol] = 'Invalid Registration...'
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
    u = get_starbucks_data(u,_user,__air_id__,parms)
    d[_user_symbol] = u
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

#def handle_geolocation(request):
    #post = django_utils.handle_json_post_vars(request)
    #geo = post['geo']
    #geolocation = None
    #if (geo): # and (ObjectTypeName.typeName(geo['latitude']) == 'float') and (ObjectTypeName.typeName(geo['longitude']) == 'float'):
	#gps = db.GeoPt(ensure_float(geo['latitude']),ensure_float(geo['longitude']))
	#geolocations = [s for s in models.Geolocation.all() if (s.gps == gps)]
	#if (len(geolocations) == 0):
	    #try:
		#geolocation = models.Geolocation(gps=gps)
		#try:
		    #if (geo['altitude']):
			#geolocation.altitude = ensure_float(geo['altitude'])
		#except Exception:
		    #pass
		#try:
		    #if (geo['heading']):
			#geolocation.heading = ensure_float(geo['heading'])
		#except Exception:
		    #pass
		#try:
		    #if (geo['horizontalAccuracy']):
			#geolocation.horizontalAccuracy = ensure_float(geo['horizontalAccuracy'])
		#except Exception:
		    #pass
		#try:
		    #if (geo['speed']):
			#geolocation.speed = ensure_float(geo['speed'])
		#except Exception:
		    #pass
		#try:
		    #if (geo['type']):
			#geolocation._type = str(geo['type'])
		#except Exception:
		    #pass
		#try:
		    #if (geo['verticalAccuracy']):
			#geolocation.verticalAccuracy = ensure_float(geo['verticalAccuracy'])
		#except Exception:
		    #pass
		#geolocation.save()
		#geolocations = [s for s in models.Geolocation.all() if (s.gps == gps)]
	    #except Exception, e:
		#logging.error(_utils.formattedException(details=e))
	#geolocation = geolocations[0]
    #return geolocation

def rest_handle_get_user(request,parms,browserAnalysis,__air_id__,__apiMap__):
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
    u = get_starbucks_data(u,_user,__air_id__,parms)
    d[_user_symbol] = u
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

#def rest_handle_user_login(request,parms,browserAnalysis,__air_id__,__apiMap__):
    #d = {}
    #u = {}
    #_user = get_user(request)
    #isLoginComplete = False
    #try:
        #from django.contrib.auth import authenticate
        #username = django_utils.get_from_post(request,'username',default=None)
        #password = django_utils.get_from_post(request,'password',default=None)
        #if username and password:
            #_user_ = authenticate(username=username, password=password)
            #if _user_ is None:
                #d[_error_symbol] = 'Invalid Login...'
            #else:
                #_user = _user_
                #login(request,_user)
		#if (__air_id__ == symbol_PDFXporter):
		    ## Remove all the data objects associated with this user who wants to begin again...
		    #statements = [s for s in models.Statement.all() if s.user.id == _user.id]
		    #for aStatement in statements:
			#texts = [t for t in models.AsciiText.all() if t.statement.id == aStatement.id]
			#for aText in texts:
			    #aText.delete()
			#items = [i for i in models.LineItem.all() if i.statement.id == aStatement.id]
			#for anItem in items:
			    #elements = [e for e in models.Element.all() if e.item.id == anItem.id]
			    #for anElement in elements:
				#anElement.delete()
			    #anItem.delete()
		#d[_isLoggedIn_symbol] = _user.is_active and _user.is_authenticated()
		#uname = str(_user)
		#u = {
	            #'id':_user.id, 
	            #'session_key':request.session.session_key,
	            #'is_active':_user.is_active, 
	            #'is_anonymous':_user.is_anonymous(),
	            #'is_authenticated':_user.is_authenticated(),
	            #'is_staff':_user.is_staff,
	            #'is_superuser':_user.is_superuser if (settings.IS_PRODUCTION_SERVER) else (_user.username == settings.SUPER_USER),
	            #'username':_user.username,
	            ##'groups':_user._get_groups(),
	            ##'permissions':_user._get_user_permissions(),
	            #'name':uname if (len(uname) > 0) else str(_user.username.split('@')[0]).capitalize()
	        #}
		#request.session['user'] = _user_
		#request.session.save()
		#geolocation = handle_geolocation(request)
		#isLoginComplete = True
		#if (__air_id__ == symbol_free4u) and (parms[-2] == symbol_starbucks):
		    #next_sunday = next_drawing()
		    ## Logout right away but report the login to avoid remaining logged-in for this specific application.
		    #u['starbucks'] = {}
		    #drawings = [s for s in models.StarbucksDrawing.all() if (s.date >= next_sunday+_utils.days_timedelta(-1))]
		    #logging.debug('%s.1 :: drawings[0]=%s' % (misc.funcName(),drawings[0]))
		    #starbucks = [s for s in models.StarbucksCheckIn.all() if (s.user.id == _user_.id) and (s.version == air_version[__air_id__]) and (s.drawing) and (s.drawing.date == drawings[0].date)]
		    #logging.debug('%s.2 :: len(starbucks)=%s' % (misc.funcName(),len(starbucks)))
		    #if (len(starbucks) == 0):
			#aStarbucksCheckIn = models.StarbucksCheckIn(user=_user_,version=air_version[__air_id__],gps=geolocation,drawing=drawings[0] if (len(drawings) > 0) else None)
			#aStarbucksCheckIn.save()
			#starbucks = [s for s in models.StarbucksCheckIn.all() if (s.user.id == _user_.id) and (s.version == air_version[__air_id__])]
		    #u['starbucks']['is_checkedin'] = (len(starbucks) > 0)
		    #starbucks = [s for s in models.StarbucksCheckIn.all() if s.version == air_version[__air_id__]]
		    #u['starbucks']['count'] = len(starbucks)
		    #from django.contrib.auth import logout
		    #logout(request)
    #except Exception, e:
	#d[_error_symbol] = _utils.formattedException(details=e)
	#d[_isLoggedIn_symbol] = False
    #d[_user_symbol] = u
    #json = dict_to_json(d)
    #return HttpResponse(content=json,mimetype=__jsonMimetype)

#def rest_handle_user_logout(request,parms,browserAnalysis,__air_id__,__apiMap__):
    #from django.contrib.auth import logout
    #d = {}
    #logout(request)
    #_user = get_user(request)
    #uname = str(_user)
    #u = {
        #'id':_user.id, 
        #'is_active':_user.is_active, 
        #'is_anonymous':_user.is_anonymous(),
        #'is_authenticated':_user.is_authenticated(),
        #'is_staff':_user.is_staff,
        #'is_superuser':_user.is_superuser if (settings.IS_PRODUCTION_SERVER) else (_user.username == settings.SUPER_USER),
        #'username':_user.username,
        ##'groups':_user._get_groups(),
        ##'permissions':_user._get_user_permissions(),
        #'name':uname if (len(uname) > 0) else str(_user.username.split('@')[0]).capitalize()
    #}
    #d[_user_symbol] = u
    #json = dict_to_json(d)
    #return HttpResponse(content=json,mimetype=__jsonMimetype)

#def handle_user_activation(request,parms,browserAnalysis,__air_id__,__apiMap__):
    #d = {}
    #username = django_utils.get_from_post(request,'username','')
    #activation_key = django_utils.get_from_post(request,'activation_key','')
    #_activation_key = django_utils.get_from_get(request,'activation','')
    #isActivated = models.RegistrationProfile.objects.activate_user(username,activation_key)
    #if (not isActivated): # this line may look funny but it works... leave it alone.
        #d[_error_symbol] = 'Invalid Activation... You must Register again to get a new Activation Code.'
    #json = dict_to_json(d)
    #return HttpResponse(content=json,mimetype=__jsonMimetype)

#def handle_user_activation_link(request,parms,browserAnalysis,__air_id__,__apiMap__):
    #from vyperlogix.products import keys
    #d = {}
    #activation_key = keys.decode(django_utils.get_from_post_or_get(request,'x','')).split(';')
    #isActivated = models.RegistrationProfile.objects.activate_user(activation_key[0],activation_key[-1])
    #d[_error_symbol] = ''
    #if (not isActivated): # this line may look funny but it works... leave it alone.
        #d[_error_symbol] = 'Invalid Activation... You must Register again to get a new Activation Code.'
    #json = dict_to_json(d)
    #_data = {
        #'message':d[_error_symbol] if (len(d[_error_symbol]) > 0) else 'Your Activation is complete. You may begin Checking-In to Win !'
    #}
    #return HttpResponseRedirect('http://www.vyperlogix.com/free-4u/activation.html?message=%s' % (urllib.quote_plus(_data['message'] if (_data.has_key('message')) else '')))

#def handle_user_reactivation(request,parms,browserAnalysis,__air_id__,__apiMap__):
    #from django.contrib.auth import authenticate
    #d = {}
    #is_okay_to_proceed = False
    #username = django_utils.get_from_post(request,'username','')
    #password = django_utils.get_from_post(request,'password','')
    #if username and password:
	#_user_ = authenticate(username=username, password=password)
	#if _user_ is None:
	    #d[_error_symbol] = 'Invalid Request... You must Register again using a your email address to get an Activation Code.'
	#else:
	    #is_okay_to_proceed = True
    #elif (username):
	#is_okay_to_proceed = True
    #if (is_okay_to_proceed):
	#isActivated = models.RegistrationProfile.objects.reactivate_user(username,__air_id__)
	#if (not isActivated):
	    #d[_error_symbol] = 'Invalid Request... You must Register again using a your email address to get an Activation Code.'
	#else:
	    #d[_message_symbol] = 'Your new Activation Code has been sent to your email address.'
    #json = dict_to_json(d)
    #return HttpResponse(content=json,mimetype=__jsonMimetype)

#def handle_updater_download(request,parms,browserAnalysis,__air_id__,__apiMap__):
    #d = updater.get_data(air_version[__air_id__],updater_domainName,__air_id__)
    #json = dict_to_json(d)
    #return HttpResponse(content=json,mimetype=__jsonMimetype)

#def handle_page_parser(request,parms,browserAnalysis,__air_id__,__apiMap__):
    #d = {}
    #_user = request.session['user'] if (request.session.has_key('user')) else None
    #_uid = django_utils.get_from_post(request,'userid')
    #if (_user) and (_uid == _user.id):
	#_id = django_utils.get_from_post(request,'id')
	#texts = [t for t in models.AsciiText.all() if t.id == _id]
	#if (len(texts) > 0):
	    #_items_ = []
	    #for t in texts:
		#for item in t._items:
		    #_items_.append(item)
	    #d['items'] = _items_
	#else:
	    #d['error'] = 'WARNING: Cannot locate the textual information.'
	    #d['success'] = False
    #else:
	#d['error'] = 'WARNING: User Authentication Error.'
	#d['success'] = False
    #json = dict_to_json(d)
    #return HttpResponse(content=json,mimetype=__jsonMimetype)

#def handle_file_upload(request,parms,browserAnalysis,__air_id__,__apiMap__):
    #import StringIO
    #import time
    #d = {}
    #f = request.FILES['file']
    #_user = request.session['user'] if (request.session.has_key('user')) else None
    #_uid = django_utils.get_from_post(request,'userid')
    #if (_user) and (_uid == _user.id):
	## f.name has the name of the uploaded file...
	#b = StringIO.StringIO()
	#try:
	    #for chunk in f.chunks():
		#b.write(chunk)
	    #statements = [s for s in models.Statement.all() if s.user.id == _uid]
	    #statement = models.Statement(user=_user) if (len(statements) == 0) else statements[0]
	    #statement.save()
	    #parser = BankStatementPDFParser()
	    #pdfReader = PdfFileReader(b)
	    #d['DocInfo'] = pdfReader.getDocumentInfo()
	    #d['NumPages'] = pdfReader.getNumPages()
	    #d['pages'] = []
	    #beginTime = time.time()
	    #for pageNo in xrange(0,d['NumPages']):
		#aPage = pdfReader.getPage(pageNo)
		#t = aPage.extractText()
		##parser.parse(statement,t)
		#anAsciiText = models.AsciiText(statement=statement,items=t,num=pageNo+1)
		#anAsciiText.save()
		#d['pages'].append(anAsciiText.id)
	    #d['etMS'] = time.time() - beginTime
	    #d['filename'] = f.name
	    #d['success'] = True
	#except Exception, e:
	    #info_string = _utils.formattedException(details=e)
	    #d['error'] = info_string
	    #d['success'] = False
    #else:
	#d['error'] = 'WARNING: User Authentication Error.'
	#d['success'] = False
    #json = dict_to_json(d)
    #return HttpResponse(content=json,mimetype=__jsonMimetype)

#def handle_user_chgpassword(request,parms,browserAnalysis,__air_id__,__apiMap__):
    #from django.contrib.auth import authenticate
    #from vyperlogix.products import keys
    #d = {}
    #_user = get_user(request)
    #isRegisterComplete = False
    #try:
        #username = django_utils.get_from_post(request,'username',default=None)
        #old_password = django_utils.get_from_post(request,'old_password',default=None)
        #password = django_utils.get_from_post(request,'password',default=None)
        #password2 = django_utils.get_from_post(request,'password2',default=None)
        #if username and password and password2:
            #if (len(username) > 0):
		#_user_ = authenticate(username=username, password=old_password)
		#if _user_ is None:
		    #d[_error_symbol] = 'Invalid Request... You must Register again using a your email address to get a new Activation Code.'
		#else:
		    #if (len(password) > 0) and (len(password2) > 0):
			#if (password == password2):
			    #users = User.all().filter('email',username.lower())
			    #if users.count() > 0:
				#models.RegistrationProfile.objects.send_passwordChg_email(users[0],keys.encode(old_password),keys.encode(password),air_id=__air_id__,domain_override=request.get_host() if (not settings.IS_PRODUCTION_SERVER) else '')
			    #else:
				#d[_error_symbol] = 'Invalid Request...'
			#else:
			    #d[_error_symbol] = 'Invalid Request... Passwords do not match, please try again..'
            #else:
                #d[_error_symbol] = 'Invalid Request... User name must be your email address, please try again.'
    #except Exception, e:
        #d[_error_symbol] = 'ERROR: %s' % (str(e))
    #json = dict_to_json(d)
    #return HttpResponse(content=json,mimetype=__jsonMimetype)

#def handle_user_passwordChg(request,parms,browserAnalysis,__air_id__,__apiMap__):
    #from django.contrib.auth import authenticate
    #from vyperlogix.products import keys
    #d = {}
    #_user = get_user(request)
    #try:
        #userid = parms[1]
        #old_password = keys.decode(parms[2])
        #new_password = keys.decode(parms[3])
	#users = [u for u in User.all() if (u.id == userid)]
	#if len(users) == 0:
	    #d[_error_symbol] = 'Invalid Request, Please Register to get a valid User Account...'
	#else:
	    #aUser = users[0]
	    #aUser.set_password(new_password)
	    #aUser.save()
	    #d[_error_symbol] = 'INFO: Your password has been changed.'
    #except Exception, e:
        #d[_error_symbol] = 'ERROR: %s' % (str(e))
    #return HttpResponseRedirect('http://www.vyperlogix.com/free-4u/activation.html?message=%s' % (urllib.quote_plus(d[_error_symbol] if (d.has_key(_error_symbol)) else '')))

#def handle_send_email(request,parms,browserAnalysis,__air_id__,__apiMap__):
    #d = {}
    #_user = get_user(request)

    #_from = django_utils.get_from_post(request,'from','')
    #_to = django_utils.get_from_post(request,'to','')
    #_subject = django_utils.get_from_post(request,'subject','')
    #_body = django_utils.get_from_post(request,'body','')
    #logging.debug('handle_send_email.1 --> from=%s, to=%s, subject=%s, message=%s' % (_from,_to,_subject,_body))
    #if (len(_from) > 0) and (len(_to) > 0) and (len(_subject) > 0) and (len(_body) > 0):
	#d[_error_symbol] = queue_email(_from,_to,_subject,_body,_body,__air_id__,parms[-2])
    #elif (__air_id__ == symbol_free4u) and (parms[-2] == symbol_starbucks):
	#next_sunday = next_drawing()
	#drawings = [s for s in models.StarbucksDrawing.all() if (s.date >= next_sunday+_utils.days_timedelta(-1))]
	#if (len(drawings) > 0):
	    #emails = [s for s in models.StarbucksFeedback.all() if (s.checkin.user == _user) and (s.checkin.version == air_version[__air_id__]) and (s.checkin.drawing == drawings[0])]
	#else:
	    #emails = [s for s in models.StarbucksFeedback.all() if (s.checkin.user == _user) and (s.checkin.version == air_version[__air_id__])]
	#if (len(emails) == 0):
	    #fromName = django_utils.get_from_post(request,'fromName','')
	    #email = django_utils.get_from_post(request,'email','')
	    #msg = django_utils.get_from_post(request,'msg','')
	    #if (_user._is_active and (_user.email == email) and (fromName) and (len(fromName) > 0) and (msg) and (len(msg) > 0)):
		#models.RegistrationProfile.objects.send_problem_email(fromName,email,msg,air_id=__air_id__,domain_override=request.get_host() if (not settings.IS_PRODUCTION_SERVER) else '')
	    #else:
		#d[_error_symbol] = 'Cannot send an email because you are not authorized to do so at this time.'
	#else:
	    #d[_error_symbol] = 'Please wait until the next drawing before trying to provide some feedback.'
    
    #json = dict_to_json(d)
    #return HttpResponse(content=json,mimetype=__jsonMimetype)

#def handle_email_task(request,parms,browserAnalysis,__air_id__,__apiMap__):
    #d = {}
    #_user = get_user(request)

    #results = ''
    #info_string = '%s :: 1. parms=(%s)' % (__name__,parms)
    #results += info_string + '\n\n'
    #_id = parms[-3]
    #emails = [s for s in models.EMailQueue.all() if s.id == _id]
    #info_string = '%s :: 2. len(emails)=(%s)' % (__name__,len(emails))
    #results += info_string + '\n\n'
    #if (len(emails) > 0):
	#from google.appengine.api import mail
        #anEmail = emails[0]
        #info_string = '%s :: 3. emails[0]=(%s)' % (__name__,anEmail)
        #results += info_string + '\n\n'
	#try:
	    #mail.send_mail(sender="%s" % (anEmail.email_from),
		          #to=anEmail.email_to,
		          #subject=anEmail.email_subject,
		          #body=anEmail.email_body,
		          #html=anEmail.email_altbody)
	    #anEmail.delete()
	    #_today = today()
	    #counts = [s for s in models.EMailStats.all() if s.date < _today]
	    #if (len(counts) > 0):
		#for aCount in counts:
		    #aCount.delete()
	    #counts = [s for s in models.EMailStats.all() if s.date == _today]
	    #if (len(counts) > 0):
		#aCount = counts[0]
		#aCount.count += 1
	    #else:
		#aCount = models.EMailStats(count=1,date=_today)
	    #aCount.save()
	    #d[_error_symbol] = results
	#except Exception, e:
	    #d[_error_symbol] = 'ERROR: %s' % (str(e))
    
    #json = dict_to_json(d)
    #return HttpResponse(content=json,mimetype=__jsonMimetype)

#def handle_get_form(request,parms,browserAnalysis,__air_id__,__apiMap__):
    #from g import xml_to_python, xml_to_json, xml2json, json_to_python
    #d = {}
    #_user = get_user(request)
    #if (_user._is_active):
        #form = forms.SmartForm(data=request.POST, files=request.FILES)
	#context = RequestContext(request)
        #context['form'] = form
        #_content = django_utils.compressContent(django_utils.render_from_string(__form__,context=context))
	#_json = xml2json(_content)
	#d['form'] = json_to_python(django_utils.compressContent(_json))
    #else:
        #d[_error_symbol] = 'Cannot respond with a form at this time.'
    #json = dict_to_json(d)
    #return HttpResponse(content=json,mimetype=__jsonMimetype)

#def handle_get_admob(request,parms,browserAnalysis,__air_id__,__apiMap__):
    #from g import xml_to_python, xml_to_json, xml2json, json_to_python
    #from vyperlogix.django.admob import admob_ad
    #d = {}
    #_user = get_user(request)
    #admob_dict = lists.HashedFuzzyLists2()
    #admob_dict["admob_site_id"] = django_utils.get_from_post(request,'admob_site_id','')
    #admob_dict["admob_postal_coode"] = django_utils.get_from_post(request,'admob_postal_coode','')
    #admob_dict["admob_area_code"] = django_utils.get_from_post(request,'admob_area_code','')
    #admob_dict["admob_coordinates"] = django_utils.get_from_post(request,'admob_coordinates','')
    #admob_dict["admob_gender"] = django_utils.get_from_post(request,'admob_gender','')
    #admob_dict["admob_keywords"] = django_utils.get_from_post(request,'admob_keywords','')
    #admob_dict["admob_search"] = django_utils.get_from_post(request,'admob_search','')
    #admob_dict["admob_siteID"] = django_utils.get_from_post(request,'admob_siteID','')
    #admob_dict["admob_mode"] = django_utils.get_from_post(request,'admob_mode',"") # test ?
    #admob_dict["alternate_content"] = __alternate_admob_content__
    #ad_content = admob_ad.admob_ad(request, admob_dict)
    #logging.info(ad_content)
    #if (not settings.IS_PRODUCTION_SERVER) and (admob_dict["admob_mode"] == 'test'):
	#ad_content = ad_content.replace('</a>','<img src="http://www.near-by.info/downloads.ezajax.us/images/ezAJAX Logo 08-17-2006a (125x125).gif"/></a>')
    #_json = xml2json(ad_content)
    #d = json_to_python(django_utils.compressContent(_json))
    #_json = dict_to_json(d)
    #return HttpResponse(content=_json,mimetype=__jsonMimetype)

def handle_get_smaato(request,parms,browserAnalysis,__air_id__,__apiMap__):
    from g import xml_to_python, xml_to_json, xml2json, json_to_python
    from vyperlogix.django.smaato import smaato_ad
    d = {}
    _user = get_user(request)
    ad_content = smaato_ad.smaato_ad(request, __alternate_admob_content__)
    logging.info(ad_content)
    _json = xml2json(ad_content)
    d = json_to_python(django_utils.compressContent(_json))
    _json = dict_to_json(d)
    return HttpResponse(content=_json,mimetype=__jsonMimetype)


