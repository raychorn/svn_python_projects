import os
import sys
import psyco
import lib.readYML
import lib.threadpool
import win32api
import win32con
import zipfile
import socket
from vyperlogix import putStr
from vyperlogix import winreg

# To-Do:
# (1). Add GUI using series of TK Dialogs.

_isVerbose = False
_isUninstall = False

_programName = ''

_yml_filename = 'setup.yml'

_installation_target_folder = 'c:\\dss\\'

_zip_source_path = ''

_mongrel_start_cmd_filename = 'mongrel_start.cmd'

_rootKeyName = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'

_pool = lib.threadpool.Pool(1000)

def updateAddOrRemoveProgramStrings(root, op='ADD'):
    op = str(op).upper()
    if (op == 'ADD'):
	subKey = winreg.get_key(root, 'DSS', winreg.KEY.ALL_ACCESS)
	subKey.values['DisplayName'] = winreg.solve('DSS - Decision Support System')
	subKey.values['DisplayVersion'] = winreg.solve('1.0.0.0')
	subKey.values['HelpLink'] = winreg.solve('mailto:support@bigfix.com')
	subKey.values['URLUpdateInfo'] = winreg.solve('http://www.bigfix.com')
	subKey.values['NoModify'] = winreg.solve(1)
	subKey.values['NoRepair'] = winreg.solve(1)
	subKey.values['Publisher'] = winreg.solve('BigFix, Inc.')
	subKey.values['UninstallString'] = winreg.solve('c:\\dss\\uninstall.exe')
    elif (op == 'REMOVE'):
	print 'root.__class__=(%s)' % str(root.__class__)
	root.remove('DSS')

def canSocketListenOn(addr,port):
	canListen = True
	try:
	    mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
	    mySocket.bind ( ( addr, port) )
	    mySocket.listen ( 1 )
	    mySocket.close()
	except socket.error, msg:
	    canListen = False
	return canListen

def locateRailsFolder(top):
	_configPath = '%sconfig' % os.sep
	for root, dirs, files in os.walk(top):
	    if ( (root.endswith(_configPath)) and ('boot.rb' in files) and ('environment.rb' in files) ):
		    return root
	return ''

def removeFiles(top):
	for root, dirs, files in os.walk(top,topdown=False):
	    for f in files:
		try:
		    fqName = root+os.sep+f
		    os.remove(fqName)
		except:
		    pass
	    if (root != top):
		try:
		    os.rmdir(root)
		except:
		    pass

def writeMongrelCommands(dict):
    global _mongrel_start_cmd_filename
    if (str(dict.__class__).find("'dict'") > -1):
	_addr = 'localhost'
	if (dict.has_key('addr')):
	    _addr = dict['addr']
	_port = 3000
	if (dict.has_key('port')):
	    _port = int(dict['port'])
	    for i in xrange(1000):
		if (canSocketListenOn(_addr,_port+i)):
		    _port += i
		    break
	_env = 'production'
	if (dict.has_key('env')):
	    _env = dict['env']
	_rails_folder = locateRailsFolder(_installation_target_folder)
	if (len(_rails_folder) > 0):
	    _rails_folder = os.sep.join(_rails_folder.split(os.sep)[0:-1])
	_mode = 'w'
	_mongrel_start_cmd_filename = _rails_folder+os.sep+_mongrel_start_cmd_filename
	os.makedirs(_rails_folder+os.sep+'tmp'+os.sep+'pids')
	if (os.path.exists(_mongrel_start_cmd_filename)):
	    _mode = 'a'
	fHand = open(_mongrel_start_cmd_filename, _mode)
	if (_mode == 'w'):
	    fHand.writelines('echo @off\n')
	fHand.writelines('mongrel_rails start -e %s -a %s -p %s -P tmp/pids/mongrel_%s.pid -l log/mongrel_%s.log\n' % (_env,_addr,_port,_port,_port))
	fHand.close()
    else:
	print 'WARNING :: Invalid object passed in from main(). Class is [%s] but should be "<type \'dict\'>".' % (str(dict.__class__))

@lib.threadpool.threadpool(_pool)
def writeDataFile(filename,data,_mode):
    try:
	fHand = open(filename,_mode)
	fHand.write(data)
	fHand.flush()
	fHand.close()
    except Exception, details:
	print '(writeDataFile) :: ERROR "%s".' % (str(details))

def copySourceFileToDest(src,dest):
    data = ''
    try:
	fHand_src = open(src,'rb')
	data = fHand_src.read()
	fHand_src.close()
    except Exception, details:
	putStr.putStr('ERROR in source file copy process due to "%s".\n\n' % str(details))
    try:
	fHand_dest = open(dest,'wb')
	fHand_dest.write(data)
	fHand_dest.close()
    except Exception, details:
	putStr.putStr('ERROR in destination file copy writing process due to "%s".\n\n' % str(details))

