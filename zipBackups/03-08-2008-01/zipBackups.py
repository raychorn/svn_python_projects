import os
import sys
import psyco
import pyodbc
from vyperlogix import _pyodbc
from vyperlogix import readYML
import threading
import win32api
import win32con
import zipfile
from vyperlogix import msiMaker
from vyperlogix.oodb import Enum
import traceback
import datetime
import zlib
import tempfile
import time
import decimal

_isVerbose = False
_isIgnoreSVN = False

_programName = ''
_yml_filename = '.yml'

_zipFileName = ''

_theFiles = []

_zippedFiles = []

class HelpReasons(Enum):
	noReason = 0
	missingZipFile = 1

class ZipMethods(Enum):
	zip = 0
	zlib = 1
	
_zipMethod = ZipMethods.zip

def zipUpFile(aZipFile,src,dst):
	try:
		_zippedFiles.append((src,dst))

		if (ZipMethods(_zipMethod) == ZipMethods(ZipMethods.zip)):
			print 'Writing #%s... "%s" as "%s"' % (len(_zippedFiles),src,dst)
			aZipFile.write( src, dst, zipfile.ZIP_DEFLATED)
		elif (ZipMethods(_zipMethod) == ZipMethods(ZipMethods.zlib)):
			isError = True
			outdata = ''
			try:
				outdata = zlib.compress(open(src, "rb").read(), zlib.Z_BEST_COMPRESSION)
				isError = False
			except:
				try:
					outdata = zlib.compress(open(src, "rb").read(), zlib.Z_BEST_SPEED)
					isError = False
				except:
					try:
						outdata = zlib.compress(open(src, "rb").read(), zlib.Z_DEFAULT_COMPRESSION)
						isError = False
					except:
						aZipFile.write( src, dst, zipfile.ZIP_DEFLATED)
			if (not isError):
				aFolder = tempfile.mkdtemp()
				aFile = open(os.sep.join([aFolder,tempfile.TemporaryFile('w').name.split(os.sep)[-1]]),'wb')
				aFile.write(outdata)
				aFile.flush()
				aFile.close()
				print 'Writing #%s... "%s"' % (len(_zippedFiles),dst)
				aZipFile.write( aFile.name, dst, zipfile.ZIP_STORED)
				os.remove(aFile.name)
				os.rmdir(aFolder)
			else:
				print 'Unable to compress and store "%s".' % dst

	except Exception, details:
		_traceBack = traceback.format_exc()
		print >>sys.stderr, '(zipUpFile).ERROR :: "%s".' % (str(details))
		print >>sys.stderr, _traceBack

def zipFiles(top,target,_mode,_excl,_incl):
	_allowedModes = ['a','w']
	if (_mode in _allowedModes):
		print '(zipFiles) :: _excl=(%s)' % (_excl)
		myZipFile = zipfile.ZipFile(_zipFileName, _mode)
		try:
			_svn = '%s.svn%s' % (os.sep,os.sep)
			for root, dirs, files in os.walk(top):
				isRootOk = True
				bool = (root.find(_svn) > -1)
				if ( (_isIgnoreSVN) and (bool) ):
					isRootOk = False
				else:
					try:
						for e in _excl:
							_e = (top+os.sep+e).replace(os.sep+os.sep,os.sep)
							isRootOk = (root.startswith(_e) == False)
							if (isRootOk == False):
								break
					except:
						pass
				if (isRootOk):
					_files = files
					_suspects = []
					for i in _incl:
						iDir = os.path.dirname(i)
						if (root.endswith(iDir)):
							_suspects.append(os.path.basename(i))
					if (len(_suspects) > 0):
						_files = _suspects
					for f in _files:
						isPathOk = True
						_f = root+os.sep+f
						bool = (_f.find(_svn) > -1)
						if ( (_isIgnoreSVN) and (bool) ):
							isPathOk = False
						if (isPathOk):
							if (isinstance(target,str)):
								_z = _f.replace(top,target)
							else:
								_z = _f
							zipUpFile(myZipFile,_f, _z)
		except Exception, details:
			_traceBack = traceback.format_exc()
			print >>sys.stderr, '(zipFiles).ERROR :: "%s".' % (str(details))
			print >>sys.stderr, _traceBack
		myZipFile.close()
	else:
		print '(zipFiles).WARNING :: Invalid mode given "%s", must be one of "%s".' % (_mode,str(_allowedModes))

def reportTime(seconds):
	_d = seconds / (60 * 60)
	_hours = int(_d)
	seconds = seconds - (_hours * (60 * 60))
	_d = seconds / 60
	_mins = int(_d)
	_secs = seconds - (_mins * 60)
	print '(reportTime) :: %02d:%02d:%02d (hh:mm:ss)' % (_hours,_mins,_secs)

