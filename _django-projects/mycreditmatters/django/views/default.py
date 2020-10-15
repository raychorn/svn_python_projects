from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseNotModified

import os, sys

from vyperlogix.misc import _utils

from vyperlogix.django import pages
from vyperlogix.html import myOOHTML as oohtml

from vyperlogix.django import django_utils

import urllib

try:
    from settings import _navigation_tabs
except ImportError:
    from mycreditmatters.settings import _navigation_tabs

try:
    from settings import _navigation_menu_type
except ImportError:
    from mycreditmatters.settings import _navigation_menu_type
    
try:
    from settings import MEDIA_ROOT
except ImportError:
    from mycreditmatters.settings import MEDIA_ROOT

try:
    from settings import MEDIA_URL
except ImportError:
    from mycreditmatters.settings import MEDIA_URL

try:
    from settings import _title
except ImportError:
    from mycreditmatters.settings import _title

def default(request):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)

    c = {'ALT_MEDIA_URL':'http://media.vyperlogix.com/mycreditmatters/',
         }
    html_body_tag = django_utils.load_content_from_template(r'content\_body_tag.html',c)
    
    c.update({'BODY_TAG':html_body_tag})
    sc = {'MEDIA_URL':'http://media.vyperlogix.com/pyeggs/media/',
          'DDTABMENU_URL':'http://media.vyperlogix.com/'
          }
    return pages.render_the_page(request,'%s' % (_title),r'content\index.html',_navigation_menu_type,_navigation_tabs,context=c,styles_context=sc)

def handle_404(request):
    return HttpResponseNotFound(pages._render_the_page(request,'MyCreditMatters - %s' % (_title),'404_content.html',_navigation_menu_type,_navigation_tabs,context={}))

def static_content(request,fullpath):
    import stat
    import mimetypes
    import rfc822
    from django.views.static import was_modified_since
    
    statobj = os.stat(fullpath)
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj[stat.ST_MTIME], statobj[stat.ST_SIZE]):
        return HttpResponseNotModified()
    mimetype = mimetypes.guess_type(fullpath)[0]
    contents = open(fullpath, 'rb').read()
    response = HttpResponse(contents, mimetype=mimetype)
    response["Last-Modified"] = rfc822.formatdate(statobj[stat.ST_MTIME])
    return response

def static(request):
    fpath = '/'.join([MEDIA_ROOT,_utils.eat_leading_token_if_empty(request.path,delim='/')])
    if (os.path.exists(fpath)):
        if (fpath.split('.')[-1] == 'txt'):
            content = _utils.readFileFrom(fpath)
            return HttpResponse(content)
        else:
            try:
                fullpath = '/'.join([MEDIA_ROOT,_utils.eat_leading_token_if_empty(request.path)])
                return static_content(request,fullpath)
            except:
                return HttpResponseNotAllowed(pages._render_the_page(request,'Vyper-Proxy&trade; - %s' % (_title),'405_content.html',_navigation_menu_type,_navigation_tabs,context={}))
    return HttpResponseNotFound(pages._render_the_page(request,'Vyper-Proxy&trade; - %s' % (_title),'404_content.html',_navigation_menu_type,_navigation_tabs,context={}))
