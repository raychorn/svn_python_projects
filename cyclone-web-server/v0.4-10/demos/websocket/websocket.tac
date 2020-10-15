#!/usr/bin/env twistd -ny
# point your browser to http://localhost:8888


import cyclone.web
from twisted.application import service, internet


class MainHandler(cyclone.web.RequestHandler):
    def get(self):
        self.render("interact.html")

class AuthMainHandler(cyclone.web.RequestHandler):
    def get(self):
        self.render("authinteract.html")


class WebSocketHandler(cyclone.web.WebSocketHandler):
    def connectionMade(self, *args, **kwargs):
        print "connection made:", args, kwargs

    def messageReceived(self, message):
        self.sendMessage("echo: %s" % message)
#        self.transport.loseConnection()

    def connectionLost(self, why):
        print "connection lost:", why

class AuthWebSocketHandler(WebSocketHandler):
    # headersReceived is called BEFORE connectionMade
    # when it raises an HTTPError exception it closes the connection
    # you may also use the regular @cyclone.web.authenticate decorator here
    # for this example, the browser has to set a cookie like this:
    #   document.cookie = "auth=user@domain:password"
    # see authinteract.html for details
    def headersReceived(self):
        try:
            username, password = self.get_cookie("auth").split(":",1)
            print "username: %s, password: %s" % (username, password)
            assert username == "user@domain" and password == "password"
        except Exception, e:
            raise cyclone.web.HTTPError(401)

class WebSocketApplication(cyclone.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/websocket", WebSocketHandler),
            (r"/auth", AuthMainHandler),
            (r"/authwebsocket", AuthWebSocketHandler),
        ]

        settings = { "template_path": "." }
        cyclone.web.Application.__init__(self, handlers, **settings)


application = service.Application("websocket")
internet.TCPServer(8888, WebSocketApplication(),
    interface="127.0.0.1").setServiceParent(application)
