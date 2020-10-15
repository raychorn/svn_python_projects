import os
import sys
import web

import threading

import json
import ujson
import urllib

__version__ = '1.0.0'

import logging
from logging import handlers

import tempfile
__dirname__ = os.sep.join([os.path.dirname(tempfile.NamedTemporaryFile().name),'vyperlogix','webservice'])

if (not os.path.exists(__dirname__)):
    os.makedirs(__dirname__)

LOG_FILENAME = os.sep.join([__dirname__,'webservice.log'])

__svc_name__ = "vCRON"

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

logger = logging.getLogger('webservice')
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

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc._utils import timeStampForFileName
from vyperlogix.misc._utils import formattedException

from vyperlogix.misc import ObjectTypeName
from vyperlogix.classes.SmartObject import SmartObject, SmartJsonObject

urls = (
    '/', 'Index',
    '/version', 'Index',
    '/favicon.ico', 'Index',
    '/crossdomain.xml', 'Index',
    '/rest/(.+)', 'Rest',
    '/rest', 'Rest',
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
    <title>(c). Copyright 2013, Vyper Logix Corp., All Rights Reserved.</title>
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

from utils import __handler__
from utils import __logger__

def get_service_config_json_fpath(fpath):
    service_config_json_fpath = lambda dn:os.sep.join([dn,'%s%s%s.json' % (__svc_name__,os.sep,__svc_name__)])
    fp = service_config_json_fpath(fpath)
    fp2 = service_config_json_fpath(os.path.abspath('.'))
    return fp if (os.path.exists(fp)) else fp2 if (os.path.exists(fp2)) else None

class Index:

    def GET(self,*args,**kwargs):
        '''
        /
        /version
        '''
        reasons = []
        d = {}
        logger.info('args is "%s".' % (str(args)))
        logger.info('kwargs is "%s".' % (kwargs))
        if (web.url() == '/version'):
            web.header('Content-Type', 'application/json')
            s = 'webservice %s, (c). Copyright 2013, VyperLogix Corp.' % (__version__)
            reasons.append('SUCCESS')
            d['version'] = s

            fname = get_service_config_json_fpath(__dirname__)
            d['has_config'] = os.path.exists(fname) if (fname) else False
            msg = 'has_config="%s".' % (d['has_config'])
            logger.info(msg)

            content = ujson.dumps({'status':','.join(reasons),'data':d})
            return content
        elif (web.url() == '/crossdomain.xml'):
            web.header('Content-Type', 'application/xml')
            so = SmartObject()
            fname = get_service_config_json_fpath(__dirname__)
            if (fname) and (os.path.exists(fname)):
                try:
                    __json__ = _utils.readFileFrom(fname, mode='r', noCRs=True)
                    if (misc.isStringValid(__json__)):
                        __data__ = ujson.loads(__json__)
                        so = SmartObject(__data__)
                except Exception, ex:
                    pass
        web.header('Content-Type', 'text/html')
        if (_utils.isBeingDebugged) and (not so.crossdomain_xml):
            crossdomain_xml = os.path.abspath('./crossdomain.xml')
            if (os.path.exists(crossdomain_xml)):
                so.crossdomain_xml = crossdomain_xml
        content = ''
        if (so.crossdomain_xml):
            content = _utils.readFileFrom(so.crossdomain_xml,noCRs=True)
            return content
        return __index__


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
        content = ujson.dumps(web.ctx.env,cls=CustomJSONENcoder)
        logger.info('%s --> %s %s' % (url,content,web.data()))
        content = ujson.dumps({'status':''.join(reasons)})
        return content

class Rest:

    def GET(self,*args,**kwargs):
        '''
        /rest/get/config
        /rest/has/config
        
        http://meyerweb.com/eric/tools/dencoder/
        '''
        web.header('Content-Type', 'application/json')
        reasons = []
        d = {}
        logger.info('args is "%s".' % (args))
        logger.info('kwargs is "%s".' % (kwargs))
        if (args[0] == 'get/config'):
            fname = get_service_config_json_fpath(__dirname__)
            if (fname) and (os.path.exists(fname)):
                __json__ = _utils.readFileFrom(fname, mode='r', noCRs=True)
                reasons.append('SUCCESS')
            else:
                __json__ = '{}'
                reasons.append('FAILURE because Config file is missing.')
            msg = '%s bytes of JSON in "%s".' % (len(__json__),fname)
            logger.info(msg)
            d['json'] = __json__
        elif (args[0] == 'has/config'):
            fname = get_service_config_json_fpath(__dirname__)
            d['has_config'] = os.path.exists(fname) if (fname) else False
            msg = 'has_config="%s".' % (d['has_config'])
            logger.info(msg)
            reasons.append('SUCCESS')
        elif (args[0] == 'isalive'):
            logger.info('Is Alive...')
            reasons.append('SUCCESS')
        else:
            msg = 'Invalid args (%s).' % (args)
            logger.warning(msg)
            reasons.append('WARNING: %s' % (msg))
        content = ujson.dumps({'status':','.join(reasons),'data':d})
        return content

    def POST(self,*args,**kwargs):
        '''
        /rest/config
        /rest/save/config
        /rest/set/config
        '''
        web.header('Content-Type', 'application/json')
        d = {}
        reasons = []
        #print >> sys.stderr, '(+++).1 --> %s' % (ObjectTypeName.typeName(web.data()))
        #print >> sys.stderr, '(+++).2 --> %s' % (web.data())
        data = json.loads(web.data())
        #######################################
        logger.info('args is "%s".' % (args))
        logger.info('kwargs is "%s".' % (kwargs))
        if (args[0] == 'save/config'):
            fname = get_service_config_json_fpath(__dirname__)
            if (fname) and (os.path.exists(fname)):
                _utils.writeFileFrom(fname, web.data())
                msg = '%s bytes of JSON in "%s".' % (len(web.data()),fname)
            else:
                msg = 'WARNING: Cannot locate "%s".' % (fname)
            logger.info(msg)
            reasons.append('SUCCESS')
        elif (args[0] == 'set/config'):
            fname = get_service_config_json_fpath(__dirname__)
            if (fname) and (os.path.exists(fname)):
                try:
                    __json__ = _utils.readFileFrom(fname, mode='r', noCRs=True)
                    if (misc.isStringValid(__json__)):
                        __data__ = ujson.loads(__json__)
                        for k,v in data.iteritems():
                            if (__data__.has_key(k)):
                                logger.info('(%s) %s="%s".' % (__data__[k],k,v))
                                __data__[k] = v
                                logger.info('(%s)".' % (__data__[k]))
                        __json__ = ujson.dumps(__data__)
                        _utils.writeFileFrom(fname, __json__)
                        reasons.append('SUCCESS')
                    else:
                        reasons.append('FAILURE because JSON is missing from Config file.')
                except Exception, ex:
                    reasons.append('FAILURE due to %s' % (ex.message))
            else:
                __json__ = '{}'
                reasons.append('FAILURE because Config file is missing.')
            d['json'] = __json__
            msg = '%s bytes of JSON in "%s".' % (len(web.data()),fname)
            logger.info(msg)
        else:
            msg = 'Invalid args (%s).' % (args)
            logger.warning(msg)
            reasons.append('WARNING: %s' % (msg))
        #######################################
        content = json.dumps({'status':','.join(reasons),'data':d})
        return content

#from web.wsgiserver import CherryPyWSGIServer

#CherryPyWSGIServer.ssl_certificate = os.path.abspath("./server.crt")
#CherryPyWSGIServer.ssl_private_key = os.path.abspath("./server.key.insecure")

class MyApplication(web.application): 
    def run(self, ip='127.0.0.1', port=9000, *middleware): 
        func = self.wsgifunc(*middleware) 
        return web.httpserver.runsimple(func, (ip, port)) 

__default_webservice__ = '127.0.0.1:9100'

def __start_webservice__(ip_port=__default_webservice__):
    '''
    python webservice.py 127.0.0.1:9999
    '''
    def __init__(ipport):
        ipport = __default_webservice__ if (ipport is None) or (len(ipport) == 0) else ipport
        logger.info('webservice %s on %s started !!!' % (__version__,ipport))
        toks = ipport.split(':')
        __ip__ = __default_ip__ = __default_webservice__.split(':')[0] if (__default_webservice__.find(':') > -1) else __default_webservice__
        if (len(toks) > 0):
            __ip__ = toks[0]
        __port__ = __default_port__ = 9000
        if (len(toks) > 1):
            __port__ = int(toks[-1]) if (toks[-1].isdigit()) else __default_port__
        app = MyApplication(urls, globals()) 
        #app = web.application(urls, globals())
        app.notfound = notfound
        logger.debug('__ip__=%s, __port__=%s' % (__ip__,__port__))
        app.run(ip=__ip__,port=__port__)         

    t = threading.Thread(target=__init__, args=[ip_port] )
    t.daemon = False
    t.start()

if (__name__ == '__main__'):
    from optparse import OptionParser
    
    parser = OptionParser("usage: %prog [options]")
    parser.add_option('-w', '--webservice', dest='webservice', action="store_true", help="start web service")
    parser.add_option('-i', '--ip', dest='ip', action="store", help="ip address", metavar="STRING", type="str")
    parser.add_option('-p', '--port', dest='port', action="store", help="port number", metavar="NUMBER", type="int")
    parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
    
    options, args = parser.parse_args()
    
    _isVerbose = False
    if (options.verbose):
        _isVerbose = True

    if (options.webservice):
        from utils import __loggerHandler__
        __loggerHandler__()
        if (options.ip is None) or (options.port is None):
            __start_webservice__()
        else:
            __start_webservice__(ip_port='%s:%s' % (options.ip,options.port))
    else:
        import requests
        from vyperlogix import misc
        from vyperlogix.misc import _utils

        url = 'http://%s/' % (__default_webservice__)

        __url__ = "%srest/has/config" % (url)
        r = requests.get(__url__, headers={'Content-Type':'application/json','Accept':'application/json'}, verify=False)
        if (r.status_code == 200):
            d = SmartJsonObject(ujson.loads(r.content))
            has_config = d.data_has_config
            print 'GET: "%s"' % (__url__)
            print 'GET: has_config="%s"' % (has_config)
            print 'BEGIN:'
            for k,v in d.iteritems():
                print '\t%s=%s' % (k,v)
            print 'END!!!'

        json = _utils.readFileFrom('./service_config.json','r')
        r = requests.post("%srest/save/config" % (url), data=json, headers={'Content-Type':'application/json','Accept':'application/json'}, verify=False)
        if (r.status_code == 200):
            d = ujson.loads(r.content)
            print 'POST:'
            print 'BEGIN:'
            for k,v in d.iteritems():
                print '\t%s=%s' % (k,v)
            print 'END!!!'

        __url__ = "%srest/has/config" % (url)
        r = requests.get(__url__, headers={'Content-Type':'application/json','Accept':'application/json'}, verify=False)
        if (r.status_code == 200):
            d = ujson.loads(r.content)
            print 'GET: "%s"' % (__url__)
            print 'BEGIN:'
            for k,v in d.iteritems():
                print '\t%s=%s' % (k,v)
            print 'END!!!'

        __url__ = "%srest/get/config" % (url)
        r = requests.get(__url__, headers={'Content-Type':'application/json','Accept':'application/json'}, verify=False)
        if (r.status_code == 200):
            d = ujson.loads(r.content)
            print 'GET: "%s"' % (__url__)
            print 'BEGIN:'
            for k,v in d.iteritems():
                print '\t%s=%s' % (k,v)
            print 'END!!!'
    