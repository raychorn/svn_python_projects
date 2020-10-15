import os
import uuid

import re

from django.conf import settings

from django.template import RequestContext

from django.contrib.auth.models import User

from django.http import HttpResponseRedirect
from django.template import TemplateDoesNotExist
from django.shortcuts import render_to_response

from vyperlogix.django import django_utils

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.classes.SmartObject import SmartObject, SmartFuzzyObject

from vyperlogix.enum.Enum import Enum

from vyperlogix.django.common.API.api import API

class LoggingMode(Enum):
    none = 2^0
    info = 2^1

def __default_superuser__():
    user = SmartFuzzyObject({'is_superuser':settings.DEBUG})
    return user

def __get_user__(request):
    user = None
    uid = request.session.get('_auth_user_id')
    if (uid):
	user = User.objects.get(pk=uid)
    if (not user):
	user = request.session.get('user')
	if (not user):
	    user = __default_superuser__()
    return user

def default(request,_get_user=None,domain='localhost',secure_endpoint='http://localhost',insecure_endpoint='http://localhost',air_id=None,air_version={},apiMap=None,logging=None,callback=None):
    try:
	__apiMap__ = apiMap if (apiMap.isAPI) else API({},secure_endpoint,insecure_endpoint)
    except:
	__apiMap__ = API({},secure_endpoint,insecure_endpoint)
    qryObj = django_utils.queryObject(request)
    parms = django_utils.parse_url_parms(request)
    context = RequestContext(request)
    
    __domainName = domain
    
    try:
	_user = __get_user__(request) if (_get_user is None) else _get_user(request)
    except:
	user = __default_superuser__()
    u = request.session.get('user')
    if (u):
	_user = u
    if (misc.isDict(_user)):
	_user = SmartFuzzyObject(_user)
    _is_method_post_ = django_utils.is_method_post(request)
       
    is_logging_info = (logging is not None)
    if (logging is not None):
	logging.info('(+++) is_logging_info=%s' % (is_logging_info))
    
    is_html = lambda url:(url.endswith('.html')) or (url.endswith('.htm'))

    try:
        s_response = ''
        __error__ = ''

        url = '/%s%s' % (str('/'.join(parms)),'/' if ( (len(parms) > 0) and (not is_html(parms[-1])) ) else '')
        
	if (is_logging_info):
	    logging.info('(1) url=%s' % (url))
	elif (settings.IS_PRODUCTION_SERVER):
	    print '(1) url=%s' % (url)
	    
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

	get_value_from = lambda value,key,default:value[key] if (v.has_key(key)) else default
	
	__isUsingChrome__ = (str(browserAnalysis.browserName).lower() == 'Chrome'.lower())
	__isUsingOpera__ = (str(browserAnalysis.browserName).lower() == 'Opera'.lower())
	__isUsingFireFox__ = (str(browserAnalysis.browserName).lower() == 'FireFox'.lower())
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
	    'isUsingChrome':__isUsingChrome__,
	    'isUsingOpera':__isUsingOpera__,
	    'isUsingFireFox':__isUsingFireFox__,
	    'isUsingChromeOrWebKit':(__isUsingChrome__) or (browserAnalysis.isBrowserWebKit),
            'qryObj':qryObj,
            'serial':str(uuid.uuid4()),
            'isShowingFlash':True,
            'isShowingTitleBar':True,
            'is_superuser':_user.is_superuser,
            'secure_endpoint':secure_endpoint,
            'insecure_endpoint':insecure_endpoint,
            'request_endpoint':secure_endpoint if (django_utils.is_request_HTTPS(request)) else insecure_endpoint,
            'version':air_version[air_id] if (air_version[air_id]) else settings.VERSION,
            'air_id':air_id,
	    'apiMap':dict([(' '.join([str(s).capitalize() for s in k.split('@')[-1].split('_')]),[get_value_from(v,'url','').replace('/'+k.split('@')[0],''),get_value_from(v,'isPostRequired',False),get_value_from(v,'fields',[])]) for k,v in __apiMap__.asPythonDict().iteritems() if (len(k.split('@')) == 2)])
        }
	try:
	    _data['IS_NOT_LOGGED_IN'] = settings.IS_NOT_LOGGED_IN if (not _user) else (len(_user.is_authenticated) == 0) if (misc.isList(_user.is_authenticated)) else not _user.is_authenticated
	except:
	    _data['IS_NOT_LOGGED_IN'] = False
	try:
	    _data['IS_LOGGED_IN'] = not _data['IS_NOT_LOGGED_IN']
	except:
	    _data['IS_LOGGED_IN'] = False
	try:
	    _data['USER_NAME'] = _user.name if (_user and _data['IS_LOGGED_IN']) else 'Anonymous'
	except:
	    _data['IS_NOT_LOGGED_IN'] = False
	try:
	    _data['IS_PRODUCTION_WEB_SERVER'] = settings.IS_PRODUCTION_WEB_SERVER
	except:
	    _data['IS_PRODUCTION_WEB_SERVER'] = False
	try:
	    _data['IS_NOT_PRODUCTION_WEB_SERVER'] = settings.IS_NOT_PRODUCTION_WEB_SERVER
	except:
	    _data['IS_NOT_PRODUCTION_WEB_SERVER'] = False
	_data['AVAILABLE_AUTH_METHODS'] = []
	try:
	    from users.g import AuthMethods
	    for n,v in AuthMethods:
		e = AuthMethods(n)
		if (e.value > 0):
		    if (e.value == 1):
			_data['IS_DJANGO_AUTH_METHOD'] = AuthMethods.django.value > 0
			_data['AVAILABLE_AUTH_METHODS'].append('IS_DJANGO_AUTH_METHOD')
		    else:
			k = 'IS_%s_AUTH_METHOD' % (n.upper())
			_data[k] = e.value > 0
			_data['AVAILABLE_AUTH_METHODS'].append(k)
	except:
	    _data['IS_DJANGO_AUTH_METHOD'] = True
	    _data['AVAILABLE_AUTH_METHODS'].append('IS_DJANGO_AUTH_METHOD')
 	if (is_logging_info):
	    logging.info('(1.1) _data=%s' % (str(_data)))
	for k,v in request.session.iteritems():
	    _data[k] = v
	if (is_logging_info):
	    logging.info('(1.2) _data=%s' % (str(_data)))
	    
	air_id = parms[-1].split('.')[0] if (len(parms) > 0) else '' # avoid the key error that would be caused without this line of code...

	if (is_logging_info):
	    logging.info('(5) air_id=%s' % (air_id))
	    logging.info('(5.1) _data=%s' % (str(_data)))

	_is_callable_ = lambda v:any([callable(x.func) for x in v]) if (misc.isList(v)) else callable(v.func)
	
	__apiMap__.__specific__ = is_html(url)
	m = __apiMap__[url]
        isUrlMapped = (m != None) and (m != []) and (_is_callable_(m))
	if (not isUrlMapped):
	    if (not is_html(url)):
		url = '/%s%s' % (str('/'.join(parms[0:-1])),'/' if (len(parms[0:-1]) > 0) else '')
	    m = __apiMap__[url]
	    isUrlMapped = (m != None) and (m != []) and (_is_callable_(m))
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
	_is_http_host_correct_ = True if (not settings.IS_HTTPS_REQUIRED) else (__apiMap__.__secure_endpoint__.find(http_host) > -1)
	_is_request_correct_ = ( (not settings.IS_PRODUCTION_SERVER) or (not settings.IS_HTTPS_REQUIRED) or ((settings.IS_PRODUCTION_SERVER) and (django_utils.is_request_HTTPS(request))) )

	def __resolve_mapping_from_rules__(m,qryObj):
	    for mm in m:
		_rules_ = [r for r in [(str(k).split('_'),k) for k in mm.keys()] if (str(r[0][0]).lower() == 'rules') and (len(r[0]) == 2)]
		_has_rules_ = any([len(r[0]) == 2 for r in _rules_])
		_is_rules_ = False
		if (_has_rules_):
		    rCnt = 0
		    for r in _rules_:
			try:
			    obj = eval(r[0][-1])
			    if (obj):
				val = mm[r[-1]]
				if (val):
				    for k,v in val.iteritems():
					if (obj[k] == v):
					    rCnt += 1
					    m = mm
					    _is_rules_ = True
					    isUrlMapped = True
					    return isUrlMapped, m, _has_rules_
					else:
					    _re_ = re.compile(v)
					    if (_re_.match(obj[k])):
						rCnt += 1
						m = mm
						_is_rules_ = True
						isUrlMapped = True
						return isUrlMapped, m, _has_rules_
			except:
			    pass
		    if (rCnt < 1):
			isUrlMapped = False
		else:
		    m = m[0]
		    isUrlMapped = True
		    return isUrlMapped, m, _has_rules_
	    return False, m, False
	isUrlMapped, m, _has_rules_ = __resolve_mapping_from_rules__(m,qryObj)
	_is_method_correct_ = ((isUrlMapped)) and ( ((m.isPostRequired) and _is_method_post_) or ((not m.isPostRequired) and not _is_method_post_) )
	if (is_logging_info):
	    logging.info('(7.0) http_host=%s' % (http_host))
	    logging.info('(7.1) isUrlMapped=%s' % (isUrlMapped))
	    try:
		logging.info('(7.2) m.isPostRequired=%s' % (m.isPostRequired))
	    except:
		pass
	    logging.info('(7.3) _is_method_post_=%s' % (_is_method_post_))
	    logging.info('(7.3.1) _is_method_correct_=%s' % (_is_method_correct_))
	    logging.info('(7.3.2) _is_http_host_correct_=%s, http_host=%s' % (_is_http_host_correct_,http_host))
	    logging.info('(7.3.3) _is_request_correct_=%s' % (_is_request_correct_))
	    logging.info('(7.3.4) _has_rules_=%s' % (_has_rules_))
	    
	    logging.info('(7.4) __apiMap__.__secure_endpoint__=%s' % (__apiMap__.__secure_endpoint__))
	    logging.info('(7.5) settings.IS_PRODUCTION_SERVER=%s' % (settings.IS_PRODUCTION_SERVER))
	    logging.info('(7.5.1) settings.IS_HTTPS_REQUIRED=%s' % (settings.IS_HTTPS_REQUIRED))
	    logging.info('(7.6) django_utils.is_request_HTTPS(request)=%s' % (django_utils.is_request_HTTPS(request)))
	    logging.info('(7.7) django_utils.get_from_environ(request,\'SERVER_PORT\',80)=%s' % (django_utils.get_from_environ(request,'SERVER_PORT',80)))
	    logging.info('(7.8) django_utils.is_Production()=%s, django_utils.is_Staging()=%s' % (django_utils.is_Production(request),django_utils.is_Staging(request)))
        if (isUrlMapped) and (_is_method_correct_) and (_is_http_host_correct_) and (_is_request_correct_): # (must be mapped), (must use POST), (must use secure endpoint) and (if production must use SSL).
	    if (is_logging_info):
		logging.info('(8.0) !!!')
            try:
                response = m.func(request,parms,browserAnalysis,air_id,__apiMap__,data=_data)
		if (is_logging_info):
		    logging.info('(8) response=%s' % (response))
		    logging.info('(9) settings.APP_SESSION_KEY=%s' % (settings.APP_SESSION_KEY))
                django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
                return response
            except Exception, e:
		info_string = _utils.formattedException(details=e)
		logging.info('%s' % (info_string))
	    return django_utils.render_main_html(request,browserAnalysis,qryObj,data=_data,is_logging_info=is_logging_info,current_site=_current_site,aid=aid,air_id=air_id,logging=logging,context=context)
	if (air_version[air_id] is None):
	    try:
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
		if (callable(callback)):
		    try:
			response = callback(request,_url_, _data)
			if (isinstance(response,HttpResponseRedirect)):
			    return response
		    except:
			logging.exception('%s'%(_url_))
		return render_to_response(_url_, _data, context_instance=context)
	    except TemplateDoesNotExist, e:
		try:
		    _url_ += 'index.htm'
		    if (callable(callback)):
			try:
			    callback(request,_url_, _data, context_instance=context)
			except:
			    pass
		    return render_to_response(_url_, _data, context_instance=context)
		except TemplateDoesNotExist, e:
		    try:
			_url_ += 'l'
			if (callable(callback)):
			    try:
				callback(request,_url_, _data, context_instance=context)
			    except:
				pass
			return render_to_response(_url_, _data, context_instance=context)
		    except TemplateDoesNotExist, e:
			info_string = _utils.formattedException(details=e)
			logging.info('%s' % (info_string))
        return django_utils.render_main_html(request,browserAnalysis,qryObj,data=_data,is_logging_info=is_logging_info,current_site=_current_site,aid=aid,air_id=air_id,logging=logging,context=context)
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        logging.warning(info_string)
        _content = '<font color="red"><small>%s</small></font>'%('<br/>'.join(info_string.split('\n'))) if (not browserAnalysis.isRunningLocal(request)) else ''
        response = render_to_response('main.html', {'HTTP_USER_AGENT':django_utils.get_from_META(request,'HTTP_USER_AGENT',''),'browserName':browserAnalysis.browserName,'browserVersion':browserAnalysis.browserVersion,'isRunningLocal':browserAnalysis.isRunningLocal(request),'isJavaScriptOptimized':browserAnalysis.isJavaScriptOptimized,'isUsingUnsupportedBrowser':browserAnalysis.isUsingUnsupportedBrowser,'isUsingMSIE':browserAnalysis.isUsingMSIE,'isBrowserWebKit':browserAnalysis.isBrowserWebKit,'isUsingAndroid':browserAnalysis.isUsingAndroid,'qryObj':qryObj,'content':_content,'isShowingFlash':False,'isShowingTitleBar':True}, context_instance=context)
        django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
        return response

