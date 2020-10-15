import os, sys
import requests

from vyperlogix import misc
from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.html.parsers.HTMLParsers import TargetedHTMLParser

from optparse import OptionParser

from vyperlogix.django import django_utils

from vyperlogix.misc import _utils

parser = OptionParser("usage: %prog [options]")
parser.add_option('-p', '--proxy', dest='proxy', help="-p 127.0.0.1:8888")
parser.add_option('-l', '--login', action='store_true', help="login directly", )

options, args = parser.parse_args()

DOMAIN_NAME = django_utils.socket.gethostname()
print '1.DOMAIN_NAME=%s' % (DOMAIN_NAME)
if (DOMAIN_NAME in ['HORNRA3']):
    if not options.proxy:
	parser.error("You must specify a proxy for the network you wish to run within.")
	print 'Cannot continue...'
	sys.exit(1)

if options.proxy:
    import socket
    from vyperlogix.sockets.proxies.socks import socks
    
    has_binding = _utils.is_valid_ip_and_port(options.proxy)
    if (has_binding):
	__proxy__ = options.proxy.split(':')
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, __proxy__[0], int(__proxy__[-1]))
        socket.socket = socks.socksocket
        print 'proxy=%s' % (':'.join([str(p) for p in __proxy__]))
    else:
        print 'WARNING: Doesn\'t seem there is a valid proxy specified as "%s".' % (options.proxy)
        print 'Cannot continue...'
        sys.exit(1)

def isInterestInThisFormTag(self,tag,attrs=[],state=None):
    a = SmartObject(dict(misc.copy(attrs)))
    if (str(tag).lower() == 'form'):
	if (state.upper() == 'START'):
	    if (str(a.id).lower().find('cpanel') > -1) and (str(a.method).lower() == 'post'):
		self.bucket.append((tag,state,a))
		self.__is__ = True
		return True
	elif (state.upper() == 'END'):
	    if (self.__is__):
		self.bucket.append((tag,state,a))
	    self.__is__ = False
	    return True
    elif (self.__is__):
	self.bucket.append((tag,state,a))
    return False

def isInterestInThisTDTag(self,tag,attrs=[],state=None):
    a = SmartObject(dict(misc.copy(attrs)))
    if (str(tag).lower() == 'td'):
	if (state.upper() == 'START'):
	    self.bucket.append((tag,state,a))
	    return True
    return False

if (__name__ == '__main__'):
    if (options.login):
	__url__ = 'http://johnny.heliohost.org:2082/login/?login_only=1'

	__data__ = {}
	__data__['user'] = 'raychorn'
	__data__['pass'] = 'peekab00'
	
	__headers__ = {}
	__headers__['Host'] = 'johnny.heliohost.org:2082'
	__headers__['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'
	__headers__['Accept'] = 'text/html,application/xhtml+xml,application/xml'
	__headers__['Accept-Language'] = 'en-US,en;q=0.5'
	__headers__['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
	__headers__['Referer'] = 'http://johnny.heliohost.org:2082/logout/'
	__headers__['Pragma'] = 'no-cache'
	__headers__['Cache-Control'] = 'no-cache'
	
	r = requests.post(__url__, data=__data__,headers=__headers__)
	if (r.status_code == 200):
	    d = SmartObject(r.json())
	    cookies = SmartObject(r.cookies.get_dict())
	    if (d.status):
		if (d.redirect):
		    __cpsession__ = cookies.cpsession
		    __cprelogin__ = cookies.cprelogin
		    del __headers__['Content-Type']
		    __headers__['Cookie'] = 'cprelogin=%s; cpsession=%s' % (__cprelogin__,__cpsession__)
		    r = requests.get('/'.join(__url__.split('?')[0].split('/')[0:3])+d.redirect, headers=__headers__)
		    if (r.status_code == 200):
			pass
		else:
		    print 'WARNING: Cannot redirect because %s.' % (d.asDict())
	    else:
		print 'WARNING: Got %s !!' % (d.asDict())
	    __data__ = r.content
	    pass
	else:
	    print 'WARNING: Failed to login with status of %s.' % (r.status_code)
    else:
	__url__ = 'http://heliohost.org/'
	r = requests.get(__url__)
	if (r.status_code == 200):
	    __data__ = r.content
	    myParser = TargetedHTMLParser()
	    myParser.targetTag('form')
	    myParser.callback = isInterestInThisFormTag
	    myParser.feed(__data__)
	    items = myParser.bucket
	    if (len(items) > 0):
		inputs = []
		for item in items:
		    if (item[0].lower() == 'input') and (item[1].upper() == 'START') and ( (not item[-1].type) or (item[-1].type.lower() not in ['hidden','submit']) ):
			inputs.append(item)
		    print '%s%s --> %s' % (item[0],(' (%s)'%item[1]) if (item[1] != item[-1]) else '',item[-1].asDict())
		if (len(inputs) == 2):
		    __url__ = items[0][-1].action
		    __data__ = {}
		    for inp in inputs:
			if (inp[-1].id) and (inp[-1].id.lower() == 'username'):
			    __data__[inp[-1].name] = 'raychorn'
			else:
			    __data__[inp[-1].name] = 'peekab00'
		    r = requests.post(__url__, data=__data__)
		    if (r.status_code == 200):
			__data__ = r.content
			myParser = TargetedHTMLParser()
			myParser.targetTag('td')
			myParser.callback = isInterestInThisTDTag
			myParser.feed(__data__)
			items = myParser.bucket
			pass
		    else:
			print 'WARNING: Cannot process login.'
		else:
		    print 'WARNING: Cannot process login form with less than 2 inputs (typically username and password)...'
		pass
	    else:
		print 'WARNING: Nothing to do !!!'
	    pass
	else:
	    print 'ERROR: Cannot fetch from "%s".' % (__url__)


