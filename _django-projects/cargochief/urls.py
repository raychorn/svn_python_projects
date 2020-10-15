# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
#from images.views import image
from django.contrib import admin

from django.template import TemplateDoesNotExist
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

admin.autodiscover()

from django.conf import settings

import os,sys
import uuid
import logging

from vyperlogix.misc import _utils
from vyperlogix.classes.SmartObject import SmartObject, SmartFuzzyObject
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.misc import ObjectTypeName

from vyperlogix.django import django_utils
from vyperlogix.django.static import django_static

has_users = False
try:
    from users.views import create_admin_user, rest_handle_user_register
    from users.views import rest_handle_get_user #, rest_handle_user_login, rest_handle_user_logout, handle_user_activation, handle_user_reactivation, handle_user_activation_link
    #from users.views import handle_user_chgpassword, handle_file_upload, handle_updater_download, handle_page_parser, handle_send_email, handle_get_form, handle_get_admob, handle_get_smaato, handle_email_task, handle_user_passwordChg
    has_users = True
except ImportError, e:
    info_string = _utils.formattedException(details=e)
    logging.error('Cannot import users functions because "%s".' % (info_string))

from users.g import air_id, air_version, air_domain, updater_domainName, current_site

from views.default import rest_handle_get_zipcode, rest_handle_get_regions, handle_best_quote2, handle_best_quote2_add_stop, handle_best_quote2_drop_stop, get_best_quote2_stops, handle_best_quote2_get_stops, handle_best_quote2_drop_stops

__api_dict__1 = {}
if (has_users):
    __api_dict__1['create_admin_user'] = SmartFuzzyObject({'url':'/create/admin/user/','func':create_admin_user,'isPostRequired':False})
    __api_dict__1['register_user'] = SmartFuzzyObject({'url':'/register/user/','func':rest_handle_user_register,'isPostRequired':True,'fields':['username','password','password2','fullname']})
    __api_dict__1['get_user'] = SmartFuzzyObject({'url':'/get/user/','func':rest_handle_get_user,'isPostRequired':True})
    __api_dict__1['get_zipcode'] = SmartFuzzyObject({'url':'/get/zipcode/','func':rest_handle_get_zipcode,'isPostRequired':True})
    __api_dict__1['get_regions'] = SmartFuzzyObject({'url':'/get/regions/','func':rest_handle_get_regions,'isPostRequired':False})
    __api_dict__1['best_quote2'] = SmartFuzzyObject({'url':'/best/quote2/','func':handle_best_quote2,'isPostRequired':True})
    __api_dict__1['best_quote2_add_stop'] = SmartFuzzyObject({'url':'/best/quote2/add/stop/','func':handle_best_quote2_add_stop,'isPostRequired':True})
    __api_dict__1['best_quote2_drop_stop'] = SmartFuzzyObject({'url':'/best/quote2/drop/stop/','func':handle_best_quote2_drop_stop,'isPostRequired':True})
    __api_dict__1['best_quote2_get_stops'] = SmartFuzzyObject({'url':'/best/quote2/get/stops/','func':handle_best_quote2_get_stops,'isPostRequired':False})
    __api_dict__1['best_quote2_drop_stops'] = SmartFuzzyObject({'url':'/best/quote2/drop/all/stops/','func':handle_best_quote2_drop_stops,'isPostRequired':True})
    #__api_dict__1['login_user'] = SmartFuzzyObject({'url':'/login/user/','func':rest_handle_user_login,'isPostRequired':True})
    #__api_dict__1['logout_user'] = SmartFuzzyObject({'url':'/logout/user/','func':rest_handle_user_logout,'isPostRequired':True})
    #__api_dict__1['activate'] = SmartFuzzyObject({'url':'/activate/','func':handle_user_activation,'isPostRequired':True})
    #__api_dict__1['reactivate'] = SmartFuzzyObject({'url':'/reactivate/','func':handle_user_reactivation,'isPostRequired':True})
    #__api_dict__1['chgpassword'] = SmartFuzzyObject({'url':'/chgpassword/','func':handle_user_chgpassword,'isPostRequired':True})
    #__api_dict__1['fileUpload'] = SmartFuzzyObject({'url':'/fileUpload/','func':handle_file_upload,'isPostRequired':True})
    #__api_dict__1['updater'] = SmartFuzzyObject({'url':'/updater/','func':handle_updater_download,'isPostRequired':False})
    #__api_dict__1['pageparser'] = SmartFuzzyObject({'url':'/pageparser/','func':handle_page_parser,'isPostRequired':True})
    #__api_dict__1['sendemail'] = SmartFuzzyObject({'url':'/send/email/','func':handle_send_email,'isPostRequired':True})
    #__api_dict__1['getform'] = SmartFuzzyObject({'url':'/get/form/','func':handle_get_form,'isPostRequired':True})
    #__api_dict__1['getadmob'] = SmartFuzzyObject({'url':'/get/admob/','func':handle_get_admob,'isPostRequired':True})
    #__api_dict__1['activation'] = SmartFuzzyObject({'url':'/activation/','func':handle_user_activation_link,'isPostRequired':False})
    #__api_dict__1['getsmaato'] = SmartFuzzyObject({'url':'/get/smaato/','func':handle_get_smaato,'isPostRequired':True})
    #__api_dict__1['emailtask'] = SmartFuzzyObject({'url':'/email/task/','func':handle_email_task,'isPostRequired':False})
    #__api_dict__1['passwordChg'] = SmartFuzzyObject({'url':'/passwordChg/','func':handle_user_passwordChg,'isPostRequired':False})\
    pass

