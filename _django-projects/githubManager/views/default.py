from django import http
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.conf import settings

import os, sys

from vyperlogix.django import django_utils

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

import mimetypes
from mimetypes import guess_type

__mimetype = mimetypes.guess_type('.html')[0]
__jsonMimetype = 'application/json'
__xmlMimetype = mimetypes.guess_type('.xml')[0]
__textMimetype = 'text/plain'

_root_ = os.path.dirname(__file__)

from views import g as gUtils

from users.g import dict_to_json

from models import Document
from forms import DocumentForm
from models import GitHubUser

from vyperlogix import github

from users.views import get_user, _error_symbol, _status_symbol

from django.views.decorators.csrf import requires_csrf_token

docfile = lambda doc:{'docfile':{'name':doc.docfile.name,'fname':doc.docfile.name.replace(os.sep,'/').split('/')[-1],'url':doc.docfile.url},'id':doc.id}

@requires_csrf_token
def rest_handle_link_github_user(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    d = {}
    u = {}
    __user__ = get_user(request)
    try:
        username = django_utils.get_from_post(request,'username',default=None)
        password = django_utils.get_from_post(request,'password',default=None)
        if username and password:
	    from vyperlogix.decorators import addto
	    from vyperlogix.crypto import blowfish
	    from vyperlogix.misc import hex
	    from github import Github
	    g = Github(username, password)

	    @addto.addto(g)
	    def requester(self):
		return self.__dict__['_Github__requester'] if (self.__dict__.has_key('_Github__requester')) else None

	    __i__ = g.requester()
	    _user = g.get_user()
	    
	    e_password = blowfish.encryptData(password,_user.email)
	    p_password = blowfish.noramlize(blowfish.decryptData(e_password, _user.email))
	    assert p_password == password, 'Something went wrong with the password encryption, method 1 !!!'
	    hex_password = hex.strToHex(e_password)
	    ee_password = hex.hexToStr(hex_password)
	    pp_password = blowfish.noramlize(blowfish.decryptData(ee_password, _user.email))
	    assert pp_password == password, 'Something went wrong with the password encryption, method 2 !!!'

	    u = {
	        'username':_user.login,
	        'name':_user.name,
	        'email':_user.email,
	        'password': hex_password
	    }

	    if (not __user__.is_anonymous()):
		githubuser = GitHubUser(username=u['username'],password=u['password'],name=u['name'],email=u['email'],user=__user__)
		githubuser.save()
	    else:
		django_utils.put_into_session(request, 'ERROR_MESSAGE', 'Something went wrong; doesn\'t seem you are logged in... and this is a bit odd because you seem to have been able to get this far into the system.')
	    
	    return HttpResponseRedirect('/github.html')
	elif (not username) or (len(username) == 0):
	    django_utils.put_into_session(request, 'ERROR_MESSAGE', 'You must enter your Github Username at this time; never fear this small bit of information will be kept safe and secure.')
	elif (not password) or (len(password) == 0):
	    django_utils.put_into_session(request, 'ERROR_MESSAGE', 'You must enter your Github password at this time; never fear this small bit of information will be kept safe and secure.')
    except Exception, e:
	django_utils.put_into_session(request, 'ERROR_MESSAGE', e.message)
    return HttpResponseRedirect('/github.html')

@requires_csrf_token
def rest_handle_github_user_unlink(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    u = {}
    __user__ = get_user(request)
    try:
        username = django_utils.get_from_post(request,'username',default=None)
        email = django_utils.get_from_post(request,'email',default=None)
        if username and email:
	    githubuser = GitHubUser.objects.get(user=__user__)
	    githubuser.delete()
	    
	    return HttpResponseRedirect('/github.html')
    except Exception, e:
	pass
    return HttpResponseRedirect('/github.html')

@requires_csrf_token
def upload_file(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    '''
    http://stackoverflow.com/questions/5871730/need-a-minimal-django-file-upload-example
    '''
    if request.method == 'POST':
        _user = get_user(request)
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
	    docfile = request.FILES['docfile']
	    fext = os.path.splitext(str(docfile.name))[-1].lower()
	    documents = Document.objects.filter(user=_user)
	    zips = [d for d in documents if (os.path.splitext(os.path.basename(d.docfile.name))[-1].lower() == '.zip')]
	    id_rsas = [d for d in documents if (os.path.basename(d.docfile.name).lower() == 'id_rsa')]
	    id_rsa_pubs = [d for d in documents if (os.path.basename(d.docfile.name).lower() == 'id_rsa.pub')]
	    if (fext == '.zip'):
		for doc in zips:
		    doc.docfile.delete()
		    doc.delete()
	    elif (os.path.basename(docfile.name) == 'id_rsa'):
		for doc in id_rsas:
		    doc.docfile.delete()
		    doc.delete()
	    elif (os.path.basename(docfile.name) == 'id_rsa.pub'):
		for doc in id_rsa_pubs:
		    doc.docfile.delete()
		    doc.delete()
            try:
                newdoc = Document(docfile = docfile, user=_user)
                newdoc.save()
            except:
                pass
        else:
	    django_utils.put_into_session(request, 'ERROR_MESSAGE', form.errors)
    return HttpResponseRedirect('/github.html')

@requires_csrf_token
def rest_handle_remove_file(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    _user = get_user(request)
    _id_ = django_utils.get_from_post(request,'id',default=None)
    documents = Document.objects.filter(user=_user).filter(id=_id_)
    for doc in documents:
        doc.docfile.delete()
        doc.delete()
    d = {}
    documents = Document.objects.filter(user=_user)
    d['documents'] = [docfile(doc) for doc in documents]
    zip_documents = [docfile(doc) for doc in documents if (os.path.splitext(str(doc.docfile.name))[-1].lower() == '.zip')]
    d['zip_document'] = zip_documents[0] if (len(zip_documents) > 0) else None
    d['suggested_repo_name'] = github.normalize_repo_name(d['zip_document'].get('fname',''))
    d['num_documents'] = len(d['documents'])
    d['num_zips'] = num_zips = len([doc for doc in documents if (os.path.splitext(str(doc.docfile.name))[-1].lower() == '.zip')])
    d['num_id_rsa'] = num_id_rsa = len([doc for doc in documents if (str(doc.docfile.name).lower() == 'id_rsa')])
    d['num_id_rsa_pub'] = num_id_rsa_pub = len([doc for doc in documents if (str(doc.docfile.name).lower() == 'id_rsa.pub')])
    d['has_full_load'] = (num_id_rsa == 1) and (num_zips == 1) and (num_id_rsa_pub == 1)
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

@requires_csrf_token
def rest_handle_github_make_repo(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    _user = get_user(request)
    _name_ = django_utils.get_from_post(request,'name',default=None)
    d = {}
    githubuser, __g__, newrepos, repos, matches = gUtils.get_githubuser_and_available_repos(request)
    try:
	gu = __g__.get_user()
	gu.create_repo(_name_)
    except Exception, ex:
	d['ERROR_MESSAGE'] = _utils.formattedException(details=ex)
    d['status'] = 'Working...'
    d['GITHUB_USER'] = githubuser.asDict()
    d['GITHUB_REPOS'] = [{'name':r[-1].name,'id':r[-1].id} for r in newrepos]
    d['GITHUB_REPO_LIST'] = [{'name':r.name,'id':r.id} for r in repos]
    d['HAS_AVAILABLE_GITHUB_REPOS'] = len(newrepos) > 0
    
    #if (_utils.isBeingDebugged):
	#d['GITHUB_REPO_LIST'] += [{'name':_name_,'id':-1}]
	#d['GITHUB_REPOS'] += [{'name':_name_,'id':-1}]
	#d['HAS_AVAILABLE_GITHUB_REPOS'] = True
	#d['status'] = 'Simulated...'

    documents = Document.objects.filter(user=_user)
    d['documents'] = [docfile(doc) for doc in documents]
    zip_documents = [docfile(doc) for doc in documents if (os.path.splitext(str(doc.docfile.name))[-1].lower() == '.zip')]
    d['zip_document'] = zip_documents[0] if (len(zip_documents) > 0) else None
    d['suggested_repo_name'] = github.normalize_repo_name(d['zip_document'].get('fname',''))

    d['num_documents'] = len(d['documents'])
    d['num_zips'] = num_zips = len([doc for doc in documents if (os.path.splitext(str(doc.docfile.name))[-1].lower() == '.zip')])
    d['num_id_rsa'] = num_id_rsa = len([doc for doc in documents if (str(doc.docfile.name).lower() == 'id_rsa')])
    d['num_id_rsa_pub'] = num_id_rsa_pub = len([doc for doc in documents if (str(doc.docfile.name).lower() == 'id_rsa.pub')])
    d['has_full_load'] = (num_id_rsa == 1) and (num_zips == 1) and (num_id_rsa_pub == 1)

    reponames = [r.name for r in repos]
    if (d['suggested_repo_name'] in reponames):
	d['suggested_repo_name'] = d['suggested_repo_name'].replace('-','')
	if (d['suggested_repo_name'] in reponames):
	    import random
	    d['suggested_repo_name'] = '%s%s' % (d['suggested_repo_name'],random.choice([ch for ch in xrange(ord('a'),ord('z')+1)]))

    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

@requires_csrf_token
def rest_handle_push_file(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    _user = get_user(request)
    _file_id_ = django_utils.get_from_post(request,'file_id',default=None)
    _filename_ = django_utils.get_from_post(request,'filename',default=None)
    _repoid_ = django_utils.get_from_post(request,'repoid',default=-1)
    try:
	_repoid_ = int(_repoid_)
    except:
	pass
    documents = Document.objects.filter(user=_user).filter(id=_file_id_)
    if (documents.count() > 0):
	from views import g as gUtils
	githubuser, __g__ = gUtils.github(request)
	if (githubuser):
	    gu = __g__.get_user()
	    if (_repoid_ == -1):
		repo_name = os.path.splitext(_filename_)[0]
		gu.create_repo(repo_name)
	    # issue the remote rest call to perform the work...
	# gather repo names here...
    from views import g as gUtils
    githubuser, __g__, newrepos, repos, matches = gUtils.get_githubuser_and_available_repos(request)
    d = {}
    d['status'] = 'Working...'
    d['GITHUB_USER'] = githubuser.asDict()
    d['GITHUB_REPOS'] = [{'name':r[-1].name,'id':r[-1].id} for r in newrepos]
    d['GITHUB_REPO_LIST'] = [{'name':r.name,'id':r.id} for r in repos]
    d['HAS_AVAILABLE_GITHUB_REPOS'] = len(newrepos) > 0
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

