__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

                   All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
import os, sys
import socket

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.lists import ListWrapper
from vyperlogix.hash import lists

from vyperlogix.misc import ObjectTypeName

__staging__ = ['127.0.0.1:8888','127.0.0.1:9000']

__production__ = ['.appspot.com']

__local_domains__ = ['127.0.0.1', 'localhost']

__both__ = __staging__ + __production__

isBeingDebugged = lambda host:(any([host.find(name) > -1 for name in ['rhorn.', '.dyn-o-saur.com', '127.0.0.1', 'localhost']]))

settings = None

_int = lambda value:int(value) if (str(value).isdigit()) else value

render_template_with_context = lambda t,c:t.render(c) if (not misc.isString(t)) else render_from_string(t,context=c)

split_url = lambda url:[t for t in url.split('/') if (len(t) > 0)]
unsplit_url = lambda toks:'/'+'/'.join(toks)+'/'

def die(reason):
    _utils.terminate(reason)

def version():
    import django
    tests = ListWrapper.ListWrapper([str(t).isdigit() for t in django.VERSION])
    i = tests.findFirstMatching(False)
    return float('.'.join([str(t) for t in list(django.VERSION[0:2])]))

def assert_version(minimum_version):
    import django
    v = version()
    __minimum_version__ = minimum_version if (isinstance(minimum_version,float)) else 1.4
    if (v < __minimum_version__):
	raise AssertionError('Requires Django %s rather than %s' % (minimum_version,django.VERSION))

def _isURL(parms,toks):
    try:
	return parms[0:len(toks)] == toks
    except:
	pass
    return False

def isURL(parms,url):
    return _isURL(parms,split_url(url))

def _is_(request,_list):
    cname = request.META['HTTP_HOST']
    __is__ = lambda name:(name in _list)
    __is_any__ = lambda name:any([str(item).lower().find(name.lower()) > -1 for item in _list])
    return __is__(cname) or __is_any__(cname)

def is_Production(request):
    from django.conf import settings
    return _is_(request,__production__) or (settings.IS_PRODUCTION_SERVER)

def is_Staging(request):
    return _is_(request,__staging__)

def site_id_for_requestor(request):
    from django.conf import settings
    from django.contrib.sites.models import Site
    
    try:
	sites = Site.objects.filter(domain=request.META['HTTP_HOST'])
	if (sites.count() == 0):
	    sites = Site.objects.all()[0]
	settings.SITE_ID = sites[0].id
    except:
	pass

def is_request_okay(request):
    hasKey = request.environ.has_key('HTTP_REFERER')
    referer = '' if (not hasKey) else request.environ['HTTP_REFERER']
    host = request.environ['HTTP_HOST']
    return True if ( (hasKey) and (referer.lower().index(host.lower()) > -1) ) or (isRunningLocal(request)) else False

def is_method_post(request):
    try:
	return request.method == 'POST'
    except:
	pass
    return False

def get_from_session(request,name,default=None):
    from vyperlogix.hash import lists
    from vyperlogix.classes.SmartObject import PyroSmartObject

    try:
	obj = request.session.get(name, default)
	return [o if (not lists.isDict(o)) else PyroSmartObject(o) for o in obj] if (misc.isList(obj)) else obj if (not lists.isDict(obj)) else PyroSmartObject(obj)
    except:
	pass
    return ''

def remove_from_session(request,key):
    if (request.session.has_key(key)):
	del request.session[key]

def put_into_session(request,key,value):
    request.session[key] = str(value)
    
def collect_from_session_using(request,criteria=None):
    keys = []
    try:
	for k in request.session.__dict__['_session_cache'].keys():
	    if (callable(criteria)):
		try:
		    if (criteria(request,k)):
			keys.append(k)
		except:
		    pass
    except:
	pass
    return keys

def get(_dict,name,default=None):
    try:
	if (_dict.has_key(name)):
	    return _int(_dict[name])
    except:
	pass
    return default

