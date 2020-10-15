# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
#from images.views import image
from django.contrib import admin

from django.template import TemplateDoesNotExist
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView

admin.autodiscover()

from django.conf import settings

import os,sys
import uuid
import logging

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.classes.SmartObject import SmartObject, SmartFuzzyObject
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.misc import ObjectTypeName

from vyperlogix.django import django_utils
from vyperlogix.django.static import django_static

has_users = False
try:
    from users.views import create_admin_user, rest_handle_user_register
    from users.views import rest_handle_get_user, rest_handle_user_passwordChange
    #, rest_handle_user_login, rest_handle_user_logout, handle_user_activation, handle_user_reactivation, handle_user_activation_link
    #from users.views import handle_user_chgpassword, handle_file_upload, handle_updater_download, handle_page_parser, handle_send_email, handle_get_form, handle_email_task, handle_user_passwordChg
    has_users = True
except ImportError, e:
    info_string = _utils.formattedException(details=e)
    logging.error('Cannot import users functions because "%s".' % (info_string))

from users.g import air_id, air_version, air_domain, updater_domainName, current_site, get_google_auth_seed

from users.views import rest_handle_user_login, rest_handle_user_register, handle_go_login, handle_go_logout, handle_go_home, handle_user_activation

from views.default import upload_file, rest_handle_remove_file, update_candidate, clear_messages

__api_dict__1 = {}
if (has_users):
    __api_dict__1['create_admin_user'] = SmartFuzzyObject({'url':'/create/admin/user/','func':create_admin_user,'isPostRequired':False})
    __api_dict__1['register_user'] = SmartFuzzyObject({'url':'/register/user/','func':rest_handle_user_register,'isPostRequired':True,'fields':['username','password','password2','fullname']})
    __api_dict__1['get_user'] = SmartFuzzyObject({'url':'/get/user/','func':rest_handle_get_user,'isPostRequired':True})
    __api_dict__1['login_user'] = SmartFuzzyObject({'url':'/login/user/','func':rest_handle_user_login,'isPostRequired':True})
    __api_dict__1['go_login'] = SmartFuzzyObject({'url':'/','rules':{'qryObj':{'Go':r"\+*Login\+*"}},'func':handle_go_login,'isPostRequired':False})
    __api_dict__1['go_home'] = SmartFuzzyObject({'url':'/','rules':{'qryObj':{'GO':r"HOME"}},'func':handle_go_home,'isPostRequired':False})
    __api_dict__1['changePassword'] = SmartFuzzyObject({'url':'/change/password/','func':rest_handle_user_passwordChange,'isPostRequired':True})
    __api_dict__1['activation'] = SmartFuzzyObject({'url':'/activation/','func':handle_user_activation,'isPostRequired':False})
    __api_dict__1['go_logout'] = SmartFuzzyObject({'url':'/logout/user/','func':handle_go_logout,'isPostRequired':False})
    __api_dict__1['remove_file'] = SmartFuzzyObject({'url':'/remove/file/','func':rest_handle_remove_file,'isPostRequired':True})
    __api_dict__1['documents'] = SmartFuzzyObject({'url':'/documents/','func':upload_file,'isPostRequired':True})
    __api_dict__1['candidates'] = SmartFuzzyObject({'url':'/candidates/','func':update_candidate,'isPostRequired':True})
    __api_dict__1['clear_messages'] = SmartFuzzyObject({'url':'/clear/messages/','func':clear_messages,'isPostRequired':False})
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

from django.utils import simplejson
from vyperlogix.django.common.urls import views

from views.models import Document, Candidate, Cities
from views.forms import DocumentForm, CandidateForm

from views.models import Candidate

class ComplexEncoder(simplejson.JSONEncoder): 
    def default(self, obj):
        from vyperlogix.misc import ObjectTypeName
        if (ObjectTypeName.typeClassName(obj).find('.QuerySet') > -1):
            items = []
            for item in obj:
                if (ObjectTypeName.typeClassName(item).find('views.models.Document') > -1): 
                    items.append(item.__json__()) 
            return items
        return simplejson.JSONEncoder.default(self, obj)
 
