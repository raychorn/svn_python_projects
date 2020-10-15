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

