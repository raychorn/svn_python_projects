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
import tempfile
from lib import tkMessageBox
from lib import WinProcesses
from lib import callExternalProgram
from lib import windowsShortcuts

# To-Do:
# 1).  DONE! Air App needs to retry the connection to the server whenever there is an error in making a connection.
# 1a). DONE! Install server into a secure temp folder and link to the existing .lnk files as normal.
# 1b). DONE! Uninstall process will read the server install location from the Registry and then uninstall the previous server automatically.
# 2).  DONE! Server does not handle the uninstall process. 
# 3).  DONE! Uninstaller does not need to clean-up the server files and the Launch cmd file.
# 4).  DONE! Launch cmd file needs to launch from the server process rather than from the AIR App EXE.
# 5).  DONE! Make log file in preparation for making the console window hidden.  Place file into the InstallLocation for the AIR App.
# 6).  DONE! Make Server console into hidden window.
# 7).  Make Server into a single .EXE. --> This might be easier if the socks.py lib is used instead of Twister.
# 8). (Minor assuming #2 is being done.) Code a custom Air App Installer to avoid running the Air App until after the server is installed and running.

# 9).  Encrypt path to server using a variation of the Oragami Data Folding Technique that goes something like this:
#         ord(ch) or 0x80 for each ch value.
#         pack 8 bits into 32 bit value
#         swap LSB/MSB for both 16 bit values
#         save in Registry as a string of hex values with no delimiters

# 10).  Figure-out which port to put the server on and place this value in the Registry as an obscured value using an abscured name...
#          port number must be stored in the program files folder in an .dat file as an obscured value with an obscured name.

_isVerbose = False
_isUninstall = False

_hasInstalledAirApp = False

_fHand_logFile = -1
_fHand_logFileName = ''

_const__installerStrategy_one = 1
_const__installerStrategy_two = 2
_const__installerStrategies = [str(i) for i in [_const__installerStrategy_one,_const__installerStrategy_two]]

_appName_airAppInstaller = 'TwistedTest.air'

_const_air_pkg_name = 'air.pkg'
_const_server_pkg_name = 'server.pkg'
_const_server_folder_name = 'server'
_const_server_exe_name = _const_server_folder_name+'.exe'

_const_air_runtime_installer_name = 'air_b2_win_100107.exe'

_installerStrategy = _const__installerStrategy_two

_original_uninstall_string = ''

_programName = ''

_rootKeyName = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'

appServerSubKey = -1

def showValues(root):
    d = {}
    if (isinstance(root, winreg.Key)):
	try:
	    print >>_fHand_logFile, '(showValues) :: root.__class__=(%s)' % str(root.__class__)
	    vals = root.values
	    print >>_fHand_logFile, '(showValues) :: vals=(%s) has (%s) items.' % (str(vals),len(vals))
	    for v in vals:
		print >>_fHand_logFile, '(showValues) :: (%s)=(%s)' % (str(v),vals[v])
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
	    print >>_fHand_logFile, '(getAIRVersionFrom) :: ERROR due to "%s".' % str(details)
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

def extractFromArchiveByName(name,pkgName):
    try:
	stuff = []
	outnm = ''
	pkg = pkgHandleByName(pkgName)
	targetdir = localFolderName()
	print >>_fHand_logFile, '(extractFromArchiveByName).1 :: pkg=(%s)' % str(pkg)
	print >>_fHand_logFile, '(extractFromArchiveByName).2 :: targetdir=(%s)' % targetdir
	pkgs = pkg.contents()
	print >>_fHand_logFile, '(extractFromArchiveByName).3 :: pkgs=(%s)' % str(pkgs)
	print >>_fHand_logFile, '(extractFromArchiveByName).4 :: name=(%s)' % str(name)
	if (name in pkgs):
	    outnm = os.path.join(targetdir, name)
	    dirnm = os.path.dirname(outnm)
	    if (os.path.exists(outnm) == False):
		if (not os.path.exists(dirnm)):
		    os.makedirs(dirnm)
		_stuff = pkg.extract(name)[1]
		stuff = [_stuff,outnm]
		print >>_fHand_logFile, '(extractFromArchiveByName).5 :: Extracted (%s) "%s" bytes.' % (name,len(_stuff))
    except Exception, details:
	print >>_fHand_logFile, 'ERROR #200 :: Cannot retrieve package item named "%s" from "%s" due to "%s".' % (name,pkgName,str(details))
    return stuff

