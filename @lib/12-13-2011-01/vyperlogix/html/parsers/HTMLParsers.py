import urllib
import httplib
from vyperlogix.hash import lists
from HTMLParser import HTMLParser

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
#from vyperlogix.decorators import properties_idiom
from HTMLParser import interesting_normal
from vyperlogix.classes.CooperativeClass import Cooperative

class TargetedHTMLParser(Cooperative,HTMLParser):
    def init(self): # do NOT implement the __init__() method to avoid problems with the super-class...
        self._targetTag = ''
        self._targetAttr = ''
        self.tagCount = 0
        self.tagContents = []
        self.rawdata = ''
        self.__offset__ = 0
        self.__lineno__ = 0
        self.__callback__ = None
        self.__bucket__ = []
        self.__is__ = False
        self.__interesting__ = interesting_normal

    def __repr__(self):
        s = '\n'.join([t for t in self.tagContents])
        return '(%s) targetTag=(%s), targetAttr=(%s), tagCount=(%s)\ntagContents=(%s).' % (str(self.__class__),self._targetTag,self._targetAttr,self.tagCount,s)

    def targetTag(self,tag):
        self.init()
        self._targetTag = tag
        if (self._targetTag == 'a'):
            self._targetAttr = 'href'

    def isInterestInThisTag(self,tag,attrs=[], state=None):
        bool = True
        if (callable(self.callback)):
            try:
                return self.callback(self,tag,attrs=attrs, state=state)
            except:
                pass
        try:
            if ( (len(self._targetTag) > 0) and (len(self._targetAttr) > 0) ):
                bool = ( (self._targetTag == tag) and (attrs[0][0] == self._targetAttr) and (str(attrs[0][1]).find('google.com') == -1) and (str(attrs[0][1]).startswith('http://') == True) )
        except:
            pass
        return bool
    
    def interesting():
        doc = "interesting"
        def fget(self):
            return self.__interesting__
        def fset(self, value):
            self.__interesting__ = value
        return locals()    
    interesting = property(**interesting())
    
    def offset():
        doc = "offset"
        def fget(self):
            return self.__offset__
        def fset(self, value):
            self.__offset__ = value
        return locals()    
    offset = property(**offset())
    
    def lineno():
        doc = "lineno"
        def fget(self):
            return self.__lineno__
        def fset(self, value):
            self.__lineno__ = value
        return locals()    
    lineno = property(**lineno())
    
    def callback():
        doc = "callback"
        def fget(self):
            return self.__callback__
        def fset(self, value):
            self.__callback__ = value
        return locals()    
    callback = property(**callback())
    
    def bucket():
        doc = "bucket"
        def fget(self):
            return self.__bucket__
        return locals()    
    bucket = property(**bucket())
    
    def handle_starttag(self, tag, attrs, state='START'):
        if (self.isInterestInThisTag(tag,attrs,state=state) == True):
            self.tagCount += 1
            items = [t for t in self.get_starttag_text().split('"') if t.startswith('http://') or t.startswith('https://')]
            if (len(items) > 0):
                self.tagContents.append(items[0])
                print "Encountered the beginning of a '%s' tag [%s]" % (tag,attrs)

    def handle_endtag(self, tag, state='END'):
        if (self.isInterestInThisTag(tag,state=state) == True):
            print "Encountered the end of a '%s' tag" % tag
            pass