def handle_json_post_vars(request):
    from vyperlogix.hash.lists import HashedFuzzyLists2
    from django.utils import simplejson
    d = HashedFuzzyLists2()
    for k,v in request.POST.iteritems():
	try:
	    d[k] = simplejson.loads(v)
	except:
	    pass
    return d

def get_from_post(request,name,default=None):
    return get(request.POST,name,default=default)

def get_from_post_or_get(request,name,default=None):
    if (is_method_post(request)):
	return get(request.POST,name,default=default)
    else:
	return get(request.GET,name,default=default)
    return default

def get_json_vars(request):
    from vyperlogix.classes.SmartObject import SmartFuzzyObject
    import re

    def handle_key_and_value(_so,k,v):
	_reToks = re.compile(r"\[(?P<t>[a-z]*)\]*")
	_regEx = r"(?P<name>[a-z]*)"
	toks = _reToks.findall(k)
	for i in xrange(0,len(toks)):
	    _regEx += r"\[(?P<t%d>[a-z]*)\]" % (i+1)
	_re = re.compile(_regEx)
	matches = _re.findall(k)
	if (len(matches) > 0):
	    _root = so
	    _matches = []
	    if (misc.isList(matches)):
		if (misc.isList(matches[0])):
		    for item in matches[0]:
			_matches.append(item)
		elif (misc.isIterable(matches[0])):
		    for item in list(matches[0]):
			_matches.append(item)
		else:
		    for item in matches:
			_matches.append(item)
	    _matches = [m for m in _matches if (len(m) > 0)]
	    if (len(_matches) > 1):
		for n in _matches[0:-1] if (len(_matches) > 1) else _matches:
		    if (not _root[n]):
			_root[n] = SmartFuzzyObject()
		    _root = _root[n]
	    n = _matches[-1]
	    _root[n] = misc.normalize_as_float(get_from_post_or_get(request,k,-1))
	else:
	    so[k] = misc.normalize_as_float(get_from_post_or_get(request,k,-1))
    
    buckets = [request.GET,request.POST]
    so = SmartFuzzyObject()
    try:
	for b in buckets:
	    for k,v in b.iteritems():
		handle_key_and_value(so,k,v)
    except Exception, ex:
	info_string = _utils.formattedException(details=ex)
	pass
    return so

def get_from_get(request,name,default=None):
    return get(request.GET,name,default=default)

def get_from_META(request,name,default=None):
    return get(request.META,name,default=default)

def get_request_headers(request):
    from vyperlogix.classes.SmartObject import SmartObject
    import re
    regex_http_          = re.compile(r'^HTTP_.+$')
    regex_content_type   = re.compile(r'^CONTENT_TYPE$')
    regex_content_length = re.compile(r'^CONTENT_LENGTH$')
    
    request_headers = {}
    for header in request.META:
	if regex_http_.match(header) or regex_content_type.match(header) or regex_content_length.match(header):
	    request_headers[header] = request.META[header]
    return SmartObject(request_headers)

def get_from_environ(request,key,default=None):
    try:
	return _int(request.environ[key])
    except:
	try:
	    return _int(request.META[key])
	except:
	    return default
    return default

def parse_Query_String(request):
    return ListWrapper.ListWrapper([tuple(t.split('=')) for t in get(request.META,'QUERY_STRING','').split('&')])

def parse_Secure_Query_String(request):
    from vyperlogix.products import keys
    def decode(value):
	try:
	    return keys._decode(value)
	except:
	    pass
	return value
    return ListWrapper.ListWrapper([tuple(t.split('=')) for t in decode(get(request.META,'QUERY_STRING','')).split('&')])

def parse_url_parms(request):
    import urllib
    return [urllib.unquote_plus(t.strip()) for t in request.META['PATH_INFO'].split('/') if (len(t.strip()) > 0)]

def d_parms(url_toks):
    from vyperlogix.hash import lists
    
    url_toks = url_toks if (misc.isList(url_toks)) else []
    t = url_toks[1:]
    if (len(t) % 2 != 0):
	t.append('')
    return lists.HashedLists2(dict([tuple(t)]))

