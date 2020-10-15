import lib.oodb
from xml.dom.minidom import parseString
import os
import sys
import shutil
from vyperlogix import decodeUnicode
import time
import traceback
import dbhash
from vyperlogix import ConnectionHandle
from vyperlogix.pyinstaller13 import ArchiveViewer
from pyinstaller13 import archive
from pyinstaller13 import carchive
#from pyinstaller13 import Build
from vyperlogix.pyinstaller13 import Build
from vyperlogix import shelved
try:
    import zlib
except ImportError:
    zlib = archive.DummyZlib()
import tempfile
_isPsyco = False
try:
    import psyco
    _isPsyco = True
except ImportError:
    pass

def DummyCallBack(data, cmd):
    pass

class Commands(lib.oodb.Enum):
    list_archives = 1
    open_archive = 2
    open_package = 3
    export_package_from = 4
    check_package_name = 5
    build_package = 6
    count_archives = 7
    build_archive = 8
    check_archive_name = 9
    remove_package_from = 10
    SHUTDOWN = 999

class LicenseLevels(lib.oodb.Enum):
    TRIAL = 1
    STANDARD = 2
    PRO = 3
    ENTERPRISE = 4

class ListToXMLOptions(lib.oodb.Enum):
    nonCSV = False
    isCSV = True

class FileTypes(lib.oodb.Enum):
    PKG = 1
    EXE = 2

xformdict = {'PYMODULE' : 'm',
	     'PYSOURCE' : 's',
	     'EXTENSION' : 'b',
	     'PYZ' : 'z',
	     'PKG' : 'a',
	     'DATA': 'x',
	     'BINARY': 'b',
	     'EXECUTABLE': 'b'}

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

def dataToXML(item,source,headTag='<UNKNOWN>'):
    data = ''
    if (isinstance(item,bool)):
	headTag='<boolean>'
    elif ( (isinstance(item,int)) or (isinstance(item,float)) ):
	headTag='<number>'
    elif (isinstance(item,str)):
	headTag='<string>'
    if (isinstance(headTag,str)):
	_headTag = headTag
	data = _headTag
	try:
	    if ( (isinstance(item,str)) or (isinstance(item,int)) ):
		data += '<item>%s</item>' % decodeUnicode.decodeUnicode(str(item).strip())
		data += '<source>%s</source>' % decodeUnicode.decodeUnicode(str(source).strip())
	except:
	    pass
	data += _headTag.replace('<','</')
    return data

def listPackagesAndArchivesRelativeTo(connHandle,top,existingFiles,countOnly=False):
    _files = []
    if (not isinstance(existingFiles,list)):
	existingFiles = []
    _fDict = dict([(f,f) for f in existingFiles])
    _xml = listItemToXML(top,'<list-head>')
    connHandle.server.__send__(connHandle,_xml)
    for root, dirs, files in os.walk(top, topdown=True):
	for name in files:
	    _nameLower = name.lower()
	    if ( (_nameLower.find('.exe') > -1) or (_nameLower.find('.pkg') > -1) ):
		_fname = os.sep.join([t for t in os.path.join(root, name).split(os.sep) if len(t) > 0])
		_fnLower = _fname.lower()
		try:
		    arch = ArchiveViewer.getArchive(_fname)
		    if (connHandle.server.isDebugging):
			print >>sys.stderr, '(listPackagesAndArchivesRelativeTo).1 :: [%s] _fname=(%s).' % (_fDict.has_key(_fnLower),str(_fname))
		    if (not _fDict.has_key(_fnLower)):
			if (countOnly == False):
			    _xml = listItemToXML(_fname)
			    connHandle.server.__send__(connHandle,_xml)
			else:
			    _files.append(_fname)
			_fDict[_fnLower] = _fname
		except Exception, details:
		    if (connHandle.server.isDebugging):
			print >>sys.stderr, '(listPackagesAndArchivesRelativeTo).ERROR :: Reason "%s".' % (str(details))
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

