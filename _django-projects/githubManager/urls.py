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

from views.default import upload_file, rest_handle_remove_file, rest_handle_link_github_user, rest_handle_github_user_unlink, rest_handle_push_file, rest_handle_github_make_repo

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
    #__api_dict__1['get_applications'] = SmartFuzzyObject({'url':'/get/applications/','func':rest_handle_get_applications,'isPostRequired':True})
    #__api_dict__1['add_application'] = SmartFuzzyObject({'url':'/add/application/','func':rest_handle_add_application,'isPostRequired':True})
    __api_dict__1['remove_file'] = SmartFuzzyObject({'url':'/remove/file/','func':rest_handle_remove_file,'isPostRequired':True})
    __api_dict__1['documents'] = SmartFuzzyObject({'url':'/documents/','func':upload_file,'isPostRequired':True})
    __api_dict__1['link_github_user'] = SmartFuzzyObject({'url':'/link/github/user/','func':rest_handle_link_github_user,'isPostRequired':True})
    __api_dict__1['unlink_github_user'] = SmartFuzzyObject({'url':'/unlink/github/user/','func':rest_handle_github_user_unlink,'isPostRequired':True})
    __api_dict__1['push_file'] = SmartFuzzyObject({'url':'/push/file/','func':rest_handle_push_file,'isPostRequired':True})
    __api_dict__1['github_make_repo'] = SmartFuzzyObject({'url':'/github/make/repo/','func':rest_handle_github_make_repo,'isPostRequired':True})
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

from views.models import Document
from views.forms import DocumentForm

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
    github_html = 'github.html'

    from users.views import get_user
    from users.models import GoogleAuthenticator
    auths = GoogleAuthenticator.objects.all()
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
    
    from django.contrib.auth.models import User

    users = User.objects.all()
    data['NUM_USERS'] = users.count()
    
    if (url.lower().find(github_html) > -1):
	from vyperlogix import github
        data['action'] = '/documents/'
        data['form'] = DocumentForm()
        documents = Document.objects.all()
	d = dict([(doc.docfile.name,doc.id) for doc in documents])
        json = simplejson.dumps(documents,cls=ComplexEncoder)
        __documents__ = simplejson.loads(json)
	num_zips = 0
	num_id_rsa = 0
	num_id_rsa_pub = 0
	zip_document = None
        for document in __documents__:
            document['docfile']['fname'] = document['docfile']['name'].replace(os.sep,'/').split('/')[-1]
	    document['docfile']['repo_name'] = github.normalize_repo_name(os.path.splitext(document['docfile']['fname'])[0])
	    document['id'] = d.get(document['docfile']['name'],-1)
	    ext = os.path.splitext(document['docfile']['fname'])[-1]
	    if (str(ext).lower().find('.zip') > -1):
		zip_document = document['docfile']
		num_zips += 1
	    elif (document['docfile']['fname'].lower() == 'id_rsa'):
		num_id_rsa += 1
	    elif (document['docfile']['fname'].lower() == 'id_rsa.pub'):
		num_id_rsa_pub += 1
        data['documents'] = __documents__
	data['zip_document'] = zip_document
	data['suggested_repo_name'] = github.normalize_repo_name(zip_document.get('fname','')) if (misc.isDict(zip_document)) else zip_document
	data['num_documents'] = len(data['documents'])
	data['num_zips'] = num_zips
	data['num_id_rsa'] = num_id_rsa
	data['num_id_rsa_pub'] = num_id_rsa_pub
	data['has_full_load'] = (num_id_rsa == 1) and (num_zips == 1) and (num_id_rsa_pub == 1)
        
        data['documents'] = __documents__
        from views import g as gUtils
	githubuser, __g__, newrepos, repos, matches = gUtils.get_githubuser_and_available_repos(request,__documents__)
        data['IS_GITHUB_USER'] = githubuser is not None
        if (githubuser):
	    gu_keys = __g__.github.get.user.keys().keys
	    data['GITHUB_USER_KEYS'] = [{'id':k._id,'title':k._title,'url':k._url,'verified':'%sVerified'%('' if (k._verified) else 'Not ')} for k in gu_keys]
	    
	    d = githubuser.asDict()
            data['GITHUB_USER'] = d
	    data['GITHUB_REPOS'] = [{'name':r[-1].name,'id':r[-1].id} for r in newrepos]
	    data['GITHUB_REPO_LIST'] = [{'name':r.name,'id':r.id} for r in repos]
	    data['GITHUB_MATCHES'] = matches
	    data['HAS_AVAILABLE_GITHUB_REPOS'] = len(newrepos) > 0
	    
	    reponames = [r.name for r in repos]
	    if (data['suggested_repo_name'] in reponames):
		data['suggested_repo_name'] = data['suggested_repo_name'].replace('-','')
		if (data['suggested_repo_name'] in reponames):
		    import random
		    data['suggested_repo_name'] = '%s%s' % (data['suggested_repo_name'],random.choice([ch for ch in xrange(ord('a'),ord('z')+1)]))
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
                (r'^crossdomain.xml$', django_static.static),
                (r'^media/', django_static.static),
                (r'^static/', django_static.static),
                #(r'^static/documents/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
                #(r'^_main/', 'django.views.generic.simple.direct_to_template',{'template': '_main.html'}),
                (r'^_main/', TemplateView.as_view(template_name="_main.html")),
                (r'.*', default),
)
