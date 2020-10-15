import os
import sys
import web

import re

import json
import urllib

try:
    from vyperlogix import misc
    from vyperlogix.lists import ConsumeableList
    from vyperlogix.misc import ObjectTypeName
    
    from vyperlogix.classes import SmartObject
except ImportError:
    print 'BEGIN:'
    for f in sys.path:
	print f
    print 'END!'

import utils

import settings

settings.__data__.__proxy__ = SmartObject.SmartObject()

__progName__ = os.path.splitext(os.path.basename(sys.argv[0]))[0]
__version__ = '1.0.1'

import logging
from logging import handlers

from vyperlogix.misc import _utils

LOG_FILENAME = './%s.log' % (__progName__)

class CannotUseGitException(Exception):
    pass

class CannotUseUnzipException(Exception):
    pass

class CommandFailedToInstall(Exception):
    pass

class MyTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):
    def __init__(self, filename, maxBytes=0, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False):
        handlers.TimedRotatingFileHandler.__init__(self, filename=filename, when=when, interval=interval, backupCount=backupCount, encoding=encoding, delay=delay, utc=utc)
        self.maxBytes = maxBytes

    def shouldRollover(self, record):
        response = handlers.TimedRotatingFileHandler.shouldRollover(self, record)
        if (response == 0):
            if self.stream is None:                 # delay was set...
                self.stream = self._open()
            if self.maxBytes > 0:                   # are we rolling over?
                msg = "%s\n" % self.format(record)
                try:
                    self.stream.seek(0, 2)  #due to non-posix-compliant Windows feature
                    if self.stream.tell() + len(msg) >= self.maxBytes:
                        return 1
                except:
                    pass
            return 0
        return response

logger = logging.getLogger(__progName__)
handler = logging.FileHandler(LOG_FILENAME)
#handler = handlers.TimedRotatingFileHandler(LOG_FILENAME, when='d', interval=1, backupCount=30, encoding=None, delay=False, utc=False)
#handler = MyTimedRotatingFileHandler(LOG_FILENAME, maxBytes=1000000, when='d', backupCount=30)
#handler = handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1000000, backupCount=30, encoding=None, delay=False)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler) 
print 'Logging to "%s".' % (handler.baseFilename)

ch = logging.StreamHandler()
ch_format = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(ch_format)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

logging.getLogger().setLevel(logging.DEBUG)

from vyperlogix.webpy.session import Session
from vyperlogix.misc._utils import timeStampForFileName
from vyperlogix.misc._utils import formattedException

urls = (
    '/', 'Index',
    '/test', 'Test',
    '/github/(.+)', 'WebProxyServer',
    '/github', 'WebProxyServer',
    '/setwindowsagentaddr', 'Nothing',
    '/setwindowsagentaddr/', 'Nothing',
)

### Templates
__fpath__ = os.path.dirname(__file__) if (os.path.isfile(__file__)) else os.path.abspath('.')
print '__fpath__=%s' % (__fpath__)
print 'os.getcwd().lower()=%s' % (os.getcwd().lower())
if (os.getcwd().lower() != __fpath__):
    if (os.path.exists(__fpath__)):
	logger.info('Changing to directory "%s".' % (__fpath__))
	os.chdir(__fpath__)
render = web.template.render('templates', base='base')

web.template.Template.globals.update(dict(
    datestr = web.datestr,
    render = render
))

def notfound():
    return web.notfound("Sorry, the page you were looking for was not found.  This message may be seen whenever someone tries to issue a negative number as part of the REST URL Signature and this is just not allowed at this time.")

class Index:

    def GET(self):
        """ Show page """
        return render.index()

class Test:

    def GET(self):
        """ Show test """
	d = {'status':'tested.'}
	web.header('Content-Type', 'application/json')
	content = json.dumps(d)
	return content

class Nothing:
    def POST(self):
	from utils import CustomJSONENcoder
        web.header('Content-Type', 'application/json')
        reasons = []
        url = web.ctx.home + web.ctx.path + web.ctx.query
        content = json.dumps(web.ctx.env,cls=CustomJSONENcoder)
        logger.info('%s --> %s %s' % (url,content,web.data()))
        content = json.dumps({'status':''.join(reasons)})
        return content