def removeFilesFrom(folder,pattern=None):
    try:
	_trashFiles = os.listdir(folder)
	print '(removeFilesFrom).1 :: _trashFiles=(%s)' % (_trashFiles)
	for f in _trashFiles:
	    isOkayToDelete = True
	    if (isinstance(pattern,str)):
		isOkayToDelete = (f.index(pattern) > -1)
	    _fname = os.path.join([folder,f])
	    print '(removeFilesFrom).2 :: isOkayToDelete=(%s), _fname=(%s)' % (isOkayToDelete,_fname)
	    if (isOkayToDelete):
		os.remove(_fname)
    except:
	pass

# +++ make a function export from a toc.data to files and get back a list of tuples that contain the toc after the contents has been spread-out.
def exportContentsFromArchive(arch):
    _toc = Build.TOC()
    print '(exportContentsFromArchive).1 :: arch.__class__=(%s)' % (str(arch.__class__))
    if (isinstance(arch,carchive.CArchive)):
	folder = tempfile.mkdtemp()
	print '(exportContentsFromArchive).2 :: folder=(%s)' % (folder)
	ndx = 0
	for t in arch.toc.data:
	    dpos, dlen, ulen, flag, typcd, nm = t[:6]
	    fHand = open(os.sep.join([folder,nm]),'wb')
	    print '(exportContentsFromArchive).3 :: fHand.name=(%s)' % (fHand.name)
	    x, data = arch.extract(ndx)
	    fHand.write(data)
	    fHand.flush()
	    fHand.close()
	    entry = (os.path.basename(fHand.name), fHand.name, Build.UNCOMPRESSED, xformdict.get(typcd,'b'))
	    _toc.append(entry)
	    ndx += 1
    print '(exportContentsFromArchive).9 :: [%s] tocData=(%s)' % (str(arch.toc.data.__class__),str(arch.toc.data))
    return _toc

def removePackageFromNamedArchive(archName,pkgName,pkgPos):
    # Process:
    #    Read the TOC.
    #    Remove the pkgName from the TOC.
    #    Export all the remaining items from the Archive.
    #    Build a new Archive using the remaining items now on disk.
    #    t=((0, 283664, 283664, 0, 'a', 'tk.pkg')) <-- arch.toc items look like this !
    if (os.path.exists(archName)):
	arch = ArchiveViewer.getArchive(archName)
	ndx = -1 if (len(pkgName) == 0) else arch.toc.find(pkgName)
	if (ndx > -1):
	    tempPath = tempfile.mkdtemp()
	    print '(removePackageFromNamedArchive) :: tempPath=(%s)' % (tempPath)
	    _pkgName = pkgName.lower()
	    _toc = [t for t in arch.toc if str(t[-1]).lower() != _pkgName]
	    _fdict = {}
	    i = 0
	    _newTOC = []
	    for t in _toc:
		fHand = open(os.sep.join([tempPath,t[-1]]),'wb')
		print '\t fHand.name=(%s), %s' % (fHand.name,t)
		_fdict[fHand.name] = t
		x, data = arch.extract(i)
		fHand.write(data)
		fHand.flush()
		fHand.close()
		_newTOC.append((os.path.basename(fHand.name), t[-1], 'DATA')) # +++ might need to replicate the actual build processing here...
		i += 1
	    # Build the EXE using the TOC and the files from _fdict - make the TOC using the same pattern already being used when packages are built.
	    try:
		Build.BUILDPATH = os.path.dirname(archName)
		_toks = os.path.basename(archName).split('.')
		_newArchName = os.sep.join([os.path.dirname(archName),'.'.join([_toks[0]+'_new',_toks[-1]])])
		print >>sys.stderr, '\t\tBuild.BUILDPATH=(%s)' % (Build.BUILDPATH)
		print >>sys.stderr, '\t\t_newArchName=(%s)' % (_newArchName)
		_arch = Build.ELFEXE(_newTOC, name=_newArchName, exclude_binaries=0)
		_isArchive = isValidPackage(_newArchName)
		print >>sys.stderr, '\t\t_isArchive=(%s)' % (_isArchive)
	    except Exception, details:
		_traceBack = traceback.format_exc()
		print >>sys.stderr, '\n(XMLProcessor.processXML.removePackageFromNamedArchive).ERROR :: Reason "%s".' % (str(details))
		print >>sys.stderr, _traceBack
	    removeFilesFrom(tempPath)
	    os.rmdir(tempPath)
    else:
	return (-1,'Invalid archive name.')
    return (-1,'UNKNOWN ERROR')

