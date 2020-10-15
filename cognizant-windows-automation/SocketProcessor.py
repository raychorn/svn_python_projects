from xml.dom.minidom import parseString
import os
import sys
import shutil
from vyperlogix.misc import decodeUnicode
import time
import traceback
import dbhash
from vyperlogix.sockets import ConnectionHandle
from vyperlogix.enum import Enum

try:
    import zlib
except ImportError:
    zlib = archive.DummyZlib()
import tempfile

def DummyCallBack(data, cmd):
    pass

class Commands(Enum.Enum):
    SHUTDOWN = 999

class LicenseLevels(Enum.Enum):
    TRIAL = 1
    STANDARD = 2
    PRO = 3
    ENTERPRISE = 4

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

class Processor:
    def __init__(self):
	self.callBack = DummyCallBack
	self.__isLicensed = LicenseLevels.TRIAL
	self.__connHandle = None
    
    def set_connHandle(self,cHandle):
	self.__connHandle = cHandle
    
    def get_connHandle(self):
	return self.__connHandle

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
		print >>sys.stderr, '(Processor.callback) :: code=(%s)' % (code)
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

    def process(self,connHandle,data):
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
			    pass # ???
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
    connHandle = property(get_connHandle, set_connHandle)
