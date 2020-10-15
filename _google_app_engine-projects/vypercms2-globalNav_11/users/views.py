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

from vyperlogix.enum.Enum import Enum

__mimetype = mimetypes.guess_type('.html')[0]

_title = 'Vyper Logix Corp, The 21st Century Python Company'

__product__ = 'Vyper-Users&trade;'
__version__ = '1.0.0.0'

__content__ = '''{{ content }}'''

__approved__ = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
		<title>Account {{ status }} !</title>
	</head>
	<body>
		<p>Congrats, your brand new shiny User Account has been <b><u>{{ status }}</u> !</b></p>
		<p>You may now proceed to <a href="{{ link }}" target="_blank">Login</a> to begin using your services.</p>
	</body>
</html>
'''

__not_approved__ = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
		<title>Account {{ status }} !</title>
	</head>
	<body>
		<p>We are sorry, your brand new shiny User Account has <b><u>NOT</u></b> been <b><u>{{ status }}</u> !</b></p>
		<p>Double check your email for the Activation Notice, you MUST click on the Activation Link to begin using your services or Register again using a different email address.</p>
	</body>
</html>
'''

__link_to_AdminTool__ = 'http://www.vyperlogix.com/admin-tool/'

def python_to_json(obj):
    from django.utils import simplejson
    
    json = simplejson.encode(obj)
    
    return json.replace('\n','')

def delete_users():
    users = models.User.all()
    for aUser in users.__iter__():
        aUser.delete()

def get_user_account(uid='',username='',password='',isApproved=False,isAdmin=False):
    def default_user_account():
        return ('raychorn','103136174d231aabe18feaf9afc92f',True,True) # peekab00 is the password encoded by as3.
    #delete_users()
    users = models.User.all()
    if (users.count() < 1):
        import uuid
        username,password,isApproved,isAdmin = default_user_account()
        aUser = models.User.create(str(uuid.uuid4()),username,password,'Admin',False,isApproved,isAdmin)
        aUser.save()
        users = models.User.all()
    if (len(str(uid)) >  0):
        users = users.filter('uid',uid).filter('isApproved',isApproved)
    else:
        users = users.filter('username',username).filter('password',password).filter('isApproved',True).filter('isloggedin',False)
    return users

def restLogin(request,parms):
    s_response = ''
    status = {'loggedin':False,'isAdmin':False,'success':False,'username':'UNKNOWN'}
    username = parms[-3]
    password = parms[-2]
    users = get_user_account(username=username,password=password)
    if (users.count() == 1):
        try:
            aUser = users[0]
            aUser.loggedin = _utils.today_localtime()
            aUser.isloggedin = True
            status['isAdmin'] = aUser.isAdmin
            aUser.save()
            status['loggedin'] = True
            status['success'] = True
            status['username'] = aUser.username
        except:
            pass
    s_response = python_to_json(status)
    return s_response

def restLogout(request,parms):
    s_response = ''
    status = {'loggedin':True}
    uid = parms[-1]
    users = get_user_account(uid=uid)
    if (users.count() == 1):
        try:
            aUser = users[0]
            aUser.loggedin = _utils.today_localtime()
            aUser.isloggedin = False
            aUser.save()
            status['loggedin'] = False
        except:
            pass
    s_response = python_to_json(status)
    return s_response

def createNewUserConfirmation(uid):
    return '/users/register/confirm/%s/' % (uid)

def send_registration_email(username,uid):
    from google.appengine.api import mail
    if not mail.is_email_valid(username):
        return False
    else:
        confirmation_url = createNewUserConfirmation(uid)
        sender_address = "Vyper Logix Support <vyperlogix@gmail.com>"
        subject = "Confirm Your Registration Request"
        body = """
Thank you for Requesting a User Account!

Your User Account will be Approved once you confirm your email address by clicking on the link below:

%s
""" % confirmation_url
        mail.send_mail(sender_address, username, subject, body, html=body)
        logging.info('confirmation_url=%s' % (confirmation_url))
    return True

def send_registration_notification_email(username):
    from google.appengine.api import mail
    if not mail.is_email_valid(username):
        return False
    else:
        sender_address = "New User <%s>" % (username)
        subject = "New User Account Registration Approved"
        body = """
New User Account !

"""
        mail.send_mail(sender_address, 'vyperlogix@gmail.com', subject, body)
    return True

