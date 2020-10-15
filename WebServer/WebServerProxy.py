#!/usr/bin/env python
"""
Webserver.py
Andrew Francis
February 25th, 2007

Example of Twisted and Stackless integration that
blocks.

The server listens on http://localhost:8888

The programme and is fine for many purposes. However there is a
flaw. Whenever the server tasklet blocks, it blocks the entire
programme. Ideally other tasklets, such as the Tick tasklet should
run while the server tasklet waits for connections.

<song>The Bleeding Heart Show - The New Pornographers</song>
"""

import stackless
from twisted.web import http

import re
import os, sys
import urllib
import json

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix.hash.lists import HashedUniqueLists
from vyperlogix.lists.ListWrapper import SeqentialList

__product__ = '%s' % (os.path.splitext(__file__.split(os.sep)[-1])[0])

class CGIEndPoint(object):
    def __init__(self,regex):
        self.regex = regex
    def __call__(self,fn):
        regex = self.regex
        def wrappedFn(*args):
            try:
                if (regex.match(args[0])):
                    return fn(*args)
            except Exception,e:
                print
                print e

        return wrappedFn

unpack_url = lambda url:[t for t in url.split('/') if (len(t) > 0)]

@CGIEndPoint(re.compile(r'^/version/'))
def handle_version_request(path):
    response = {}
    response['response'] = '%s 1.0.0' % (__product__)
    return response

def fetch_from_url(url,headers={},parms={}):
    import requests
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    __headers__ = {'User-Agent':user_agent}
    try:
        if (len(headers.keys()) > 0):
            for k,v in headers.iteritems():
                if (__headers__.has_key(k)):
                    del __headers__[k]
                __headers__[k] = v
    except:
        pass
    __data__ = {}
    try:
        if (len(parms.keys()) > 0):
            for k,v in parms.iteritems():
                __data__[k] = v
    except:
        pass
    try:
        r = requests.get(url,headers=__headers__,params=__data__)
    except:
        return None
    return r.text

class Server(object):

    def execute(self, port, requestChannel):
        MyRequestHandler.requestChannel = requestChannel
        reactor.listenTCP(int(port.split(':')[-1]), MyHttpFactory(), interface=port.split(':')[0])
        reactor.run()


class Cgi(object):
    def __init__(self, name, channel):
        self.name = name
        self.channel = channel
        self.count = 0
        return

    def execute(self):
        while (1):
            response = {}
            request = self.channel.receive()
            print 'Cgi.execute path=%s' % (request.path)
            toks = request.path.split('/')
            if (request.path.find('://') == -1):
                path = request.path +'/' if (not request.path.endswith('/')) else ''
                resp = handle_version_request(path)
                if (resp is None):
                    response['error'] = 'UNKNOWN COMMAND'
                response['response'] = resp
                response['command'] = '/'.join(toks)
            else:
                url = '/'.join(toks[1:])
                _response = fetch_from_url(url)
                if (_response is None):
                    response['error'] = 'ERROR: Missing Valid URL !!!  Use (http://%s%s/url-goes-here)' % (request.host.host,':%s' % (request.host.port) if (request.host.port) else '')
                else:
                    response['response'] = _response
            response = json.dumps(response)
            self.channel.send(response)
            stackless.schedule()

class MyRequestHandler(http.Request):

    def process(self):

        MyRequestHandler.requestChannel.send(self)
        result = MyRequestHandler.requestChannel.receive()
        self.write(result)
        self.finish()

class MyHttp(http.HTTPChannel):
    requestFactory = MyRequestHandler

class MyHttpFactory(http.HTTPFactory):
    protocol = MyHttp

def args():
    for arg in sys.argv:
        yield arg
    yield None

if (__name__ == "__main__"):
    from twisted.internet import reactor

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()
    
    args = {'--help':'show some help.',
            '--verbose':'output more stuff.',
            '--debug':'debug some stuff.',
            '--bind=?':'must be in the form of 127.0.0.1:19999.',
            '--proxy=?':'must be a valid socks proxy in the form of 127.0.0.1:8080.',
            }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = __args__.programName
    
	_isVerbose = __args__.get_var('isVerbose',Args._bool_,False)
	if (_isVerbose):
	    print >>sys.stdout, 'DEBUG: _isVerbose=%s' % (_isVerbose)
	_isDebug = __args__.get_var('isDebug',Args._bool_,False)
	if (_isVerbose):
	    print >>sys.stdout, 'DEBUG: _isDebug=%s' % (_isDebug)
	_isHelp = __args__.get_var('isHelp',Args._bool_,False)
	if (_isVerbose):
	    print >>sys.stdout, 'DEBUG: _isHelp=%s' % (_isHelp)
    
	if (_isHelp):
	    ppArgs()
	    sys.exit()

	_bind = __args__.get_var('bind',Args._str_,'')
	if (_isVerbose):
	    print >>sys.stdout, 'DEBUG: _bind=%s' % (_bind)

	_proxy = __args__.get_var('proxy',Args._str_,'')
	if (_isVerbose):
	    print >>sys.stdout, 'DEBUG: _proxy=%s' % (_proxy)

	print 'Listening to #%s.' % (_bind)
	
	if (len(_proxy) > 0):
	    print 'Using Socks Proxy via #%s.' % (_proxy)
	    from vyperlogix.sockets.proxies.socks import socks
	    import socket
	    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, _proxy.split(':')[0], int(_proxy.split(':')[-1]))
	    socket.socket = socks.socksocket
	    
	channel = stackless.channel()
	    
	cgiTasklet = Cgi("cgiTasklet-1", channel)
	server = Server()
	    
	stackless.tasklet(cgiTasklet.execute)()
	stackless.tasklet(server.execute)(_bind, channel)
	    
	while (stackless.getruncount() > 1):
	    stackless.schedule()
	