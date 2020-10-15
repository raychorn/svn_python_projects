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

import BeautifulSoup

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

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

class ZoneEdit(CooperativeClass.Cooperative):
    def __init__(self,username,password):
	self.callback_addForm = None
	self.callback_editForm = None
	
	self._url = 'http://www.zoneedit.com/'
	self.url = '%sauth/' % (self._url)
    
	self.browser = mechanize.Browser(
	    factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True)
	    )
	self.browser.set_handle_robots(False)
	self.browser.add_password(self.url, username, password)

	self.__zone__ = None

    def _drill_into_Zone_Facet(self,url):
	self.request = urllib2.Request(url)
	self.request.add_header("Referer", self.referer)
	self.browser.open(self.request)
	c = self.browser.response().read()
	self.soup = BeautifulSoup.BeautifulSoup(c)
	self.forms = self.soup.findAll('form')
	self.d_newForm_actions = lists.HashedLists2()
	for f in self.forms:
	    self.d_newForm = lists.HashedLists2()
	    self.d_form = lists.HashedFuzzyLists2(dict(f.attrs))
	    if (self.d_form['name'] == 'add'):
		children = f.findChildren('input')
		for aChild in children:
		    self.d_child = lists.HashedFuzzyLists2(dict(aChild.attrs))
		    self.d_newForm[self.d_child['name']] = self.d_child['value']
		action = self.d_form['action']
		self.d_newForm_actions[self.d_form['name']] = action
		if (callable(self.callback_addForm)):
		    try:
			self.callback_addForm(self,action=action)
		    except:
			pass
	    elif (self.d_form['name'] == 'edit'):
		children = f.findChildren('input')
		self.tuples = []
		self.d_tuples = lists.HashedFuzzyLists2()
		elements = []
		pattern = ['id','oldfrom','oldto','del']
		p = []
		for aChild in children:
		    d_form = lists.HashedLists2(dict(aChild.attrs))
		    name = str(d_form['name'])
		    if (pattern[len(p)] == name):
			elements.append(d_form)
			p.append(name)
			if (p == pattern):
			    self.tuples.append(elements)
			    oldfrom = [e for e in elements if (e['name'] == 'oldfrom')]
			    oldto = [e for e in elements if (e['name'] == 'oldto')]
			    if (len(oldfrom) == 1) and (len(oldto) == 1):
				self.d_tuples[oldfrom[0]['value']] = oldto[0]['value'],elements
			    elements = []
			    p = []
		action = self.d_form['action']
		self.d_newForm_actions[self.d_form['name']] = action
		if (callable(self.callback_editForm)):
		    try:
			self.callback_editForm(self,action=action)
		    except:
			pass
		    
    def _drill_into_Zone(self,url,facet='CNAME'):
	self.request = urllib2.Request(url)
	self.request.add_header("Referer", self.referer)
	self.browser.open(self.request)
	for aLink in self.browser.links():
	    if (aLink.url.find('?zone=%s&type=%s' % (self.zoneName,facet)) > -1):
		self._drill_into_Zone_Facet(aLink.absolute_url)
    
    def drill_into_Zone(self,zoneName,facet='CNAME'):
	'''drill into the Zone using the specified facet.'''
	self.zoneName = zoneName
	self.referer = self._url
	self.request = urllib2.Request(self.url)
	self.request.add_header("Referer", self.referer)
	self.browser.open(self.request)
	for aLink in self.browser.links():
	    if (aLink.url.find('?zone=%s' % (self.zoneName)) > -1):
		self._drill_into_Zone(aLink.absolute_url,facet=facet)

    def __processForm__(self,d_form,action):
	url = '%s%s%s' % (self.url,'/' if (not self.url.endswith('/')) else '',action)
	request = urllib2.Request(url)
	request.add_header("Referer", self.referer)
	data = urllib.urlencode([(k,v) for k,v in d_form.iteritems()])
	self.browser.open(request, data)
	c = ''.join([l.strip() for l in self.browser.response().readlines() if (len(l.strip()) > 0)])
	soup = BeautifulSoup.BeautifulSoup(c)
	forms = soup.findAll('form')
	for f in forms:
	    d_newForm = lists.HashedLists2()
	    d_form = lists.HashedFuzzyLists2(dict(f.attrs))
	    if (d_form['name'] == 'edit'):
		submits = []
		children = f.findChildren('input')
		for aChild in children:
		    d_child = lists.HashedFuzzyLists2(dict(aChild.attrs))
		    if (d_child['type'] == 'submit'):
			submits.append(d_child)
		    else:
			d_newForm[d_child['name']] = d_child['value']
		url = '%s%s%s' % (self.url,'/' if (not self.url.endswith('/')) else '',d_form['action'])
		request = urllib2.Request(url)
		request.add_header("Referer", self.referer)
		try:
		    aSubmit = [aSubmit for aSubmit in submits if (aSubmit['value'].lower() == 'yes')][0]
		    d_newForm[aSubmit['name']] = aSubmit['value']
		except:
		    pass
		data = urllib.urlencode([(k,v) for k,v in d_newForm.iteritems()])
		self.browser.open(self.request, data)

    def add_to_Zone(self,d_form,action):
	self.__processForm__(d_form,action)

    def delete_from_Zone(self,d_form,action):
	self.__processForm__(d_form,action)

    def zones(self):
	zones = []
	self.referer = self._url
	self.request = urllib2.Request(self.url)
	self.request.add_header("Referer", self.referer)
	self.browser.open(self.request)
	for aLink in self.browser.links():
	    if (aLink.url.find('?zone=') > -1):
		zones.append(aLink.url.split('?')[-1].split('=')[-1].lower())
	return zones
    
    def zone(self,name):
	self.__zone__ = name

    def cnames(self):
	cnames = []
	self.drill_into_Zone(self.__zone__,facet='CNAME')
	for t in self.tuples:
	    oldfroms = [d for d in t if (d['name'] == 'oldfrom')]
	    if (len(oldfroms) > 0):
		cnames.append(str(oldfroms[0]['value']))
	return cnames
    
from vyperlogix.classes.MagicObject import MagicObject2

class ZoneEditProxy(MagicObject2):
    '''
    This object holds onto a ZoneEdit object that interfaces with ZoneEdit.Com.
    '''
    def __init__(self,zone_proxy):
	self.__zone_proxy__ = zone_proxy
	
    def zone_proxy():
	doc = "zone_proxy"
	def fget(self):
	    return self.__zone_proxy__
	return locals()
    zone_proxy = property(**zone_proxy())
	
    def __call__(self,*args,**kwargs):
	s = 'self.zone_proxy.%s(*args,**kwargs)' % (self.n.pop())
	try:
	    objects = eval(s)
	except Exception, details:
	    objects = None
	    info_string = _utils.formattedException(details=details)
	return objects if (objects is not None) else self