def writeExtractedStuffToDisk(args):
    _retCode = -1
    try:
	stuff,outnm = args
	print >>_fHand_logFile, '(writeExtractedStuffToDisk) :: Saving  "%s" bytes into (%s)' % (len(stuff),outnm)
	fHand = open(outnm, 'wb')
	fHand.write(stuff)
	fHand.flush()
	fHand.close()
	_retCode = 0
    except Exception, details:
	print >>_fHand_logFile, 'ERROR #301 :: Cannot write contents for "%s" due to "%s".' % (outnm,str(details))
    return _retCode

def issueSysErrorByNumber(num):
    if (num in [401,402, 403, 404, 405, 406, 407, 408]):
	if (num in [402, 405, 408]):
	    _errMsg = 'ERROR #%s :: Cannot install Adobe AIR Runtime due to some kind of system error.\nDownload and install the latest Adobe AIR Runtime from http://www.adobe.com and then return to try to run this program again.' % num
	elif (num in [401]):
	    _errMsg = 'ERROR #%s :: Cannot install the Application most likely because you may have performed an uninstall during the installation process.\n\nTry running the Installer again but this time don\'t perform an uninstall.\n\nIf all else fails seek Technical Support at http://www.sexyblondessoftware.com.' % num
	elif (num in [403]):
	    _errMsg = 'ERROR #%s :: Cannot install this application due to some kind of system error.\nYou may be able to get Technical Support online from http://www.sexyblondessoftware.com.' % num
	elif (num in [404]):
	    _errMsg = 'ERROR #%s :: Cannot launch this application due to some kind of system error.\nYou may be able to get Technical Support online from http://www.sexyblondessoftware.com.' % num
	elif (num in [406, 407]):
	    _errMsg = 'ERROR #%s :: Cannot launch the server for this application due to some kind of system error.\nYou may be able to get Technical Support online from http://www.sexyblondessoftware.com.' % num
	print >>_fHand_logFile, _errMsg
	if (num not in [401]):
	    _errMsg += '\n\nDo you want to try to install the Adobe AIR Runtime again or CANCEL to take care of this yourself ?'
	tkMessageBox.showwarning('ERROR',_errMsg)
	sys.exit(-1)

def getPIDforNamedProcess(name):
    _pid = -1
    try:
	_win_proc = WinProcesses.WinProcesses()
	_pid = _win_proc.getProcessIdByName(name)
    except:
	pass
    return _pid

def locateAIRAppShortcuts(vals,likeName):
    _report = []
    print >>_fHand_logFile, '(locateAIRAppShortcuts) :: likeName=(%s)' % likeName
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
    if (len(_report) == 0):
	_installLocation = ''
	try:
	    _installLocation = str(vals['InstallLocation'].value)
	except:
	    pass
	_report.append([_installLocation,_installLocation])
    return _report

def writeServerLaunchCommandFile(serverPath,path):
    if (os.path.exists(path)):
	_pName = os.path.basename(path)
	toks = _pName.split('.')
	toks.pop()
	pName = '.'.join(toks)
	pDir = os.path.dirname(path)
	fname = os.sep.join([pDir,'Launch'+pName+'.cmd'])
	print >>_fHand_logFile, '(writeServerLaunchCommandFile) :: serverPath=(%s)' % serverPath
	try:
	    fHand = open(fname,'w')
	    _newPath = '"%s" --launch="%s"' % (serverPath,path)
	    _contents = '\n'.join(['@start "%s" /b %s\n\n' % (pName,_newPath)])
	    fHand.writelines(_contents)
	    fHand.flush()
	    fHand.close()
	except Exception, details:
	    print >>_fHand_logFile, '(writeServerLaunchCommandFile) :: ERROR due to "%s".' % str(details)
    return fname

def adjustAIRAppShortcuts(_paths,serverPath):
    cmdFName = ''
    if (isinstance(_paths, list)):
	for p in _paths:
	    if (len(p) == 2):
		_fname, _path = p
		if (_path.find(' --launch=') == -1):
		    #os.remove(_fname)
		    if (os.path.exists(cmdFName) == False):
			if (serverPath.find('server.exe') == -1):
			    serverPath += os.sep+'server.exe'
			cmdFName = writeServerLaunchCommandFile(serverPath,_path)
		    windowsShortcuts.makeWindowsShortcut(_fname,cmdFName,None,None,None)
    return cmdFName

