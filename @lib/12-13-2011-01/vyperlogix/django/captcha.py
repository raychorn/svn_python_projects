from django.shortcuts import render_to_response
import os, sys
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.template.loader import render_to_string
from django.template import Context

from vyperlogix.django import django_utils

from vyperlogix import misc
from vyperlogix.django import pages
from vyperlogix.misc import _utils

from vyperlogix.hash import lists

def render_captcha_form(request,form_name=None,font_name=None,font_size=18,choices='QWERTYPASDFGHJKLZXCVBNM23456789',fill=(255,255,255),bgImage='bg.jpg'):
    try:
        imghash = ''
        tempname = ''
        imgtext = ''
        try:
            from random import choice
            import Image, ImageDraw, ImageFont, sha
            _settings = django_utils.get_from_session(request,'settings',default=lists.HashedLists2())
            if (not _settings.has_key('SECRET_KEY')):
                from django.conf import settings as _settings
            SALT = _settings.SECRET_KEY[:20]
            imgtext = ''.join([choice(choices) for i in range(5)])
            imghash = sha.new(SALT+imgtext).hexdigest()
            image_fname = os.path.join(_settings.MEDIA_ROOT,bgImage)
            im=Image.open(image_fname)
            draw=ImageDraw.Draw(im)
            font_fname = os.path.join(_settings.MEDIA_ROOT,font_name)
            font=ImageFont.truetype(font_fname, font_size)
            draw.text((10,10),imgtext, font=font, fill=fill)
            _captcha_symbol = 'captcha'
            image_name = '%s.jpg' % (imgtext)
            temp = os.path.join(_settings.MEDIA_ROOT,_captcha_symbol,image_name)
            _utils._makeDirs(os.path.dirname(temp))
            tempname = '/'.join([_settings.MEDIA_URL,_captcha_symbol,image_name])
            if (os.path.exists(tempname)):
                os.remove(tempname)
            im.save(temp, "JPEG")
        except:
            imghash = ''
            tempname = ''
            imgtext = ''
    except Exception, e:
        return _utils.formattedException(details=e)

    if (misc.isString(form_name)):
        c = {'hash': imghash, 'tempname': tempname}
        http_host = django_utils.get_http_host(request).split(':')[0]
        if (django_utils.isBeingDebugged(http_host)):
            c['imgtext'] = imgtext
        ctx = Context(c, autoescape=False)
        return render_to_string(form_name, context_instance=ctx)
    else:
        return render_to_string('405.html', {})

def is_captcha_form_valid(request):
    import sha
    if request.POST:
        data = request.POST.copy()
        _settings = django_utils.get_from_session(request,'settings',default=lists.HashedLists2())
        if (not _settings.has_key('SECRET_KEY')):
            from django.conf import settings as _settings
        SALT = _settings.SECRET_KEY[:20]
        try:
            return data['imghash'] == sha.new(SALT+data['imgtext']).hexdigest()
        except:
            return False
    return False

