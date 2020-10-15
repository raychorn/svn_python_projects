from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.conf import settings

from django.shortcuts import render_to_response

from utils import __context__

import os
import re

from vyperlogix import misc

def default(request):
    context = __context__(request)
    context['IS_NOT_LOGGED_IN'] = False
    return render_to_response('main.html', context, content_type="text/html")

def not_yet_implemented(request):
    return render_to_response('not-yet-implemented.html', __context__(request), content_type="text/html")

def acceptable_use_policy(request):
    return render_to_response('acceptable-use-policy.html', __context__(request), content_type="text/html")

def contact(request):
    return render_to_response('contact.html', __context__(request), content_type="text/html")

def terms(request):
    return render_to_response('terms-of-use.html', __context__(request), content_type="text/html")