def unZIPTotarget(zipSrc,toFolder):
    if (os.path.exists(zipSrc)):
	try:
	    if (os.path.exists(toFolder) == False):
		print 'mkdir "%s".' % toFolder
		os.mkdir(toFolder)
	    myZipFile = zipfile.ZipFile( zipSrc, "r")
	    for f in myZipFile.namelist():
		data = myZipFile.read(f)
		_sep = ''
		if (toFolder.endswith(os.sep) == False):
		    _sep = os.sep
		p = '%s%s%s' % (toFolder,_sep,f.replace('/',os.sep))
		b = os.path.dirname(p)
		print 'UnZipping fileName=(%s) to (%s) [%s], len(data)=(%s)' % (f,p,b,len(data))
		try:
		    os.makedirs(b)
		except:
		    pass
		writeDataFile(p,data,'wb')
	    myZipFile.close()
	except Exception, details:
	    print 'WARNING :: ERROR "%s".' % (str(details))
    else:
	print 'WARNING :: Invalid zip file name passed from main(). ZIP file is [%s] but should it does not exist.' % (zipSrc)

def cleanPathStrings(path):
    try:
	ignoring = '%seee%s' % (os.sep,os.sep)
	toks = []
	_toks = path.split(';')
	for t in _toks:
	    if (t.find(ignoring) == -1):
		toks.append(t)
	path = ';'.join(toks)
    except:
	pass
    return path

def adjustPathsInCommandFiles():
	root = 'c:/ruby/bin'
	_root = '%s/ruby/bin' % _installation_target_folder
	_files = os.listdir(_root)
	files = []
	for f in _files:
	    _f = f.lower()
	    if ( (_f.find('.bat') > -1) or (_f.find('.cmd') > -1) ):
		files.append(f)
	pat = ''.join(root.split(':')[1:])
	_pat = ''.join(_root.split(':')[1:]).replace(os.sep,'/').replace('//','/')
	for f in files:
	    try:
		_fname = _root+'/'+f
		_fname2 = _fname+'.new'
		fHand = open(_fname,'r')
		fHand2 = open(_fname2,'w')
		_lines = fHand.readlines()
		lines = []
		for l in _lines:
		    _l = l
		    if (_l.find(pat) > -1):
			_l = _l.replace(pat,_pat)
		    lines.append(_l)
		fHand2.writelines('\n'.join(lines))
		fHand2.flush()
		fHand.close()
		fHand2.close()
		os.remove(_fname)
		os.rename(_fname2,_fname)
	    except Exception, details:
		putStr.putStr('(adjustPathsInCommandFiles).ERROR "%s".\n' % (str(details)))