def isValidPackage(fname):
    _isPkg = False
    try:
	ArchiveViewer.getArchive(fname)
	_isPkg = True
    except:
	pass
    return _isPkg

class XMLProcessor:
    def __init__(self):
	self.callBack = DummyCallBack
	self.__isPsyco = _isPsyco
	self.__isLicensed = LicenseLevels.TRIAL
	self.__persistDbName = 'persist.dbx'
	self.__connHandle = None
    
    def set_connHandle(self,cHandle):
	self.__connHandle = cHandle
    
    def get_connHandle(self):
	return self.__connHandle

    def set_persistDbName(self,fname):
	self.__persistDbName = fname
    
    def get_persistDbName(self):
	return self.__persistDbName

    def set_isPsyco(self,bool):
	self.__isPsyco = bool
    
    def get_isPsyco(self):
	return self.__isPsyco

    def set_isLicensed(self,level):
	if (level in [n[1] for n in LicenseLevels]):
	    self.__isLicensed = level
    
    def get_isLicensed(self):
	return self.__isLicensed

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
	    _toc = arch.toc.data
	    if (len(_toc) == 0):
		_emptyLine = []
		_emptyLine.append('NO PACKAGES')
		lines.append(','.join(_emptyLine))
	    else:
		lines.append('pos,length,uncompressed,iscompressed,type,name'.split(','))
		for t in _toc:
		    l = [x for x in str(t)[1:-1].split(',') if len(x.strip())>0]
		    l[-2] = l[-2].replace("'",'')
		    l[-1] = l[-1].replace("'",'')
		    lines.append(l)
	except Exception, details:
	    print >>sys.stderr, '(linesFromArchive).ERROR due to "%s".' % str(details)
	    print >>sys.stderr, traceback.format_exc()
	if (self.connHandle.server.isDebugging):
	    print >>sys.stderr, '(linesFromArchive) lines=(%s).' % str(lines)
	return lines
    
    def __readPersistentList(self,typName):
	db = dbhash.open(self.persistDbName,'c')
	typName = str(FileTypes(FileTypes.PKG)).split('.')[-1] if not isinstance(typName,str) else typName
	_files = (db[typName] if db.has_key(typName) else '').split(',')
	_filesDirty = False
	if (self.connHandle.server.isDebugging):
	    print >>sys.stderr, '(readPersistentList[%s]).(%s) :: _files=(%s)' % (typName,self.persistDbName,str(_files))
	_fDict = {}
	for f in _files:
	    _fn = os.sep.join([t for t in str(f).split(os.sep) if len(t) > 0])
	    _fnLower = _fn.lower()
	    if (os.path.exists(_fn) == False):
		_filesDirty = True
	    elif (_fDict.has_key(_fnLower) == False):
		_fDict[_fnLower] = _fn
	if (_filesDirty):
	    db[typName] = ','.join(_fDict.values())
	db.close()
	return _fDict.keys()

    def __writePersistentList(self,_files,typName):
	db = dbhash.open(self.persistDbName,'c')
	typName = str(FileTypes(FileTypes.PKG)).split('.')[-1] if not isinstance(typName,str) else typName
	if (isinstance(_files,list)):
	    if (self.connHandle.server.isDebugging):
		print >>sys.stderr, '(writePersistentList[%s]).(%s) :: _files=(%s)' % (typName,self.persistDbName,_files)
	    _fDict = {}
	    for f in _files:
		_fn = os.sep.join([t for t in str(f).split(os.sep) if len(t) > 0])
		_fnLower = _fn.lower()
		if (_fDict.has_key(_fnLower) == False):
		    _fDict[_fnLower] = _fn
	    db[typName] = ','.join(_fDict.values())
	else:
	    print >>sys.stderr, '(writePersistentList[%s]).WARNING :: _files is an instance of "%s" but it needs to be an instance of "list".' % (typName,type(_files))
	db.close()
    
    def readPersistentPackagesList(self):
	return self.__readPersistentList(str(FileTypes(FileTypes.PKG)).split('.')[-1])

    def writePersistentPackagesList(self,_files):
	self.__writePersistentList(_files,str(FileTypes(FileTypes.PKG)).split('.')[-1])
    
    def readPersistentArchivesList(self):
	return self.__readPersistentList(str(FileTypes(FileTypes.EXE)).split('.')[-1])

    def writePersistentArchivesList(self,_files):
	self.__writePersistentList(_files,str(FileTypes(FileTypes.EXE)).split('.')[-1])
    
    def processXML(self,connHandle,data):
	self.connHandle = connHandle
	print >>sys.stderr, '(XMLProcessor.processXML) :: data=(%s), data.__class__=(%s)' % (str(data),str(data.__class__))
	try:
	    if (len(data) > 0):
		docs = [parseString(d) for d in data.split('\x00')]
		for doc in docs:
		    cmds = doc.getElementsByTagName("command")
		    argVal = ''
		    print >>sys.stderr, 'cmds=(%s)' % str(cmds)
		    for c in cmds:
			_cmd = self.getText(c.childNodes)
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
			    if ( (Commands(_cmd) == Commands(Commands.list_archives)) or (Commands(_cmd) == Commands(Commands.count_archives)) ):
				_path = os.path.abspath(os.curdir if len(argVal) == 0 else os.sep.join([t for t in str(argVal[0]).lower().split(os.sep) if len(t) > 0]))
				print >>sys.stderr, 'LIST ARCHIVES, _path=(%s)' % str(_path)
				_countOnly = True if (Commands(_cmd) == Commands(Commands.count_archives)) else False
				_files = self.readPersistentPackagesList()
				files = listPackagesAndArchivesRelativeTo(connHandle,_path,_files,_countOnly)
				_fDict = {}
				for f in files:
				    if (_fDict.has_key(f) == False):
					_fDict[f] = f
				for f in _files:
				    if (_fDict.has_key(f) == False):
					_fDict[f] = f
				files = _fDict.keys()
				files.sort()
				_xml = '<null></null>'
				if (_countOnly):
				    _xml = dataToXML(len(files),str(Commands(_cmd)).split('.')[-1])
				elif (len(files) > 0):
				    _xml = self.listToXML(files)
				return (_xml,_cmd)
			    elif (Commands(_cmd) == Commands(Commands.open_archive)):
				lines = []
				try:
				    _fn = os.sep.join([t for t in str(argVal[0]).split(os.sep) if len(t) > 0])
				    arch = ArchiveViewer.getArchive(_fn)
				    lines = self.linesFromArchive(arch,_fn,_open_archive_file_types)
				    print >>sys.stderr, 'OPEN ARCHIVE, arch=(%s)' % str(arch)
				    print >>sys.stderr, '"%s" lines' % (len(lines))
				    _xml = self.listToXML(lines,ListToXMLOptions.isCSV)
				except Exception, details:
				    _title = 'Programming Error'
				    errCode = '(%s).ERROR in OPEN ARCHIVE due to "%s".' % (_cmd,str(details))
				    print >>sys.stderr, errCode
				    _traceBack = traceback.format_exc()
				    print >>sys.stderr, _traceBack
				    return ('<error><title>%s</title><details>%s, %s</details></error>' % (_title,_details,_traceBack),str(_cmd))
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
					_title = 'Programming Error'
					errCode,details = retVal
					print >>sys.stderr, '(XMLProcessor.processXML).ERROR due to "%s" from exportPackageFromNamedArchive().' % (details)
					return ('<error><title>%s</title><details>%s</details></error>' % (_title,_details),str(_cmd))
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
				    _xml = self.listToXML(list(stats),ListToXMLOptions.isCSV)
				    _arch.lib.close()
				    return (_xml,_cmd)
				else:
				    _title = 'Programming Error'
				    errCode,details = retVal
				    print >>sys.stderr, '(XMLProcessor.processXML).ERROR in EXPORT PACKAGE due to "%s" from exportPackageFromNamedArchive().' % (details)
				    return ('<error><title>%s</title><details>%s</details></error>' % (_title,_details),str(_cmd))
			    elif (Commands(_cmd) == Commands(Commands.remove_package_from)):
				archName,pkgName,pkgPos = argVal
				print >>sys.stderr, 'REMOVE PACKAGE FROM, archName=(%s), pkgName=(%s), pkgPos=(%s)' % (archName,pkgName,pkgPos)
				retVal = removePackageFromNamedArchive(archName,pkgName,pkgPos)
				print >>sys.stderr, '\tretVal=(%s)' % (str(retVal))
				return (_cmd,_cmd)
			    elif (Commands(_cmd) == Commands(Commands.build_archive)):
				print >>sys.stderr, 'BUILD ARCHIVE, argVal=(%s)' % (str(argVal))
				_archName = argVal[0]
				_archLimit = int(argVal[1])
				_pkgFiles = argVal[2:][0].split(',')
				print >>sys.stderr, '\t\t_pkgName=(%s)' % (_archName)
				print >>sys.stderr, '\t\t_pkgFiles=(%s)' % (_pkgFiles)
				print >>sys.stderr, '\t\t_pkgLimit=(%s)' % (_archLimit)
				_files = self.readPersistentArchivesList()
				print >>sys.stderr, '\t\tlen(_files)=(%s)' % (len(_files))
				_curDir = os.path.abspath(os.path.curdir)
				_template = os.sep.join([_curDir,'archiveTemplate.spec'])
				_archiveSpec = os.sep.join([_curDir,'archiveSpec.txt'])
				_archiveTemplate = os.sep.join([_curDir,'archive-template.dat'])
				print >>sys.stderr, '\t\t_curDir=(%s)' % (_curDir)
				print >>sys.stderr, '\t\t[%s] (%s)' % (_template,os.path.exists(_template))
				print >>sys.stderr, '\t\t[%s] (%s)' % (_archiveTemplate,os.path.exists(_archiveTemplate))
				if ( os.path.exists(_template) and os.path.exists(_archiveTemplate) and os.path.exists(_archiveSpec) ):
				    if ( (isinstance(_pkgFiles,list)) and (len(_pkgFiles) > 0) ):
					if ( (_archLimit == -1) or (len(_files) < _archLimit) ):
					    _isPkg = False
					    _lines = []
					    _lines.append("buildPath = '%s'\n" % _curDir.replace('\\\\','/').replace('\\','/'))
					    _toc = ["('%s', '%s', 'DATA')" % (os.path.basename(f),f.replace('\\\\','/').replace('\\','/')) for f in _pkgFiles]
					    _lines.append("toc1 = [%s]\n" % ','.join(_toc))
					    _lines.append("useConsole = True\n")
					    _lines.append("useShelved = True\n")
					    _lines.append("shelvedFname = '%s'\n" % _archiveTemplate.replace('\\\\','/').replace('\\','/'))
					    _lines.append("exeName = '%s'\n" % _archName.replace('\\\\','/').replace('\\','/'))
    
					    fHand = open(_archiveSpec,'w')
					    fHand.writelines(_lines)
					    fHand.flush()
					    fHand.close()
					    try:
						print >>sys.stderr, '\t\tBuild _template=(%s)' % (_template)
						_pkg = Build.build(_template)

						print >>sys.stderr, '\t\tBuild.HOMEPATH=(%s)' % (Build.HOMEPATH)
						print >>sys.stderr, '\t\tBuild.SPECPATH=(%s)' % (Build.SPECPATH)
						print >>sys.stderr, '\t\tBuild.BUILDPATH=(%s)' % (Build.BUILDPATH)
						print >>sys.stderr, '\t\tBuild.WARNFILE=(%s)' % (Build.WARNFILE)
						
						_isPkg = isValidPackage(_archName)
						
						if (0):
						    _fname = os.path.join(os.path.dirname(_archName),'out0.toc')
						    if (os.path.exists(_fname)):
							os.remove(_fname)
						    _fname = os.path.join(os.path.dirname(_archName),'out1.toc')
						    if (os.path.exists(_fname)):
							os.remove(_fname)
						    _fname = os.path.join(os.path.dirname(_archName),'out1.pkg')
						    if (os.path.exists(_fname)):
							os.remove(_fname)

						if (_isPkg):
						    _files.append(_archName)
						    self.writePersistentArchivesList(_files)
					    except Exception, details:
						_title = 'ERROR :: Runtime Error in "%s".' % Commands(_cmd)
						_traceBack = traceback.format_exc()
						_details = '%s\n\n%s' % (str(details),_traceBack)
						print >>sys.stderr, '(XMLProcessor.processXML).ERROR due to "%s".' % (_details)
						return ('<error><title>%s</title><details>%s</details></error>' % (_title,_details),str(_cmd))
					    
					    print >>sys.stderr, '\t\t_isPkg=(%s)' % (_isPkg)
					    _xml = dataToXML(_isPkg,argVal[0])
					    _cmd = str(_cmd)
					    return (_xml,_cmd)
					else:
					    _title = 'WARNING :: Time to Upgrade your License'
					    _details = 'Licensed Limit has been reached.\n\nYour License allows you to create no more than "%s" Archives and you have already created "%s".\n\nPlease upgrade your License to continue.' % (_archLimit,len(_files))
					    print >>sys.stderr, '(XMLProcessor.processXML).ERROR due to "%s".' % (_details)
					    return ('<error><title>%s</title><details>%s</details></error>' % (_title,_details),str(_cmd))
				    else:
					_title = 'Programming Error'
					_details = 'Invalid list of files when attempting to make a New Archive.\n\nThis is a programming error.\n\nPlease report this error to the folks who produce this product.'
					print >>sys.stderr, '(XMLProcessor.processXML).ERROR due to "%s".' % (_details)
					return ('<error><title>%s</title><details>%s</details></error>' % (_title,_details),str(_cmd))
				else:
				    _title = 'Runtime Error'
				    _details = 'Unable to locate the file named "%s" and/or "%s".\n\nThis is a serious error.\n\nPlease reinstall this product or report this error to the folks who produce this product.' % (_template,_archiveTemplate)
				    print >>sys.stderr, '(XMLProcessor.processXML).ERROR due to "%s".' % (_details)
				    return ('<error><title>%s</title><details>%s</details></error>' % (_title,_details),str(_cmd))
			    elif (Commands(_cmd) == Commands(Commands.check_package_name)):
				_isPkg = False
				if (os.path.exists(argVal[0])):
				    try:
					arch = ArchiveViewer.getArchive(argVal[0])
					_isPkg = True
				    except Exception, details:
					print >>sys.stderr, '(XMLProcessor.processXML).ERROR :: Reason "%s".' % (str(details))
				_xml = dataToXML(_isPkg,argVal[0])
				print >>sys.stderr, 'CHECK PACKAGE NAME, [%s] argVal=(%s)' % (_isPkg,str(argVal))
				print >>sys.stderr, '\t\t_xml=(%s)' % (_xml)
				_cmd = str(_cmd)
				return (_xml,_cmd)
			    elif (Commands(_cmd) == Commands(Commands.build_package)):
				print >>sys.stderr, 'BUILD PACKAGE, argVal=(%s)' % (str(argVal))
				_pkgName = argVal[0]
				_pkgLimit = int(argVal[1])
				_pkgFiles = argVal[2:][0].split(',')
				print >>sys.stderr, '\t\t_pkgName=(%s)' % (_pkgName)
				print >>sys.stderr, '\t\t_pkgFiles=(%s)' % (_pkgFiles)
				print >>sys.stderr, '\t\t_pkgLimit=(%s)' % (_pkgLimit)
				_files = self.readPersistentPackagesList()
				print >>sys.stderr, '\t\tlen(_files)=(%s)' % (len(_files))
				if ( (isinstance(_pkgFiles,list)) and (len(_pkgFiles) > 0) ):
				    if ( (_pkgLimit == -1) or (len(_files) < _pkgLimit) ):
					_toc = [] # Build.TOC()
					for f in _pkgFiles:
					    _toc.append((os.path.basename(f), f, 'DATA'))
					_isPkg = False
					try:
					    Build.BUILDPATH = os.path.dirname(_pkgName)
					    print >>sys.stderr, '\t\tBuild.BUILDPATH=(%s)' % (Build.BUILDPATH)
					    print >>sys.stderr, '\t\t_toc=(%s)' % (_toc)
					    _pkg = Build.PKG(_toc, name=_pkgName, exclude_binaries=0)
					    _isPkg = isValidPackage(_pkgName)
					    os.remove(os.path.join(os.path.dirname(_pkgName),'out0.toc'))
					    if (_isPkg):
						_files.append(_pkgName)
						self.writePersistentPackagesList(_files)
					except Exception, details:
					    _traceBack = traceback.format_exc()
					    print >>sys.stderr, '\n(XMLProcessor.processXML.%s).ERROR :: Reason "%s".' % (Commands(_cmd),str(details))
					    print >>sys.stderr, _traceBack
					print >>sys.stderr, '\n\t\t_toc=(%s)' % (_toc)
					print >>sys.stderr, '\t\t_isPkg=(%s)' % (_isPkg)
					_xml = dataToXML(_isPkg,argVal[0])
					_cmd = str(_cmd)
					return (_xml,_cmd)
				    else:
					_title = 'WARNING :: Time to Upgrade your License'
					_details = 'Licensed Limit has been reached.\n\nYour License allows you to create no more than "%s" Packages and you have already created "%s".\n\nPlease upgrade your License to continue.' % (_pkgLimit,len(_files))
					print >>sys.stderr, '(XMLProcessor.processXML).ERROR due to "%s".' % (_details)
					return ('<error><title>%s</title><details>%s</details></error>' % (_title,_details),str(_cmd))
				else:
				    _title = 'Programming Error'
				    _details = 'Invalid list of files when attempting to make a New Package.\n\nThis is a programming error.\n\nPlease report this error to the folks who produce this product.'
				    print >>sys.stderr, '(XMLProcessor.processXML).ERROR due to "%s".' % (_details)
				    return ('<error><title>%s</title><details>%s</details></error>' % (_title,_details),str(_cmd))
			    else:
				_cmd = str(_cmd)
				return (_cmd,_cmd)
			else:
			    _title = 'Programming Error'
			    _details = 'Invalid command valud of "%s".' % str(_cmd)
			    print >>sys.stderr, '(XMLProcessor.processXML).ERROR due to "%s".' % (_details)
			    return ('<error><title>%s</title><details>%s</details></error>' % (_title,_details),str(_cmd))
			print >>sys.stderr, '\n'
	except Exception, details:
	    _title = 'Exception'
	    _details = 'parsing error due to "%s".' % str(details)
	    print >>sys.stderr, _details
	    _traceBack = traceback.format_exc()
	    print >>sys.stderr, _traceBack
	    return ('<error><title>%s</title><details>%s, %s</details></error>' % (_title,_details,_traceBack),str(_cmd))

    isPsyco = property(get_isPsyco, set_isPsyco)
    isLicensed = property(get_isLicensed, set_isLicensed)
    persistDbName = property(get_persistDbName, set_persistDbName)
    connHandle = property(get_connHandle, set_connHandle)
