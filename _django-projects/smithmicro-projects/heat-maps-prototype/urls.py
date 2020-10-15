# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
#from images.views import image
from django.contrib import admin

from django.template import TemplateDoesNotExist
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

admin.autodiscover()

from django.conf import settings

from django.template import RequestContext
from django.shortcuts import render_to_response

import os,sys
import uuid
import logging

from vyperlogix.django import django_utils
from vyperlogix.django.static import django_static
from vyperlogix.misc import _utils
from vyperlogix.classes.SmartObject import SmartObject, SmartFuzzyObject
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.misc import ObjectTypeName

from vyperlogix.enum.Enum import Enum

class LoggingMode(Enum):
    none = 2^0
    info = 2^1

has_users = False
try:
    #from users.views import rest_handle_get_user, rest_handle_user_login, rest_handle_user_logout, rest_handle_user_register, handle_user_activation, handle_user_reactivation, handle_user_activation_link
    #from users.views import handle_user_chgpassword, handle_file_upload, handle_updater_download, handle_page_parser, handle_send_email, handle_get_form, handle_get_admob, handle_get_smaato, handle_email_task, handle_user_passwordChg
    has_users = True
except ImportError, e:
    info_string = _utils.formattedException(details=e)
    logging.error('Cannot import users functions because "%s".' % (info_string))

has_smithmicro = False
try:
    from smithmicro.views import handle_json_request, handle_points_json_request, handle_post_map_bounds_request, handle_get_count_request, handle_get_region_request
    has_smithmicro = True
except ImportError, e:
    info_string = _utils.formattedException(details=e)
    logging.error('Cannot import smithmicro functions because "%s".' % (info_string))

from users.views import APIVersion1000, APIVersion1001, API

from users.g import air_id, air_version, air_domain, updater_domainName, current_site

__api_dict__1 = {}
if (has_users):
    #__api_dict__1['get_user'] = SmartFuzzyObject({'url':'/get/user/','func':rest_handle_get_user,'isPostRequired':True})
    #__api_dict__1['login_user'] = SmartFuzzyObject({'url':'/login/user/','func':rest_handle_user_login,'isPostRequired':True})
    #__api_dict__1['logout_user'] = SmartFuzzyObject({'url':'/logout/user/','func':rest_handle_user_logout,'isPostRequired':True})
    #__api_dict__1['register_user'] = SmartFuzzyObject({'url':'/register/user/','func':rest_handle_user_register,'isPostRequired':True})
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
if (has_smithmicro):
    __api_dict__1['get_smithmicro_json'] = SmartFuzzyObject({'url':'/get/smithmicro/json/','func':handle_json_request,'isPostRequired':False})
    __api_dict__1['get_smithmicro_pts_json'] = SmartFuzzyObject({'url':'/get/smithmicro/points/json/','func':handle_points_json_request,'isPostRequired':False})
    __api_dict__1['get_smithmicro_specific_pts_json'] = SmartFuzzyObject({'url':'/get/smithmicro/points/json/','func':handle_points_json_request,'isPostRequired':True})
    __api_dict__1['get_smithmicro_post_map_bounds'] = SmartFuzzyObject({'url':'/post/smithmicro/bounds/','func':handle_post_map_bounds_request,'isPostRequired':True})
    __api_dict__1['get_smithmicro_count_json'] = SmartFuzzyObject({'url':'/get/smithmicro/count/json/','func':handle_get_count_request,'isPostRequired':True})
    __api_dict__1['get_smithmicro_region_json'] = SmartFuzzyObject({'url':'/get/smithmicro/region/json/','func':handle_get_region_request,'isPostRequired':True})

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

