import os
import sys
import web

import Queue
import threading

import json
import requests

from vyperlogix.classes.SmartObject import SmartObject

__version__ = '1.0.1'

import logging
from logging import handlers

__SERVICE_NAME__ = 'dirwatcherservice'

LOG_FILENAME = './%s.log' % (__SERVICE_NAME__)

__cdn__ = {}

__cdn__ = SmartObject(__cdn__)

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

logger = logging.getLogger(__SERVICE_NAME__)
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
ch.setLevel(logging.INFO)
logger.addHandler(ch)

logging.getLogger().setLevel(logging.INFO)

def main_is_frozen():
    import imp
    return (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__"))

if main_is_frozen():
    import zipfile
    import pkg_resources
    
    my_file = pkg_resources.resource_stream('__main__',sys.executable)
    print '%s' % (my_file)
    
    import tempfile
    __vyperlogix__ = tempfile.NamedTemporaryFile().name
    
    zip = zipfile.ZipFile(my_file)
    data = zip.read("vyperlogix_2_7.zip")
    file = open(__vyperlogix__, 'wb')
    file.write(data)
    file.flush()
    file.close()
    __vyperlogix__ = file.name
    print '__vyperlogix__ --> "%s".' % (__vyperlogix__)
    
    import atexit
    @atexit.register
    def __cleanup__():
	print '__cleanup__ --> "%s".' % (__vyperlogix__)
	os.remove(__vyperlogix__)
	
    import signal
    signal.signal(signal.SIGTERM, __cleanup__)

    import zipextimporter
    zipextimporter.install()
    sys.path.insert(0, __vyperlogix__)
    
    print 'BEGIN:'
    for f in sys.path:
	print f
    print 'END !!'

__imports__ = [f for f in sys.path if (f.replace(os.sep,'/').split('/')[-1].lower().find('django') > -1)]

from vyperlogix.webpy.session import Session
from vyperlogix.misc._utils import timeStampForFileName
from vyperlogix.misc._utils import formattedException

from vyperlogix.misc import _utils

from vyperlogix.lists.ListWrapper import ListWrapper

from vyperlogix.django import django_utils

paths = ListWrapper(sys.path)

for m in __imports__:
    i = paths.findFirstMatching(m)
    if (i > -1):
	del sys.path[i]
	
django_utils.assert_version(1.4)

urls = (
    '/', 'Index',
    '/watcher/(.+)', 'Watcher',
    '/watcher', 'Watcher',
    '/setwindowsagentaddr', 'Nothing',
    '/setwindowsagentaddr/', 'Nothing',
)

### Templates
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

__command_property__ = 'command'
__beginSession_command__ = 'begin-session'
__log_command__ = 'log-message'

__folder_property__ = 'folder'
__product_property__ = 'product'
__message_property__ = 'message'
__level_property__ = 'level'
__commands__ = {
    __beginSession_command__:__beginSession_command__,
    __folder_property__:__folder_property__,
    __product_property__:__product_property__,
    __command_property__:__command_property__,
    __message_property__:__message_property__,
    __level_property__:__level_property__,
    __log_command__:__log_command__
}
__valid_commands__ = list(set(__commands__.keys()))
__loggerFileName__ = None

def flush_handlers():
    try:
	for handler in list(logger.handlers):
	    handler.flush()
    except:
	pass
    
def change_logging_product(product):
    from vyperlogix.misc import ObjectTypeName
    try:
	for handler in list(logger.handlers):
	    if (ObjectTypeName.typeClassName(handler) == 'logging.handlers.TimedRotatingFileHandler'):
		handler.flush()
		b = os.path.basename(handler.baseFilename)
		toks = os.path.splitext(b)
		parts = toks[0].split('-')
		__is__ = False
		if (len(parts) == 1):
		    parts.append(product)
		    __is__ = True
		elif (parts[-1] != product):
		    parts[-1] = product
		    __is__ = True
		if (__is__):
		    toks[0] = parts.join('-')
		    b = toks.join('')
		    handler.baseFilename = handler.baseFilename.replace(os.path.basename(handler.baseFilename),b)
		    logger.info('Changed logging to product "%s".' % (product))
    except:
	pass

class CustomJSONENcoder(json.JSONEncoder):
    def default(self, o):
	from vyperlogix.misc import ObjectTypeName
	obj = {'__class__':ObjectTypeName.typeClassName(o)}
	try:
	    for k,v in o.__dict__.iteritems():
		obj[k] = v
	except AttributeError:
	    if (ObjectTypeName.typeClassName(o) == 'file'):
		obj['name'] = o.name
		obj['mode'] = o.mode
	    else:
		pass
	    pass
	return obj

from standalone.conf import settings

class Nothing:
    def POST(self):
	web.header('Content-Type', 'application/json')
	reasons = []
	url = web.ctx.home + web.ctx.path + web.ctx.query
	content = json.dumps(web.ctx.env,cls=CustomJSONENcoder)
	logger.info('%s --> %s %s' % (url,content,web.data()))
	content = json.dumps({'status':''.join(reasons)})
	return content

class Watcher:

    def GET(self, args):
        '''
        '''
        web.header('Content-Type', 'application/json')
        toks = args.split('/')
        app_name = toks[0]
        reasons = ['OK %s %s'%(__SERVICE_NAME__,__version__)]
        content = json.dumps({'status':''.join(reasons)})
        return content

    def POST(self):
	web.header('Content-Type', 'application/json')
	content = json.dumps({'status':reasons})
	return content

app = web.application(urls, globals())
app.notfound = notfound

if (__name__ == '__main__'):
    '''
    python dirwatcherservice.py 127.0.0.1:9999
    '''
    from optparse import OptionParser
    
    parser = OptionParser("usage: %prog [options] 127.0.0.1:9999")
    parser.add_option('-s', '--syncdb', dest='syncdb', action="store_true", help="should the database be created?")
    parser.add_option('-r', '--repl', dest='repl', action="store_true", help="start a REPL with access to your models")
    parser.add_option('-d', '--dumpdata', dest='dumpdata', action="store_true", help="django dumpdata")
    parser.add_option('-i', '--inspectdb', dest='inspectdb', action="store_true", help="django inspectdb")
    parser.add_option('--dm', '--mysql', dest='mysql', action="store_true", help="mysql db")
    parser.add_option('--ds', '--sqlite3', dest='sqlite3', action="store_true", help="sqlite3 db")
    
    options, args = parser.parse_args()

    DOMAIN_NAME = django_utils.socket.gethostname()
    print '1.DOMAIN_NAME=%s' % (DOMAIN_NAME)
	
    if (not options.mysql) and (not options.sqlite3):
	options.sqlite3 = True
	#raise AssertionError('Either mysql or sqlite3 is required.')

    __database_name__ = 'dirwatcherservicedb'
    
    if options.mysql:
	print 'INFO: Using mysql... Database "%s".' % (__database_name__)
	if (DOMAIN_NAME in ['HPDV7-6163us']):
	    DATABASES = {
		'default': {
		    'ENGINE': 'django.db.backends.mysql',
		    'NAME': __database_name__,
		    'USER' : 'root',
		    'PASSWORD' : 'peekab00',
		    'HOST' : '127.0.0.1',
		    'PORT' : '33306',
		}
	    }
	elif (DOMAIN_NAME in ['HORNRA3']):
	    DATABASES = {
		'default': {
		    'ENGINE': 'django.db.backends.mysql',
		    'NAME': __database_name__,
		    'USER' : 'root',
		    'PASSWORD' : 'peekab00',
		    'HOST' : '127.0.0.1',
		    'PORT' : '33307',
		}
	    }
    elif options.sqlite3:
	__database_name__ = '%s/%s.sqlite' % (os.path.dirname(sys.argv[0]).replace(os.sep,'/'),__database_name__)
	
	options.syncdb = not os.path.exists(__database_name__)

	print 'INFO: Using sqlite3... Database "%s".' % (__database_name__)
	DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': __database_name__,
            }
        }

    settings = settings(
        DATABASES = DATABASES
    )
    
    import models

    from django.core.management import call_command
    if options.syncdb:
	# run a simple command - here syncdb - from the management suite
	call_command('syncdb')
    elif options.repl:
	# start the shell, access to your models through import standalone.models
	call_command('shell')
	sys.exit(1)
    elif options.dumpdata:
	call_command('dumpdata')
	sys.exit(1)
    elif options.inspectdb:
	call_command('inspectdb')
	sys.exit(1)

    from models import GoogleAuthenticator
    auths = GoogleAuthenticator.objects.all()
    if (auths.count() == 0):
	from utils import get_google_auth_seed
	d = get_google_auth_seed()
	auth = GoogleAuthenticator(otpseed=d['seed'],sitename=d['name'],href=d['href'])
	auth.save()
	auths = GoogleAuthenticator.objects.all()

    is_installing_memcached = False
    try:
	from vyperlogix.memcache import MemcacheConnectionSniffer
	success = MemcacheConnectionSniffer('127.0.0.1', 11211, 10).exists()
	if (not success):
	    is_installing_memcached = True
	    print >>sys.stderr, 'Cannot locate memcache.'
    except:
	is_installing_memcached = True
	print >>sys.stderr, 'Cannot locate memcache due to a system failure of some kind.'
	
    if (is_installing_memcached):
	'''
	Build a GUI via Adobe AIR to facilitate this level of functionality.
	'''
	__os__ = _utils.os_platform()
	__is_os_64_bit__ = __os__.endswith(64)
	__is_64_bit__ = _utils.is_os_64bit()
	if (__is_os_64_bit__ != __is_64_bit__):
	    raise AssertionError('Something is wrong with your 64 bit detection logic.')
	if (__is_os_64_bit__):
	    __remote__ = '/downloads.vyperlogix.com/web/content/memcached/installers/windows/memcached-win64'
	else:
	    __remote__ = '/downloads.vyperlogix.com/web/content/memcached/installers/windows/memcached-win32'
	print >>sys.stderr, 'Please install memcached.'

    has_binding = any([_utils.is_valid_ip_and_port(arg) for arg in args])
    if (not has_binding):
	sys.argv.append('127.0.0.1:9999')
	
    def __init__():
	logger.info('%s %s started !!!' % (__SERVICE_NAME__,__version__))
	flush_handlers()
        app.run()
    
    t = threading.Thread(target=__init__)
    t.daemon = False
    t.start()
    
	