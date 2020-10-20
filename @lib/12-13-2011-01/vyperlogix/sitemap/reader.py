import re
import string
import sys
import httplib
import urllib2
from xml.dom import minidom

from vyperlogix.misc import _utils

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

class ModelSitemap:
    def __init__(self):
        self.data = []

    def links (self, address):
        file_request = urllib2.Request(address)
        file_opener = urllib2.build_opener()
        file_feed = file_opener.open(file_request).read()

        items = []

        file_feed = _utils.ascii_only(file_feed)
        try:
            file_xml = minidom.parseString(file_feed)
            item_nodes = file_xml.getElementsByTagName("url")
    
            for item in item_nodes:
                nodes = []
                for node in [n for n in item.childNodes if (n.nodeName == 'loc')]:
                    try:
                        nodes.append(node.firstChild.data)
                    except:
                        pass
                for n in nodes:
                    items.append(n)
        except Exception, e:
            info_string = _utils.formattedException(details=e)
            items.append(info_string)
            items.append(str(file_feed))

        return items

def read_sitemap_links(url):
    sitemap = ModelSitemap()
    links = sitemap.links(url)
    return links

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
    