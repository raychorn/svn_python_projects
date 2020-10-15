import os
import sys
import psyco
import win32api
import win32con
from lib import putStr
from lib import winreg
from pyinstaller13 import carchive
import subprocess
import Tkinter
from lib import tkMessageBox
from lib import WinProcesses
from lib import callExternalProgram
from lib import windowsShortcuts

# To-Do:
# 1). Install socket server in same folder as AIR App.
# 2). Rewrite shortcuts to launch AIR App via socket server component.

_isVerbose = False
_isUninstall = False

_const__installerStrategy_one = 1
_const__installerStrategy_two = 2
_const__installerStrategies = [str(i) for i in [_const__installerStrategy_one,_const__installerStrategy_two]]

_const_air_pkg_name = 'air.pkg'
_const_server_pkg_name = 'server.pkg'
_const_server_folder_name = 'server'
_const_server_exe_name = _const_server_folder_name+'.exe'

_installerStrategy = _const__installerStrategy_two

_original_uninstall_string = ''

_programName = ''

_rootKeyName = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'

def showValues(root):
    d = {}
    if (isinstance(root, winreg.Key)):
	try:
	    print '(showValues) :: root.__class__=(%s)' % str(root.__class__)
	    vals = root.values
	    print '(showValues) :: vals=(%s) has (%s) items.' % (str(vals),len(vals))
	    for v in vals:
		print '(showValues) :: (%s)=(%s)' % (str(v),vals[v])
		d[str(v)] = vals[v]
	except:
	    pass
    return d

def getAIRVersionFrom(root):
    if (isinstance(root, winreg.Key)):
	_vers = None
	toks = []
	num = -1
	try:
	    _vers = root.values['DisplayVersion'].value
	    toks = _vers.split('.')
	    mask = 10**(len(toks)-2)
	    i = 0
	    num = 0
	    for i in xrange(len(toks)-1):
		try:
		    num += (mask * int(toks[i]))
		    mask = mask / 10
		except:
		    break
	except Exception, details:
	    print '(getAIRVersionFrom) :: ERROR due to "%s".' % str(details)
    return (_vers, toks, num)

def localFolderName():
    return os.environ['_MEIPASS2']

def pkgHandleByName(pkgName):
    try:
	this = carchive.CArchive(sys.executable)
	return this.openEmbedded(pkgName)
    except:
	pass
    return None

def tocFromArchiveByName(pkgName):
    try:
	return pkgHandleByName(pkgName).contents()
    except:
	pass
    return []

def extractStuffFrom(pkg,name,targetdir):
    try:
	return [pkg.extract(name)[1],os.path.join(targetdir, name)]
    except:
	pass
    return []

def writeExtractedFileToDisk(pkg,name,targetdir):
    try:
	stuff = extractStuffFrom(pkg,name,targetdir)
	if (len(stuff) > 0):
	    outnm = os.path.join(targetdir, name)
	    if (os.path.exists(outnm) == False):
		if (not os.path.exists(targetdir)):
		    os.makedirs(targetdir)
		writeExtractedStuffToDisk(stuff)
    except:
	pass

def extractAllStuffToDiskFromNamedPkg(pkgName,targetdir):
    pkg = pkgHandleByName(pkgName)
    if (pkg):
	pkgs = pkg.contents()
	for name in pkgs:
	    writeExtractedFileToDisk(pkg,name,targetdir)
