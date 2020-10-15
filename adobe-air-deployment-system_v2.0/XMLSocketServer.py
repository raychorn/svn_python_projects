import os
import sys
from twisted.internet.protocol import Factory, Protocol
try:
    from twisted.internet import reactor
except Exception, details:
    print >>sys.stderr, 'ERROR due to "%s".  Possible Corrective Action(s):  Make sure your Firewall is open for this application.  Some Firewalls can be made to block network access on a per application basis.' % details
from xml.dom.minidom import parseString
import time
_isPsyco = False
try:
    import psyco
    _isPsyco = True
except:
    pass
import Queue
from lib import callExternalProgram
from lib import threadpool
from lib import winreg
from lib import decodeUnicode
import tempfile
from lib.pyinstaller13 import ArchiveViewer
from pyinstaller13 import archive
from pyinstaller13 import carchive
try:
    import zlib
except ImportError:
    zlib = archive.DummyZlib()

# To-Do:
#
#  1).  Lift-out the code away from the TCP/IP Engine to allow the other Engine to be used instead.
#  2).  Better define the various logging levels to make --production less verbose than --development

_isVerbose = False
_isDevelopment = True
_isProduction = (not _isDevelopment)

_launch_fileName = ''
_uninstall_fileName = ''

_fHand_logFile = -1
_fHand_logFileName = ''

_port = 55555

_pool = threadpool.Pool(10)

_rootKeyName = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'

_const_shutdown_symbol = '@@@Shutdown@@@'

_const_list_archives_symbol = 'list_archives'
_const_open_archive_symbol = 'open_archive'
_const_open_package_symbol = 'open_package'

def getText(nodelist):
    rc = ""
    print >>_fHand_logFile, 'nodelist=(%s)' % str(nodelist)
    for node in nodelist:
	print >>_fHand_logFile, 'node=(%s)' % str(node)
	print >>_fHand_logFile, 'node.nodeType=(%s)' % str(node.nodeType)
	if node.nodeType == node.TEXT_NODE:
	    rc = rc + node.data
	print >>_fHand_logFile, '\n'
    return decodeUnicode.decodeUnicode(str(rc))

def listToXML(items):
    data = '<list>'
    try:
	for i in items:
	    if (isinstance(i,str)):
		s = decodeUnicode.decodeUnicode(str(i).strip())
	    else:
		s = ','.join([decodeUnicode.decodeUnicode(str(t).strip()) for t in list(i)])
	    data += '<item>%s</item>' % s
    except:
	pass
    data += '</list>'
    return data

def linesFromArchive(arch,archName,onlyTheseTypes=[]):
    lines = []
    try:
	fHand = tempfile.TemporaryFile('w+')
	print >>_fHand_logFile, '(linesFromArchive) :: fHand.name=(%s)' % fHand.name
	ArchiveViewer.show(archName,arch,fHand)
	fHand.seek(0)
	lines = [str(l).strip() for l in fHand.readlines()]
	lines[0] = ','.join([str(l).strip() for l in lines[0].split(',')])
	lines[1:] = [','.join([str(i).strip() for i in str(l).replace('[','').replace('(','').replace(')','').replace(']','').replace("'","").split(',')]) for l in lines[1:]]
	_lines = []
	for l in lines[1:]:
	    if (len(onlyTheseTypes) > 0):
		for t in onlyTheseTypes:
		    if (l.find(t) > -1):
			_lines.append(l)
			break
	    else:
		_lines.append(l)
	lines[1:] = _lines
	fHand.close()
    except Exception, details:
	print >>_fHand_logFile, '(linesFromArchive).ERROR due to "%s".' % str(details)
    return lines
    
