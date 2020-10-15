#!/usr/bin/env python"""ThreadedWebserver.pyAndrew FrancisFebruary 25th, 2007Example of Twisted and Stackless integration thatallows non-blockingtasklets to executeThe server listens on http://localhost:8000Unlike the previous example, ThreadedWebserver runsStackless in aseparate thread. While Twisted is blocked waiting forconnections,the tick tasklet (or any other tasklet) can execute.<song>Tom Sawyer - Rush</song>"""import stacklessfrom twisted.web           import httpclass Server(object):    def execute(self, port, requestChannel):        MyRequestHandler.channel = requestChannel        reactor.listenTCP(port, MyHttpFactory())        reactor.run()class Cgi(object):    def __init__(self, name, channel):        self.name = name        self.channel = channel        self.count = 0        return    def execute(self):        while (1):            path = self.channel.receive()            print path            self.channel.send("<html><body>" + self.name + " received path: " + path + "count :" + str(self.count) + "</body></html>")            self.count = self.count + 1            stackless.schedule()def tick():    count = 0    while (1):        # we don't want too much output        if count % 1000000 == 0:            print "tick ", count        count += 1        stackless.schedule()class MyRequestHandler(http.Request):    def process(self):        channel.send(self.path)        result = channel.receive()        self.write(result)        self.finish()class MyHttp(http.HTTPChannel):    requestFactory = MyRequestHandlerclass MyHttpFactory(http.HTTPFactory):    protocol = MyHttpdef stacklessThread(requestChannel):    cgiTasklet = Cgi("cgiTasklet-1", requestChannel)    stackless.tasklet(cgiTasklet.execute)()    """    in this example, if the tick tasklet did notexist,    Stackless would complain about deadlock since the    last runnable tasklet (cgiTasklet) would beblocked    """    stackless.tasklet(tick)()    while (stackless.getruncount() > 1):        stackless.schedule()if __name__ == "__main__":    from twisted.internet import reactor    channel = stackless.channel()    reactor.callInThread(stacklessThread,channel)    Server().execute(8000, channel)    reactor.run()   