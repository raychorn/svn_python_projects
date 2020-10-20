import re
import string
import sys
import httplib
import urllib2
from xml.dom import minidom

from vyperlogix.misc import _utils
from vyperlogix.classes import SmartObject
from vyperlogix.misc import ObjectTypeName

import urllib
import mechanize, urllib2
from vyperlogix.url import _urllib2

from BeautifulSoup import BeautifulStoneSoup

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

class ModelFeed:
    def __init__(self):
        self.data = []
	self.browser = mechanize.Browser(
	    factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True)
	    )
	self.browser.set_handle_robots(False)

    def walk_nodes(self, url, callback=None):
	self.referer = url
	self.request = urllib2.Request(url)
	self.request.add_header("Referer", self.referer)
	self.browser.open(self.request)
	c = self.browser.response().read()
	self.soup = BeautifulStoneSoup(c)

        try:
	    item_nodes = self.soup.findAll("item")
            for item in item_nodes:
		so = SmartObject.SmartObject()
                for node in item.recursiveChildGenerator():
		    if (ObjectTypeName.typeClassName(node) == 'BeautifulSoup.Tag') and (node.string):
			so[node.name] = _utils.ascii_only(node.string.extract())
		if (callable(callback)):
		    callback(so)
        except Exception, e:
            info_string = _utils.formattedException(details=e)
	    so = SmartObject.SmartObject()
	    s.info_string = info_string
            items.append(so)

    def links(self, url):
        items = []

	def handle_node(node):
	    items.append(node.link)

        try:
	    self.walk_nodes(url,handle_node)
        except Exception, e:
            info_string = _utils.formattedException(details=e)
            items.append(info_string)
            items.append(str(file_feed))

        return items

    def nodes(self, url):
        items = []

	def handle_node(node):
	    items.append(node)

        try:
	    self.walk_nodes(url,handle_node)
        except Exception, e:
            info_string = _utils.formattedException(details=e)
            items.append(info_string)
            items.append(str(file_feed))

        return items

def read_feed_links(feedurl):
    feed = ModelFeed()
    links = feed.links(feedurl)
    return links

def read_feed(feedurl):
    feed = ModelFeed()
    nodes = feed.nodes(feedurl)
    return nodes

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

    def main(feedname):
        links = read_feed_links(feedname)
        #print links
        objects = read_feed(feedname)
        print objects

    #main('http://python2.wordpress.com/feed/') 
    #main('http://rss.slashdot.org/Slashdot/slashdot') 
    main('http://pypi.python.org/pypi?%3Aaction=rss')
    