def adjustAirAppUninstallerRegVals(serverSubKey, vals, serverFname):
    _vals = serverSubKey.values
    try:
	_prevPath = str(_vals['InstallLocation'].value)
	if (os.path.exists(_prevPath)):
	    for root, dirs, files in os.walk(_prevPath, topdown=False):
		for f in files:
		    _fname = root+os.sep+f
		    print >>_fHand_logFile, '(adjustAirAppUninstallerRegVals).1 :: _fname=(%s)' % _fname
		    if (os.path.exists(_fname)):
			os.remove(_fname)
		os.rmdir(root)
		print >>_fHand_logFile, '(adjustAirAppUninstallerRegVals).2 :: root=(%s)' % root
    except Exception, details:
	print >>_fHand_logFile, '(adjustAirAppUninstallerRegVals).ERROR :: Reason: "%s".' % str(details)
    _vals['InstallLocation'] = winreg.solve(os.path.dirname(serverFname))

    if (0): # The specific technique will be more of a mystery if we do not provide an uninstaller for the server,
	_vals['DisplayIcon'] = winreg.solve(serverFname)
	_vals['DisplayName'] = winreg.solve(str(vals['DisplayName'].value)+' Server')
	_vals['DisplayVersion'] = winreg.solve(str(vals['DisplayName'].value))
	_vals['NoModify'] = winreg.solve(1)
	_vals['NoRepair'] = winreg.solve(1)
	_vals['Publisher'] = winreg.solve(str(vals['Publisher'].value))
	_vals['UninstallString'] = winreg.solve(os.path.dirname(serverFname)+os.sep+_const_server_exe_name+' --uninstall=dummy')