def compressContent(content):
    _compressContent = lambda s:s.replace(chr(13),'').replace(chr(10),'').replace('   ','').replace('  ','').replace('> <','><').replace(' />','/>')
    return _compressContent(content)

def isRunningLocal(request):
    from django.conf import settings
    return lambda request:((request.META['HTTP_HOST'] if (request.META.has_key('HTTP_HOST')) else '').split(':')[0] in __local_domains__) and (not settings.IS_PRODUCTION_SERVER)

def queryObject(request):
    from vyperlogix.classes.SmartObject import SmartObject
    query_object = lambda qs:SmartObject(dict([(t.split('=')[0],t.split('=')[-1]) for t in qs.split('&')]))
    return query_object(request.META['QUERY_STRING'] if (request.META.has_key('QUERY_STRING')) else '')

def give_response_session_id_using(request,response,key):
    import uuid
    request.session[key] = str(uuid.uuid4())
    try:
	request.session.save()
    except: # just in case the app engine barfs on this one...
	pass
    response.set_cookie(key,request.session[key])

def get_browser_analysis(request,parms,isExternalLink):
    from vyperlogix.django import browsers
    from vyperlogix.classes.SmartObject import SmartObject
    d = SmartObject()
    d.browserName,d.browserVersion,d.isRobot = browsers.get_browser_name_version_from(request.META['HTTP_USER_AGENT'] if (request.META.has_key('HTTP_USER_AGENT')) else '')
    d.isRunningLocal = isRunningLocal(request)
    d.isJavaScriptOptimized = ((d.browserName == 'Firefox') and (d.browserVersion >= 3.5)) or ((d.browserName == 'Chrome') and (d.browserVersion >= 5.0))
    d.isBrowserWebKit = ((d.browserName == 'WebKit') and (d.browserVersion >= 533.0))
    d.isUsingAndroid = ((d.browserName in ['AndroidSafari','AndroidWebKit']) and (d.browserVersion >= 530.0))
    d.isBrowserAcceptable = ((d.browserName == 'Opera') and (d.browserVersion >= 9.8)) or (d.isBrowserWebKit) or (d.isUsingAndroid)
    d.isUsingUnsupportedBrowser = (not d.isJavaScriptOptimized) and (not d.isBrowserAcceptable)
    referer = get_from_META(request,'HTTP_REFERER','UNKNOWN REFERER')
    d.isUsingAdobeAIR = (referer == 'app:/VyperBlogAdmin.swf')
    d.isUsingSupportedBrowser = (not d.isUsingUnsupportedBrowser) or (d.isUsingAdobeAIR)
    d.isUsingMSIE = (d.browserName == 'MSIE')
    expected_referer = '%s%s'%(request.META['SERVER_NAME'] if (request.META.has_key('SERVER_NAME')) else '',':%s'%(request.META['SERVER_PORT'] if (request.META.has_key('SERVER_PORT')) and (request.META['SERVER_PORT'] != 80) else ''))
    isExternalLink = isExternalLink if (isinstance(isExternalLink,bool)) else False
    _referer = request.META['HTTP_REFERER'] if (request.META.has_key('HTTP_REFERER')) else ''
    d.isRefererAcceptable = (_referer.find(expected_referer) > -1) if (len(_referer) > 0) else isExternalLink
    return d

def render_main_html(request,browserAnalysis,qryObj,data={},is_logging_info=False,current_site=None,aid=None,air_id=None,logging=None,context=None):
    from django.conf import settings
    from django.shortcuts import render_to_response
    from django.template import TemplateDoesNotExist

    if (is_logging_info) and (logging):
	logging.info('render_main_html.1 --> current_site=%s'%(current_site))

    if (is_logging_info) and (logging):
	logging.info('(1) data=%s' % (str(data)))
    try:
	response = render_to_response('main-%s.html' % (air_id), data, context_instance=context)
    except TemplateDoesNotExist, e:
	pass
	try:
	    response = render_to_response('main-%s.html' % (aid), data, context_instance=context)
	except TemplateDoesNotExist, e:
	    pass
	    try:
		response = render_to_response('main-%s.html' % (current_site), data, context_instance=context)
	    except TemplateDoesNotExist, e:
		pass
		try:
		    response = render_to_response('main.html', data, context_instance=context)
		except TemplateDoesNotExist, e:
		    pass
		    response = render_to_response('404.html', data, context_instance=context)
    give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
    return response

