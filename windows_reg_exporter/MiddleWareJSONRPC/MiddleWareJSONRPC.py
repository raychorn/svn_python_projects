#!/usr/bin/env python
"""
Webserver.py
Andrew Francis
February 25th, 2007

Example of Twisted and Stackless integration that
blocks.

The server listens on http://localhost:8000

The programme and is fine for many purposes. However there is a
flaw. Whenever the server tasklet blocks, it blocks the entire
programme. Ideally other tasklets, such as the Tick tasklet should
run while the server tasklet waits for connections.

<song>The Bleeding Heart Show - The New Pornographers</song>
"""

import stackless
from twisted.web import http

import os, sys
import urllib
import simplejson

import re

from vyperlogix import misc

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

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

@CGIEndPoint(re.compile(r'^/registry/'))
def handle_registry_request(path):
    _response = {}
    fpath = urllib.unquote_plus(unpack_url(path).pop())
    if (os.path.isfile(fpath)):
        ftype = os.path.splitext(fpath)[-1]
        fpath = os.path.dirname(fpath)
        _response['fpath'] = fpath
        _response['files'] = [f for f in os.listdir(fpath) if (f.find(ftype) > -1)]
    return _response

class Server(object):

    def execute(self, port, requestChannel):
        MyRequestHandler.requestChannel = requestChannel
        reactor.listenTCP(port, MyHttpFactory())
        reactor.run()


class Cgi(object):
    def __init__(self, name, channel):
        self.name = name
        self.channel = channel
        self.count = 0
        return

    def execute(self):
        while (1):
            path = self.channel.receive()
            print 'Cgi.execute path=%s' % (path)
            _response = handle_registry_request(path)
            if (not _response):
                _response = {}
            self.count = self.count + 1
            _response['count'] = self.count
            _json = simplejson.dumps(_response)
            self.channel.send(_json)
            stackless.schedule()

class MyRequestHandler(http.Request):

    def process(self):

        MyRequestHandler.requestChannel.send(self.path)
        result = MyRequestHandler.requestChannel.receive()
        self.write(result)
        self.finish()

class MyHttp(http.HTTPChannel):
    requestFactory = MyRequestHandler

class MyHttpFactory(http.HTTPFactory):
    protocol = MyHttp

def do_server(port):
    from twisted.internet import reactor
    
    __port = port

    channel = stackless.channel()

    cgiTasklet = Cgi("cgiTasklet-1", channel)
    server = Server()

    stackless.tasklet(cgiTasklet.execute)()
    stackless.tasklet(server.execute)(__port, channel)

    while (stackless.getruncount() > 1):
	stackless.schedule()

if (__name__ == "__main__"):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
	    '--port=?':'TCP/IP Port.',
	    }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = __args__.programName
	
	_isVerbose = __args__.get_var('isVerbose',bool,False)
	_isDebug = __args__.get_var('isDebug',bool,False)
	_isHelp = __args__.get_var('isHelp',bool,False)

	__port__ = __args__.get_var('port',misc.isInteger,8000)

	if (_isHelp):
	    ppArgs()
	    sys.exit()
	    
	do_server(__port__)
	    
