import os
import sys
import web

import Queue
import threading

import json
import urllib

import requests

__version__ = '1.0.0'

import logging
from logging import handlers

fpath = os.path.dirname(sys.argv[0])
fpath = '.' if (len(fpath) == 0) else fpath
LOG_FILENAME = os.sep.join([fpath,'webproxy.log'])

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

logger = logging.getLogger('webproxy')
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
    print 'BEGIN:'
    for f in sys.path:
        print f
    print 'END!!'

from libs.utils import is_ip_address_valid

urls = (
    '/*.', 'Index',
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
    <title>(c).2014, All Rights Reserved.</title>
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

<p><b>webproxy (%s)</b></p>

</body>
</html>
'''

class Index:

    def GET(self):
        """ Show page """
        s = 'webproxy %s' % (__version__)
        web.header('Content-Type', 'text/html')
        content = __index__
        for t in web.ctx['headers']:
            web.header(t[0], t[-1])
        __path = web.ctx['path']
        try:
            r = requests.get('%s%s%s' % ('http://' if (__remote__.find('://') == -1) else '',__remote__,__path))
            content = r.content
        except:
            pass
        return content

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

if (0):
    try:
        from web.wsgiserver import CherryPyWSGIServer

        CherryPyWSGIServer.ssl_certificate = os.path.abspath("./server.crt")
        CherryPyWSGIServer.ssl_private_key = os.path.abspath("./server.key.insecure")
    except ImportError:
        pass

app = web.application(urls, globals())
app.notfound = notfound

if __name__ == '__main__':
    '''
    python webproxy.py 127.0.0.1:9100
    '''
    from optparse import OptionParser

    if (len(sys.argv) == 1):
        sys.argv.insert(len(sys.argv), '-h')

    parser = OptionParser("usage: %prog [options]")
    parser.add_option("-l", "--listen", action="store", type="string", help="IP Address Port for WebHead.", dest="listen")
    parser.add_option("-r", "--remote", action="store", type="string", help="Address for Remote Node, can be ip:port or www.address.com.", dest="remote")
    parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")

    options, args = parser.parse_args()

    _isVerbose = False
    if (options.verbose):
        _isVerbose = True

    _listen = '127.0.0.1:9100'
    if (options.listen and is_ip_address_valid(options.listen)):
        __listen__ = options.listen.split(':')
        _listen[-1] = int(_listen[-1]) if (str(_listen[-1]).isdigit()) else _listen[-1]
    else:
        print >> sys.stderr, 'WARNING: Please make sure the value appearing after the -l option is a valid ip address and port in the form of 127.0.0.1:8888 however not this specific address unless this is your specific address.'

    __remote__ = None
    if (options.remote):
        __remote__ = options.remote
    else:
        print >> sys.stderr, 'WARNING: Please make sure the value appearing after the -r option is a valid internet address.'

    sys.argv = [sys.argv[0]]

    import re
    __re__ = re.compile(r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):([0-9]{1,5})", re.MULTILINE)
    has_binding = any([__re__.match(arg) for arg in sys.argv])
    if (not has_binding):
        sys.argv.append(_listen)
    print 'BEGIN: args'
    for arg in sys.argv:
        print arg
    print 'END!! args'

    def __init__():
        logger.info('webproxy %s started !!!' % (__version__))
        app.run()

    t = threading.Thread(target=__init__)
    t.daemon = False
    t.start()
