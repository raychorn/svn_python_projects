from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from xml.dom.minidom import parseString
import time
import psyco
import Queue

_isVerbose = False

_port = 8000

_queue = Queue.Queue(100)

def getText(nodelist):
    rc = ""
    for node in nodelist:
	if node.nodeType == node.TEXT_NODE:
	    rc = rc + node.data
    return rc

class XMLSocketProtocol(Protocol):
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
		if (val == '@@@Shutdown@@@'):
		    exit(1)
            else:
                pass
        except Exception, details:
	    print 'parsing error due to "%s".' % str(details)
       
    def connectionLost(self, reason='connectionDone'):
        print self.ip+' disconnected'

class XMLSocket(Factory):
    clients=[]
    _queue.put('<hello>hello world</hello>\x00')
    protocol = XMLSocketProtocol
    def __init__(self, protocol=None):
        self.protocol = protocol
        reactor.callLater(0,self.sendMsg)
    def sendMsg(self):
        msg = _queue.get()
	_queue.task_done()
        if msg:
            for client in self.clients:
                client.transport.write(msg+"\x00")
        reactor.callLater(0,self.sendMsg)

if ( (len(sys.argv) > 1) and (sys.argv[1] == '--help') ):
    print '--help               ... displays this help text.'
    print '--port=port_number   ... port number.'
else:
    toks = sys.argv[0].split(os.sep)
    _programName = toks[-1]
    for i in xrange(len(sys.argv)):
	bool = (sys.argv[i].find('--port=') > -1)
	if (bool): 
	    toks = sys.argv[i].split('=')
	    if (sys.argv[i].find('--port=') > -1):
		if (str(toks[1]).isdigit()):
		    _port = int(toks[1])
	elif (sys.argv[i].find('--verbose') > -1):
	    _isVerbose = True

psyco.full()
reactor.listenTCP(_port, XMLSocket(XMLSocketProtocol))
print 'XMLSocket Server listening on port %s.' % _port
reactor.run()
