from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.conf import settings

from django.shortcuts import render_to_response

import os
import re

def default(request):
    __data__ = {"url": request.META.get('PATH_INFO','/')}
    return render_to_response('main.html', __data__, content_type="text/html")

def contact(request):
    __data__ = {"url": request.META.get('PATH_INFO','/')}
    return render_to_response('contact.html', __data__, content_type="text/html")

def terms(request):
    __data__ = {"url": request.META.get('PATH_INFO','/')}
    return render_to_response('terms-of-use.html', __data__, content_type="text/html")