def patterns_insert(prefix, pattern_list, index, tuples):
    from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
    
    pattern_list = pattern_list if (misc.isList(pattern_list)) else [pattern_list]
    for t in tuples:
        regex, view_or_include = t[:2]
        default_kwargs = t[2:]
        if type(view_or_include) == list:
            pattern_list.append(RegexURLResolver(regex, view_or_include[0], *default_kwargs))
        else:
            pattern_list.append(RegexURLPattern(regex, prefix and (prefix + '.' + view_or_include) or view_or_include, *default_kwargs))
    return pattern_list

def load_content_from_template(template_name,context):
    from django.template import Context
    from django.template.loader import get_template
    
    t_body_tag = get_template(template_name)
    c = Context(context, autoescape=False)
    return t_body_tag.render(c)

def render_from_string(source,context={}):
    from django.template import Context
    from django.template import loader
    from django.template.loader import get_template
    
    _content = ''
    tplate = source
    if (misc.isString(source)):
	tplate = loader.get_template_from_string(source)
    toks1 = ObjectTypeName.typeClassName(tplate).split('.')
    toks2 = 'django.template.Template'.split('.')
    cnt = 0
    for t in toks2:
	if (t in toks1):
	    cnt += 1
    if (cnt == len(toks2)):
	_content = tplate.render(Context(context, autoescape=False))
    return _content
    
def paginate(items,items_name,selector,pageNo=1,numPerPage=10,maxPages=15,callback=None):
    from vyperlogix.html import myOOHTML as oohtml

    def navigate_pages():
        articles.append(['<hr align="left" color="silver" width="80%"/>'])
        articles.append(['<h3>More %s...</h3>' % (items_name)])
        _get_page_link_ = lambda pg,n,m:oohtml.renderAnchor('%s' % ('/%s/%s/%s/%d/' % (selector,m,pg,numPerPage)),n,target='_top')
        _get_page_link = lambda pg,n:_get_page_link_(pg,n,'page')
        get_page_link = lambda pg:_get_page_link(pg.replace('+',''),pg)
        pageLinks = [oohtml.renderAnchor('%s' % ('/%s/%s/%s/%d/' % (selector,'page',1,numPerPage)),'Start',target='_top') if (pageNo > 1) else 'Start',oohtml.renderAnchor('%s' % ('/%s/%s/%s/%d' % (selector,'page',pageNo-1,numPerPage)),'Prev',target='_top') if (pageNo > 1) else 'Prev']
        r = ['%d'%(i) for i in xrange(pageNo,totalPages+1 if (pageNo > totalPages-numPerPage) else pageNo+numPerPage)]
	if (len(r) < numPerPage):
	    pg = pageNo-(numPerPage-len(r))
	    if (pg < 1):
		pg = 1
	    r = ['%d'%(i) for i in xrange(pg,pageNo)] + r
	isAtEnd = False
	if (int(r[-1]) < totalPages):
	    r[-1] = '%s+'%(r[-1])
	else:
	    isAtEnd = True
        pageLinks += [get_page_link(i) if (int(i.replace('+','')) != pageNo) else '%s'%(i) for i in r]
        pageLinks += [_get_page_link_(pageNo+1,'Next','next')  if (pageNo < totalPages) else 'Next',_get_page_link(totalPages,'End') if (not isAtEnd) else 'End']
        delim = '&nbsp;'*5
        articles.append(['<small>%s</small>' % (delim.join(pageLinks))])
        articles.append(['<center><small>Page %d of %d</small></center>' % (pageNo,totalPages)])
        articles.append(['<hr align="left" color="silver" width="80%"/>'])
    
    h = oohtml.Html()
    articles = []
    totalNum = len(items)
    totalPages = (totalNum / numPerPage) + (1 if ((totalNum % numPerPage) > 0) else 0)

    if (totalNum > numPerPage):
        navigate_pages()
	
    iBegin = (pageNo-1)*numPerPage
    iEnd = iBegin+numPerPage
    for item in items[iBegin:iEnd]:
        try:
            if (callable(callback)):
                callback(item,articles,items_name,selector)
        except Exception, details:
            info_string = _utils.formattedException(details=details)
            return info_string
    if (totalNum > numPerPage):
        navigate_pages()
    h.html_simple_table(articles)
    content = h.toHtml()
    return content

