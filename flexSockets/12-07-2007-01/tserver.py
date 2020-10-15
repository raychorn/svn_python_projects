from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

class Echo(Protocol):
    def connectionMade(self):
        print '(Echo.connectionMade) :: .'
            
    def connectionLost(self, reason):
        print '(Echo.connectionLost) :: .'
        self.transport.loseConnection()
    
    def dataReceived(self, data):
        print '(Echo.dataReceived) :: data=(%s)' % (data)
        self.transport.write(data)

def main():
    print '(main) :: Waiting for connection from client.'
    factory = Factory()
    factory.protocol = Echo
    reactor.listenTCP(7800, factory)
    reactor.run()

if (__name__ == '__main__'):
    main()

