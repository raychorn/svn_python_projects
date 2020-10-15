__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., All Rights Reserved.

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
import os, sys
import ujson
import requests

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.classes.SmartObject import SmartObject
from vyperlogix.classes.MagicObject import MagicObject2

GET_VERBS = ['has','is','get']

normalize_uri = lambda uri:(uri+'/') if (not uri.endswith('/')) else uri
    
class vCronMagicProxy(MagicObject2):
    def __init__(self, url):
        self.__url__ = normalize_uri(url)+ ('rest/' if (url.find('/rest') == -1) else '')
	self.basename = 'vcron'

    def __call__(self,*args,**kwargs):
	from vyperlogix.lists import ConsumeableList
	n = ConsumeableList(self.n)
	items = []
	for item in n:
	    if (item.startswith('__') and item.endswith('__')):
		break
	    items.append(item)
	s = 'self.__handler__(%s, *args,**kwargs)' % ('[%s]'%(','.join(['"%s"'%(i) for i in items])))
	try:
	    results = eval(s,globals(),locals())
	except Exception, details:
	    results = None
	    print >> sys.stderr, _utils.formattedException(details=details)
	return results

    def __getattr__(self,name):
	normalize = lambda n:'__%s__'%(n)
        if name in ('__str__','__repr__'): return lambda:'instance of %s at %s' % (str(self.__class__),id(self))
	__name__ = normalize(name)
	if (self.__dict__.has_key(__name__)):
	    self.__reset_magic__()
	    return self.__dict__[__name__]
        if not self.__dict__.has_key('n'):self.n=[]
	if (name == self.basename):
	    self.__reset_magic__()
	    self.n.append(name)
	    return self
        self.n.append(name)
        return self
        
    def __handler__(self,items,*args,**kwargs):
	uri = []
	parms = []
	useGET = any([(item in GET_VERBS) or (any([(item.find(v) > -1) for v in GET_VERBS])) for item in items])
	for item in items:
	    uri.append(item)
	if (uri[0] == self.basename):
	    for item in items[1:]:
		uri.append(item)
	    for arg in args:
		uri.append(arg)
	    for k,v in kwargs.iteritems():
		parms.append('%s=%s'%(k,v))
	    if (len(parms) > 0):
		uri.append('?%s'%('&'.join(parms)))
	__uri__ = '/'.join(uri)
	print '\t --> %s' % (__uri__)
	__headers__ = {'Content-Type':'application/json','Accept':'application/json'}
	__uri__ = normalize_uri(self.url)+__uri__
	if (useGET) or (len(args) == 0):
	    r = requests.get(__uri__,headers=__headers__, verify=False)
	else:
	    r = requests.post(__uri__, data=args[0], headers=__headers__, verify=False)
	if (r.status_code != 200):
	    r.raise_for_status()
	d = r.json()
	status = d.get('status',None)
	if (str(status).upper() != 'SUCCESS'):
	    raise ValueError('Cannot retrieve the requested value at this time due to the following: %s' % (status))
	return SmartObject(d)

if (__name__ == '__main__'):
    g = vCronMagicProxy('http://127.0.0.1:9100')
    url = g.url
    print 'url=%s' % (url)

    so = g.isalive()
    print so.asPythonDict()

    so = g.has.config()
    print so.asPythonDict()

    if (not so.data_has_config):
	__json__ = _utils.readFileFrom('./service_config.json','r')
	so = g.save.config(__json__)
	print so.asPythonDict()
    so = g.get.config()
    d = SmartObject(ujson.loads(so.data_json))
    print d.asPythonDict()
