# -*- coding: utf-8 -*-
import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, update_object
from mimetypes import guess_type
from django.shortcuts import render_to_response
from django.template import loader
from django.template import Context

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site, RequestSite

from random import choice, sample

import models

import re

import mimetypes

import logging

from settings import TEMPLATE_DIRS,USE_I18N

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc import _utils
from vyperlogix.django import django_utils
from vyperlogix.django.static import django_static

from vyperlogix.enum import Enum

class ImageTypes(Enum.Enum):
    none = 0
    tb = 1

class ImageFolderTypes(Enum.Enum):
    default = 0
    logo = 1

__mimetype = mimetypes.guess_type('.html')[0]

_title = 'Vyper Logix Corp, The 21st Century Python Company'

__product__ = 'SecureImage&trade;'
__version__ = '1.0.0.0'

__content__ = '''{{ content }}'''

_image_types_ = ['jpg','gif','png']

ext_mimetypes = {}

import random

def image(request,args): # /get-image/tb/logo or /get-image/
    import settings, glob, os.path
    isOkay = django_utils.is_request_okay(request)
    if (isOkay):
        parms = django_utils.parse_url_parms(request)
        image_ext = None
        image_data = None
        image_type = ImageTypes.none
        image_folder_type = ImageFolderTypes.default
        if (len(parms) > 1):
            image_type = ImageTypes(parms[1])
        if (len(parms) > 2):
            image_folder_type = ImageFolderTypes(parms[2])
        image_dir = settings.LOGO_IMAGES_DIR if (image_folder_type.value == 1) else settings.DEFAULT_IMAGES_DIR
        for t in _image_types_:
            ext_mimetypes[t] = mimetypes.guess_type('.%s' % (t))[0]
        if (os.path.isdir(image_dir) == False):
            raise Http404('ERROR 101 :: No images are available at this time.')
        images = []
        for ext in ext_mimetypes.keys():
            paths = [n for n in glob.glob(os.path.join(image_dir, '*.' + ext)) if (image_type.value == 0) or (os.path.splitext(n)[0].endswith(image_type.name))]
            images.extend(paths)
        if (len(images) == 0):
            raise Http404('ERROR 201 :: No images are available at this time.')
        try:
            _images_ = request.session.get('__random_image__')
            _is_list = misc.isList(_images_)
            _images_ = [_images_] if (not _is_list) and (_images_ != None) else _images_[0] if (_is_list) else []
            _images_ = [_images_] if (not misc.isList(_images_)) else _images_
            l_images = list(set(images)-set(_images_))
            if (len(l_images) == 0):
                l_images = images
                _images_ = []
            image = random.choice(l_images)
            #image_ext =  os.path.splitext(image)[-1].split('.')[-1]
            #image_data = open(image, 'rb').read()
            _images_.append(image)
            request.session['__random_image__'] = _images_
            request.session.save()
        except:
            raise Http404('ERROR 301 :: No images are available at this time.')
        return django_static.serve(image,nocache=True) #HttpResponse(image_data, mimetype=ext_mimetypes.get(image_ext))
    return HttpResponseNotFound(pages._render_the_page(request,__title__,'404.html',None,None,context={}))