def __init__(_root_,isAdjustingPath=False):
    '''Initialize the sys.path for django under win32.'''
    import os, sys
    
    if (sys.platform == 'win32'):
	if (isAdjustingPath):
	    pass
	from vyperlogix import misc
	from vyperlogix.django import django_utils
	from vyperlogix.lists.ListWrapper import ListWrapper
	
	fp = os.path.dirname(os.path.abspath(_root_))
	while (fp.split(os.sep)[-1].find('django') > -1):
	    fp = os.path.dirname(fp)
	s = ListWrapper(sys.path)
	l = ListWrapper(list(set(s.findAllContaining(fp))))
	t = os.path.join(fp,'django')
	if (os.path.exists(t)):
	    l.append(t)
	    i = l.findFirstMatching(fp)
	    if (i > -1):
		del l[i]
	l = misc.sort(l)
	for item in l:
	    i = s.findFirstMatching(item)
	    while (i > -1):
		del s[i]
		i = s.findFirstMatching(item)
	sys.path = s.copy()
	for item in misc.reverse(l):
	    sys.path.insert(0, item)
	return 'settings'
    else:
	fpath = os.path.dirname(os.path.abspath(_root_))
	if (fpath not in sys.path):
	    sys.path.insert(0, fpath)
	return '%s.settings' % (fpath.split(os.sep)[-1])

def get_http_host(request):
    return request.META['HTTP_X_FORWARDED_SERVER'] if (request.META.has_key('HTTP_X_FORWARDED_SERVER')) else request.META['HTTP_HOST'] if (request.META.has_key('HTTP_HOST')) else ''

def get_fully_qualified_http_host(request):
    host = get_from_environ(request,'HTTP_X_FORWARDED_HOST',get_http_host(request))
    toks = host.split(':')
    port = toks[-1]
    host = toks[0]
    port = int(port) if (port.isdigit()) else 80
    isPort = port not in [80,443]
    return '%s%s%s' % (host,':' if (isPort) else '',port if (isPort) else '')

def is_request_HTTPS(request):
    _port = get_from_environ(request,'SERVER_PORT',80)
    return (_port == 443) if (is_Production or is_Staging) else True

def get_server_name(request,default='vyperlogix.com'):
    _servername = get_from_environ(request,'SERVER_NAME',default).replace('www.','')
    _servername = _servername if (_servername.find('127.0.0.1') == -1) and (_servername.find('localhost') == -1) else default
    return _servername

def seek_installed_apps(_root,INSTALLED_APPS=()):
    import os, re
    _reSVN = re.compile(r"[._]svn\Z")
    _re = re.compile(r"__init__\.py|models\.py|views\.py")
    td = list(INSTALLED_APPS)
    if (os.path.exists(_root)):
	_dirs = []
	for f in os.listdir(_root):
	    if (not _reSVN.search(f)):
		fp = os.path.join(_root,f)
		if (os.path.isdir(fp)):
		    d = lists.HashedLists2()
		    for ff in os.listdir(fp):
			if _re.search(ff) and (d[ff] is None):
			    d[ff] = 1
		    if (len(d) == 3):
			_dirs.append(f)
	for dName in _dirs:
	    td.append(dName)
    return tuple(td)
