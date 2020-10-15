from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from xml.dom.minidom import parseString
import time
import psyco
#from vyperlogix import putStr

_port = 8000

def getText(nodelist):
    rc = ""
    for node in nodelist:
	if node.nodeType == node.TEXT_NODE:
	    rc = rc + node.data
    return rc

class Radio(Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)
        self.transport.write(self.factory.msg)
        self.ip = self.transport.getHost().host
        print self.ip+' connected'
        
    def dataReceived(self, data):
        print data
        try:
            doc = parseString(data[0:-1])
	    cmds = doc.getElementsByTagName("command")
	    for c in cmds:
		_cmd = getText(c.childNodes)
		if (_cmd == '@@@Shutdown@@@'):
		    exit(1)
		self.transport.write('<data>%s</data>\x00' % _cmd)
            else:
                pass
        except Exception, details:
	    print 'parsing error due to "%s".' % str(details)
       
    def connectionLost(self, reason='connectionDone'):
        print self.ip+' disconnected'

class XMLSocket(Factory):
    clients=[]
    msg = '<data>hello world</data>\x00'
    protocol = Radio
    services = [["radio",Radio]]
    def __init__(self, protocol=None):
        self.protocol=protocol
        reactor.callLater(0,self.sendMsg)
    def sendMsg(self):
        msg=self.msg
        if msg:
            for client in self.clients:
                client.transport.write(msg+"\x00")
	#else:
	#    time.sleep(0.1)
        #reactor.callLater(0,self.sendMsg)

psyco.full()
reactor.listenTCP(_port, XMLSocket(Radio))
print 'XMLSocket Server listening on port %s.' % _port
reactor.run()
