from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from xml.dom.minidom import parseString
import time
_isPsyco = False
try:
    import psyco
    _isPsyco = True
except:
    pass
import Queue
import os
import sys
from vyperlogix import callExternalProgram
from vyperlogix import threadpool
from vyperlogix import winreg
import tempfile

_isVerbose = False

_launch_fileName = ''
_uninstall_fileName = ''

_fHand_logFile = -1
_fHand_logFileName = ''

_port = 8000

_pool = threadpool.Pool(10)

_rootKeyName = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'

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
        print >>_fHand_logFile, data
        try:
            doc = parseString(data[0:-1])
	    cmds = doc.getElementsByTagName("command")
	    for c in cmds:
		_cmd = getText(c.childNodes)
		if (_cmd == '@@@Shutdown@@@'):
		    if (_isPsyco):
			time.sleep(5)
		    exit(1)
            else:
                pass
        except Exception, details:
	    print >>_fHand_logFile, 'parsing error due to "%s".' % str(details)
       
    def connectionLost(self, reason='connectionDone'):
        print >>_fHand_logFile, self.ip+' disconnected'
	if (_isPsyco):
	    try:
		reactor.stop()
	    except Exception, details:
		print >>sys.stderr, 'ERROR when attempting to stop the reactor, due to "%s".' % str(details)

class XMLSocket(Factory):
    clients=[]
    msg = '<hello>hello world, there are "%s" clients connected.</hello>\x00' % len(clients)
    protocol = XMLSocketProtocol
    #services = [["socket",XMLSocketProtocol]]
    def __init__(self, protocol=None):
        self.protocol = protocol
        reactor.callLater(0,self.sendMsg)
    def sendMsg(self):
        msg = self.msg
        if msg:
            for client in self.clients:
                client.transport.write(msg+"\x00")

@threadpool.threadpool(_pool)
def launchAirApp(fname):
    print >>_fHand_logFile, 'Launching the AIR App "%s".' % fname
    if (os.path.exists(fname)):
	print >>_fHand_logFile, 'Launched the AIR App "%s".' % fname
	callExternalProgram.callExternalProgram(fname)

def cleanUpCommandFileContents(_installLocation,_fnameY):
    cmds = []
    if (os.path.exists(_installLocation)):
	for root, dirs, files in os.walk(_installLocation, topdown=False):
	    for d in dirs:
		cmds.append('del "%s%s%s%s*.*" < "%s"' % (root,os.sep,d,os.sep,_fnameY))
		cmds.append('rmdir "%s%s"' % (root,d))
	    cmds.append('del "%s%s*.*" < "%s"' % (root,os.sep,_fnameY))
	    cmds.append('rmdir "%s"' % (root))
	cmds.append('del "%s"' % (_fnameY))
    return cmds

def writeFileUsing(fname,lines):
    fHand = open(fname,'w')
    fHand.writelines('\n'.join(lines))
    fHand.flush()
    fHand.close()

def locateNameOfAirAppForThisServer(serverFolderName):
    root = winreg.get_key(winreg.HKEY.LOCAL_MACHINE, _rootKeyName, winreg.KEY.ALL_ACCESS)
    print >>sys.stderr, 'root.__class__=(%s)' % (str(root.__class__))
    print >>sys.stderr, 'root.keys.__class__=(%s)' % (str(root.keys.__class__))
    toks = serverFolderName.lower().split(os.sep)
    for k in root.keys:
	print >>sys.stderr, 'k=(%s), k.__class__=(%s)' % (str(k),str(k.__class__))
	subKey = winreg.get_key(root, k, winreg.KEY.ALL_ACCESS)
	for v in subKey.values:
	    x = str(subKey.values[str(v)].value)
	    xToks = x.lower().split(os.sep)
	    print >>sys.stderr, '(%s) x=(%s), serverFolderName=(%s)' % (k,str(x),serverFolderName)
	    if (toks[-1] == xToks[-1]):
		return k
	print >>sys.stderr, '\n'
    return ''

