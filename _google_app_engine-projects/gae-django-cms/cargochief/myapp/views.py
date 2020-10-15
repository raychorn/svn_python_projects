# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, \
    update_object
from google.appengine.ext import db
from mimetypes import guess_type
#from myapp.forms import PersonForm
from myapp.models import Contract, File, Person
from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response

from django.conf import settings

def list_people(request):
    return object_list(request, Person.all(), paginate_by=10)

def show_person(request, key):
    return object_detail(request, Person.all(), key)

def add_person(request):
    return create_object(request, form_class=PersonForm,
        post_save_redirect=reverse('myapp.views.show_person',
                                   kwargs=dict(key='%(key)s')))

def edit_person(request, key):
    return update_object(request, object_id=key, form_class=PersonForm,
        post_save_redirect=reverse('myapp.views.show_person',
                                   kwargs=dict(key='%(key)s')))

def delete_person(request, key):
    return delete_object(request, Person, object_id=key,
        post_delete_redirect=reverse('myapp.views.list_people'))

def download_file(request, key, name):
    file = get_object_or_404(File, key)
    if file.name != name:
        raise Http404('Could not find file with this name!')
    return HttpResponse(file.file,
        content_type=guess_type(file.name)[0] or 'application/octet-stream')

def create_admin_user(request):
    _admin_username = settings.SUPER_USER
    _admin_password = settings.SUPER_PASSWORD
    user = User.get_by_key_name(_admin_username)
    if (not user) or (user.username != _admin_username) or not (user.is_active and user.is_staff and user.is_superuser and user.check_password(_admin_password)):
        user = User(key_name=_admin_username, username=_admin_username, email=settings.SUPER_EMAIL, first_name=settings.SUPER_FIRSTNAME, last_name=settings.SUPER_LASTNAME, is_active=True, is_staff=True, is_superuser=True)
        user.set_password(_admin_password)
        user.put()
    return render_to_response(request, 'main.html')