def restRegisterNewUser(request,parms):
    s_response = ''
    status = {'success':False}
    username = parms[-4]
    password = parms[-3]
    fullname = parms[-2]
    try:
        import uuid
        uid = str(uuid.uuid4())
        isUserDjangoAdmin = False #userCheckDjangoAdmin(username)
        aUser = models.User.create(uid=uid,username=username,fullname=fullname,password=password,isloggedin=False,isApproved=False,isAdmin=False)
        aUser.isApproved = isUserDjangoAdmin
        aUser.isAdmin = isUserDjangoAdmin
        aUser.save()
        status['success'] = True
        send_registration_email(username,uid)
        send_registration_notification_email(username)
    except unique.UniqueConstraintViolatedError, e:
        status['success'] = False
    except Exception, e:
        status['success'] = False
        status['Exception'] = _utils.formattedException(e)
    s_response = python_to_json(status)
    return s_response

def userRegisterConfirmation(request,parms):
    status = {'success':False}
    uid = parms[-1]
    users = get_user_account(uid=uid,isApproved=False)
    if (users.count() == 1):
        try:
            aUser = users[0]
            aUser.loggedin = _utils.today_localtime()
            aUser.isApproved = True
            aUser.isloggedin = False
            aUser.save()
            users = get_user_account(uid=uid)
            status['success'] = True
        except:
            pass
    return status

def usernameDjangoAdmin():
    from vyperlogix.products import keys
    return keys.decode('F2E1F9E3E8EFF2EE')

def passwordDjangoAdmin():
    from vyperlogix.products import keys
    return keys.decode('F0E5E5EBE1E2B0B0')

def emailDjangoAdmin():
    from vyperlogix.products import keys
    return keys.decode('F2E1F9E3E8EFF2EEC0E7EDE1E9ECAEE3EFED')

def userCheckDjangoAdmin(email):
    from django.contrib.auth.models import User
    users = User.all().filter('email',email).filter('is_staff',True).filter('is_active',True).filter('is_superuser',True)
    return (users.count() == 1)

def userCheckAdmin(request,parms):
    from vyperlogix.products import keys
    from django.contrib.auth.models import User
    s_response = ''
    status = {'success':False}
    users = User.all()
    if (users.count() == 0):
        aUser = User(username=usernameDjangoAdmin())
        aUser.set_password(passwordDjangoAdmin())
        aUser.is_staff = True
        aUser.is_active = True
        aUser.is_superuser = True
        aUser.email = emailDjangoAdmin()
        aUser.save()
        users = User.all()
        status['success'] = (users.count() == 1)
    s_response = python_to_json(status)
    return s_response


def default(request,path):
    try:
        s_response = ''
        __error__ = ''
        
        parms = django_utils.parse_url_parms(request)

        isRestLogin = (len(parms) > 0) and (parms[0:3] == [u'rest', u'users', u'login']) # /rest/users/login/username/password/
        isRestLogout = (len(parms) > 0) and (parms[0:3] == [u'rest', u'users', u'logout']) # /rest/users/logout/uid/
        isRestRegisterNewUser = (len(parms) > 0) and (parms[0:3] == [u'rest', u'users', u'register']) # /rest/users/register/username/password/fullname/
        isUserRegisterConfirmation = (len(parms) > 0) and (parms[0:3] == [u'users', u'register', u'confirm']) # /users/register/confirm/uid/
        isCheckAdminUser = (len(parms) > 0) and (parms[0:3] == [u'users', u'check', u'admin']) # /users/check/admin/
        #isRestDomains = (path == 'domains/') # /users/domains/
        mimetype = mimetypes.guess_type('.json')[0]
        if (isRestLogin):
            s_response = restLogin(request,parms)
        elif (isRestLogout):
            s_response = restLogout(request,parms)
        elif (isRestRegisterNewUser):
            s_response = restRegisterNewUser(request,parms)
        elif (isUserRegisterConfirmation):
            s_response = userRegisterConfirmation(request,parms)
            t = loader.get_template_from_string(__approved__ if (s_response['success']) else __not_approved__)
            c = {'link':__link_to_AdminTool__,'status':'Approved'}
            content = t.render(Context(c,autoescape=False))
            return HttpResponse(content.replace('\n',''), mimetype=__mimetype)
        elif (isCheckAdminUser):
            s_response = userCheckAdmin(request,parms)
        else:
            __error__ = 'INVALID Request.'
            data = {'success':False,'message':__error__}
            s_response = python_to_json(data)
        t = loader.get_template_from_string(__content__)
        c = {'content':s_response}
        content = t.render(Context(c,autoescape=False))
        return HttpResponse(content,mimetype=mimetype)
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        status = {'error':','.join(info_string.split('\n'))}
        s_response = python_to_json(status)
        return HttpResponse(s_response, mimetype=__mimetype)

