from lib.oodb import Enum
from xml.dom.minidom import parseString
import os
import sys
import shutil
from lib import decodeUnicode
import time
import traceback
import dbhash
from lib import ConnectionHandle
from lib import shelved

def DummyCallBack(data, cmd):
    pass

class Commands(Enum):
    SHUTDOWN = 999

class LicenseLevels(Enum):
    TRIAL = 1
    STANDARD = 2
    PRO = 3
    ENTERPRISE = 4

class ListToXMLOptions(Enum):
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

class XMLProcessor:
    def __init__(self):
	self.callBack = DummyCallBack
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
			    elif (Commands(_cmd) == Commands(Commands.remove_package_from)):
				archName,pkgName,pkgPos = argVal
				print >>sys.stderr, 'REMOVE PACKAGE FROM, archName=(%s), pkgName=(%s), pkgPos=(%s)' % (archName,pkgName,pkgPos)
				retVal = removePackageFromNamedArchive(archName,pkgName,pkgPos)
				print >>sys.stderr, '\tretVal=(%s)' % (str(retVal))
				return (_cmd,_cmd)
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

    isLicensed = property(get_isLicensed, set_isLicensed)
    persistDbName = property(get_persistDbName, set_persistDbName)
    connHandle = property(get_connHandle, set_connHandle)