def launchAirAppUninstaller(fname):
    root = winreg.get_key(winreg.HKEY.LOCAL_MACHINE, _rootKeyName, winreg.KEY.ALL_ACCESS)
    toks = sys.argv[0].split(os.sep)
    toks.pop()
    toks.pop()
    try:
	appSubKey = winreg.get_key(root, toks[-1]+'Server', winreg.KEY.ALL_ACCESS)
    except Exception, details:
	print >>sys.stderr, 'ERROR due to "%s".' % str(details)
    vals = appSubKey.values
    _original_uninstall_string = ''
    _installLocation = ''
    try:
	_installLocation = str(vals['InstallLocation'].value)
    except:
	pass
    # write a command file in a temp folder and run it to perform the clean-up.
    _root = tempfile.mkdtemp()
    _fname = _root+os.sep+'clean-'+toks[-1]+'.cmd'
    _fnameY = _root+os.sep+'y.txt'
    try:
	writeFileUsing(_fnameY,['y',''])
	writeFileUsing(_fname,cleanUpCommandFileContents(_installLocation,_fnameY))
	callExternalProgram.callExternalProgram(_fname)
    except:
	pass

if (_isPsyco):
    psyco.full()

if ( (len(sys.argv) > 1) and (sys.argv[1] == '--help') ):
    print >>sys.stderr, '--help                           ... displays this help text.'
    print >>sys.stderr, '--port=port_number               ... port number.'
    print >>sys.stderr, '--launch=fileName_to_execute     ... port number.'
    print >>sys.stderr, '--uninstall=original_uninstaller ... uninstall the AIR App and clean-up afterwards using the original uninstaller from Adobe.'
else:
    toks = sys.argv[0].split(os.sep)
    _programName = toks[-1]
    for i in xrange(len(sys.argv)):
	bool = ( (sys.argv[i].find('--port=') > -1) or (sys.argv[i].find('--launch=') > -1) or (sys.argv[i].find('--uninstall=') > -1) )
	if (bool): 
	    toks = sys.argv[i].split('=')
	    if (sys.argv[i].find('--port=') > -1):
		if (str(toks[1]).isdigit()):
		    _port = int(toks[1])
	    elif (sys.argv[i].find('--launch=') > -1):
		_launch_fileName = toks[1]
	    elif (sys.argv[i].find('--uninstall=') > -1):
		_uninstall_fileName = toks[1]
	elif (sys.argv[i].find('--verbose') > -1):
	    _isVerbose = True

try:
    toks = sys.argv[0].split(os.sep)
    toks.pop()
    toks.pop()
    _time = time.localtime()
    _fHand_logFileName = os.sep.join([os.sep.join(toks),_programName.replace('.exe','')+'_%s-%s-%s-%s-%s-%s.log' % (_time[1],_time[2],_time[0],_time[3],_time[4],_time[5])])
    _fHand_logFile = open(_fHand_logFileName,'w')
except Exception, details:
    print >>sys.stderr, "Execution of Log File Creation failed:", details

if ( (len(_launch_fileName) > 0) or (len(_uninstall_fileName) == 0) ):
    if ( (len(_launch_fileName) > 0) and (_launch_fileName.find('.exe') > -1) ):
	launchAirApp(_launch_fileName)
    try:
	reactor.listenTCP(_port, XMLSocket(XMLSocketProtocol))
	print 'XMLSocket Server listening on port %s.' % _port
	reactor.run()
    except Exception, details:
	print 'ERROR in starting the XMLSocket Server due to "%s".' % str(details)

if (len(_uninstall_fileName) > 0):
    launchAirAppUninstaller(_uninstall_fileName)

try:
    _fHand_logFile.flush()
    _fHand_logFile.close()
except Exception, details:
    print >>sys.stderr, "Execution of Log File Finalization failed:", details