__api_dict__2 = {}
try:
    __domainName = settings.CURRENT_SITE if (settings.IS_PRODUCTION_SERVER) else settings.LOCALHOST
except Exception, e:
    info_string = _utils.formattedException(details=e)
    logging.info('(Error.101) =%s' % (info_string))
    __domainName = settings.DOMAIN_NAME
__api_dict__2['secure_endpoint'] = 'http%s://%s'%('s' if (settings.IS_PRODUCTION_SERVER) else '',__domainName) if (len(__domainName) > 0) else settings.LOCALHOST
__api_dict__2['insecure_endpoint'] = 'http://%s'%(__domainName if (settings.IS_PRODUCTION_SERVER) else settings.LOCALHOST)

logging.info('(1) __domainName=%s, settings.IS_PRODUCTION_SERVER=%s' % (__domainName,settings.IS_PRODUCTION_SERVER))

from vyperlogix.django.common.API.api import API, APIVersion1000, APIVersion1001

__api__ = APIVersion1001(__api_dict__2,__api_dict__2['secure_endpoint'],__api_dict__2['insecure_endpoint'])
__api__.appendVersion1000(__api_dict__1)

m = __api__.asMap()
__apiMap__ = API({},__api_dict__2['secure_endpoint'],__api_dict__2['insecure_endpoint'])
__apiMap__.__append__(m,noPrepare=True)

if (not settings.IS_PRODUCTION_SERVER):
    #x = __api__.get_user
    #assert (x.key) and (x.key == __api_dict__1['get_user'].key), 'Oops, something is wrong with #1.'
    #x = __api__.insecure_endpoint
    #assert (x) and (x == __api_dict__2['insecure_endpoint']), 'Oops, something is wrong with #2.'
    #x = __api__[API.make_key('get_user',APIVersion1000.__version__)]
    #assert (x.key) and (x.key == __api_dict__1['get_user'].key), 'Oops, something is wrong with #3.'
    #x = __api__[API.make_key('get_user',APIVersion1001.__version__)]
    #assert (x.key) and (x.key == __api_dict__1['get_user'].key), 'Oops, something is wrong with #4.'
    #x = __api__[API.make_key('insecure_endpoint',APIVersion1000.__version__)]
    #assert (x) and (x == __api_dict__2['insecure_endpoint']), 'Oops, something is wrong with #5.'
    #x = __api__[API.make_key('insecure_endpoint',APIVersion1001.__version__)]
    #assert (x) and (x == __api_dict__2['insecure_endpoint']), 'Oops, something is wrong with #6.'
    pass

from vyperlogix.django.common.urls import views

def handle_callback(request,url,data):
    if (url.find('best-quote-2') > -1):
        pass
    pass

def default(request):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    #django_utils.put_into_session(request,'__apiMap__',__apiMap__.asPythonDict())
    #foo = __apiMap__.asPythonDict()
    return views.default(request,apiMap=__apiMap__,domain=__domainName,secure_endpoint=__api_dict__2['secure_endpoint'],insecure_endpoint=__api_dict__2['insecure_endpoint'],air_id=air_id,air_version=air_version,logging=logging,callback=handle_callback)

urlpatterns = patterns('',
                (r'^admin/', include(admin.site.urls)),
                (r'^crossdomain.xml$', django_static.static), # this is intercepted and handled by cherokee
                (r'^media/', django_static.static),           # this is intercepted and handled by cherokee
                (r'^static/', django_static.static),          # this is intercepted and handled by cherokee
                (r'^_main/', 'django.views.generic.simple.direct_to_template',{'template': '_main.html'}),
                (r'.*', default),
)