def main(specs):
    if (str(specs.__class__).find("'list'") > -1):
	if (len(specs) > 0):
	    root = winreg.get_key(winreg.HKEY.LOCAL_MACHINE, _rootKeyName, winreg.KEY.ALL_ACCESS)
	    if (os.path.exists(_zip_source_path)):
		# perform the unzip
		print '(main) :: _installation_target_folder=(%s)' % _installation_target_folder
		putStr.putStr('\nRemoving the prior installation from "%s".\n\n' % _installation_target_folder)
		removeFiles(_installation_target_folder)
		putStr.putStr('Copying files into "%s".\n\n' % _installation_target_folder)
		unZIPTotarget(_zip_source_path,_installation_target_folder)
		_pool.join()
		# verify the installation from the zip file
		# write the mongrel start file
		putStr.putStr('Creating the Server Start-up Batch File in "%s".\n\n' % _mongrel_start_cmd_filename)
		if (os.path.exists(_mongrel_start_cmd_filename)):
		    os.remove(_mongrel_start_cmd_filename)
		_port = 3000
		_addr = 'localhost'
		for m in specs:
		    d = {}
		    toks = m.value.split(',')
		    for t in toks:
			_toks = t.split('=')
			d[_toks[0]] = _toks[-1]
		    print '(main) :: m=(%s), toks=(%s), d=(%s)' % (str(m),toks,d)
		    if (d.has_key('port')):
			_port = int(d['port'])
		    if (d.has_key('addr')):
			_addr = d['addr']
		    writeMongrelCommands(d)
		# start the mongrels
		#putStr.putStr('\nSetup complete.\n\nPress any key to start the server process...')
		putStr.putStr('\nSetup complete.\n\n')
		os.chdir(_installation_target_folder)
		putStr.putStr('Type the following command to start your Mongrel Server.\n\n')
		putStr.putStr('@start "Mongrel Server" /b "%s"\n\n' % _mongrel_start_cmd_filename)
		putStr.putStr('This is the URL for your client:\n\n')
		putStr.putStr('http://localhost:%s/dss/dss.html\n\n' % _port)
		_server_cmd = 'server.cmd'
		_rubyPath = '%sruby%sbin' % (_installation_target_folder,os.sep)
		adjustPathsInCommandFiles() # this is a hack for now but it should work... revisit this issue later-on if required to make this more elegant.
		try:
		    fHand = open(_server_cmd,'w')
		    fHand.writelines('SET PATH=%s;%s\n' % (_rubyPath,cleanPathStrings(os.environ['PATH'])))
		    fHand.writelines('cd %s\n' % os.path.dirname(_mongrel_start_cmd_filename))
		    fHand.writelines('%s\n' % _mongrel_start_cmd_filename)
		    fHand.close()
		except Exception, details:
		    putStr.putStr('ERROR: Unable to save the %s file due to "%s".\n\n' % (_server_cmd,str(details)))
		_client_cmd = 'client.cmd'
		try:
		    fHand = open(_client_cmd,'w')
		    fHand.writelines('@start "DSS" /b "C:\Program Files\Internet Explorer\iexplore.exe" http://%s:%s/dss/dss.html\n' % (_addr,_port))
		    fHand.close()
		except Exception, details:
		    putStr.putStr('ERROR: Unable to save the %s file due to "%s".\n\n' % (_client_cmd,str(details)))
		putStr.putStr('You may use the DOS command "%s" to start your Mongrel server\nset pathand test your client using the "%s" command.\n\n' % (_server_cmd,_client_cmd))
		putStr.putStr('You will find these commands in the "%s" folder.\n\n' % _installation_target_folder)
		_src = os.path.dirname(_zip_source_path) + os.sep + 'uninstall.exe'
		_dest = _installation_target_folder + 'uninstall.exe'
		copySourceFileToDest(_src,_dest)
		# Add Registry Entry to allow for uninstall.
		updateAddOrRemoveProgramStrings(root,'ADD')
	    elif (_isUninstall == True):
		putStr.putStr('\nPerforming uninstall... found in "%s".\n\n' % _installation_target_folder)
		removeFiles(_installation_target_folder)
		putStr.putStr('Uninstall completed.\n\n')
		# Remove Registry Entry that allows for uninstall.
		updateAddOrRemoveProgramStrings(root,'REMOVE')
	    else:
		print 'WARNING :: Invalid ZIP Path Spec. [%s] cannot be found.' % (_zip_source_path)
	else:
	    print 'WARNING :: Invalid object passed in from YML file because it is empty. Object is [%s].' % (str(specs))
    else:
	print 'WARNING :: Invalid object passed in from YML file. Class is [%s] but should be "<type \'list\'>".' % (str(specs.__class__))

_mongrelSpecs = []

if ( (len(sys.argv) == 1) or (sys.argv[1] == '--help') ):
    print '--help                      ... displays this help text.'
    print '--verbose                   ... output more stuff.'
    print '--uninstall                 ... perform uninstall.'
    print '--yml=yml_filename          ... yml file name.'
    print '--target=folder_name        ... installation target folder name.'
    print '--zipPath=zip_path          ... path for the zip file installing from.'
else:
    toks = sys.argv[0].split(os.sep)
    _programName = toks[-1]
    for i in xrange(len(sys.argv)):
	bool = ( (sys.argv[i].find('--yml=') > -1) or (sys.argv[i].find('--target=') > -1) or (sys.argv[i].find('--zipPath=') > -1) )
	if (bool): 
	    toks = sys.argv[i].split('=')
	    if (sys.argv[i].find('--yml=') > -1):
		_yml_filename = toks[1].replace('/',os.sep)
		ymlReader = lib.readYML.ymlReader(_yml_filename)
		ymlReader.read()
		cName = win32api.GetComputerName()
		try:
		    n = 'setup'
		    yml = ymlReader.objectsNamed(n)
		    _mongrelSpecs = (yml[0]).attrsForName('mongrel')
		except Exception, details:
		    print '(init).ERROR_READING_YML_FILE :: "%s"' % str(details)
	    elif (sys.argv[i].find('--target=') > -1):
		_installation_target_folder = toks[1].replace('/',os.sep)
	    elif (sys.argv[i].find('--zipPath=') > -1):
		_zip_source_path = toks[1].replace('/',os.sep)
		if (os.path.exists(_zip_source_path) == False):
		    _zip_source_path = ''
	elif (sys.argv[i].find('--verbose') > -1):
	    _isVerbose = True
	elif (sys.argv[i].find('--uninstall') > -1):
	    _isUninstall = True
psyco.bind(main)
main(_mongrelSpecs)
