import os
import sys
import psyco
import pyodbc
import lib.threadpool
import lib._pyodbc
import lib.readYML
import threading
import win32api
import win32con
import zipfile
import lib.msiMaker

_isVerbose = False
_isIgnoreSVN = False
_isMakingMSI = False

_programName = ''
_yml_filename = 'nightlyBuild.yml'

_pool = lib.threadpool.Pool(100)

_zipFileName = 'dss.zip'

_theFiles = []

def zipFiles(top,target,_mode,_excl,_incl):
	_allowedModes = ['a','w']
	if (_mode in _allowedModes):
		if (_isMakingMSI == False):
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
							_z = _f.replace(top,target)
							if (_isMakingMSI):
								_theFiles.append([_f, _z])
							else:
								print 'Writing... "%s" as "%s"' % (_f,_z)
								myZipFile.write( _f, _z, zipfile.ZIP_DEFLATED)
		except Exception, details:
			print '(zipFiles).ERROR :: "%s".' % (str(details))
		if (_isMakingMSI == False):
			myZipFile.close()
	else:
		print '(zipFiles).WARNING :: Invalid mode given "%s", must be one of "%s".' % (_mode,str(_allowedModes))

def main(specs,files):
	if ( (str(specs.__class__).find("'list'") > -1) and (str(files.__class__).find("'list'") > -1) ):
		if ( (_isMakingMSI == False) and (os.path.exists(_zipFileName)) ):
			os.remove(_zipFileName)
		_mode = "w"
		incl = []
		for y in files:
			toks = y.value.split(',')
			top = toks[0]
			if (top.endswith(os.sep) == False):
				top += os.sep
			if (len(toks) > 1):
				incl = [top+i for i in (','.join(toks[1:]).replace('+','').replace('[','').replace(']','').split(','))]
			print '(main) :: y=(%s), top=(%s), incl=(%s)' % (str(y),top,incl)
		for y in specs:
			toks = y.value.split(',')
			dest = toks[0]
			src = toks[1]
			excl = []
			if (len(toks) > 2):
				excl = ','.join(toks[2:]).replace('-','').replace('[','').replace(']','').split(',')
			print '(main) :: y=(%s), src=(%s), dest=(%s), excl=(%s)' % (str(y),src,dest,excl)
			zipFiles(src,dest,_mode,excl,incl)
			_mode = "a"
	else:
		print 'WARNING :: Invalid object passed in from YML file. Class is [%s] but should be "<type \'list\'>".' % (str(specs.__class__))
	if (_isMakingMSI):
		print '(main) :: _isMakingMSI=(%s), len(_theFiles)=(%s)' % (_isMakingMSI,len(_theFiles))
		msiFactory = lib.msiMaker.msiMaker('DSS','BigFix, Inc.',r'C:\ruby',"1.0.0")
		print '(main) :: msiFactory=(%s)' % (str(msiFactory))
		msiFactory.make_msi(_theFiles)
	_pool.join()

if ( (len(sys.argv) == 1) or (sys.argv[1] == '--help') ):
	print '--help                      ... displays this help text.'
	print '--verbose                   ... output more stuff.'
	print '--ignoreSVN                 ... ignore any path that refers to ".svn".'
	print '--makeMSI                   ... make MSI instead of ZIP based package.'
	print '--yml=yml_filename          ... yml file name.'
	print '--zip=zip_filename          ... zip file name.'
else:
	_sourceSpecs = []
	toks = sys.argv[0].split(os.sep)
	_programName = toks[-1]
	for i in xrange(len(sys.argv)):
		bool = ( (sys.argv[i].find('--yml=') > -1) or (sys.argv[i].find('--zip=') > -1) )
		if (bool): 
			toks = sys.argv[i].split('=')
			if (sys.argv[i].find('--yml=') > -1):
				_yml_filename = toks[1]
				ymlReader = lib.readYML.ymlReader(_yml_filename)
				ymlReader.read()
				cName = win32api.GetComputerName()
				try:
					n = 'source_%s' % cName
					yml = ymlReader.objectsNamed(n)
					_sourceSpecs = (yml[0]).attrsForName('folder')
					print '(init) :: n=(%s), _sourceSpecs=(%s)' % (n,_sourceSpecs)
					_sourceFiles = (yml[0]).attrsForName('files')
					print '(init) :: n=(%s), _sourceFiles=(%s)' % (n,_sourceFiles)
				except Exception, details:
					print '(init).ERROR_READING_YML_FILE :: "%s". Did you remember to put a definition in for the current computer you are running on, named "%s".' % (str(details),cName)
			elif (sys.argv[i].find('--zip=') > -1):
				_zipFileName = toks[1]
		elif (sys.argv[i].find('--verbose') > -1):
			_isVerbose = True
		elif (sys.argv[i].find('--ignoreSVN') > -1):
			_isIgnoreSVN = True
		elif (sys.argv[i].find('--makeMSI') > -1):
			_isMakingMSI = True
psyco.bind(main)
main(_sourceSpecs,_sourceFiles)


