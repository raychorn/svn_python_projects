import os
import sys
import web

import Queue
import threading

import json
import urllib

__version__ = '1.0.2'

import logging
from logging import handlers

LOG_FILENAME = './loggerwebservice.log'

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

logger = logging.getLogger('loggerwebservice')
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

verbose = False
import imp
if (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__")):
    import zipfile
    import pkg_resources

    import re
    __regex_libname__ = re.compile(r"(?P<libname>.*)_2_7\.zip", re.MULTILINE)

    my_file = pkg_resources.resource_stream('__main__',sys.executable)

    import tempfile
    __dirname__ = os.path.dirname(tempfile.NamedTemporaryFile().name)

    zip = zipfile.ZipFile(my_file)
    files = [z for z in zip.filelist if (__regex_libname__.match(z.filename))]
    for f in files:
        libname = f.filename
        data = zip.read(libname)
        fpath = os.sep.join([__dirname__,os.path.splitext(libname)[0]])
        __is__ = False
        if (not os.path.exists(fpath)):
            os.mkdir(fpath)
        else:
            fsize = os.path.getsize(fpath)
            if (fsize != f.file_size):
                __is__ = True
        fname = os.sep.join([fpath,libname])
        if (verbose):
            print 'INFO: fname is "%s".' % (fname)
            print 'INFO: __is__ is "%s".' % (__is__)
        if (not os.path.exists(fname)) or (__is__):
            file = open(fname, 'wb')
            file.write(data)
            file.flush()
            file.close()
            if (verbose):
                print 'INFO: fname(2) is "%s".' % (fname)
        __module__ = fname

        import zipextimporter
        zipextimporter.install()
        sys.path.insert(0, __module__)

from vyperlogix.webpy.session import Session
from vyperlogix.misc._utils import timeStampForFileName
from vyperlogix.misc._utils import formattedException

from vyperlogix.misc import _utils

urls = (
    '/', 'Index',
    '/logger/(.+)', 'Logger',
    '/logger', 'Logger',
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

class Nothing:
    def POST(self):
	web.header('Content-Type', 'application/json')
	reasons = []
	url = web.ctx.home + web.ctx.path + web.ctx.query
	content = json.dumps(web.ctx.env,cls=CustomJSONENcoder)
	logger.info('%s --> %s %s' % (url,content,web.data()))
	content = json.dumps({'status':''.join(reasons)})
	return content

class Logger:

    def GET(self, args):
        '''
        /logger/galaxywars/begin-session/pathname-url-encoded
        /logger/galaxywars/message-url-encoded
        
        /logger/galaxywars/begin-session/C%3A%5CTemp%5Csample
        
        http://127.0.0.1:8080/logger/galaxywars/begin-session/C%3A%5CTemp%5Csample
        http://127.0.0.1:8080/logger/galaxywars/Now%20is%20the%20time%20for%20all%20good%20men...2
        
        http://meyerweb.com/eric/tools/dencoder/
        '''
        web.header('Content-Type', 'application/json')
        toks = args.split('/')
        app_name = toks[0]
        reasons = []
        content = json.dumps({'status':''.join(reasons)})
        return content

    def POST(self):
	web.header('Content-Type', 'application/json')
	reasons = []
	data = json.loads(web.data())
	product = data[__product_property__] if (data.has_key(__product_property__)) else None
	message = data[__message_property__] if (data.has_key(__message_property__)) else None
	level = data[__level_property__] if (data.has_key(__level_property__)) else None
	if (product) and (message):
	    change_logging_product(product)
	    content = '%s :: %s' % (product,message)
	    if (level) and (level in ['error','fatal','warn','warning','debug']):
		r = 'Changing logger level to "%s".' % (level)
		logger.info(r)
		reasons.append('INFO: %s' % (r))
		if (level == 'fatal'):
		    logger.fatal(content)
		elif (level == 'error'):
		    logger.error(content)
		elif (level in ['warn','warning']):
		    logger.warning(content)
		elif (level == 'debug'):
		    logger.debug(content)
		flush_handlers()
		reasons.append('INFO: Logged %s message.' % (level))
	    else:
		logger.info(content)
		flush_handlers()
		reasons.append('INFO: Logged info message.')
	else:
	    reasons.append('WARNING: Missing product or message from payload.')
	    logger.info('%s :: %s' % (product,message))
	    flush_handlers()
	content = json.dumps({'status':reasons})
	return content

app = web.application(urls, globals())
app.notfound = notfound

if __name__ == '__main__':
    '''
    python loggerwebservice.py 127.0.0.1:9999
    '''
    has_binding = any([_utils.is_valid_ip_and_port(arg) for arg in sys.argv])
    if (not has_binding):
	sys.argv.append('127.0.0.1:9999')
    print 'BEGIN: args'
    for arg in sys.argv:
	print arg
    print 'END!! args'
	
    def __init__():
	logger.info('loggerwebservice %s started !!!' % (__version__))
	flush_handlers()
        app.run()
    
    t = threading.Thread(target=__init__)
    t.daemon = False
    t.start()
    
	