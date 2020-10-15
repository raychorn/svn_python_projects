from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, update_object
from django.template import RequestContext
from mimetypes import guess_type
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user, login

from django.template import loader, Template, TemplateDoesNotExist
from django.template import Context
from django.conf import settings

import models

import re
import logging
import mimetypes

from datetime import datetime,timedelta

import uuid
import urllib

from django.contrib.sitemaps.views import sitemap

__mimetype = mimetypes.guess_type('.html')[0]
__jsonMimetype = 'application/json'
__xmlMimetype = mimetypes.guess_type('.xml')[0]
__textMimetype = 'text/plain'

def dict_to_json(dct):
    json = ''
    try:
        from django.utils import simplejson
        json = simplejson.dumps(dct)
    except Exception, e:
        import _utils
        info_string = _utils.formattedException(details=e)
        json = {'__error__':info_string}
    return json

def rest_sample(request,parms=None,browserAnalysis=None,__air_id__=None,__apiMap__=None):
    d = {}
    _user = get_user(request)
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)