class XMLSocketProtocol(Protocol):
    def connectionMade(self):
        self.write(self.factory.msg,'connection')
        self.ip = self.transport.getHost().host
        print self.ip+' connected'
	
    def write(self, data, cmd):
	if ( (isinstance(data,str)) and (isinstance(cmd,str)) ):
	    data = '<resp value="%s">%s</resp>' % (cmd,data)
	    if (not data.endswith('\x00')):
		data += '\x00'
	    if (_isDevelopment):
		print >>_fHand_logFile, 'RESP:"%s"' % str(data)
	    self.transport.write(data)
	else:
	    _data = '<resp value="Exception"><error>Invalid data (<![CDATA[%s]]>)[<![CDATA[%s]]>] or cmd (<![CDATA[%s]]>)[<![CDATA[%s]]>].</error></resp>\x00' % (str(data),str(data.__class__),str(cmd),str(cmd.__class__))
	    print >>_fHand_logFile, 'RESP:"%s"' % str(_data)
	    self.transport.write(_data)

    def dataReceived(self, data):
        print >>_fHand_logFile, '(dataReceived) :: data=(%s), data.__class__=(%s)' % (str(data),str(data.__class__))
        try:
            doc = parseString(data[0:-1])
	    cmds = doc.getElementsByTagName("command")
	    argVal = ''
	    print >>_fHand_logFile, 'cmds=(%s)' % str(cmds)
	    for c in cmds:
		_cmd = getText(c.childNodes)
		print >>_fHand_logFile, 'c=(%s)' % str(c)
		if (c.hasAttribute('value')):
		    argVal = decodeUnicode.decodeUnicode(c.getAttribute('value'))
		if (len(_cmd) == 0):
		    _cmd = argVal
		    argVal = ''
		if ( (len(_cmd) > 0) and (len(argVal) > 0) ):
		    _cmd, argVal = (argVal, _cmd)
		print >>_fHand_logFile, '_cmd=(%s) [%s]' % (str(_cmd),str(_cmd.__class__))
		print >>_fHand_logFile, 'argVal=(%s) [%s]' % (str(argVal),str(argVal.__class__))
		if (_cmd == _const_shutdown_symbol):
		    if (_isPsyco):
			time.sleep(5)
		    self.transport.loseConnection()
		    try:
			exit(1)
		    except:
			pass
		elif (_cmd == _const_list_archives_symbol):
		    files = []
		    for f in os.listdir('.'):
			if (f.find('.exe') > -1):
			    files.append(f)
		    _xml = listToXML(files)
		    self.write(_xml,_cmd)
		elif (_cmd == _const_open_archive_symbol):
		    arch = ArchiveViewer.getArchive(argVal)
		    lines = linesFromArchive(arch,argVal,['.pkg'])
		    print >>_fHand_logFile, 'OPEN ARCHIVE, arch=(%s)' % str(arch)
		    print >>_fHand_logFile, '"%s" lines' % (len(lines))
		    _xml = listToXML(lines)
		    self.write(_xml,_cmd)
		elif (_cmd == _const_open_package_symbol):
		    _arch = None
		    try:
			toks = argVal.split(',')
			archName, pkgName = toks
			arch = ArchiveViewer.getArchive(archName)
			pkgFolder = tempfile.mkdtemp()
			pkgTempName = tempfile.TemporaryFile('w')
			fHandPkg = open(os.sep.join([pkgFolder,pkgTempName.name.split(os.sep)[-1]]),'wb')
			ndx = arch.toc.find(pkgName)
			dpos, dlen, ulen, flag, typcd, nm = arch.toc[ndx]
			x, data = arch.extract(ndx)
			fHandPkg.write(data)
			fHandPkg.flush()
			fHandPkg.close()
			if typcd == 'z':
			    _arch = ZlibArchive(fHandPkg.name)
			else:
			    _arch = carchive.CArchive(fHandPkg.name)
		    except Exception, details:
			print >>_fHand_logFile, '(%s).ERROR due to "%s".' % (_cmd,str(details))
		    lines = linesFromArchive(_arch,pkgName,[])
		    print >>_fHand_logFile, 'OPEN PACKAGE, archName=(%s), pkgName=(%s)' % (archName,pkgName)
		    print >>_fHand_logFile, '"%s" lines' % (len(lines))
		    _xml = listToXML(lines)
		    self.write(_xml,_cmd)
		    _arch.lib.close()
		    os.remove(fHandPkg.name)
		    pkgTempName.close()
		    os.rmdir(pkgFolder)
		else:
		    _cmd = str(_cmd)
		    self.write(_cmd,_cmd)
		print >>_fHand_logFile, '\n'
        except Exception, details:
	    _details = 'parsing error due to "%s".' % str(details)
	    self.write('<error>%s</error>' % _details,'Exception')
       
    def connectionLost(self, reason='connectionDone'):
        print >>_fHand_logFile, self.ip+' disconnected'
	if (_isPsyco):
	    try:
		reactor.stop()
	    except Exception, details:
		print >>sys.stderr, 'ERROR when attempting to stop the reactor, due to "%s".' % str(details)

class XMLSocket(Factory):
    msg = '<hello>AIR Deployment & Packaging System Version 2.0</hello>'
    protocol = XMLSocketProtocol
    def __init__(self, protocol=None):
        self.protocol = protocol

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

def arePathsSimilar(path1,path2):
    bool = False
    try:
	toks1 = path1.split(os.sep)
	toks2 = path2.split(os.sep)
	bool = (toks1[0] == toks2[0])
    except:
	pass
    return bool

if (_isPsyco):
    psyco.full()

if ( (len(sys.argv) > 1) and (sys.argv[1] == '--help') ):
    print >>sys.stderr, '--help                           ... displays this help text.'
    print >>sys.stderr, '--development                    ... development mode.'
    print >>sys.stderr, '--production                     ... production mode (lowers the logging level).'
    print >>sys.stderr, '--port=port_number, 49152-65535  ... port number.'
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
		    p = int(toks[1])
		    if ( (p >= 49152) and (p <= 65535) ):
			_port = p
		    else:
			print >>sys.stderr, 'ERROR: Port is out of range and must fall betweem 48152 and 65535 (inclusive) but cannot be "%s".' % p
	    elif (sys.argv[i].find('--launch=') > -1):
		_launch_fileName = toks[1]
	    elif (sys.argv[i].find('--uninstall=') > -1):
		_uninstall_fileName = toks[1]
	elif (sys.argv[i].find('--verbose') > -1):
	    _isVerbose = True
	elif (sys.argv[i].find('--development') > -1):
	    _isDevelopment = True
	elif (sys.argv[i].find('--production') > -1):
	    _isDevelopment = False
    _isProduction = (not _isDevelopment)

try:
    _isRunningDevelopment = False
    toks = sys.argv[0].split(os.sep)
    toks.pop()
    toks.pop()
    _time = time.localtime()
    _tmpDir = tempfile.mkdtemp()
    _baseName = ''.join((_programName.split('.')[0:-1]))+'_%02d-%02d-%04d-%02d-%02d-%02d.log' % (_time[1],_time[2],_time[0],_time[3],_time[4],_time[5])
    _fHand_logFileName = os.sep.join([os.sep.join(toks),_baseName])
    if (not arePathsSimilar(_tmpDir,_fHand_logFileName)):
	_toks = sys.argv[0].split(os.sep)
	_toks.pop()
	_fHand_logFileName = os.sep.join([os.sep.join(_toks),_baseName])
	_isRunningDevelopment = True
    os.rmdir(_tmpDir)
    if (_isRunningDevelopment):
	_fHand_logFile = sys.stderr
    else:
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
