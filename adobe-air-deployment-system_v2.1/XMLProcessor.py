from lib import Enum
from xml.dom.minidom import parseString
import os
import sys
from lib import decodeUnicode
import time
import traceback
from lib import ConnectionHandle
from lib.pyinstaller13 import ArchiveViewer
from pyinstaller13 import archive
from pyinstaller13 import carchive
try:
    import zlib
except ImportError:
    zlib = archive.DummyZlib()
import tempfile

def DummyCallBack(data, cmd):
    pass

class Commands(Enum.Enum):
    list_archives = 1
    open_archive = 2
    open_package = 3
    export_package_from = 4
    SHUTDOWN = 999

class ListToXMLOptions(Enum.Enum):
    nonCSV = False
    isCSV = True

def listItemToXML(item,headTag='<list-item>'):
    data = ''
    if (isinstance(headTag,str)):
	_headTag = headTag
	data = _headTag
	try:
	    if ( (isinstance(item,str)) or (isinstance(item,int)) ):
		data += '<item>%s</item>' % decodeUnicode.decodeUnicode(str(item).strip())
	except:
	    pass
	data += _headTag.replace('<','</')
    return data

def listPackagesAndArchivesRelativeTo(connHandle,top):
    _files = []
    _xml = listItemToXML(top,'<list-head>')
    connHandle.server.__send__(connHandle,_xml)
    for root, dirs, files in os.walk(top, topdown=True):
	for name in files:
	    if ( (name.find('.exe') > -1) or (name.find('.pkg') > -1) ):
		_fname = os.path.join(root, name)
		try:
		    arch = ArchiveViewer.getArchive(_fname)
		    _xml = listItemToXML(_fname)
		    connHandle.server.__send__(connHandle,_xml)
		except Exception, details:
		    print >>sys.stderr, '(listPackagesAndArchivesRelativeTo).ERROR :: Reason "%s".' % (str(details))
    #_files.insert(0,top)
    return _files

def exportPackageFromNamedArchive(archName,pkgName,destFile=None):
    if (os.path.exists(archName)):
	arch = ArchiveViewer.getArchive(archName)
	ndx = -1 if (len(pkgName) == 0) else arch.toc.find(pkgName)
	if (ndx > -1):
	    pkgFolder = tempfile.mkdtemp() if (destFile == None) else os.path.dirname(destFile)
	    pkgTempName = tempfile.TemporaryFile('w') if (destFile == None) else destFile
	    try:
		fHandPkg = open(os.sep.join([pkgFolder,pkgTempName.name.split(os.sep)[-1]]),'wb')
	    except:
		print >>sys.stderr, '(exportPackageFromNamedArchive) :: pkgTempName=(%s)' % pkgTempName
		fHandPkg = open(pkgTempName,'wb')
	    dpos, dlen, ulen, flag, typcd, nm = arch.toc[ndx]
	    x, data = arch.extract(ndx)
	    fHandPkg.write(data)
	    fHandPkg.flush()
	    fHandPkg.close()
	    try:
		if typcd == 'z':
		    _arch = ZlibArchive(fHandPkg.name)
		else:
		    _arch = carchive.CArchive(fHandPkg.name)
		return ((dpos, dlen, ulen, flag, typcd, nm),_arch,fHandPkg,pkgTempName,pkgFolder)
	    except Exception, details:
		return (-1,str(details))
    else:
	return (-1,'Invalid archive name.')
    return (-1,'UNKNOWN ERROR')

