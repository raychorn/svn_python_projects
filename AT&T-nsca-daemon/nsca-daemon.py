import os
import sys
import web
import utils

'''
Requires: web.py --> http://webpy.org/
'''

import threading

__version__ = '1.0.0'

import logging
from logging import handlers

__PROGNAME__ = os.path.splitext(os.path.basename(sys.argv[0]))[0]
LOG_FILENAME = os.sep.join([os.path.dirname(sys.argv[0]),'%s.log' % (__PROGNAME__)])

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

logger = logging.getLogger(__PROGNAME__)
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

urls = (
    '/', 'Index',
    '/nsca/(.+)', 'NSCA',
    '/nsca', 'NSCA',
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

__index__ = '''
<html>
<head>
    <title>(c). Copyright 2013, AT&T, All Rights Reserved.</title>
    <style>
        #menu {
            width: 200px;
            float: left;
        }
    </style>
</head>
<body>

<ul id="menu">
    <li><a href="/">Home</a></li>
</ul>

<p><b>UNAUTHORIZED ACCESS</b></p>

</body>
</html>
'''

class Index:

    def GET(self):
        """ Show page """
	s = '%s %s' % (__PROGNAME__,__version__)
	return __index__

class Nothing:
    def POST(self):
	web.header('Content-Type', 'text/html')
	return __index__

class NSCA:
    def GET(self):
        web.header('Content-Type', 'text/html')
	return __index__

    def POST(self):
	web.header('Content-Type', 'text/html')
	__command__ = web.data()
	content = 'NOTHING'
	if (utils.isUsingLinux):
	    try:
		infile, outfile, errfile = os.popen3(__command__)
		stdout_lines = outfile.readlines()
		stderr_lines = errfile.readlines()
		content = stdout_lines + stderr_lines
	    except Exception, ex:
		from exceptions import formattedException
		content = formattedException(details=ex)
	return content

app = web.application(urls, globals())
app.notfound = notfound

if __name__ == '__main__':
    '''
    python root-daemon-att.py linux-command
    '''
    import re
    __re__ = re.compile(r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):([0-9]{1,5})", re.MULTILINE)
    has_binding = any([__re__.match(arg) for arg in sys.argv])
    if (not has_binding):
	sys.argv.append('127.0.0.1:9999')
	
    def __init__():
	logger.info('%s %s started !!!' % (__PROGNAME__,__version__))
        app.run()
    
    t = threading.Thread(target=__init__)
    t.daemon = False
    t.start()
        
