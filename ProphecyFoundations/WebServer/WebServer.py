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

@CGIEndPoint(re.compile(r'^/file/'))
def handle_file_request(path):
    _response = {}
    fpath = urllib.unquote_plus(unpack_url(path).pop())
    if (os.path.isfile(fpath)):
	content = [l.strip() for l in open(fpath, 'r').readlines()]
        _response['content'] = content
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
	    _response = handle_file_request(path)
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

if (__name__ == "__main__"):
    from twisted.internet import reactor
    
    __port = 8000

    channel = stackless.channel()

    cgiTasklet = Cgi("cgiTasklet-1", channel)
    server = Server()

    stackless.tasklet(cgiTasklet.execute)()
    stackless.tasklet(server.execute)(__port, channel)

    while (stackless.getruncount() > 1):
        stackless.schedule()
