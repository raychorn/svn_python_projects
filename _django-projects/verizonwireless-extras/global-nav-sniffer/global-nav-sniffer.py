import os, sys, re
import datetime
import random

from vyperlogix import misc
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.misc import _utils

from vyperlogix.hash import lists

from vyperlogix.classes import CooperativeClass

import urllib
import mechanize, urllib2
from vyperlogix.url import _urllib2

from vyperlogix.xml.xml_utils import quote_plus_if_required

import BeautifulSoup

__copyright__ = """\
(c). Copyright 1990-2014, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

class VerizonWireless(CooperativeClass.Cooperative):
    def __init__(self):
	self.__html__ = None
	
	self._url = 'http://www.verizonwireless.com/b2c/index.html'
	self.url = '%s' % (self._url)
    
	self.browser = mechanize.Browser(
	    factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True)
	    )
	self.browser.set_handle_robots(False)

    def html():
        doc = "html"
        def fget(self):
            return self.__html__
        def fset(self, html):
            self.__html__ = _utils.ascii_only(html)
        return locals()
    html = property(**html())

    def global_nav(self, html=None):
	xml = '<{{ head_tag }} metaField="{{ metadata_tag }}" dataField="{{ body_tag }}">'
	xml += '<{{ metadata_tag }} xmlLabel="{{ xmlLabel }}"/>'
	xml += '<{{ metadata_tag }} xmlUrl="{{ xmlUrl }}"/>'
	xml += '<{{ metadata_tag }} xmlType="{{ xmlType }}"/>'
	xml += '<{{ metadata_tag }} xmlData="{{ xmlData }}"/>'
	xml += '<{{ metadata_tag }} xmlGroup="{{ xmlGroup }}"/>'
	xml += '<{{ metadata_tag }} xmlOrientation="{{ xmlOrientation }}"/>'

	def recurse_into(aTag,hasKids=False):
	    _xml = ''
	    is_valid_tag = lambda t:(t.name in ['div','ul','li','a'])
	    if (misc.ObjectTypeName.typeClassName(aTag) == 'BeautifulSoup.Tag') and (is_valid_tag(aTag)):
		for aKid in aTag.childGenerator() if (is_valid_tag(aTag)) else []:
		    if (misc.ObjectTypeName.typeClassName(aKid) == 'BeautifulSoup.Tag'):
			print misc.ObjectTypeName.typeClassName(aKid), aKid.name
			if (aKid.name == 'ul'):
			    _xml += recurse_into(aKid,hasKids=hasKids)
			    if (hasKids):
				_xml += '</{{ body_tag }}>'
				hasKids = not hasKids
			elif (aKid.name == 'li'):
			    kids = aKid.findChildren(name='ul')
			    _xml += recurse_into(aKid,hasKids=(len(kids) > 0))
			elif (aKid.name == 'a'):
			    d = lists.HashedFuzzyLists(aKid.attrMap)
			    url = d['href']
			    url = url[0] if (misc.isList(url)) else url
			    label = aKid.contents
			    label = label[0] if (misc.isList(label)) else label
			    _xml += '<{{ body_tag }} {{ xmlLabel }}="%s" {{ xmlUrl }}="%s"%s>' % (quote_plus_if_required(label),quote_plus_if_required(url),'/' if (not hasKids) else '')
			    _xml += recurse_into(aKid,hasKids=hasKids)
	    return _xml
	    
	if (html is not None):
	    self.html = _utils.ascii_only(html)
	if (len(self.html) == 0):
	    self.referer = self._url
	    self.request = urllib2.Request(self.url)
	    self.request.add_header("Referer", self.referer)
	    self.browser.open(self.request)
	    self.html = self.browser.response();
	soup = BeautifulSoup.BeautifulSoup(self.html)
	tags = ListWrapper.ListWrapper()
	divs = soup.findAll(id='gn')
	for aDiv in divs:
	    for aTag in aDiv.childGenerator():
		if (misc.ObjectTypeName.typeClassName(aTag) not in ['BeautifulSoup.NavigableString','BeautifulSoup.Comment']) and (aTag.name != 'script'):
		    tags.append(aTag)
	tag_stack = []
	for aTag in tags:
	    print misc.ObjectTypeName.typeClassName(aTag), aTag.name
	    if (aTag.name == 'h2'):
		kids = aTag.findChildren(name='a')
		if (len(kids) > 0):
		    d = lists.HashedFuzzyLists(kids[0].attrMap)
		    url = d['href']
		    url = url[0] if (misc.isList(url)) else url
		    label = kids[0].contents
		    label = label[0] if (misc.isList(label)) else label
		    if (misc.ObjectTypeName.typeClassName(label) == 'BeautifulSoup.Tag'):
			label = label.contents
			label = label[0] if (misc.isList(label)) else label
		    xml += '<{{ body_tag }} {{ xmlLabel }}="%s" {{ xmlUrl }}="%s" align="left" handCursor="true">' % (quote_plus_if_required(label),quote_plus_if_required(url))
		    tag_stack.insert(0,'{{ body_tag }}')
	    else:
		xml += recurse_into(aTag)
		while (len(tag_stack) > 0):
		    xml += '</%s>' % (tag_stack.pop())
	print '='*40
	xml += '</{{ head_tag }}>'
	return xml
    
from vyperlogix.classes.MagicObject import MagicObject2

class VerizonWirelessProxy(MagicObject2):
    '''
    This object holds onto a VerizonWireless object that interfaces with VerizonWireless.Com.
    '''
    def __init__(self,proxy):
	self.__proxy__ = proxy
	
    def proxy():
	doc = "proxy"
	def fget(self):
	    return self.__proxy__
	return locals()
    proxy = property(**proxy())
	
    def __call__(self,*args,**kwargs):
	s = 'self.proxy.%s(*args,**kwargs)' % (self.n.pop())
	try:
	    objects = eval(s)
	except Exception, details:
	    objects = None
	    info_string = _utils.formattedException(details=details)
	return objects if (objects is not None) else self
	
if (__name__ == '__main__'):
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

    from vyperlogix.lists import ListWrapper
    from vyperlogix.misc import ReportTheList
    from vyperlogix.products import keys
    
    from vyperlogix.django import django_utils
    from vyperlogix.classes.SmartObject import SmartFuzzyObject

    find_files = lambda dname,pattern:[f for f in os.listdir(dname) if (os.path.splitext(f)[-1] in ['.html','.htm']) and (f.lower().find(pattern.lower()) > -1)]
	
    logged_in_state_html = ''
    logged_out_state_html = ''
    dname = os.path.dirname(__file__)
    so_logged_in_state = SmartFuzzyObject()
    try:
	files = find_files(dname,'LoggedIn')
	if (len(files) > 0):
	    fname = os.path.join(dname,files[0])
	    so_logged_in_state.fname = fname
	    logged_in_state_html = _utils.readFileFrom(fname)
	    so_logged_in_state.content = logged_in_state_html
    except:
	pass
    so_logged_out_state = SmartFuzzyObject()
    try:
	files = find_files(dname,'LoggedOut')
	if (len(files) > 0):
	    fname = os.path.join(dname,files[0])
	    so_logged_out_state.fname = fname
	    logged_out_state_html = _utils.readFileFrom(fname)
	    so_logged_out_state.content = logged_out_state_html
    except:
	pass

    def get_context(head_tag,body_tag=None,metadata_tag=None,label_tag=None,url_tag=None,type_tag=None,data_tag=None,group_tag=None):
	if (isinstance(head_tag,tuple)):
	    head_tag,body_tag,metadata_tag,label_tag,url_tag,type_tag,data_tag,group_tag = head_tag
	return {'head_tag':head_tag, 'body_tag':body_tag, 'metadata_tag':metadata_tag, 'xmlLabel':label_tag, 'xmlUrl':url_tag, 'xmlType':type_tag, 'xmlData':data_tag, 'xmlGroup':group_tag}

    const_schema_level1 = 'menu','menuitem','meta','label','url','type','data','group'
    const_schema_level2 = 'a','b','c','l','u','t','d','g'
    
    os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'
    
    po = VerizonWirelessProxy(VerizonWireless())
    xml = po.global_nav(so_logged_in_state.content)
    toks = list(os.path.splitext(so_logged_in_state.fname))
    toks[-1] = '.xml'
    fname = ''.join(toks)
    if (misc.ObjectTypeName.typeClassName(xml) in ('str','unicode')):
	xml = django_utils.render_from_string(xml,context=get_context(const_schema_level1))
	_utils.writeFileFrom(fname,xml)
	print 'INFO: Wrote some content to "%s".' % (fname)
    else:
	print 'WARNING: Was not able to save anything in the file named "%s".' % (fname)
    
    po = VerizonWirelessProxy(VerizonWireless())
    xml = po.global_nav(so_logged_out_state.content)
    toks = list(os.path.splitext(so_logged_out_state.fname))
    toks[-1] = '.xml'
    fname = ''.join(toks)
    if (misc.ObjectTypeName.typeClassName(xml) in ('str','unicode')):
	xml = django_utils.render_from_string(xml,context=get_context(const_schema_level1))
	_utils.writeFileFrom(fname,xml)
	print 'INFO: Wrote some content to "%s".' % (fname)
    else:
	print 'WARNING: Was not able to save anything in the file named "%s".' % (fname)
    
