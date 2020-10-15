from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseNotModified

import os, sys

from vyperlogix.misc import _utils

from vyperlogix.django import pages
from vyperlogix.html import myOOHTML as oohtml

import urllib

try:
    from settings import _navigation_tabs
except ImportError:
    from resources.settings import _navigation_tabs

try:
    from settings import _navigation_menu_type
except ImportError:
    from resources.settings import _navigation_menu_type
    
try:
    from settings import MEDIA_ROOT
except ImportError:
    from resources.settings import MEDIA_ROOT

try:
    from settings import MEDIA_URL
except ImportError:
    from resources.settings import MEDIA_URL

try:
    from settings import _title
except ImportError:
    from resources.settings import _title

def default(request):
    import urllib
    from vyperlogix.lists.ListWrapper import ListWrapper
    from models import Node
    
    strip_prefix = lambda url:url.replace('/folder','').replace('//','/')
    
    def render_icon(url,name,isfile=True,isurl=False):
        h = oohtml.Html()
        span = h.tagSPAN('')
        gif_name = 'document' if (isfile) else 'url' if (isurl) else 'folder'
        if (isfile):
            typ = name.split('.')[-1]
            if (typ in ['py','pyc','pyo']):
                gif_name = 'python'
            elif (typ == 'html'):
                gif_name = 'html'
            elif (typ in ['gif','png','ico']):
                gif_name = 'image'
            elif (typ == 'jpg'):
                gif_name = 'jpeg'
            elif (typ == 'css'):
                gif_name = 'css'
            elif (typ in ['zip','tar','gz']):
                gif_name = 'zipfile'
            elif (typ in ['exe','com']):
                gif_name = 'executable'
            elif (typ in ['cmd','bat','sh']):
                gif_name = 'command'
            elif (typ in ['c','cpp']):
                gif_name = 'code'
        img = span.tag(oohtml.oohtml.IMG,src='/icons/%s.gif' % (gif_name),title=name,alt=name)
        span.text2('&nbsp;%s' % (name))
        if (isurl):
            link = oohtml.renderAnchor('%s' % (name),h.toHtml(),target='_blank')
        else:
            link = oohtml.renderAnchor('%s' % (url if (len(url) > 0) else '/'),h.toHtml(),target='_top')
        return link

    def render_nodes(tag,prefix,nodes):
        try:
            for node in nodes.order_by('name'):
                #link = oohtml.renderAnchor('/folder%s/%s/' % (prefix,urllib.quote_plus(node.name)),node.name,target='_top')
                link = render_icon('/folder%s/%s/' % ('%s%s'%('/' if (len(prefix) > 0) else '',prefix),urllib.quote_plus(node.name)),node.name,isfile=node.is_file == 1,isurl=node.is_url == 1)
                tag._tagLI(link)
        except Exception, details:
            info_string = _utils.formattedException(details=details)
            tag._tagLI(info_string.replace('\n','<BR/>'))

    def render_folder_open(tag,url):
        title = lambda url:url if (len(url) > 0) else '(Up One Level)'
        _url = '/'.join(_utils.eat_leading_token_if_empty(strip_prefix(url)).split('/')[0:-1])
        h = oohtml.Html()
        span = h.tagSPAN('')
        img = span.tag(oohtml.oohtml.IMG,src='/icons/folder_open.gif',title=title(_url),alt=title(_url))
        span.text2('&nbsp;%s' % (strip_prefix(_url)))
        if (len(_url) > 0):
            _url = '/folder%s%s%s' % ('/' if (_url[0] != '/') else '',_url,'/' if (_url[-1] != '/') else '')
        link = oohtml.renderAnchor('%s' % (_url if (len(_url) > 0) else '/'),h.toHtml(),target='_top')
        tag._tagLI(link)

    folder_path = url_toks = ListWrapper([urllib.unquote_plus(t) for t in request.path.split('/') if (len(t) > 0)])
    
    i = url_toks.find('folder')

    h = oohtml.Html()
    ul = h.tag(oohtml.oohtml.UL)
    prefix = '/'.join(folder_path)
    
    nodes = Node.objects.filter(parent=-1)
    if (i > -1):
        render_folder_open(ul,request.path)
        ul = ul.tag(oohtml.oohtml.UL)
        folder_path = url_toks[i+1:]
        prefix = '/'.join(folder_path)
        for token in folder_path:
            _nodes = nodes.filter(name=token)
            for node in _nodes:
                nodes = Node.objects.filter(parent=node.id)
        render_nodes(ul,prefix,nodes)
    else:
        render_nodes(ul,prefix,nodes)

    content = h.toHtml()

    return pages.render_the_page(request,'%s' % (_title),'_home.html',_navigation_menu_type,_navigation_tabs,context={'HOME_CONTENT':content})

def about(request):
    return pages.render_the_page(request,'About - %s' % (_title),'_about.html',_navigation_menu_type,_navigation_tabs,context={})

def handle_404(request):
    return HttpResponseNotFound(pages._render_the_page(request,'Vyper-Proxy&trade; - %s' % (_title),'404_content.html',_navigation_menu_type,_navigation_tabs,context={}))

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
