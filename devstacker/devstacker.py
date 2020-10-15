import os
import sys
import time

import re
import zipfile
import logging

__normalize__ = lambda fp:fp.replace('/',os.sep) if (fp) else fp
__denormalize__ = lambda fp:fp.replace(os.sep,'/') if (fp) else fp

__version__ = '1.0.0.0'
name = 'devstacker%s' % (__version__)

if (__name__ == '__main__'):
    ### BEGIN: LOGGING ###############################################################
    logger = logging.getLogger(name)
    logger.setLevel = logging.INFO
    logging.basicConfig(level=logger.level)
    
    stderr_log_handler = logging.StreamHandler()
    logger.addHandler(stderr_log_handler)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fpath = os.path.dirname(sys.argv[0])
    fpath = fpath if (len(fpath) > 0) else __normalize__(os.path.expanduser('~/logs'))
    if (not os.path.exists(os.path.dirname(fpath))):
	os.makedirs(fpath)
    log_fname = '%s/%s_%s.log' % (fpath,name,time.time())
    log_fname = __normalize__(log_fname)
    file_log_handler = logging.FileHandler(log_fname)
    file_log_handler.setFormatter(formatter)
    logger.addHandler(file_log_handler)
    stderr_log_handler.setFormatter(formatter)
    stderr_log_handler.setLevel = logger.level
    
    print 'DEBUG: Logging to "%s".' % (log_fname)
    logger.info('devstacker v%s' % (__version__))
    ### END: LOGGING ##################################################################
    
    __adapterpakfilebuilder_symbol__ = 'AdapterPakFileBuilder' ###### DO NOT CHANGE !!! ######
    
    from optparse import OptionParser
    
    parser = OptionParser("usage: %prog [options]")
    parser.add_option('-l', '--logger', dest='logger', help="log messages from SSH interface - can produce a lot of messages when used.", action="store_true")
    parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
    parser.add_option('-i', '--input', dest='input', help="input commands from this file.", action="store", type="string")
    parser.add_option('-d', '--dir', dest='directory', help="the vagrant project directory.", action="store", type="string")
   
    if (len(sys.argv) == 1):
	sys.argv.append('-h')
    
    options, args = parser.parse_args()
    
    __use_tar_for_project_uploads_ = True # this will be made into a real feature in the next release however for now we need to validate this works.    
    
    _isVerbose = False
    if (options.verbose):
	_isVerbose = True
    logger.info('DEBUG: _isVerbose=%s' % (_isVerbose))
    
    _isUsingSSHLogger = False
    if (options.logger):
	_isUsingSSHLogger = True
    logger.info('DEBUG: _isUsingSSHLogger=%s' % (_isUsingSSHLogger))
    
    __input__ = None
    if (options.input):
	__input__ = options.input
    logger.info('DEBUG: __input__=%s' % (__input__))
    
    __directory__ = None
    if (options.directory):
	__directory__ = options.directory
    logger.info('DEBUG: __directory__=%s' % (__directory__))
    
    def callersName():
	""" get name of caller of a function """
	import sys
	return sys._getframe(2).f_code.co_name
    
    def formattedException(details='',_callersName=None,depth=None,delims='\n'):
	_callersName = _callersName if (_callersName is not None) else callersName()
	import sys, traceback
	exc_info = sys.exc_info()
	stack = traceback.format_exception(*exc_info)
	stack = stack if ( (depth is None) or (not isInteger(depth)) ) else stack[0:depth]
	try:
	    info_string = delims.join(stack)
	except:
	    info_string = '\n'.join(stack)
	return '(' + _callersName + ') :: "' + str(details) + '". ' + info_string
    
    __imported__ = False

    __zips__ = []
    
    import imp
    logger.info('DEBUG: hasattr(sys, "frozen")=%s' % (hasattr(sys, "frozen")))
    logger.info('DEBUG: hasattr(sys, "importers")=%s' % (hasattr(sys, "importers")))
    logger.info('DEBUG: imp.is_frozen("__main__")=%s' % (imp.is_frozen("__main__")))
    if (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__")):
	import pkg_resources
    
	__regex_libname__ = re.compile(r"(?P<libname>.*)_2_7\.zip", re.MULTILINE)
	
	my_file = pkg_resources.resource_stream('__main__',sys.executable)
	if (_isVerbose):
	    logger.info('%s' % (my_file))
    
	import tempfile
	__dirname__ = os.path.dirname(tempfile.NamedTemporaryFile().name)
	logger.debug('__dirname__=%s' % (__dirname__))
    
	zip = zipfile.ZipFile(my_file)
	files = [z for z in zip.filelist]
	logger.debug('files=%s' % (files))
	for f in files:
	    try:
		libname = f.filename
		if (_isVerbose):
		    logger.debug('1. libname=%s' % (libname))
		if (libname.lower().endswith('.zip')):
		    data = zip.read(libname)
		    fp = os.path.splitext(libname)[0]
		    if (fp.find('/') > -1):
			fpath = __normalize__(__dirname__)
		    else:
			fpath = __normalize__(os.sep.join([__dirname__,fp]))
		    __is__ = False
		    if (os.path.exists(fpath)):
			fsize = os.path.getsize(fpath)
			if (_isVerbose):
			    logger.debug('3. fsize=%s' % (fsize))
			    logger.debug('4. f.file_size=%s' % (f.file_size))
			if (fsize != f.file_size):
			    __is__ = True
			    if (_isVerbose):
				logger.debug('5. __is__=%s' % (__is__))
		    fname = os.sep.join([fpath,__normalize__(libname)])
		    if (not os.path.exists(fname)) or (__is__):
			if (_isVerbose):
			    logger.debug('6. fname=%s' % (fname))
			fp = os.path.dirname(fname)
			if (not os.path.exists(fp)):
			    os.makedirs(fp)
			file = open(fname, 'wb')
			file.write(data)
			file.flush()
			file.close()
		    if (__regex_libname__.match(f.filename)):
			__module__ = fname
			if (_isVerbose):
			    logger.info('7. __module__=%s' % (__module__))
		
			if (_isVerbose):
			    logger.info('__module__ --> "%s".' % (__module__))
		
			import zipextimporter
			zipextimporter.install()
			sys.path.insert(0, __module__)
			
			__imported__ = True
		    else:
			logger.info('DEBUG: ZIP=%s' % (f.filename))
			__zips__.append(fname)
	    except Exception, details:
		logger.exception('EXCEPTION: %s\n%s' % (details,formattedException(details=details)))
    else:
	fpath = os.path.abspath('./zips')
	if (os.path.exists(fpath)):
	    for f in [ff for ff in os.listdir(fpath) if (str(os.path.splitext(ff)[-1]).lower() == '.zip')]:
		fname = os.sep.join([fpath,f])
		logger.info('DEBUG: ZIP=%s' % (fname))
		__zips__.append(fname)
    
	if (_isVerbose and __imported__):
	    logger.info('BEGIN:')
	    for f in sys.path:
		print f
	    logger.info('END !!')
    
    logger.info('DEBUG: __zips__=%s' % (__zips__))
	
    import atexit
    @atexit.register
    def __terminate__():
	import os, signal
	pid = os.getpid()
	os.kill(pid,signal.SIGTERM)
    
    from vyperlogix import paramiko
    
    from vyperlogix.daemon.daemon import Log
    from vyperlogix.daemon.daemon import CustomLog
    from vyperlogix.logging import standardLogging
    
    from vyperlogix import misc
    from vyperlogix.misc import _utils
    
    from vyperlogix.lists.ListWrapper import ListWrapper
    
    from vyperlogix.classes.SmartObject import SmartObject
    
    from vyperlogix.misc import ObjectTypeName
    from vyperlogix.hash import lists
    
    from vyperlogix.tar import tarutils
    
    from vyperlogix.enum import Enum
    
    __devstacker_symbol__ = 'devstacker'
    
    #__reIF__ = re.compile(r"IF NOT EXISTS (/)?([^/\0]+(/)?)+ THEN mkdir (/)?([^/\0]+(/)?)+", re.DOTALL | re.MULTILINE)
    
    if (_isVerbose):
	from vyperlogix.misc import ioTimeAnalysis
	ioTimeAnalysis.initIOTime(__devstacker_symbol__)
	ioTimeAnalysis.ioBeginTime(__devstacker_symbol__)
    
    class EntityType(Enum.Enum):
	none = 0
    
    __ip__ = None #'16.83.121.123'
    if (len(args) > 0):
	__ip__ = args[0] if (_utils.is_ip_address_valid(args[0])) else None
    
    __port__ = 2222
    
    __username__ = 'vagrant'

    if (_isVerbose):
	if (__input__ is not None):
	    logger.info('input is %s' % (__input__ ))
	if (__directory__ is not None):
	    logger.info('directory is %s' % (__directory__ ))
	if (__ip__ is not None):
	    logger.info('ip is %s' % (__ip__))
	if (__port__ is not None):
	    logger.info('port is %s' % (__port__))
	if (__username__ is not None):
	    logger.info('username is %s' % (__username__))
	if (_isUsingSSHLogger is not None):
	    logger.info('logger is %s' % (_isUsingSSHLogger))
    
    __home_directory__ = os.path.expanduser("~")
    
    __ssh_directory__ = os.sep.join([__home_directory__,'ssh'])
    if (not os.path.exists(__ssh_directory__)):
	os.makedirs(__ssh_directory__)
    __ssh_known_hosts__ = os.sep.join([__ssh_directory__,'known_hosts'])
    if (not os.path.exists(__ssh_known_hosts__)):
	fOut = open(__ssh_known_hosts__,'w')
	print >> fOut, ''
	fOut.flush()
	fOut.close()
    
    def __sftp__():
	return paramiko.ParamikoSFTP(__ip__,int(__port__),__username__,password=__password__,callback=None,use_manual_auth=True,auto_close=False,logger=logger if (_isUsingSSHLogger) else None)
    
    def __callback__(size, file_size):
	pcent = size/file_size
	if (pcent > 0.0):
	    logger.info('%4.2f %%' % ((size/file_size)*100.0))

    logger.info('BEGIN:')
    #########################################################################
    
    if (os.path.exists(__input__)):
	requires_tokens = ['Host:','Port:','Username:','Private key:']
	
	oBuf = _utils.stringIO()
	
	from vyperlogix.process.shell import SmartShell

	__cmd__ = 'cd "%s" & vagrant %s' % (__directory__,'ssh')
	ss = SmartShell(sysout=oBuf)
	ss.execute(command=__cmd__)
	
	lines = [str(l).rstrip() for l in oBuf.getvalue().split('\n')]
	
	__required__ = SmartObject()
	for l in lines:
	    for r in requires_tokens:
		if (l.find(r) > -1):
		    toks = [str(t).strip() for t in l.split(':')]
		    __required__[toks[0].replace(' ','_')] = ':'.join(toks[1:])
		    break
    
	if (1):
	    ####################################
	    #__required__.Host = '16.83.121.123'
	    __required__.Host = '192.168.1.21'
	    __required__.Port = '22'
	    __required__.Username = 'root'
	    __required__.Password = 'Compaq123'
	    ####################################
		
	__host__ = __required__.Host
	if (not misc.isStringValid(__host__)):
	    logger.error('ERROR: Cannot proceed without a valid ip address that must be the first argument before any options.')
	    __terminate__()
	    
	import paramiko
	
	ssh = paramiko.SSHClient()
	ssh.load_system_host_keys()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	if (__required__.Private_key):
	    print 'Connecting with vagrant VM Host=%s:%s, Username=%s, Private_key=%s' % (__host__,__required__.Port,__required__.Username,__required__.Private_key)
	    ssh.connect(__host__, username=__required__.Username, port=int(__required__.Port), look_for_keys=False, key_filename=__required__.Private_key)
	else:
	    print 'Connecting with VM Host=%s:%s, Username=%s, Password=%s' % (__host__,__required__.Port,__required__.Username,__required__.Password)
	    ssh.connect(__host__, username=__required__.Username,password=__required__.Password, port=int(__required__.Port), allow_agent=False, look_for_keys=False)
	#ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls -la', timeout=30)
	#for l in ssh_stdout:
	    #print 'SSH_STDOUT: %s' % (l)
	#for l in ssh_stderr:
	    #print 'SSH_STDERR: %s' % (l)
	
	fIn = open(__input__, 'r')
	for item in fIn:
	    print 'BEGIN: %s' % ('='*40)
	    print item
	    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(item, timeout=30)
	    for l in ssh_stdout:
		print 'SSH_STDOUT: %s' % (l)
	    for l in ssh_stderr:
		print 'SSH_STDERR: %s' % (l)
	    print 'END: %s' % ('='*40)
	fIn.close()

	ssh.close()	    
    else:
	logger.warning('Cannot proceed without an input file using -i or --input.')

    #sftp = __sftp__()
    #cmd = 'rm %s' % (sname_dest)
    #responses = sftp.exec_command(cmd)
    #logger.info(cmd)
    #logger.info('\n'.join(responses))

    #########################################################################
    logger.info('END!')
    
    #sftp.close()

    if (_isVerbose):
	ioTimeAnalysis.ioEndTime(__devstacker_symbol__)
	ioTimeAnalysis.ioTimeAnalysisReport()