def get_user(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    return user

def default(request):
    global air_id
    
    qryObj = django_utils.queryObject(request)
    parms = django_utils.parse_url_parms(request)
    context = RequestContext(request)
    try:
	_user = get_user(request)
    except:
	_user = SmartFuzzyObject({'is_superuser':settings.DEBUG})
    _is_method_post_ = django_utils.is_method_post(request)
       
    _logging_mode = LoggingMode.none
    is_logging_info = _logging_mode == LoggingMode.info
    
    is_html = lambda url:(url.endswith('.html')) or (url.endswith('.htm'))

    try:
        s_response = ''
        __error__ = ''

        url = '/%s%s' % (str('/'.join(parms)),'/' if ( (len(parms) > 0) and (not is_html(parms[-1])) ) else '')
        
	if (is_logging_info):
	    logging.info('(1) url=%s' % (url))
	    
        if (url.find('/activate/') > -1):
            toks = ListWrapper(url.split('/'))
            i = toks.findFirstMatching('activate')
            if (i > -1):
                del toks[i+1]
            url = '/'.join(toks)
        
        browserAnalysis = django_utils.get_browser_analysis(request,parms,any([]))

	_current_site = __domainName
	_current_site = _current_site.replace('.appspot','').replace('.com','').lower()

	aid = parms[-1] if (len(parms) > 0) else ''

	def render_main_html(request,browserAnalysis,qryObj,is_logging_info=False):
	    if (is_logging_info):
		logging.info('render_main_html.1 --> _current_site=%s'%(_current_site))

	    _data = {
	        'HTTP_USER_AGENT':django_utils.get_from_META(request,'HTTP_USER_AGENT',''),
	        'browserName':browserAnalysis.browserName,
	        'browserVersion':browserAnalysis.browserVersion,
	        'isRunningLocal':browserAnalysis.isRunningLocal(request),
	        'isJavaScriptOptimized':browserAnalysis.isJavaScriptOptimized,
	        'isUsingUnsupportedBrowser':browserAnalysis.isUsingUnsupportedBrowser,
	        'isUsingMSIE':browserAnalysis.isUsingMSIE,
	        'isBrowserWebKit':browserAnalysis.isBrowserWebKit,
	        'isUsingAndroid':browserAnalysis.isUsingAndroid,
	        'qryObj':qryObj,
	        'serial':str(uuid.uuid4()),
	        'isShowingFlash':True,
	        'isShowingTitleBar':True,
	        'is_superuser':_user.is_superuser,
	        'secure_endpoint':__api_dict__2['secure_endpoint'],
	        'insecure_endpoint':__api_dict__2['insecure_endpoint'],
	        'request_endpoint':__api_dict__2['secure_endpoint'] if (django_utils.is_request_HTTPS(request)) else __api_dict__2['insecure_endpoint'],
	        'version':air_version[air_id] if (air_version[air_id]) else 2.0,
	        'air_id':air_id
	    }
	    if (is_logging_info):
		logging.info('(1) _data=%s' % (str(_data)))
	    try:
		response = render_to_response('main-%s.html' % (air_id), _data)
	    except TemplateDoesNotExist, e:
		if (is_logging_info):
		    info_string = _utils.formattedException(details=e)
		    logging.info('(2) %s' % (info_string))
		try:
		    response = render_to_response('main-%s.html' % (aid), _data)
		except TemplateDoesNotExist, e:
		    if (is_logging_info):
			info_string = _utils.formattedException(details=e)
			logging.info('(3) %s' % (info_string))
		    try:
			response = render_to_response('main-%s.html' % (_current_site), _data)
		    except TemplateDoesNotExist, e:
			if (is_logging_info):
			    info_string = _utils.formattedException(details=e)
			    logging.info('(4) %s' % (info_string))
			try:
			    response = render_to_response('main.html', _data)
			except TemplateDoesNotExist, e:
			    if (is_logging_info):
				info_string = _utils.formattedException(details=e)
				logging.info('(5) %s' % (info_string))
			    response = render_to_response('404.html', _data)
            django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
            return response
	
	air_id = parms[-1].split('.')[0] if (len(parms) > 0) else '' # avoid the key error that would be caused without this line of code...

	if (is_logging_info):
	    logging.info('(5) air_id=%s' % (air_id))

	__apiMap__.__specific__ = is_html(url)
	m = __apiMap__[url]
        isUrlMapped = (m != None) and (m != []) and (m.key) and (callable(m.func))
	if (not isUrlMapped):
	    if (not is_html(url)):
		url = '/%s%s' % (str('/'.join(parms[0:-1])),'/' if (len(parms[0:-1]) > 0) else '')
	    m = __apiMap__[url]
	    isUrlMapped = (m != None) and (m != []) and (m.key) and (callable(m.func))
	    if (isUrlMapped):
		air_id = aid

		if (is_logging_info):
		    logging.info('(6) air_id=%s' % (air_id))

		if (settings.IS_PRODUCTION_SERVER):
		    settings.DOMAIN_NAME = settings.APPSPOT_NAME = air_domain[air_id]
	    else:
		_m_ = [k for k in air_version.keys() if ((len(aid) > 0) and ((aid.lower().find(k.lower()) > -1) or (k.lower().find(aid.lower()) > -1))) or (k.lower().find(_current_site) > -1) or (_current_site.lower().find(k.lower()) > -1)]
		air_id = _m_[0] if (len(_m_) > 0) else air_id

		if (is_logging_info):
		    logging.info('(7) air_id=%s, _m_=%s, aid=%s' % (air_id,_m_,aid))
		
        http_host = django_utils.get_from_META(request,'HTTP_HOST',default='')
        if (__apiMap__.__secure_endpoint__.find('127.0.0.1') > -1) and (http_host.find('localhost') > -1):
            http_host = http_host.replace('localhost','127.0.0.1')
	http_host = http_host.split(':')[0]
	if (is_logging_info):
	    logging.info('(7.0) http_host=%s' % (http_host))
	    logging.info('(7.1) isUrlMapped=%s' % (isUrlMapped))
	    try:
		logging.info('(7.2) m.isPostRequired=%s' % (m.isPostRequired))
	    except:
		pass
	    logging.info('(7.3) _is_method_post_=%s' % (_is_method_post_))
	    logging.info('(7.4) __apiMap__.__secure_endpoint__=%s' % (__apiMap__.__secure_endpoint__))
	    logging.info('(7.5) settings.IS_PRODUCTION_SERVER=%s' % (settings.IS_PRODUCTION_SERVER))
	    logging.info('(7.6) django_utils.is_request_HTTPS(request)=%s' % (django_utils.is_request_HTTPS(request)))
	    logging.info('(7.7) django_utils.get_from_environ(request,\'SERVER_PORT\',80)=%s' % (django_utils.get_from_environ(request,'SERVER_PORT',80)))
	    logging.info('(7.8) django_utils.is_Production()=%s, django_utils.is_Staging()=%s' % (django_utils.is_Production(request),django_utils.is_Staging(request)))
        if (isUrlMapped) and ( ((m.isPostRequired) and _is_method_post_) or ((not m.isPostRequired) and not _is_method_post_) ) and (__apiMap__.__secure_endpoint__.find(http_host) > -1) and ( (not settings.IS_PRODUCTION_SERVER) or ((settings.IS_PRODUCTION_SERVER) and (django_utils.is_request_HTTPS(request)))): # (must be mapped), (must use POST), (must use secure endpoint) and (if production must use SSL).
            try:
                response = m.func(request,parms,browserAnalysis,air_id,__apiMap__)
		if (is_logging_info):
		    logging.info('(8) response=%s' % (response))
		    logging.info('(9) settings.APP_SESSION_KEY=%s' % (settings.APP_SESSION_KEY))
                django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
                return response
            except Exception, e:
		info_string = _utils.formattedException(details=e)
		logging.info('%s' % (info_string))
	    return render_main_html(request,browserAnalysis,qryObj,is_logging_info)
	if (air_version[air_id] is None):
	    try:
		_data = {}
		_message = django_utils.get_from_post_or_get(request,'message','')
		if (len(_message) > 0):
		    _data['message'] = _message
		_url_ = os.sep+os.sep.join([c for c in url.split('/') if (len(c) > 0)])
		_s_ = os.sep.join([settings.MEDIA_ROOT,_url_])
		if (os.path.isfile(_s_)) and (os.path.exists(_s_)):
		    _url_ = '/static/'+'/'.join([c for c in url.split('/') if (len(c) > 0)])
		    try:
			return HttpResponseRedirect(_url_) # allow the web server to handle this rather than the application server...
		    except:
			pass
		    return django_static.serve(_s_) # if all else fails the application server should handle the request...
		_url_ = '/'.join(url.split('/')[1 if (url.startswith('/')) else 0:])
		return render_to_response(_url_, _data)
	    except TemplateDoesNotExist, e:
		try:
		    _url_ += 'index.htm'
		    return render_to_response(_url_, _data)
		except TemplateDoesNotExist, e:
		    try:
			_url_ += 'l'
			return render_to_response(_url_, _data)
		    except TemplateDoesNotExist, e:
			info_string = _utils.formattedException(details=e)
			logging.info('%s' % (info_string))
        return render_main_html(request,browserAnalysis,qryObj,is_logging_info)
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        logging.warning(info_string)
        _content = '<font color="red"><small>%s</small></font>'%('<br/>'.join(info_string.split('\n'))) if (not browserAnalysis.isRunningLocal(request)) else ''
        response = render_to_response('main.html', {'HTTP_USER_AGENT':django_utils.get_from_META(request,'HTTP_USER_AGENT',''),'browserName':browserAnalysis.browserName,'browserVersion':browserAnalysis.browserVersion,'isRunningLocal':browserAnalysis.isRunningLocal(request),'isJavaScriptOptimized':browserAnalysis.isJavaScriptOptimized,'isUsingUnsupportedBrowser':browserAnalysis.isUsingUnsupportedBrowser,'isUsingMSIE':browserAnalysis.isUsingMSIE,'isBrowserWebKit':browserAnalysis.isBrowserWebKit,'isUsingAndroid':browserAnalysis.isUsingAndroid,'qryObj':qryObj,'content':_content,'isShowingFlash':False,'isShowingTitleBar':True})
        django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
        return response

urlpatterns = patterns('',
                (r'^admin/', include(admin.site.urls)),
                (r'^crossdomain.xml$', django_static.static), # this is intercepted and handled by cherokee
                (r'^media/', django_static.static),           # this is intercepted and handled by cherokee
                (r'^static/', django_static.static),          # this is intercepted and handled by cherokee
                (r'^_main/', 'django.views.generic.simple.direct_to_template',{'template': '_main.html'}),
                (r'.*', default),
)
