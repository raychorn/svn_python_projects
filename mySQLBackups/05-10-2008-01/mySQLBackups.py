import glob
import os, sys
import time
import Args
import PrettyPrint
import handlers.ExceptionHandler

_isVerbose = False
_destpath = ''
_binpath = ''
_freq = -1
_maxbackups = 120
_host = '127.0.0.1'
_username = ''
_password = ''

_mySQLDumpCommands = ['mysqldump.exe']

def add_to_zip(fname):
    import zipfile
    aName = fname.replace('.sql', '.zip')
    print 'Created new backup '+aName
    zp = zipfile.ZipFile(aName, 'w', zipfile.ZIP_DEFLATED)
    zp.write(fname)
    zp.close()

def runProcess(detailsPath,args):
    import os
    import _utils
    import subprocess
    if (not os.path.exists(detailsPath)):
	os.mkdir(detailsPath)
    args = args if isinstance(args,list) else [args]
    pp = args[0]
    for p in args[0].split('"'):
	if (os.path.exists(p)):
	    pp = p
	    break
    if (args[-1].startswith('>')):
	fOut = open(args[-1].replace('> ','').replace('>','').replace('"',''),'w')
	del args[-1]
    else:
	fOut = open('%s_%s.txt' % (os.sep.join([detailsPath,'.'.join(_utils.timeStamp().replace(':','').split('.')[0:-1])]),os.path.basename(pp).replace('.','_')),'w')
    e = os.environ
    print 'args=%s' % args
    p = subprocess.Popen(args, env=e, stdout=fOut, shell=False)
    p.wait()
    fOut.flush()
    fOut.close()

def main(host,username,password,destpath,binpath,maxbackups):
    cmd = os.sep.join([binpath,_mySQLDumpCommands[0]])
    if (os.path.exists(cmd)):
	mySqlDumpCommand = [cmd,'--host=%s' % host,'--user=%s' % username,'--password=%s' % password,'--single-transaction','--all-databases']

	print "--- START ---"
	
	# create new backup
	baseBackupFileName = '%s_%s' % (host,username)
	newBackupFileName = os.sep.join([destpath,baseBackupFileName + time.strftime("_%Y%m%d_%H%M%S", time.localtime())+".sql"])
	mySqlDumpCommand.append('> "%s"' % (newBackupFileName))
	print mySqlDumpCommand
	runProcess(destpath,mySqlDumpCommand)
	
	# compress new backup
	add_to_zip(newBackupFileName)
	os.remove(newBackupFileName)
	
	# delete old backups
	oldBackupFileNames = glob.glob(os.sep.join([destpath,baseBackupFileName+"_*_*.zip"]))
	oldBackupFileNames.sort()
	print 'len(oldBackupFileNames)=[%s], maxbackups=[%s]' % (len(oldBackupFileNames),maxbackups)
	if (len(oldBackupFileNames) > maxbackups):
	    for fileName in oldBackupFileNames[0:len(oldBackupFileNames)-maxbackups]:
		os.remove(fileName)
		print 'Deleted old backup "%s".' % fileName
	else:
	    print 'Deleted no old backup files.'
	
	print "--- END ---"
    else:
	print 'ERROR :: Unable to locate the "%s" command.  Recommend you adjust the binpath argument.' % cmd

if (__name__ == '__main__'):
    excp = handlers.ExceptionHandler.ExceptionHandler(notifyMachineNames=[]) # 'UNDEFINED3','SQL2005'
    
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()
	
    args = {'--help':'displays this help text.','--verbose':'output more stuff.','--destpath=?':'path to backups.','--binpath=?':'path to mySQL binaries.','--freq=?':'how often (seconds) should the progpath be executed.','--maxbackups=?':'how many backups should be retained.','--host=?':'host address (127.0.0.1 by default).','--username=?':'username for the host account.','--password=?':'password for the host user account.'}
    _argsObj = Args.Args(args)
    print >>sys.stderr, '_argsObj=(%s)' % str(_argsObj)

    if ( (len(sys.argv) == 1) or (sys.argv[-1] == args.keys()[0]) ):
	ppArgs()
    else:
	try:
	    _isVerbose = _argsObj.booleans['isVerbose'] if _argsObj.booleans.has_key('isVerbose') else False
	except:
	    _isVerbose = False
    
	try:
	    _freq = int(_argsObj.arguments['freq']) if _argsObj.arguments.has_key('freq') else -1
	except:
	    _freq = -1
	    
	try:
	    _maxbackups = int(_argsObj.arguments['maxbackups']) if _argsObj.arguments.has_key('maxbackups') else False
	except:
	    _maxbackups = -1
    
	try:
	    if _argsObj.arguments.has_key('host'):
		_host = _argsObj.arguments['host']
	except:
	    pass
	    
	try:
	    if _argsObj.arguments.has_key('username'):
		_username = _argsObj.arguments['username']
	except:
	    pass
	    
	try:
	    if _argsObj.arguments.has_key('password'):
		_password = _argsObj.arguments['password']
	except:
	    pass
	    
	try:
	    if _argsObj.arguments.has_key('destpath'):
		_destpath = os.path.abspath(_argsObj.arguments['destpath'])
	    else:
		_destpath = ''
	except:
	    _destpath = ''
	    
	try:
	    if _argsObj.arguments.has_key('binpath'):
		_binpath = os.path.abspath(_argsObj.arguments['binpath'])
	    else:
		_binpath = ''
	except:
	    _binpath = ''

	if (os.path.exists(_destpath)) and (os.path.exists(_binpath)) and (_maxbackups > -1) and (len(_host) > 0) and (len(_username) > 0) and (len(_password) > 0):
	    if (_freq > -1):
		while (1):
		    main(_host,_username,_password,_destpath,_binpath,_maxbackups)
		    time.sleep(_freq)
	    else:
		main(_host,_username,_password,_destpath,_binpath,_maxbackups)
	else:
	    print 'ERROR :: Unable to launch this program using the arguments as listed below.'
	    ppArgs()
	    print str(sys.argv)