class XMLProcessor:
    def __init__(self):
	self.callBack = DummyCallBack
	self._isPsyco = False
	try:
	    self._isPsyco = (str(psyco.full).find("'function'") > -1)
	except:
	    pass
    
    def __callback__(self, code):
	if (str(type(self.callBack)).find("'function'") > -1):
	    try:
		self.callBack(code)
	    except:
		print >>sys.stderr, '(XMLProcessor.callback) :: code=(%s)' % (code)
		print >>sys.stderr, traceback.format_exc()
    
    def getText(self, nodelist):
	rc = ""
	print >>sys.stderr, 'nodelist=(%s)' % str(nodelist)
	for node in nodelist:
	    print >>sys.stderr, 'node=(%s)' % str(node)
	    print >>sys.stderr, 'node.nodeType=(%s)' % str(node.nodeType)
	    if node.nodeType == node.TEXT_NODE:
		rc = rc + node.data
	    print >>sys.stderr, '\n'
	return decodeUnicode.decodeUnicode(str(rc))
    
    def isCommandValid(self,cmd):
	try:
	    x = Commands(cmd)
	    return True
	except:
	    return False
	return False

    def listToXML(self,items,isCSV=ListToXMLOptions.nonCSV):
	_headTag = '<list>' if isCSV == ListToXMLOptions.nonCSV else '<csv>'
	data = _headTag
	try:
	    for i in items:
		if ( (isinstance(i,str)) or (isinstance(i,int)) ):
		    s = decodeUnicode.decodeUnicode(str(i).strip())
		else:
		    s = ','.join([decodeUnicode.decodeUnicode(str(t).strip()) for t in list(i)])
		data += '<item>%s</item>' % s
	except:
	    pass
	data += _headTag.replace('<','</')
	return data

    def linesFromArchive(self,arch,archName,onlyTheseTypes=[]):
	lines = []
	try:
	    fHand = tempfile.TemporaryFile('w+')
	    print >>sys.stderr, '(linesFromArchive) :: fHand.name=(%s)' % fHand.name
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
	    if (len(lines) == 1):
		_emptyLine = []
		_toks = lines[0].split(',')
		print '(linesFromArchive).1 :: _toks="%s"' % str(_toks)
		for e in _toks:
		    if (e == 'name'):
			_emptyLine.append('NO PACKAGES')
		    else:
			_emptyLine.append('')
		print '(linesFromArchive).2 :: _emptyLine="%s"' % str(_emptyLine)
		lines.append(','.join(_emptyLine))
		print '(linesFromArchive).3 :: lines="%s"' % str(lines)
	    fHand.close()
	except Exception, details:
	    print >>sys.stderr, '(linesFromArchive).ERROR due to "%s".' % str(details)
	    print >>sys.stderr, traceback.format_exc()
	return lines

    def processXML(self,connHandle,data):
	print >>sys.stderr, '(XMLProcessor.processXML) :: data=(%s), data.__class__=(%s)' % (str(data),str(data.__class__))
	try:
	    if (len(data) > 0):
		if (data.endswith('\x00')):
		    doc = parseString(data[0:-1])
		else:
		    doc = parseString(data)
		cmds = doc.getElementsByTagName("command")
		argVal = ''
		print >>sys.stderr, 'cmds=(%s)' % str(cmds)
		for c in cmds:
		    _cmd = self.getText(c.childNodes)
		    #print >>sys.stderr, 'c=(%s)' % str(c)
		    if (c.hasAttribute('value')):
			argVal = decodeUnicode.decodeUnicode(c.getAttribute('value'))
		    if (len(_cmd) == 0):
			_cmd = argVal
			argVal = ''
		    if ( (len(_cmd) > 0) and (len(argVal) > 0) ):
			_cmd, argVal = (argVal, _cmd)
		    if (argVal == ''):
			# argVal processing has changed however we maintain compatability with earlier version that used the now deprecated pattern.
			argVal = []
			args = c.getElementsByTagName("arg")
			for a in args:
			    if (a.hasAttribute('value')):
				argVal.append(decodeUnicode.decodeUnicode(a.getAttribute('value')))
		    if (str(_cmd).isdigit()):
			_cmd = int(_cmd)
		    print >>sys.stderr, '_cmd=(%s) [%s]' % (str(_cmd),str(_cmd.__class__))
		    print >>sys.stderr, 'argVal=(%s) [%s]' % (str(argVal),str(argVal.__class__))
		    print >>sys.stderr, 'isCommandValid(%s)=(%s)' % (_cmd,self.isCommandValid(_cmd))
		    print >>sys.stderr, 'Commands(%s)=(%s)' % (_cmd,Commands(_cmd))
		    _open_archive_file_types = ['.pkg']
		    if (Commands(_cmd) == Commands(Commands.SHUTDOWN)):
			return None
		    elif (self.isCommandValid(_cmd)):
			if ( (Commands(_cmd) == Commands(Commands.open_archive)) and ( ( (isinstance(argVal,str)) and (argVal.endswith('.pkg')) ) or (isinstance(argVal,list) and (argVal[0].endswith('.pkg'))) ) ):
			    _cmd = Commands.open_archive
			    _open_archive_file_types = []
			if (Commands(_cmd) == Commands(Commands.list_archives)):
			    _path = os.path.abspath(os.curdir)
			    files = listPackagesAndArchivesRelativeTo(connHandle,_path)
			    files.sort()
			    _xml = self.listToXML(files)
			    return (_xml,_cmd)
			elif (Commands(_cmd) == Commands(Commands.open_archive)):
			    lines = []
			    try:
				arch = ArchiveViewer.getArchive(argVal[0])
				lines = self.linesFromArchive(arch,argVal[0],_open_archive_file_types)
				print >>sys.stderr, 'OPEN ARCHIVE, arch=(%s)' % str(arch)
				print >>sys.stderr, '"%s" lines' % (len(lines))
				_xml = self.listToXML(lines,ListToXMLOptions.isCSV)
			    except Exception, details:
				errCode = '(%s).ERROR in OPEN ARCHIVE due to "%s".' % (_cmd,str(details))
				print >>sys.stderr, errCode
				print >>sys.stderr, traceback.format_exc()
				return ('<error>%s</error>' % errCode,'Programming Error')
			    return (_xml,_cmd)
			elif (Commands(_cmd) == Commands(Commands.open_package)):
			    _arch = None
			    _xml = ''
			    try:
				fHandPkg = None
				pkgTempName = None
				pkgFolder = None
				archName, pkgName = argVal[0].split(',')
				print >>sys.stderr, 'OPEN PACKAGE, archName=(%s), pkgName=(%s)' % (archName,pkgName)
				retVal = exportPackageFromNamedArchive(archName,pkgName)
				if ( (isinstance(retVal,tuple)) and (isinstance(retVal[0],tuple)) ):
				    stats,_arch,fHandPkg,pkgTempName,pkgFolder = retVal
				else:
				    errCode,details = retVal
				    print >>sys.stderr, '(XMLProcessor.processXML).ERROR due to "%s" from exportPackageFromNamedArchive().' % (details)
				    return ('<error>%s</error>' % details,'Programming Error')
			    except Exception, details:
				print >>sys.stderr, '(%s).ERROR in OPEN PACKAGE due to "%s".' % (_cmd,str(details))
				print >>sys.stderr, traceback.format_exc()
			    if (_arch):
				lines = self.linesFromArchive(_arch,pkgName,[])
				_xml = self.listToXML(lines,ListToXMLOptions.isCSV)
				_arch.lib.close()
			    try:
				os.remove(fHandPkg.name)
			    except:
				pass
			    try:
				pkgTempName.close()
			    except:
				pass
			    try:
				os.rmdir(pkgFolder)
			    except:
				pass
			    return (_xml,_cmd)
			elif (Commands(_cmd) == Commands(Commands.export_package_from)):
			    archName,pkgName,destFolder = argVal
			    print >>sys.stderr, 'EXPORT PACKAGE FROM, archName=(%s), pkgName=(%s), destFolder=(%s)' % (archName,pkgName,destFolder)
			    retVal = exportPackageFromNamedArchive(archName,pkgName,destFolder)
			    if ( (isinstance(retVal,tuple)) and (isinstance(retVal[0],tuple)) ):
				if (len(retVal) == 2):
				    stats,_arch = retVal
				elif (len(retVal) == 5):
				    stats,_arch,_fHandPkg,_pkgTempName,_pkgFolder = retVal
				    stats = list(stats)
				    stats.append(_pkgTempName)
				print >>sys.stderr, '+++ stats=(%s)' % (str(stats))
				_xml = self.listToXML(list(stats),ListToXMLOptions.isCSV)
				print >>sys.stderr, '+++ _xml=(%s)' % (_xml)
				_arch.lib.close()
				return (_xml,_cmd)
			    else:
				errCode,details = retVal
				print >>sys.stderr, '(XMLProcessor.processXML).ERROR in EXPORT PACKAGE due to "%s" from exportPackageFromNamedArchive().' % (details)
				return ('<error>%s</error>' % details,'Programming Error')
			else:
			    _cmd = str(_cmd)
			    return (_cmd,_cmd)
		    else:
			_details = 'Invalid command valud of "%s".' % str(_cmd)
			print >>sys.stderr, '(XMLProcessor.processXML).ERROR due to "%s".' % (_details)
			return ('<error>%s</error>' % _details,'Programming Error')
		    print >>sys.stderr, '\n'
	except Exception, details:
	    _details = 'parsing error due to "%s".' % str(details)
	    print >>sys.stderr, _details
	    _traceBack = traceback.format_exc()
	    print >>sys.stderr, _traceBack
	    return ('<error>%s, %s</error>' % (_details,_traceBack),'Exception')