def mainProcess():
    global _hasInstalledAirApp
    global appServerSubKey
    
    d = os.path.dirname(sys.executable)
    print >>_fHand_logFile, '(mainProcess).1 :: d=(%s)' % str(d)
    root = winreg.get_key(winreg.HKEY.LOCAL_MACHINE, _rootKeyName, winreg.KEY.ALL_ACCESS)
    subKey = winreg.get_key(root, 'Adobe AIR', winreg.KEY.ALL_ACCESS)
    #showValues(subKey)
    _vers = getAIRVersionFrom(subKey)

    _appRegKeyName = _appName_airAppInstaller.split('.')[0]
    _appEXEName = _appRegKeyName + '.exe'

    appSubKey = winreg.get_key(root, _appRegKeyName, winreg.KEY.ALL_ACCESS)
    dAppRegValues = showValues(appSubKey)

    appServerSubKey = winreg.get_key(root, _appRegKeyName+'Server', winreg.KEY.ALL_ACCESS)
    
    # figure-out if there is a buildtime in the Registry for the AIR App that was previously installed.
    stuff = extractFromArchiveByName('buildtime.txt',_const_air_pkg_name)
    print >>_fHand_logFile, '(mainProcess).2 :: stuff=(%s)' % (str(stuff))

    _isTimeForUninstall = True # default is to always assume there is an uninstall
    
    if (_installerStrategy == _const__installerStrategy_one):
	_thisBuildTimeSecs = 0.0
	if (len(dAppRegValues) > 0):
	    if (dAppRegValues.has_key('BuildTime')):
		_lastBuildTimeSecs = float(dAppRegValues['BuildTime'])
		if (len(stuff) > 0):
		    _thisBuildTimeSecs = float(stuff[0])
		    _isTimeForUninstall = (_thisBuildTimeSecs > _lastBuildTimeSecs) # this catches the uninstall in case there is no need to perform the uninstall at this time.
		    print >>_fHand_logFile, '(mainProcess).3a :: _isTimeForUninstall=(%s), _thisBuildTimeSecs=(%s), _lastBuildTimeSecs=(%s)' % (_isTimeForUninstall,_thisBuildTimeSecs,_lastBuildTimeSecs)
    elif ( (_installerStrategy == _const__installerStrategy_two) and (not _hasInstalledAirApp) ):
	print >>_fHand_logFile, '(mainProcess).3b :: _isTimeForUninstall=(%s)' % (_isTimeForUninstall)
	_isTimeForUninstall = True
	dAppRegValues = {} # simulate the need for an installation assuming the appwas previously installed.
    print >>_fHand_logFile, '(mainProcess).3 :: _isTimeForUninstall=(%s), len(dAppRegValues)=(%s)' % (_isTimeForUninstall,len(dAppRegValues))

    print >>_fHand_logFile, '(mainProcess).4 :: _vers=(%s)' % str(_vers)
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
	    print >>_fHand_logFile, '(mainProcess).5 :: _isTimeForUninstall=(%s)' % (_isTimeForUninstall)
	    if ( (_isTimeForUninstall) and (_installerStrategy == _const__installerStrategy_one) ):
		_uninstallStr = ''
		try:
		    _uninstallStr = appSubKey.values['UninstallString'].value
		except:
		    pass
		if (len(_uninstallStr) > 0):
		    print >>_fHand_logFile, '(mainProcess).6 :: _uninstallStr=(%s), callExternalProgram() !' % str(_uninstallStr)
		    tkMessageBox.showinfo('INFO','You are about to install a new version of the AIR Application.\n\nAt this time you should choose the option(s) to Uninstall the old version.\n\nYou will be prompted to Install the new version after the old version has been uninstalled.')
		    _retCode = callExternalProgram.callExternalProgram(_uninstallStr)
		    dAppRegValues = showValues(appSubKey)
		    print >>_fHand_logFile, '(mainProcess).7 :: len(dAppRegValues)=(%s)' % str(len(dAppRegValues))
		if (len(dAppRegValues) > 0):
		    # Determine if the AIR App has been uninstalled and if not then display the following prompt.
		    tkMessageBox.showinfo('INFO','You are about to install a new version of the AIR Application.  The Adobe AIR Installer will prompt you to either run the current version or Uninstall the old version.  You will want to Uninstall the old version before installing the new version.')
	    # Try to launch the AIR App.  (a) Determine if the AIR App has been installed, if not (b) Install the AIR App or (c) Run the AIR App.
	    print >>_fHand_logFile, '(mainProcess).7a :: len(dAppRegValues)=(%s)' % str(len(dAppRegValues))
	    if ( (len(dAppRegValues) == 0) or ( (_isTimeForUninstall) and (_installerStrategy == _const__installerStrategy_one) ) ):
		stuff = extractFromArchiveByName(_appName_airAppInstaller,_const_air_pkg_name)
		print >>_fHand_logFile, '(mainProcess).7b :: len(stuff)=(%s)' % str(len(stuff))
		if (len(stuff) > 0):
		    _retCode = writeExtractedStuffToDisk(stuff)
		    print >>_fHand_logFile, '(mainProcess).8 :: (%s) _retCode=(%s)' % (_appName_airAppInstaller,_retCode)
		    if (_retCode == 0):
			_retCode = callExternalProgram.callExternalProgram(stuff[-1])
			print >>_fHand_logFile, '(mainProcess).9 :: callExternalProgram(%s) =(%s)' % (stuff[-1],_retCode)
			if ( (_retCode != None) and (_retCode < 0) ):
			    issueSysErrorByNumber(403)
			elif (_installerStrategy == _const__installerStrategy_one):
			    vals = appSubKey.values
			    try:
				if (str(vals['Publisher'].value) == 'UNKNOWN'):
				    print >>_fHand_logFile, '(main) :: Updating Registry values.'
				    try:
					vals['DisplayVersion'] = winreg.solve('1.0.0.0')
				    except:
					pass
				    try:
					vals['Publisher'] = winreg.solve('Hierarchical Applications Limited, Inc.')
				    except:
					pass
				    if (len(_original_uninstall_string) == 0):
					try:
					    _original_uninstall_string = str(vals['_UninstallString'].value)
					except:
					    _original_uninstall_string = str(vals['UninstallString'].value)
					vals['_UninstallString'] = winreg.solve(_original_uninstall_string)
				    try:
					vals['UninstallString'] = winreg.solve('%s --uninstall="%s"' % (_programName,_original_uninstall_string))
				    except:
					pass
				    try:
					vals['BuildTime'] = winreg.solve(_thisBuildTimeSecs)
				    except:
					pass
			    except:
				pass
			elif (_installerStrategy == _const__installerStrategy_two):
			    print >>_fHand_logFile, '(mainProcess).10 :: Adjusting registry values for _const__installerStrategy_two'
			    vals = appSubKey.values
			    try:
				if (str(vals['Publisher'].value) == 'UNKNOWN'):
				    vals['Publisher'] = winreg.solve('Hierarchical Applications Limited, Inc.')
			    except:
				pass
			    try:
				vals['BuildTime'] = winreg.solve(_thisBuildTimeSecs)
			    except:
				pass
			_hasInstalledAirApp = True
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
		    print >>_fHand_logFile, '(mainProcess).11 :: toks=(%s)' % (str(toks))
		    _appFQName = os.sep.join(toks)
		    print >>_fHand_logFile, '(mainProcess).12 :: _appFQName=(%s)' % (str(_appFQName))
		    if (os.path.exists(_appFQName)):
			_paths = locateAIRAppShortcuts(appSubKey.values,_appEXEName)
			print >>_fHand_logFile, '(mainProcess).13 :: _paths=(%s)' % (str(_paths))
			if (len(_paths) > 0):
			    print >>_fHand_logFile, '(mainProcess).14 :: len(_paths[0])=(%s)' % (str(len(_paths[0])))
			    if (len(_paths[0]) == 2):
				_fname_server, _serverTargetPath = _paths[0]
				_serverTargetPath = tempfile.mkdtemp()
				print >>_fHand_logFile, '(mainProcess).15 :: _fname_server=(%s), _serverTargetPath=(%s)' % (_fname_server,_serverTargetPath)
				_serverTargetDir = _serverTargetPath
				stuff = extractFromArchiveByName(_const_server_exe_name,_const_air_pkg_name)
				print >>_fHand_logFile, '(mainProcess).16 :: len(stuff)=(%s), _const_server_exe_name=(%s) from _const_air_pkg_name=(%s)' % (len(stuff),_const_server_exe_name,_const_air_pkg_name)
				_toc = tocFromArchiveByName(_const_server_pkg_name)
				print >>_fHand_logFile, '(mainProcess).17 :: len(_toc)=(%s)' % (len(_toc))
				if (len(stuff) > 0):
				    stuff[-1] = os.sep.join([_serverTargetDir,os.path.basename(stuff[-1])])
				    _serverTargetPath = stuff[-1]
				    print >>_fHand_logFile, '(mainProcess).18 :: _serverTargetPath=(%s)' % (_serverTargetPath)
				    _retCode = writeExtractedStuffToDisk(stuff)
				    if (_retCode == 0):
					__serverTargetPath = adjustAIRAppShortcuts(_paths,_serverTargetPath)
					print >>_fHand_logFile, '(mainProcess).18a :: _serverTargetPath=(%s), __serverTargetPath=(%s)' % (_serverTargetPath,__serverTargetPath)
					_retCode = callExternalProgram.callExternalProgram(__serverTargetPath)
					if (_retCode < 0):
					    issueSysErrorByNumber(407)
					else:
					    print >>_fHand_logFile, '(mainProcess).19 :: _paths=(%s), _serverTargetPath=(%s)' % (_paths,_serverTargetPath)
					    adjustAirAppUninstallerRegVals(appServerSubKey, appSubKey.values, _serverTargetPath)
					    _isAppRunning = True
				elif (len(_toc) > 0):
				    _serverTargetPath = _serverTargetDir + os.sep + _const_server_folder_name
				    print >>_fHand_logFile, '(mainProcess).20 :: _serverTargetPath=(%s)' % (_serverTargetPath)
				    extractAllStuffToDiskFromNamedPkg(_const_server_pkg_name,_serverTargetPath)
				    _serverEXEName = adjustAIRAppShortcuts(_paths,_serverTargetPath)
				    print >>_fHand_logFile, '(mainProcess).21 :: _serverEXEName=(%s)' % (_serverEXEName)
				    if (os.path.exists(_serverEXEName)):
					__serverTargetPath = _serverEXEName
					print >>_fHand_logFile, '(mainProcess).22 :: _paths=(%s), _serverTargetPath=(%s), __serverTargetPath=(%s)' % (_paths,_serverTargetPath,__serverTargetPath)
					adjustAirAppUninstallerRegVals(appServerSubKey, appSubKey.values, _serverTargetPath)
					_isAppRunning = True
					if (0): # Fail to launch the server now because it cannot run as a sub-process...
					    _retCode = callExternalProgram.callExternalProgram(_serverEXEName)
					    print >>_fHand_logFile, '(mainProcess).23 :: _serverEXEName=(%s), _retCode=(%s)' % (_serverEXEName,_retCode)
					    if ( (_retCode != None) and (_retCode < 0) ):
						issueSysErrorByNumber(407)
					elif (len(_paths) > 0):
					    _retCode = None
					    _isShortCutDesktop = False
					    _isShortCutStartMenu = False
					    try:
						for p in _paths:
						    if (p[0].find('Desktop') > -1):
							_isShortCutDesktop = True
						    if (p[0].find('Start Menu') > -1):
							_isShortCutStartMenu = True
					    except:
						pass
					    _phrase = ''
					    if (_isShortCutDesktop):
						_phrase += 'Desktop'
					    if (_isShortCutStartMenu):
						if (len(_phrase) > 0):
						    _phrase += ' or the '
						_phrase += 'Start Menu'
					    if (len(_phrase) > 0):
						tkMessageBox.showinfo('INFO','You have successfully installed the Application.\n\nYou may start this Application using one of the shortcuts, see your %s.\n\nIf you launched the Application from the Installer you will now see an error message telling you to close the Application and re-launch using one of the Application Shortcuts.  Please do so now.' % (_phrase))
				    else:
					issueSysErrorByNumber(406)
				else:
				    issueSysErrorByNumber(406)
		    else:
			issueSysErrorByNumber(404)

	    if (not _isAppRunning):
		print >>_fHand_logFile, '(mainProcess).26 :: mainProcess() because _isAppRunning=(%s)' % (_isAppRunning)
		mainProcess()
	else:
	    _resp = tkMessageBox.askyesno("You are about to install the latest version of Adobe AIR", "This Application requires the latest version of the Adobe AIR Runtime.\n\n%s\n\nAfter Adobe AIR has been successfully installed you will be able to use this Application.\n\nClick the YES button now to proceed to install the Adobe AIR Runtime or click the NO button to stop now." % _prevVersInstalled)
	    if (_resp):
		stuff = extractFromArchiveByName(_const_air_runtime_installer_name,_const_air_pkg_name)
		if (len(stuff) > 0):
		    _retCode = writeExtractedStuffToDisk(stuff)
		    if (_retCode == 0):
			_retCode = callExternalProgram.callExternalProgram(stuff[-1])
			if (_retCode < 0):
			    issueSysErrorByNumber(402)
		else:
		    issueSysErrorByNumber(408)
		print >>_fHand_logFile, '(mainProcess).27 :: mainProcess() !'
		mainProcess()