def main(specs,files):
	print '(main).1 :: specs=(%s), files=(%s)' % (specs,files)
	if (os.path.exists(_zipFileName)):
		os.remove(_zipFileName)
	_mode = "w"
	incl = []
	if (isinstance(files,list)):
		for y in files:
			toks = y.value.split(',')
			top = toks[0]
			if (top.endswith(os.sep) == False):
				top += os.sep
			if (len(toks) > 1):
				incl = [top+i for i in (','.join(toks[1:]).replace('+','').replace('[','').replace(']','').split(','))]
			print '(main) :: y=(%s), top=(%s), incl=(%s)' % (str(y),top,incl)
	elif (_isVerbose):
			print '(main) :: Missing files which is (%s).' % str(files)
	if (isinstance(specs,list)):
		for y in specs:
			toks = y.value.split(',')
			dest = toks[0]
			try:
				src = toks[1]
			except:
				src = dest
				dest = None
			excl = []
			if (len(toks) > 2):
				excl = ','.join(toks[2:]).replace('-','').replace('[','').replace(']','').split(',')
			print '(main) :: y=(%s), src=(%s), dest=(%s), excl=(%s)' % (str(y),src,dest,excl)
			_beginTime = datetime.datetime.now()
			zipFiles(src,dest,_mode,excl,incl)
			_endTime = datetime.datetime.now()
			_elapsedTime = _endTime - _beginTime
			print '(main) :: Elapsed seconds=(%s)' % (_elapsedTime.seconds)
			reportTime(_elapsedTime.seconds)
			_mode = "a"
	elif (_isVerbose):
			print '(main) :: Missing specs which is (%s).' % str(specs)
	print '(main) :: Waiting for threads to complete.'

def readYMLFile(fname):
	cName,yml,_sourceSpecs,_sourceFiles = [None,None,None,None]
	print '(readYMLFile) :: fname=(%s)' % fname
	if (os.path.exists(fname)):
		ymlReader = readYML.ymlReader(fname)
		ymlReader.read()
		cName = win32api.GetComputerName()
		try:
			n = 'source_%s' % cName
			print '(readYMLFile) :: n=(%s)' % n
			yml = ymlReader.objectsNamed(n)
			_sourceSpecs = (yml[0]).attrsForName('folder')
			print '(readYMLFile) :: n=(%s), _sourceSpecs=(%s)' % (n,_sourceSpecs)
			_sourceFiles = (yml[0]).attrsForName('files')
			print '(readYMLFile) :: n=(%s), _sourceFiles=(%s)' % (n,_sourceFiles)
		except Exception, details:
			print '(ymlReader).ERROR_READING_YML_FILE :: "%s". Did you remember to put a definition in for the current computer you are running on, named "%s".' % (str(details),cName)
	return (cName,yml,_sourceSpecs,_sourceFiles)

def notifyProgramOptions(reason=None):
	print 'Something may be missing from the arguments used.\n'
	if ( (not reason) or (HelpReasons(reason) == HelpReasons(HelpReasons.noReason)) ):
		print '\t--help                      ... displays this help text.'
	if ( (not reason) or (HelpReasons(reason) == HelpReasons(HelpReasons.noReason)) ):
		print '\t--verbose                   ... output more stuff.'
	if ( (not reason) or (HelpReasons(reason) == HelpReasons(HelpReasons.noReason)) ):
		print '\t--ignoreSVN                 ... ignore any path that refers to ".svn".'
	if ( (not reason) or (HelpReasons(reason) == HelpReasons(HelpReasons.noReason)) ):
		print '\t--yml=yml_filename          ... yml file name.'
	if ( (not reason) or (HelpReasons(reason) == HelpReasons(HelpReasons.noReason)) or (HelpReasons(reason) == HelpReasons(HelpReasons.missingZipFile)) ):
		print '\t--zip=zip_filename          ... zip file name.'
		print '\t--useZIP                    ... use ZIP compression method. (default)'
		print '\t--useZLIB                   ... use ZLIB compression method.'

try:
	if ( (len(sys.argv) == 1) and (sys.argv[1] == '--help') ):
		notifyProgramOptions()
except:
	pass

_sourceSpecs = []
toks = sys.argv[0].split(os.sep)
_programName = toks[-1]
_yml_filename = '.'.join([_programName.split('.')[0],_yml_filename.split('.')[-1]])
print '(%s) :: _yml_filename=(%s)' % (__name__,_yml_filename)
cName,yml,_sourceSpecs,_sourceFiles = readYMLFile(_yml_filename)[:4]
for i in xrange(len(sys.argv)):
	bool = ( (sys.argv[i].find('--yml=') > -1) or (sys.argv[i].find('--zip=') > -1) )
	if (bool): 
		toks = sys.argv[i].split('=')
		if (sys.argv[i].find('--yml=') > -1):
			_yml_filename = toks[1]
			cName,yml,_sourceSpecs,_sourceFiles = readYMLFile(_yml_filename)[:4]
		elif (sys.argv[i].find('--zip=') > -1):
			_toks = toks[1].split('.')
			_toks[0] += time.strftime("_%m-%d-%Y_%H-%M-%S", time.localtime())
			_zipFileName = '.'.join(_toks)
	elif (sys.argv[i].find('--verbose') > -1):
		_isVerbose = True
	elif (sys.argv[i].find('--ignoreSVN') > -1):
		_isIgnoreSVN = True
	elif (sys.argv[i].find('--useZIP') > -1):
		_zipMethod = ZipMethods.zip
	elif (sys.argv[i].find('--useZLIB') > -1):
		_zipMethod = ZipMethods.zlib
psyco.bind(main)
_zipMethod = ZipMethods.zip
if (len(_zipFileName) > 0):
	main(_sourceSpecs,_sourceFiles)
else:
	notifyProgramOptions(HelpReasons.missingZipFile)
sys.exit(-1)

