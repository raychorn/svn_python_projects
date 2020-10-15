#!/usr/bin/env python
"""
Webserver.py
Andrew Francis
February 25th, 2007

Example of Twisted and Stackless integration that
blocks.

The server listens on http://localhost:8000

The programme and is fine for many purposes. However
there is a
flaw. Whenever the server tasklet blocks, it blocks
the entire
programme. Ideally other tasklets, such as the Tick
tasklet should
run while the server tasklet waits for connections.

<song>The Bleeding Heart Show - The New
Pornographers</song>
"""


import stackless
from twisted.web           import http

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
            print path
            self.channel.send("<html><body>" + self.name + " received path: " + path + "count :" + str(self.count) + "</body></html>")
            self.count = self.count + 1
            stackless.schedule()


def tick():
    count = 0
    while (1):
        print "tick: ", count
        count += 1
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


if __name__ == "__main__":
    from twisted.internet import reactor

    channel = stackless.channel()

    cgiTasklet = Cgi("cgiTasklet-1", channel)
    server = Server()

    stackless.tasklet(cgiTasklet.execute)()
    stackless.tasklet(server.execute)(8000, channel)
    stackless.tasklet(tick)()

    while (stackless.getruncount() > 1):
        stackless.schedule()
