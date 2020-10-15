from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.conf import settings

from vyperlogix.django.decorators import cache

from vyperlogix.misc import _utils

import os

from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix.js import minify

from vyperlogix.django import pages
from vyperlogix.html import myOOHTML as oohtml

from vyperlogix.django import django_utils

from vyperlogix.products import keys

from vyperlogix.django.rss import content as rss_content

import urllib

import socket

_title = 'PDFxporter 1.0'
sub_title = 'Take Control of your PDF Bank Statements'

def render_static_html(request,_title,template_name,template_folder='',context={}):
    return pages._render_the_template(request,_title,template_name,context=context,template_folder=template_folder)

@cache.cache(settings.CACHE_TIMER)
def rss_feed(url):
    return rss_content.rss_content(url)

def formatTimeStr():
    return '%m/%d/%Y %H:%M:%S'

def formatYYYYStr():
    return '%Y'

def default(request):
    from content import models as content_models
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    
    menu_tags = content_models.Content.objects.order_by('menu_tag')
    
    normalize_url = lambda url:'/' if (not str(url).startswith('/')) else ''
    
    t_analytics = get_template('new/_google_analytics.html')
    t_footer = get_template('new/_footer.html')
    _context = {'GOOGLE_ANALYTICS':t_analytics.render(Context({})),
		'LEFT_CONTENT':'',
		'INNER_CONTENT':'',
		'FOOTER':t_footer.render(Context({'CURRENT_YEAR':_utils.timeStampLocalTime(format=_utils.formatDate_YYYY())})),
		'TITLE':'%s - %s (%s)'
		}
    is_bold = False
    aTag = None
    _filler = '&nbsp;'*10
    menu_links = [[]]
    if (len(url_toks) > 0):
	menu_links.append([_filler,'<a href="%s" target="_top">%s</a>' % ('/','Home')])
    for _aTag in menu_tags:
	_url = '%s%s%s' % (normalize_url(_aTag.url),_aTag.url,normalize_url(_aTag.url))
	_url_ = '%s%s%s' % (normalize_url(url_toks[0]),url_toks[0],normalize_url(url_toks[0])) if (len(url_toks) == 1) else ''
	is_bold = _url == _url_
	if (is_bold):
	    h = oohtml.Html()
	    h.tagB(_aTag.menu_tag)
	    tag_content = h.toHtml()
	    aTag = _aTag
	    _anchor = tag_content
	    _context['INNER_CONTENT'] = aTag.content
	else:
	    tag_content = _aTag.menu_tag
	    _anchor = oohtml.renderAnchor(_url,tag_content,target="_top")
	menu_links.append([_filler,_anchor])
	
    h = oohtml.Html()
    h.html_simple_table(menu_links, width="255", border="0")
    left_content = h.toHtml()

    _context['LEFT_CONTENT'] = left_content
    
    if (len(url_toks) == 0):
	inner_home_context = {'LATEST_NEWS_CONTENT':rss_feed('http://www.pypi.info/feeds/rss2/'),
			      }
	_context['INNER_CONTENT'] = render_static_html(request,'','_inner_home.html',template_folder='new',context=inner_home_context)
    now = _utils.timeStamp(format=pages.formatTimeStr())
    _context['TITLE'] = _context['TITLE'] % (_title,sub_title,now)
    return pages.render_the_template(request,'%s' % (_title),'index.html',context=_context,template_folder='new')