def get_all_pushable_files_from(fpath):
    __callback__ = lambda top,dirs,f:True if (str(f).lower().endswith('.zip')) else False
    allfiles = _utils.get_allfiles_from(fpath,callback=__callback__,topdown=True,followlinks=True)
    allfiles = filter(os.path.isfile, allfiles)
    return allfiles

def log_all_from(items):
    for item in items:
        logger.info(item)

class CustomJSONENcoder(json.JSONEncoder):
    def default(self, o):
	from vyperlogix.misc import ObjectTypeName
	is_none = lambda v:ObjectTypeName.typeClassName(v) == 'github.GithubObject._NotSetType'
	__class__ = ObjectTypeName.typeClassName(o)
	obj = {'__class__':__class__}
	if (__class__ == 'datetime.datetime'):
	    obj['isoformat'] = o.isoformat()
	else:
	    try:
		for k,v in o.__dict__.iteritems():
		    try:
			obj[k] = eval('o.%s'%(k[1:]))
		    except:
			pass
	    except AttributeError:
		pass
	return obj

class WebProxyServer:

    __GET_COMMAND__ = 'get'
    __USER_COMMAND__ = 'user'

    def GET(self, args):
        '''
        /github/githubuser/githubpassword/get/user/id

        http://127.0.0.1:9909/github/
        '''
        reasons = []
        exceptions = []
        response = {}
        web.header('Content-Type', 'application/json')
        toks = args.split('/')
	
	__proxy__ = settings.__data__.__proxy__

	def take_if_possible(items,index):
	    item = items[index] if (len(items) > index) else None
	    if (item):
		index += 1
	    return item,index
        try:
	    __i__ = 0
	    __githubuser__,__i__ = take_if_possible(toks,__i__)
	    __githubpassword__,__i__ = take_if_possible(toks,__i__)
	    __cmd__,__i__ = take_if_possible(toks,__i__)
	    logger.info('__githubuser__=%s' % (__githubuser__))
	    logger.info('__githubpassword__=%s' % (__githubpassword__))
	    logger.info('__cmd__=%s' % (__cmd__))
	    __github__ = Github(__githubuser__, __githubpassword__, client_id=__github_client_id__,client_secret=__github_client_secret__)
	    __is__GET_COMMAND__ = __cmd__ == WebProxyServer.__GET_COMMAND__
	    __is__USER_COMMAND__ = __cmd__ == WebProxyServer.__USER_COMMAND__
            if (__is__GET_COMMAND__) or (__is__USER_COMMAND__):
                logger.info('BEGIN %s.' % (__cmd__.upper()))
		__object__,__i__ = take_if_possible(toks,__i__)
		__entity__ = None
		if (__is__GET_COMMAND__):
		    __entity__,__i__ = take_if_possible(toks,__i__)
		__verb__,__i__ = take_if_possible(toks,__i__)
		__data__,__i__ = take_if_possible(toks,__i__)
		assert(__i__ == len(toks))
		if (__object__ in ['user','repos']):
		    u = __github__.get_user()
		    assert(ObjectTypeName.typeName(__github__) == 'github.MainClass.Github')
		if (__entity__):
		    if (__entity__ == 'id'):
			assert(str(u.id).isdigit())
			response['userid'] = u.id
		    elif (__entity__ == 'email'):
			assert(len(u.email) > 0)
			response['email'] = u.email
		    elif (__entity__ == 'repos'):
			try:
			    repos = [r for r in u.get_repos()]
			except:
			    repos = []
			if (__verb__):
			    if (__verb__ == 'available'):
				commits = []
				for r in repos:
				    try:
					c = [commit for commit in r.get_commits()]
				    except:
					c = []
				    commits.append({'commits':c,'repo':r})
				newrepos = [c for c in commits if (len(c['commits']) == 0)]
				response['available'] = newrepos
			response['repos'] = repos
		    elif (__entity__ == 'keys'):
			try:
			    keys = [k for k in u.get_keys()]
			except:
			    keys = []
			response['keys'] = keys
		elif (__object__ == 'repos'):
		    if (__verb__ == 'create'):
			assert(__data__ is not None)
			repo = u.create_repo(__data__)
			response['repo'] = repo
			try:
			    repos = [r for r in u.get_repos()]
			except:
			    repos = []
			response['repos'] = repos
		    else:
			logger.warning('UNDEFINED VERB.')
			reasons.append('UNDEFINED VERB.')
		else:
		    try:
			response['user'] = u
		    except:
			logger.warning('UNDEFINED OBJECT.')
			reasons.append('UNDEFINED OBJECT.')
		reasons.append('SUCCESS')
		logger.info('END %s !!!' % (__cmd__.upper()))
            else:
                logger.warning('UNDEFINED COMMAND.')
                reasons.append('UNDEFINED COMMAND.')
        except Exception, ex:
            __exception__ = _utils.formattedException(details=ex)
            exceptions.append(__exception__)

        i = 0
        for exception in exceptions:
            response['exception_%s' % (i)] = exception
            i += 1
        
        response['status'] = ''.join(reasons)
        content = json.dumps(response,cls=CustomJSONENcoder)
        return content

    def POST(self):
        web.header('Content-Type', 'application/json')
        reasons = []
        data = json.loads(web.data())
        content = json.dumps({'status':reasons})
        return content

