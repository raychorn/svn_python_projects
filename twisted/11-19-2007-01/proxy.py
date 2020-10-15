from twisted.internet import reactor
from twisted.web import proxy, server

site = server.Site(proxy.ReverseProxyResource('www.yahoo.com', 80, ''))
reactor.listenTCP(8080, site)
reactor.run()