def main():
    Tkinter.Tk().withdraw()
    print >>_fHand_logFile, '(main) :: _installerStrategy=(%s)' % _installerStrategy
    mainProcess()

if ( (len(sys.argv) > 1) and (sys.argv[1] == '--help') ):
    print >>sys.stderr, '--help                             ... displays this help text.'
    print >>sys.stderr, '--verbose                          ... output more stuff.'
    print >>sys.stderr, '--uninstall=air-uninstall-string   ... completely uninstall this app.'
    print >>sys.stderr, '--strategy=number                  ... specify the installer strategy, "2" overrides the "--uninstall=" switch completely.'
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
try:
    _fHand_logFileName = os.sep.join([tempfile.mkdtemp(),_programName+'.log'])
    _fHand_logFile = open(_fHand_logFileName,'w')
except Exception, details:
    print >>sys.stderr, "Execution of Log File Creation failed:", details
try:
    main()
except Exception, details:
    print >>sys.stderr, "Execution of Main() failed:", details
try:
    _fHand_logFile.flush()
    _fHand_logFile.close()
except Exception, details:
    print >>sys.stderr, "Execution of Log File Finalization failed:", details
try:
    _vals = appServerSubKey.values
    _installPath = str(_vals['InstallLocation'].value)
    _newName = os.sep.join([_installPath,os.path.basename(_fHand_logFileName)])
    os.rename(_fHand_logFileName,_newName)
    os.rmdir(os.path.dirname(_fHand_logFileName))
except Exception, details:
    print >>sys.stderr, "Execution of Log File Relocation failed:", details
