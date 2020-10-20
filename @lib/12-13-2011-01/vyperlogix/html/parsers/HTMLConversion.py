from vyperlogix import misc
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.misc import _utils

from vyperlogix.hash import lists

from vyperlogix.classes import CooperativeClass

import urllib
import mechanize, urllib2
from vyperlogix.url import _urllib2

import BeautifulSoup

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

__parse__ = lambda s:misc.__unpack__(s).split(' (')[-1].split(')')[0]

class HTMLConversion(CooperativeClass.Cooperative):
    def __init__(self):
	self.__html__ = None
	
    @classmethod
    def unpack(self,s):
	return misc.__unpack__(s)

    @classmethod
    def parse(self,s):
	return __parse__(s)

    def html():
        doc = "html"
        def fget(self):
            return self.__html__
        def fset(self, html):
            self.__html__ = _utils.ascii_only(html)
        return locals()
    html = property(**html())

    def process(self, html=None):
	l = lists.HashedLists()
	n = 1
	def recurse_into(aTag,_list=lists.HashedLists(),n=1):
	    is_tag = lambda t:(misc.ObjectTypeName.typeClassName(t) == 'BeautifulSoup.Tag')
	    is_valid_tag = lambda t:(t.name in ['table','tr','th','td'])
	    if (is_tag(aTag)) and (is_valid_tag(aTag)):
		for aKid in aTag.childGenerator() if (is_valid_tag(aTag)) else []:
		    if (is_tag(aKid)):
			print misc.ObjectTypeName.typeClassName(aKid), aKid.name,
			if (aKid.name == 'table'):
			    recurse_into(aKid,_list=_list,n=n)
			elif (aKid.name == 'tr'):
			    n += 1
			    print
			    recurse_into(aKid,_list=_list,n=n)
			elif (aKid.name in ['th','td']):
			    data = aKid.contents if (misc.isList(aKid.contents)) and (len(aKid.contents) == 1) else [misc.unpack([t for t in aKid.contents if (not is_tag(t))])]
			    print data
			    _list['%s' % (n)] = data
	    return
	
	if (html is not None):
	    self.html = _utils.ascii_only(html)
	soup = BeautifulSoup.BeautifulSoup(self.html)
	tables = soup.findAll('table')
	for aTable in tables:
	    recurse_into(aTable,_list=l,n=n)
	print '='*40
	keys = misc.sortCopy([int(k) for k in l.keys()])
	items = ListWrapper()
	for k in keys:
	    _items = l['%s' % (k)]
	    items.append([_items])
	return items
    
from vyperlogix.classes.MagicObject import MagicObject2

class HTMLConversionProxy(MagicObject2):
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
