from django.template.loader import get_template
from django.template import Context
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound
from django.conf import settings

from django.db.models import Q

from downloads import models as downloads_models

from vyperlogix.django.decorators import cache

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.html import myOOHTML as oohtml

from vyperlogix.lists.ListWrapper import ListWrapper

from vyperlogix.misc import ObjectTypeName

from vyperlogix.html import anchors
from vyperlogix.html.strip import strip_tags

from vyperlogix.django import django_utils

from vyperlogix.misc import jsmin

from vyperlogix.django import pages

from vyperlogix.products import keys

from vyperlogix.django import captcha

from vyperlogix.decorators.TailRecursive import tail_recursion

from vyperlogix.mail import validateEmail

from vyperlogix.django.sqlalchemy import post_vars

from vyperlogix.enum.Enum import Enum

from views import default as views_default

import os
import urllib
import random
import mimetypes

import md5

import utils

import mechanize, urllib2

import BeautifulSoup

class TokenOptions(Enum):
    none = 0
    count = 1
    filelist = 2
    rawlist = 3
    downloadslist = 4

def get_token(url):
    req = urllib2.Request(url)
    req.add_header("Referer", url)
    #req.add_header("X-Forwarded-For", '10.1.10.1')
    r = mechanize.urlopen(req)
    return r

def fetch_remote_token(option):
    b = get_token('http://downloads.near-by.info/get_token.php')
    _token = b.read().strip().upper()
    _toks = [keys._decode(t) for t in _token.split(',')]
    #_toks[0] = _utils.getFromDateTimeStr(_toks[0],format=_utils.format_PHPDateTimeStr())
    soup = BeautifulSoup.BeautifulSoup(_toks[-1])
    items = soup.findAll('name')
    if (option == TokenOptions.count):
	return '%d' % (len(items))
    elif (option == TokenOptions.filelist) or (option == TokenOptions.downloadslist):
	l = sorted([item.contents[0] for item in items],cmp=lambda x,y: cmp(x.lower(), y.lower()))
	h = oohtml.Html()
	ul = h.tagUL()
	for item in l:
	    if (option == TokenOptions.downloadslist):
		secs = _utils.timeSeconds() + (60*60*2)
		dt = _utils.timeStampLocalTime(secs,format='%B %d, %Y %H:%M:%S')
		anchor = 'http://downloads.near-by.info/download.php?f=%s&x=%s' % (keys._encode(item),keys._encode(dt))
		_item = '<a href="%s" target="_blank" title="Downloading %s">%s</a>' % (anchor,item,item)
	    else:
		_item = item
	    ul._tagLI(_item)
	return h.toHtml()
    elif (option == TokenOptions.rawlist):
	l = sorted([item.contents[0] for item in items],cmp=lambda x,y: cmp(x.lower(), y.lower()))
	return l
    return 'UNKNOWN'

def remote_count(request):
    return HttpResponse(fetch_remote_token(TokenOptions.count))

def remote_list(request):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    return HttpResponse(fetch_remote_token(TokenOptions.filelist if (url_toks[-1] == '0') else TokenOptions.downloadslist))

def downloads(request,SSL=False):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)

    if (utils.is_authenticated(request)) and (len(url_toks) == 2):
	f = url_toks[-1]
	t_content = get_template('_downloads_downloading.html')
	d = {'URL':'http://downloads.near-by.info/download.php?f=%s' % (keys._encode(f)),
	     'TITLE':f,
	     'CAPTION':f
	     }
	c = Context(d)
	content = t_content.render(c)
	return HttpResponse(content)
    
    _content = ''
    if (len(url_toks) == 2):
	HttpResponseRedirect('/downloads/')
    h = oohtml.Html()
    div = h.tagDIV(_content,style="background-color:#FF6; color: #00F; .h3 { color:#00F; font-size: 18px; }")

    s_content = ''
    s_non_members_notice = ''
    if (utils.is_authenticated(request)):
	t_members_content = get_template('_downloads_members.html')
	s_content = ''
    else:
	t_members_content = get_template('_downloads_non-members.html')
	s_non_members_notice = '(for Members only - <a href="/register/" target="_top" style="color: #00F; font-size: 12px;">Get Registered</a>)'

    c = Context({'CONTENT':s_content})
    members_content = t_members_content.render(c)

    t_content1 = get_template('_downloads_page1.html')
    c = Context({'DOWNLOADS_LIST':members_content, 'NON_MEMBERS_NOTICE':s_non_members_notice})
    content1 = t_content1.render(c)
    
    t_content = get_template('_downloads_page.html')
    _logged_in = '1' if (utils.is_authenticated(request)) else '0'
    c = Context({'page_content_right':h.toHtml(), 'page_content_left':content1, 'LOGGEDIN':_logged_in})
    content = t_content.render(c)

    return views_default._default(request,content)
