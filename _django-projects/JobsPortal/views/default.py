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

from models import Document, Candidate
from forms import DocumentForm, CandidateForm

from users.views import get_user, _error_symbol, _status_symbol

from django.views.decorators.csrf import requires_csrf_token

docfile = lambda doc:{'docfile':{'name':doc.docfile.name,'fname':doc.docfile.name.replace(os.sep,'/').split('/')[-1],'url':doc.docfile.url},'id':doc.id}

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
	    documents = Document.objects.filter(user_id=_user.id)
	    acceptable_types = ['.doc','.docx']
	    docs = [d for d in documents if (os.path.basename(d.docfile.name) == str(docfile.name))]
	    if (fext in acceptable_types):
		for doc in docs:
		    doc.docfile.delete()
		    doc.delete()
		try:
		    newdoc = Document(docfile = docfile, user_id=_user.id)
		    newdoc.save()
		    if (len(docs) == 0):
			django_utils.remove_from_session(request, 'ERROR_MESSAGE')
		    else:
			django_utils.put_into_session(request, 'ERROR_MESSAGE', 'Removed the previously uploaded duplicate file of the same name.')
		    django_utils.put_into_session(request, 'STATUS_MESSAGE', 'File "%s" successfully uploaded.' % (docfile.name))
		except Exception, details:
		    django_utils.remove_from_session(request, 'STATUS_MESSAGE')
		    django_utils.put_into_session(request, 'ERROR_MESSAGE', 'Cannot complete upload due to "%s".' % (details))
	    else:
		django_utils.remove_from_session(request, 'STATUS_MESSAGE')
		django_utils.put_into_session(request, 'ERROR_MESSAGE', 'Cannot complete upload due to incorrect file type.')
        else:
	    django_utils.remove_from_session(request, 'STATUS_MESSAGE')
	    django_utils.put_into_session(request, 'ERROR_MESSAGE', form.errors)
    return HttpResponseRedirect('/jobs.html')

@requires_csrf_token
def rest_handle_remove_file(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    _user = get_user(request)
    _id_ = django_utils.get_from_post(request,'id',default=None)
    documents = Document.objects.filter(user_id=_user.id).filter(id=_id_)
    __documents__ = []
    for doc in documents:
	__documents__.append(doc.docfile.name)
        doc.docfile.delete()
        doc.delete()
    __status_message__ = ''
    if (len(documents) > 0):
	plural = 's' if (len(__documents__) > 1) else ''
	__status_message__ = 'File%s %s successfully deleted.' % (plural, ', '.join(['"%s"'%(os.path.basename(doc)) for doc in __documents__]) )
	django_utils.put_into_session(request, 'STATUS_MESSAGE', __status_message__)
    else:
	django_utils.remove_from_session(request, 'STATUS_MESSAGE')
    d = {}
    documents = Document.objects.filter(user_id=_user.id)
    d['documents'] = [docfile(doc) for doc in documents]
    d['num_documents'] = len(d['documents'])
    d['STATUS_MESSAGE'] = __status_message__
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

@requires_csrf_token
def update_candidate(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    '''
    '''
    if request.method == 'POST':
        _user = get_user(request)
        form = CandidateForm(request.POST)
        if form.is_valid():
	    fullname = request.POST.get('fullname',None)
	    phone = request.POST.get('phone',None)
	    city = request.POST.get('city',None)
	    state = request.POST.get('state',None)
	    zipcode = request.POST.get('zipcode',None)
	    relocateable = request.POST.get('relocateable',False)
	    if (str(relocateable).upper() in ['YES','TRUE']):
		relocateable = True
	    else:
		relocateable = False
	    candidates = Candidate.objects.filter(user=_user)
	    for candidate in candidates:
		candidate.delete()
	    try:
		newcandidate = Candidate(fullname=fullname, user=_user)
		newcandidate.phone = phone
		newcandidate.city = city
		newcandidate.state = state
		newcandidate.zipcode = zipcode
		newcandidate.relocateable = relocateable
		newcandidate.save()
		django_utils.put_into_session(request, 'STATUS_MESSAGE', 'Your Profile has been successfully saved.')
	    except Exception, details:
		django_utils.remove_from_session(request, 'STATUS_MESSAGE')
		django_utils.put_into_session(request, 'ERROR_MESSAGE', 'Cannot save your Profile due to "%s".' % (details))
        else:
	    django_utils.remove_from_session(request, 'STATUS_MESSAGE')
	    django_utils.put_into_session(request, 'ERROR_MESSAGE', form.errors)
    return HttpResponseRedirect('/jobs.html')

@requires_csrf_token
def clear_messages(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    '''
    '''
    d = {}
    if request.method == 'GET':
	django_utils.remove_from_session(request, 'STATUS')
	django_utils.remove_from_session(request, 'STATUS_MESSAGE')
	django_utils.remove_from_session(request, 'ERROR')
	django_utils.remove_from_session(request, 'ERROR_MESSAGE')
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

