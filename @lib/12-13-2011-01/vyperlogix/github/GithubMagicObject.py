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
import os, sys
import json
import requests

from github import Github

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.classes.SmartObject import SmartObject
from vyperlogix.classes.MagicObject import MagicObject2

normalize_uri = lambda uri:(uri+'/') if (not uri.endswith('/')) else uri
    
class GitHubMagicProxy(MagicObject2):
    def __init__(self, username, password, uri, client_id=None, client_secret=None):
        self.__username__ = username
        self.__password__ = password
        self.__client_id__ = client_id
        self.__client_secret__ = client_secret
        self.__uri__ = uri
	self.basename = 'github'

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

    def github_user_repos_create(self, name):
        r = requests.get(normalize_uri(self.uri)+'github/%s/%s/user/repos/create/%s' % (self.username,self.password,name))
        if (r.status_code != 200):
            r.raise_for_status()
        d = r.json()
        status = d.get('status',None)
        if (str(status).upper() != 'SUCCESS'):
            raise ValueError('Cannot retrieve the requested value at this time due to the following: %s' % (status))
        return SmartObject(d)
        
if (__name__ == '__main__'):
    __github_client_id__ = 'd89bfe797d057ded5bcd'
    __github_client_secret__ = 'dd0e228521ee0e09d666d5102c7cf5d16954b234'
    g = GitHubMagicProxy('raychorn', 'peekab00', 'http://127.0.0.1:9909', client_id=__github_client_id__, client_secret=__github_client_secret__)
    print 'g.github_userid=%s' % (g.github_userid)
    uri = g.uri
    print 'uri=%s' % (uri)
    username = g.username
    print 'username=%s' % (username)
    password = g.password
    print 'password=%s' % (password)
    client_id = g.client_id
    print 'client_id=%s' % (client_id)
    client_secret = g.client_secret
    print 'client_secret=%s' % (client_secret)
    user = g.github.get.user()
    print 'user=%s' % (user)
    print 'user_id=%s' % (user.user__id)
    print 'user_email=%s' % (user.user__email)
    repos = g.github.get.user.repos().repos
    print 'repos=%s' % (repos)
    repos_available = g.github.get.user.repos.available().available
    print 'repos_available=%s' % (repos_available)
    repos = g.github.user.repos.create('My Repo Name')
    print 'repos=%s' % (repos)
