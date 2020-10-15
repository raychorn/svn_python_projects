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

_root_ = os.path.dirname(__file__)