app = web.application(urls, globals())
app.notfound = notfound

if __name__ == '__main__':
    '''
    python WebProxyServer 127.0.0.1:9999

    python webProxyServer.py --proxy=127.0.0.1:8888 127.0.0.1:9999
    '''
    import re
    __re2__ = re.compile(r"--(?P<option>\w*)=(?P<value>%s)"%(_utils.__regex_valid_ip_and_port__), re.MULTILINE)
    options = {}
    args = ConsumeableList([arg for arg in sys.argv])
    i = 0
    for arg in sys.argv:
        matches = __re2__.match(arg)
        if (matches):
            opts = matches.groupdict()
            if (opts.has_key('option')) and (opts.has_key('value')):
                options[opts['option']] = opts['value']
            x = args[i]
        i += 1
    #sys.argv = args.__list__
    has_binding = any([_utils.is_valid_ip_and_port(arg) for arg in args])
    if (not has_binding):
        sys.argv.append('127.0.0.1:9999')
    if (options.has_key('proxy')):
	__proxy__ = settings.__data__.__proxy__
	__proxy__.proxy = options['proxy'].split(':')
	try:
	    if (len(__proxy__.proxy) == 2):
		__proxy__.proxy[-1] = int(__proxy__.proxy[-1])
		if (misc.isInteger(__proxy__.proxy[-1])):
		    import socket
		    from vyperlogix.sockets.proxies.socks import socks

		    __proxy__.__default_proxy_before__ = socks._defaultproxy
		    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, __proxy__.proxy[0], int(__proxy__.proxy[-1]))
		    __proxy__.__default_proxy_after__ = socks._defaultproxy
		    __proxy__.__socket_socket_before__ = socket.socket
		    socket.socket = socks.socksocket
		    __proxy__.__socket_socket_after__ = socket.socket
		    print 'proxy=%s' % (':'.join([str(p) for p in __proxy__.proxy]))
		else:
		    print 'ERROR: Invalid proxy=%s, due to malformed port number.' % (__proxy__.proxy)
	    else:
		print 'ERROR: Invalid proxy=%s, due to missing ":" (--proxy=127.0.0.1:8080).' % (__proxy__.proxy)
	except Exception, ex:
	    info_string = _utils.formattedException(details=ex,depth=2,delims='\n\t')
	    print 'ERROR: Invalid proxy=%s, due to the following:\n%s.' % (__proxy__.proxy,info_string)

    def __init__():
        logger.info('%s %s started !!!' % (__progName__,__version__))
        app.run()

    __init__() 

