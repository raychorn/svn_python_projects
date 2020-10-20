from vyperlogix import misc
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.misc import _utils

from vyperlogix.hash import lists

from vyperlogix.classes import CooperativeClass

from xml.dom.minidom import parse, parseString

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

class XML2JSon(CooperativeClass.Cooperative):
    def __init__(self,callback=None,callbackB4=None,callbackNodeName=None,verbose=False):
	self.__xml__ = None
	self.__verbose__ = verbose
	self.__callback__ = callback
	self.__callbackB4__ = callbackB4
	self.__callbackNodeName__ = callbackNodeName
	
    @classmethod
    def unpack(self,s):
	return misc.__unpack__(s)

    @classmethod
    def parse(self,s):
	return __parse__(s)

    def xml():
        doc = "xml"
        def fget(self):
            return self.__xml__
        def fset(self, xml):
            self.__xml__ = _utils.ascii_only(xml)
        return locals()
    xml = property(**xml())

    def verbose():
        doc = "verbose"
        def fget(self):
            return self.__verbose__
        def fset(self, verbose):
            self.__verbose__ = verbose if (isinstance(verbose,bool)) else False
        return locals()
    verbose = property(**verbose())

    def callback():
        doc = "callback"
        def fget(self):
            return self.__callback__
        def fset(self, callback):
            self.__callback__ = callback
        return locals()
    callback = property(**callback())
    
    def callbackB4():
        doc = "callbackB4"
        def fget(self):
            return self.__callbackB4__
        def fset(self, callbackB4):
            self.__callbackB4__ = callbackB4
        return locals()
    callbackB4 = property(**callbackB4())
    
    def callbackNodeName():
        doc = "callbackNodeName"
        def fget(self):
            return self.__callbackNodeName__
        def fset(self, callbackNodeName):
            self.__callbackNodeName__ = callbackNodeName
        return locals()
    callbackNodeName = property(**callbackNodeName())

    def _process(self, xml=None):
	d = lists.HashedLists()
	def recurse_into(aTag):
	    _d_ = lists.HashedLists()
	    is_tag = lambda t:(misc.ObjectTypeName.typeClassName(t) == 'xml.dom.minidom.Element')
	    if (is_tag(aTag)):
		_d_[aTag.nodeName] = lists.HashedLists(dict(aTag.attributes.items()))
		for aKid in aTag.childNodes:
		    if (is_tag(aKid)):
			if (self.verbose):
			    print misc.ObjectTypeName.typeClassName(aKid), aKid.nodeName
			node = recurse_into(aKid)
			for k,v in node.iteritems():
			    misc._unpack_(_d_[aTag.nodeName])[k] = misc._unpack_(v)
			    if (callable(self.callback)):
				self.callback(k,misc._unpack_(misc._unpack_(_d_[aTag.nodeName])[k]))
			    if (callable(self.callbackNodeName)):
				_k_ = self.callbackNodeName(k)
				if (k != _k_):
				    _x_ = misc._unpack_(_d_[aTag.nodeName])
				    del _x_[k]
				    _x_[_k_] = misc._unpack_(v)
				    pass
				pass
		    else:
			try:
			    misc._unpack_(_d_[aTag.nodeName])['data'] = aKid.data
			except:
			    pass
	    return _d_
	
	if (xml is not None):
	    self.xml = _utils.ascii_only(xml)
	dom = parseString(self.xml)
	for aChild in dom.childNodes:
	    d[aChild.nodeName] = recurse_into(aChild)
	    try:
		__d = misc._unpack_(d[aChild.nodeName])
		if (__d.has_key(aChild.nodeName)) and (len(list(set(__d.keys()) - set([aChild.nodeName]))) == 0):
		    d = __d
	    except Exception, e:
		print 'ERROR', _utils.formattedException(details=e)
	if (self.verbose):
	    print '='*40
	return d
    
    def process(self, xml=None):
	import simplejson
	d = self._process(xml=xml) if (isinstance(xml,str)) or (isinstance(xml,unicode)) else xml
	if (callable(self.callbackB4)):
	    self.callbackB4(d)
	try:
	    _d_ = d.asJSONSerializable()
	except:
	    _d_ = d
	json = simplejson.dumps(_d_,separators=(',\n', ':\n'))
	return json
    
from vyperlogix.classes.MagicObject import MagicObject2

class XMLConversionProxy(MagicObject2):
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
	    print 'ERROR', info_string
	return objects if (objects is not None) else self