# +++
def extractFromArchiveByName(name,pkgName):
    try:
	stuff = []
	outnm = ''
	pkg = pkgHandleByName(pkgName)
	targetdir = localFolderName()
	print '(extractFromArchiveByName) :: pkg=(%s)' % str(pkg)
	print '(extractFromArchiveByName) :: targetdir=(%s)' % targetdir
	pkgs = pkg.contents()
	print '(extractFromArchiveByName) :: pkgs=(%s)' % str(pkgs)
	if (name in pkgs):
	    outnm = os.path.join(targetdir, name)
	    dirnm = os.path.dirname(outnm)
	    if (os.path.exists(outnm) == False):
		if (not os.path.exists(dirnm)):
		    os.makedirs(dirnm)
		_stuff = pkg.extract(name)[1]
		stuff = [_stuff,outnm]
		print '(extractFromArchiveByName) :: Extracted (%s) "%s" bytes.' % (name,len(_stuff))
    except Exception, details:
	print >>sys.stderr, 'ERROR #200 :: Cannot retrieve package item named "%s" from "%s" due to "%s".' % (name,pkgName,str(details))
    return stuff

def writeExtractedStuffToDisk(args):
    _retCode = -1
    try:
	stuff,outnm = args
	print '(writeExtractedStuffToDisk) :: Saving  "%s" bytes into (%s)' % (len(stuff),outnm)
	fHand = open(outnm, 'wb')
	fHand.write(stuff)
	fHand.flush()
	fHand.close()
	_retCode = 0
    except Exception, details:
	print >>sys.stderr, 'ERROR #301 :: Cannot write contents for "%s" due to "%s".' % (outnm,str(details))
    return _retCode

def issueSysErrorByNumber(num):
    if (num in [401,402, 403, 404, 405, 406, 407]):
	if (num in [401,402, 405]):
	    _errMsg = 'ERROR #%s :: Cannot install Adobe AIR Runtime due to some kind of system error.\nDownload and install the latest Adobe AIR Runtime from http://www.adobe.com and then return to try to run this program again.' % num
	elif (num in [403]):
	    _errMsg = 'ERROR #%s :: Cannot install this application due to some kind of system error.\nYou may be able to get technical support online from http://www.sexyblondessoftware.com.' % num
	elif (num in [404]):
	    _errMsg = 'ERROR #%s :: Cannot launch this application due to some kind of system error.\nYou may be able to get technical support online from http://www.sexyblondessoftware.com.' % num
	elif (num in [406, 407]):
	    _errMsg = 'ERROR #%s :: Cannot launch the server for this application due to some kind of system error.\nYou may be able to get technical support online from http://www.sexyblondessoftware.com.' % num
	print >>sys.stderr, _errMsg
	_resp = tkMessageBox.askretrycancel('ERROR',_errMsg + '\n\nDo you want to try to install the Adobe AIR Runtime again or CANCEL to take care of this yourself ?')
	if (_resp != tkMessageBox.RETRY):
	    sys.exit(-1)

def getPIDforNamedProcess(name):
    _pid = -1
    try:
	_win_proc = WinProcesses.WinProcesses()
	_pid = _win_proc.getProcessIdByName(name)
    except:
	pass
    return _pid

def locateAIRAppShortcuts(likeName):
    _report = []
    root = localFolderName()
    toks = root.split('/')
    while (len(toks) > 2):
	toks.pop()
    _root = os.sep.join(toks)
    _likeName = os.sep + likeName
    for root, dirs, files in os.walk(_root):
	for f in files:
	    if (f.find('.lnk') > -1):
		_fname = os.sep.join([root,f])
		_path = windowsShortcuts.getPathFromShortcut(_fname)
		if (_path[0].find(_likeName) > -1):
		    _report.append([_fname,_path[0]])
    return _report

def writeServerLaunchCommandFile(serverPath,path):
    if (os.path.exists(path)):
	_pName = os.path.basename(path)
	toks = _pName.split('.')
	toks.pop()
	pName = '.'.join(toks)
	pDir = os.path.dirname(path)
	fname = os.sep.join([pDir,'Launch'+pName+'.cmd'])
	try:
	    fHand = open(fname,'w')
	    _newPath = '%s --launch="%s"' % (serverPath,path)
	    _contents = '\n'.join(['@start "%s" /b "%s"\n\n' % (pName,_newPath)])
	    fHand.writelines(_contents)
	    fHand.flush()
	    fHand.close()
	except Exception, details:
	    print '(writeServerLaunchCommandFile) :: ERROR due to "%s".' % str(details)
    return fname