def handle_callback(request,url,data):
    data['url'] = url
    headers = django_utils.get_request_headers(request)
    http_referer = headers.HTTP_REFERER.split('/')[-1].lower() if (headers.HTTP_REFERER) else None
    jobs_html = 'jobs.html'

    from users.views import get_user
    
    from users.models import GoogleAuthenticator
    auths = GoogleAuthenticator.objects.all()

    if (settings.IS_USING_GOOGLE_AUTHENTICATOR):
	data['AUTH_SEED'] = None
	data['AUTH_HREF'] = None
	if (auths.count() == 0):
	    d = get_google_auth_seed()
	    auth = GoogleAuthenticator(otpseed=d['seed'],sitename=d['name'],href=d['href'])
	    data['AUTH_SEED'] = d['seed']
	    data['AUTH_HREF'] = d['href']
	    auth.save()
	    auths = GoogleAuthenticator.objects.all()
	else:
	    data['AUTH_SEED'] = auths[0].otpseed
	    data['AUTH_HREF'] = auths[0].href
    data['AUTHS_COUNT'] = auths.count()
    
    __user__ = get_user(request)
    
    normalize_doc_name = lambda name:''.join([ch if ( ((ch.lower() >= 'a') and (ch.lower() <= 'z')) or ((ch >= '0') and (ch <= '9')) ) else '-' for ch in os.path.splitext(name)[0]])
    
    if (url.lower().find(jobs_html) > -1):
        data['document_action'] = '/documents/'
        data['document_form'] = DocumentForm()
	documents = Document.objects.filter(user_id=__user__.id)
	d = dict([(doc.docfile.name,doc.id) for doc in documents])
        json = simplejson.dumps(documents,cls=ComplexEncoder)
        __documents__ = simplejson.loads(json)
	num_docs = 0
	document = None
        for document in __documents__:
            document['docfile']['fname'] = document['docfile']['name'].replace(os.sep,'/').split('/')[-1]
	    document['docfile']['name'] = normalize_doc_name(os.path.splitext(document['docfile']['fname'])[0])
	    document['id'] = d.get(document['docfile']['name'],-1)
	    ext = os.path.splitext(document['docfile']['fname'])[-1]
	    if (str(ext).lower().find('.doc') > -1):
		document = document['docfile']
		num_docs += 1
        data['documents'] = __documents__
	data['document'] = document
	data['num_documents'] = len(data['documents'])
	data['num_docs'] = num_docs
	data['has_full_load'] = (num_docs == 1)
        data['documents'] = __documents__
	
	candidates = Candidate.objects.filter(user=__user__)
	data['has_candidates'] = True
	data['really_has_candidates'] = candidates.count() > 0
	data['candidate_form'] = CandidateForm()
	data['candidate_action'] = '/candidates/'
	data['candidates'] = [(candidate.asDict().get('candidate',{})) for candidate in candidates] if (candidates.count() > 0) else [(Candidate().asDict().get('candidate',{}))]
	
	myCountry = 'US' if (candidates.count() == 0) else candidates[0].city.country
	countries = Cities.objects.order_by('country').values_list('country').distinct()
	__countries__ = [c[0] if (misc.isIterable(c)) else c for c in countries]
	if (myCountry):
	    data['countries'] = [{'abbrev':c,'selected':'' if (c != myCountry) else ' selected'} for c in __countries__]
	else:
	    wrapper = ListWrapper(__countries__)
	    i = wrapper.findFirstMatching('US')
	    if (i > 0):
		myCountry = __countries__[i]
		del __countries__[i]
		__countries__.insert(0,{'abbrev':myCountry,'selected':' selected'})
	    data['countries'] = __countries__[0:1]+[{'abbrev':c,'selected':''} for c in __countries__[1:]]
	
	myState = None if (candidates.count() == 0) else candidates[0].city.region
	if (myCountry):
	    states = Cities.objects.filter(country=myCountry).order_by('region').values_list('region').distinct()
	else:
	    states = Cities.objects.order_by('region').values_list('region').distinct()
	__states__ = [s[0] if (misc.isIterable(s)) else s for s in states]
	data['states'] = [{'abbrev':s,'selected':'' if (s != myState) else ' selected'} for s in __states__]
	
    pass

def default(request):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    #django_utils.put_into_session(request,'__apiMap__',__apiMap__.asPythonDict())
    #foo = __apiMap__.asPythonDict()
    return views.default(request,apiMap=__apiMap__,domain=__domainName,secure_endpoint=__api_dict__2['secure_endpoint'],insecure_endpoint=__api_dict__2['insecure_endpoint'],air_id=air_id,air_version=air_version,logging=logging,callback=handle_callback)

urlpatterns = patterns('',
                (r'^admin/', include(admin.site.urls)),
                (r'^crossdomain.xml$', django_static.static),
                (r'^media/', django_static.static),
                (r'^static/', django_static.static),
                #(r'^static/documents/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
                #(r'^_main/', 'django.views.generic.simple.direct_to_template',{'template': '_main.html'}),
                (r'^_main/', TemplateView.as_view(template_name="_main.html")),
                (r'.*', default),
)
