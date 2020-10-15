# -*- coding: utf-8 -*-
import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, update_object
from google.appengine.ext import db
from mimetypes import guess_type
from django.template import loader
from django.template import Context

from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response
from django.contrib.auth.decorators import login_required

from random import choice, sample
from google.appengine.api import memcache

from vyperlogix.google.gae import unique

import models

import re

import mimetypes

import logging

from settings import TEMPLATE_DIRS,USE_I18N

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc import _utils
from vyperlogix.django import django_utils

from vyperlogix.enum import Enum

class ImageTypes(Enum.Enum):
    none = 0
    tb = 1

__mimetype = mimetypes.guess_type('.html')[0]

_title = 'Vyper Logix Corp, The 21st Century Python Company'

__product__ = 'SecureImage&trade;'
__version__ = '1.0.0.0'

__content__ = '''{{ content }}'''

def image(request,args):
    import settings, glob, random, os.path
    parms = django_utils.parse_url_parms(request)
    image_ext = None
    image_data = None
    image_dir = settings.BANNER_DIR
    image_type = ImageTypes.none
    if (len(parms) > 1):
        image_type = ImageTypes(parms[1])
    ext_mimetypes = {
        'jpg': 'image/jpeg',
        'gif': 'image/gif',
        'png': 'image/png', }
    if (os.path.isdir(image_dir) == False):
        raise Http404('ERROR 101 :: No images are available at this time.')
    images = []
    for ext in ext_mimetypes.keys():
        paths = [n for n in glob.glob(os.path.join(image_dir, '*.' + ext)) if (image_type.value == 0) or (os.path.splitext(n)[0].endswith(image_type.name))]
        images.extend(paths)
    if (len(images) == 0):
        raise Http404('ERROR 201 :: No images are available at this time.')
    try:
        image = random.choice(images)
        image_ext =  os.path.splitext(image)[-1].split('.')[-1]
        image_data = open(image, 'rb').read()
    except:
        raise Http404('ERROR 301 :: No images are available at this time.')
    return HttpResponse(image_data, mimetype=ext_mimetypes.get(image_ext))