def adjustAIRAppShortcuts(_paths,serverPath):
    if (isinstance(_paths, list)):
	for p in _paths:
	    if (len(p) == 2):
		_fname, _path = p
		if (_path.find(' --launch=') == -1):
		    os.remove(_fname)
		    cmdFName = writeServerLaunchCommandFile(serverPath,_path)
		    windowsShortcuts.makeWindowsShortcut(_fname,cmdFName,None,None,None)

def mainProcess():
    d = os.path.dirname(sys.executable)
    print '(main) :: d=(%s)' % str(d)
    root = winreg.get_key(winreg.HKEY.LOCAL_MACHINE, _rootKeyName, winreg.KEY.ALL_ACCESS)
    subKey = winreg.get_key(root, 'Adobe AIR', winreg.KEY.ALL_ACCESS)
    #showValues(subKey)
    _vers = getAIRVersionFrom(subKey)

    _appName_airAppInstaller = 'TwistedTest.air'
    _appRegKeyName = _appName_airAppInstaller.split('.')[0]
    _appEXEName = _appRegKeyName + '.exe'

    appSubKey = winreg.get_key(root, _appRegKeyName, winreg.KEY.ALL_ACCESS)
    dAppRegValues = showValues(appSubKey)
    
    # figure-out if there is a buildtime in the Registry for the AIR App that was previously installed.
    stuff = extractFromArchiveByName('buildtime.txt',_const_air_pkg_name)
    print '(main) :: stuff=(%s)' % (str(stuff))

    _isTimeForUninstall = True # default is to always assume there is an uninstall
    
    if (_installerStrategy == _const__installerStrategy_one):
	_thisBuildTimeSecs = 0.0
	if (len(dAppRegValues) > 0):
	    if (dAppRegValues.has_key('BuildTime')):
		_lastBuildTimeSecs = float(dAppRegValues['BuildTime'])
		if (len(stuff) > 0):
		    _thisBuildTimeSecs = float(stuff[0])
		    _isTimeForUninstall = (_thisBuildTimeSecs > _lastBuildTimeSecs) # this catches the uninstall in case there is no need to perform the uninstall at this time.
		    print '(main) :: _isTimeForUninstall=(%s), _thisBuildTimeSecs=(%s), _lastBuildTimeSecs=(%s)' % (_isTimeForUninstall,_thisBuildTimeSecs,_lastBuildTimeSecs)
    print '(main) :: _isTimeForUninstall=(%s)' % (_isTimeForUninstall)

    print '(main) :: _vers=(%s)' % str(_vers)
    if ( (_vers[-1] >= 105) and (len(dAppRegValues) == 0) ):
	if (_installerStrategy == _const__installerStrategy_one):
	    _resp = tkMessageBox.askyesno('QUESTION','Adobe AIR is installed.\n\nNow it is time to install this Application.\n\nThis is a self-signed Application which means the Publisher name may not be known to the Adobe AIR Installer however this is normal.\n\nYou may proceed by pressing the YES button below or click the NO button to stop.')
	    if (not _resp):
		sys.exit(-1)
    if (_vers[-1] <= 105):
	_prevVersInstalled = 'You do not now have any version of Adobe AIR installed therefore you MUST install the latest version of Adobe AIR Runtime by pressing the YES button below.'
	if (_vers[-1] != -1):
	    _prevVersInstalled = 'You have a previous version of Adobe AIR installed however that version is not out of date and MUST be replaced by pressing the YES button below.'
	if (_vers[-1] == 105):
	    print '(main) :: _isTimeForUninstall=(%s)' % (_isTimeForUninstall)
	    if ( (_isTimeForUninstall) and (_installerStrategy == _const__installerStrategy_one) ):
		_uninstallStr = ''
		try:
		    _uninstallStr = appSubKey.values['UninstallString'].value
		except:
		    pass
		if (len(_uninstallStr) > 0):
		    print '(main) :: _uninstallStr=(%s), callExternalProgram() !' % str(_uninstallStr)
		    tkMessageBox.showinfo('INFO','You are about to install a new version of the AIR Application.\n\nAt this time you should choose the option(s) to Uninstall the old version.\n\nYou will be prompted to Install the new version after the old version has been uninstalled.')
		    _retCode = callExternalProgram.callExternalProgram(_uninstallStr)
		    dAppRegValues = showValues(appSubKey)
		    print '(main) :: len(dAppRegValues)=(%s)' % str(len(dAppRegValues))
		if (len(dAppRegValues) > 0):
		    # Determine if the AIR App has been uninstalled and if not then display the following prompt.
		    tkMessageBox.showinfo('INFO','You are about to install a new version of the AIR Application.  The Adobe AIR Installer will prompt you to either run the current version or Uninstall the old version.  You will want to Uninstall the old version before installing the new version.')
	    # Try to launch the AIR App.  (a) Determine if the AIR App has been installed, if not (b) Install the AIR App or (c) Run the AIR App.
	    if ( (len(dAppRegValues) == 0) or ( (_isTimeForUninstall) and (_installerStrategy == _const__installerStrategy_one) ) ):
		stuff = extractFromArchiveByName(_appName_airAppInstaller,_const_air_pkg_name)
		if (len(stuff) > 0):
		    _retCode = writeExtractedStuffToDisk(stuff)
		    if (_retCode == 0):
			_retCode = callExternalProgram.callExternalProgram(stuff[-1])
			if (_retCode < 0):
			    issueSysErrorByNumber(403)
			elif (_installerStrategy == _const__installerStrategy_one):
			    vals = appSubKey.values
			    try:
				if (str(vals['Publisher'].value) == 'UNKNOWN'):
				    print '(main) :: Updating Registry values.'
				    vals['DisplayVersion'] = winreg.solve('1.0.0.0')
				    vals['Publisher'] = winreg.solve('Hierarchical Applications Limited, Inc.')
				    if (len(_original_uninstall_string) == 0):
					try:
					    _original_uninstall_string = str(vals['_UninstallString'].value)
					except:
					    _original_uninstall_string = str(vals['UninstallString'].value)
					vals['_UninstallString'] = winreg.solve(_original_uninstall_string)
				    vals['UninstallString'] = winreg.solve('%s --uninstall="%s"' % (_programName,_original_uninstall_string))
				    vals['BuildTime'] = winreg.solve(_thisBuildTimeSecs)
			    except:
				pass
			elif (_installerStrategy == _const__installerStrategy_one):
			    vals = appSubKey.values
			    if (str(vals['Publisher'].value) == 'UNKNOWN'):
				vals['Publisher'] = winreg.solve('Hierarchical Applications Limited, Inc.')
		    else:
			issueSysErrorByNumber(405)
		else:
		    issueSysErrorByNumber(401)

	    _isAppRunning = False

	    if (not _isAppRunning):
		dAppRegValues = showValues(appSubKey)
		if (len(dAppRegValues) > 0):
		    vals = appSubKey.values
		    _appFQName = '%s' % vals['InstallLocation'].value
		    toks = []
		    _toks = _appFQName.split(os.sep)
		    for t in _toks:
			if (len(t) > 0):
			    toks.append(t)
		    toks.append(_appEXEName)
		    print '(main) :: toks=(%s)' % (str(toks))
		    _appFQName = os.sep.join(toks)
		    print '(main) :: _appFQName=(%s)' % (str(_appFQName))
		    if (os.path.exists(_appFQName)):
			_paths = locateAIRAppShortcuts(_appEXEName)
			if (len(_paths) > 0):
			    # install and launch the server
			    if (len(_paths[0]) == 2):
				_fname_server, _serverTargetPath = _paths[0]
				_serverTargetDir = os.path.dirname(_serverTargetPath)
				adjustAIRAppShortcuts(_paths,_serverTargetPath)
				stuff = extractFromArchiveByName(_const_server_exe_name,_const_air_pkg_name)
				if (len(stuff) > 0):
				    stuff[-1] = os.sep.join([_serverTargetDir,os.path.basename(stuff[-1])])
				    _serverTargetPath = stuff[-1]
				    _retCode = writeExtractedStuffToDisk(stuff)
				    if (_retCode == 0):
					_retCode = callExternalProgram.callExternalProgram(stuff[-1])
					if (_retCode < 0):
					    issueSysErrorByNumber(407)
				elif (len(tocFromArchiveByName(_const_server_pkg_name)) > 0):
				    _serverTargetPath = _serverTargetDir + os.sep + _const_server_folder_name
				    extractAllStuffToDiskFromNamedPkg(_const_server_pkg_name,_serverTargetPath)
				    _serverEXEName = _serverTargetPath + os.sep + _const_server_exe_name
				    if (os.path.exists(_serverEXEName)):
					_retCode = callExternalProgram.callExternalProgram(_serverEXEName)
					if (_retCode < 0):
					    issueSysErrorByNumber(407)
				    else:
					issueSysErrorByNumber(406)
				else:
				    issueSysErrorByNumber(406)
			# +++
			_retCode = callExternalProgram.callExternalProgram(_appFQName)
			if (_retCode < 0):
			    issueSysErrorByNumber(404)
			else:
			    _isAppRunning = True
		    else:
			issueSysErrorByNumber(404)

	    if (not _isAppRunning):
		mainProcess()
	else:
	    _resp = tkMessageBox.askyesno("You are about to install the latest version of Adobe AIR", "This Application requires the latest version of the Adobe AIR Runtime.\n\n%s\n\nAfter Adobe AIR has been successfully installed you will be able to use this Application.\n\nClick the YES button now to proceed to install the Adobe AIR Runtime or click the NO button to stop now." % _prevVersInstalled)
	    if (_resp):
		stuff = extractFromArchiveByName('air_b2_win_100107.exe',_const_air_pkg_name)
		if (len(stuff) > 0):
		    _retCode = writeExtractedStuffToDisk(stuff)
		    if (_retCode == 0):
			_retCode = callExternalProgram.callExternalProgram(stuff[-1])
			if (_retCode < 0):
			    issueSysErrorByNumber(402)
		else:
		    issueSysErrorByNumber(401)
		mainProcess()

