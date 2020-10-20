__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

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
import os, sys
import json
import requests

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.classes.SmartObject import SmartObject
from vyperlogix.classes.MagicObject import MagicObject2

normalize_uri = lambda uri:(uri+'/') if (not uri.endswith('/')) else uri
    
class WebAccelerator(MagicObject2):
    def __init__(self, username, password, uri, client_id=None):
        self.__username__ = username
        self.__password__ = password
        self.__client_id__ = client_id
        self.__uri__ = uri
	self.basename = 'webproxy'
	self.__ip_port__ = self.__uri__.split('://')[-1].split('/')[0]
	self.__cmd__ = "python %s %s" % ('"C:\@python-projects\django-projects\web-proxy-dev\web.py\webProxyServer.py"','"%s"' % (self.__ip_port__))

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
	uri.append(items[0])
	if (uri[0] == self.basename):
	    uri.append(self.username)
	    uri.append(self.password)
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
	r = requests.get(normalize_uri(self.uri)+__uri__)
	if (r.status_code != 200):
	    r.raise_for_status()
	d = r.json()
	status = d.get('status',None)
	if (str(status).upper() != 'SUCCESS'):
	    raise ValueError('Cannot retrieve the requested value at this time due to the following: %s' % (status))
	return SmartObject(d)

    def create(self, name=None):
	'''create the instance'''
	# for local this is a simple process with a pid
	# for local the entry-point being run as a process is the web-accelrator
	# for local the web accelerator is a simple http server, then a simple TCP/IP proxy.
	import os, sys
	import subprocess
	
	cwd = os.path.abspath(os.path.curdir)
	fname = os.sep.join([cwd,'run-proxy.cmd'])
	
	python_path = ';'.join(sys.path)
	fOut = open(fname, 'w')
	try:
	    print >> fOut, 'SET PYTHONPATH=%s' % (python_path)
	    print >> fOut, ''
	    print >> fOut, self.__cmd__
	except:
	    pass
	fOut.flush()
	fOut.close()
	
	# self.__process__ = subprocess.Popen(fname, shell=True, stdout = subprocess.PIPE)
	
	
	import os, time, sys, subprocess
	
	print 'main begin'
	self.__process__ = subprocess.Popen([fname, '0'], close_fds=True)
	print 'main end'	

	#stdout, stderr = self.__process__.communicate()
	print self.__process__.returncode # is 0 if success	
	
	#self.__process__ = subprocess.Popen(["dir", "."])	
	
	# for AWS this creates a VM and begins the orchestration process.
        return self

    def destroy(self, name=None):
	'''destroy the instance'''
	# for local this take the pid and destroys the process
	from vyperlogix.process import killProcByPID
	
	killProcByPID(self.__process__.pid)
	
	# for AWS this performs a shutdown for the previously created VM.
        return self

if (__name__ == '__main__'):
    __client_id__ = 'd89bfe797d057ded5bcd' # oAuth Token, sctually... later on.
    p = WebAccelerator('raychorn', 'peekab00', 'http://127.0.0.1:9909', client_id=__client_id__)
    uri = p.uri
    print 'uri=%s' % (uri)
    username = p.username
    print 'username=%s' % (username)
    password = p.password
    print 'password=%s' % (password)
    client_id = p.client_id
    print 'client_id=%s' % (client_id)
    
    p.create()
    
    print 'pid=%s' % (p.__process__.pid)
    