def main():
    Tkinter.Tk().withdraw()
    print '(main) :: _installerStrategy=(%s)' % _installerStrategy
    mainProcess()

if ( (len(sys.argv) > 1) and (sys.argv[1] == '--help') ):
    print '--help                             ... displays this help text.'
    print '--verbose                          ... output more stuff.'
    print '--uninstall=air-uninstall-string   ... completely uninstall this app.'
    print '--strategy=number                  ... specify the installer strategy, "2" overrides the "--uninstall=" switch completely.'
else:
    toks = sys.argv[0].split(os.sep)
    _programName = toks[-1]
    for i in xrange(len(sys.argv)):
	bool = ( (sys.argv[i].find('--uninstall=') > -1) or (sys.argv[i].find('--strategy=') > -1) )
	if (bool): 
	    toks = sys.argv[i].split('=')
	    if (sys.argv[i].find('--uninstall=') > -1):
		_original_uninstall_string = toks[1].replace('/',os.sep)
	    elif (sys.argv[i].find('--strategy=') > -1):
		if ( (str(toks[1]).isdigit()) and (str(toks[1]) in _const__installerStrategies) ):
		    _installerStrategy = int(toks[1])
	elif (sys.argv[i].find('--verbose') > -1):
	    _isVerbose = True
psyco.full()
main()

