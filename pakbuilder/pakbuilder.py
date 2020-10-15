import os
import sys
import time

import re
import zipfile
import logging

__normalize__ = lambda fp:fp.replace('/',os.sep) if (fp) else fp
__denormalize__ = lambda fp:fp.replace(os.sep,'/') if (fp) else fp

__version__ = '1.5.0.0'
name = 'PAKbuilder%s' % (__version__)

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
    logger.info('PAKbuilder v%s' % (__version__))
    ### END: LOGGING ##################################################################
    
    __adapterpakfilebuilder_symbol__ = 'AdapterPakFileBuilder' ###### DO NOT CHANGE !!! ######
    
    from optparse import OptionParser
    
    parser = OptionParser("usage: %prog ip-address [options]")
    parser.add_option('-a', '--adapterpakfilebuilder', dest='adapterpakfilebuilder', help="The fully qualified directory path on Linux box for the parent of the %s directory." % (__adapterpakfilebuilder_symbol__), action="store", type="string")
    parser.add_option('-b', '--buildnumber', dest='buildnumber', help="The Adapter Build Number for the %s/adapter-installer-conf/adapter-config.properties file." % (__adapterpakfilebuilder_symbol__), action="store", type="string")
    parser.add_option('-c', '--copypaktofolder', dest='copypaktofolder', help="Copy the PAK file to a different directory other than the parent of the project source; this allows the PAK file to be copied directly to your local disk in case you run this command from your development VM.", action="store", type="string")
    parser.add_option('-d', '--dest', dest='dest', help="Destination of project, typically the fully qualified directory path of project root on Linux box that matches the %s/adapter-installer-conf/adapter-config.properties::ADAPTER_LOCATION." % (__adapterpakfilebuilder_symbol__), action="store", type="string")
    parser.add_option('-f', '--flags', dest='flags', help="Remote debugging flags.", action="store", type="string")
    parser.add_option('-i', '--incrementbuildnumber', dest='incrementbuildnumber', help="Auto-increments the build number for each build; you must specify the build number but this option automates the build number and the version number in the describe.xml for you otherwise you may wish to change the build number for each build manually.", action="store_true")
    parser.add_option('-k', '--clearbuildnumber', dest='clearbuildnumber', help="clears the build number to match the -b option exactly rather than using the build number from the adapter-config.properties file.", action="store_true")
    parser.add_option('-l', '--logger', dest='logger', help="log messages from SSH interface - can produce a lot of messages when used.", action="store_true")
    parser.add_option('-n', '--adaptername', dest='adaptername', help="The Adapter Name for the %s/adapter-installer-conf/adapter-config.properties file." % (__adapterpakfilebuilder_symbol__), action="store", type="string")
    parser.add_option('-o', '--override', dest='override', help="Override handling the key value of the AdapterKind tag so it does not have to match the adaptername option.", action="store_true")
    parser.add_option('-p', '--port', dest='port', help="linux host ssh port, typically 22", action="store", type="int")
    parser.add_option('-r', '--remotedebugger', dest='remotedebugger', help="Enables remote debugging for the Analytics VM given the ipaddress, port, username, password and destination with override; override will be taken for remote debugging flags like \"server=y,suspend=n,address=8004\" options.", action="store_true")
    parser.add_option('-s', '--source', dest='source', help="Source of project, typically the fully qualified folder path of project root.", action="store", type="string")
    parser.add_option('-u', '--username', dest='username', help="Linux username, typically root", action="store", type="string")
    parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
    parser.add_option('-w', '--password', dest='password', help="Linux password, typically Compaq123", action="store", type="string")
    parser.add_option('-x', '--experimental', dest='experimental', help="Use this one at your own risk however this one exists just for development purposes and may not do anything useful otherwise.", action="store_true")

   
    if (len(sys.argv) == 1):
	sys.argv.append('-h')
    
    options, args = parser.parse_args()
    
    __use_tar_for_project_uploads_ = True # this will be made into a real feature in the next release however for now we need to validate this works.    
    
    _isVerbose = False
    if (options.verbose):
	_isVerbose = True
    logger.info('DEBUG: _isVerbose=%s' % (_isVerbose))
    
    _isExperimental = False
    if (options.experimental):
	_isExperimental = True
    logger.info('DEBUG: _isExperimental=%s' % (_isExperimental))
    
    _isUsingSSHLogger = False
    if (options.logger):
	_isUsingSSHLogger = True
    logger.info('DEBUG: _isUsingSSHLogger=%s' % (_isUsingSSHLogger))
    
    __use_tar__ = True
    
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
    
    __pakbuilder_symbol__ = 'pakbuilder'
    __pakbuilder_eclipse_project_upload_symbol__ = 'pakbuilder-eclipse-project-upload'
    __pakbuilder_eclipse_project_tar_symbol__ = 'pakbuilder-eclipse-project-tar'
    __pakbuilder_eclipse_project_tar_upload_symbol__ = 'pakbuilder-eclipse-project-tar-upload'
    __pakbuilder_eclipse_project_untar_symbol__ = 'pakbuilder-eclipse-project-untar'
    
    from ant_installer import __is_response_iterable__, __is_response_iterable_empty__
    
    if (_isVerbose):
	from vyperlogix.misc import ioTimeAnalysis
	ioTimeAnalysis.initIOTime(__pakbuilder_symbol__)
	ioTimeAnalysis.ioBeginTime(__pakbuilder_symbol__)
    
    class EntityType(Enum.Enum):
	none = 0
	folder = 2^0
	file = 2^1
    
    def unZipInto(_zip,target,isVerbose=False,callback=None):
	try:
	    iterable = None
	    typ = ObjectTypeName.typeClassName(_zip)
	    if (typ == 'zipfile.ZipFile'):
		iterable = (f.filename for f in _zip.filelist)
	    else:
		raise AttributeError('Invalid _zip attribute cann be of type "%s".' % (typ))
	    if (isVerbose):
		print '*** iterable = %s' % (str(iterable))
	    if (iterable):
		for f in iterable:
		    _f_ = __normalize__(f)
		    fname = os.path.join(target,_f_)
		    if (f.endswith('/')):
			if (not os.path.exists(fname)):
			    os.makedirs(fname)
			if (callable(callback)):
			    try:
				callback(EntityType.folder,f)
			    except:
				pass
		    else:
			__bytes__ = _zip.read(f)
			if (isVerbose):
			    print '%s -> %s [%s]' % (f,fname,__bytes__)
			_utils.writeFileFrom(fname,__bytes__,mode='wb')
			if (callable(callback)):
			    try:
				callback(EntityType.file,f,fname)
			    except:
				pass
	except Exception, _details:
	    if (isVerbose):
		print _utils.formattedException(details=_details)
    
    __ip__ = None #'16.83.121.123'
    if (len(args) > 0):
	__ip__ = args[0] if (_utils.is_ip_address_valid(args[0])) else None
    
    normalize = lambda items:[s for s in [''.join(ll[0:ll.findFirstMatching('#') if (ll.findFirstMatching('#') > -1) else len(ll)]).strip() for ll in [ListWrapper(l) for l in items if (len(l) > 0)]] if (len(s) > 0)]

    __remotedebugger__ = False
    if (options.remotedebugger):
	__remotedebugger__ = True
    
    if (not misc.isStringValid(__ip__)):
	logger.error('ERROR: Cannot proceed without a valid ip address that must be the first argument before any options.')
	__terminate__()
    
    __port__ = 22
    if (options.port):
	__port__ = options.port
    
    __username__ = 'root'
    if (options.username):
	__username__ = options.username
    
    __password__ = 'Compaq123'
    if (options.password):
	__password__ = options.password
	
    __source__ = None
    if (options.source):
	__source__ = options.source
    
    __adapterpakfilebuilder__ = None
    __copypaktofolder__ = None
    __adaptername__ = None
    __buildnumber__ = None
    __incrementbuildnumber__ = False
    __override__ = False
    __clearbuildnumber__ = False

    if (not __remotedebugger__):
	if (not __source__) or (not os.path.exists(__source__)) or (not os.path.isdir(__source__)):
	    logger.error('ERROR: Cannot proceed without a valid fully qualified path name as the -s or --source argument on the command line.')
	    __terminate__()
	    
	__dot_project__ = __source__+os.sep+'.project'
	if (not os.path.exists(__dot_project__)) or (not os.path.isfile(__dot_project__)):
	    logger.error('ERROR: Cannot proceed without a valid Eclipse project path as the -s or --source argument on the command line.')
	    __terminate__()
		
	__build_deploy__ = __source__+os.sep+'build'+os.sep+'deploy'
	if (not os.path.exists(__build_deploy__)) or (not os.path.isdir(__build_deploy__)):
	    logger.error('ERROR: Cannot proceed without a valid Eclipse project path as the -s or --source argument on the command line.')
	    __terminate__()
	    
	files = [os.sep.join([__build_deploy__,f]) for f in os.listdir(__build_deploy__) if (os.path.splitext(f)[-1] == '.jar')]
	
	if (len(files) == 0) or (len(files) > 1):
	    logger.error('ERROR: Cannot proceed unless your Eclipse project has been successfully built; there should be no more than a single jar file and there is not at this time.')
	    __terminate__()

	if (options.adapterpakfilebuilder):
	    __adapterpakfilebuilder__ = options.adapterpakfilebuilder
	
	if (not __adapterpakfilebuilder__):
	    logger.error('ERROR.1: Cannot proceed without a valid fully qualified %s path name as the -a or --adapterpakfilebuilder argument on the command line.' % (__adapterpakfilebuilder_symbol__))
	    __terminate__()
	
	if (options.copypaktofolder):
	    __copypaktofolder__ = options.copypaktofolder
	
	if (options.adaptername):
	    __adaptername__ = options.adaptername
	
	if (not __adaptername__):
	    logger.error('ERROR: Cannot proceed without adapter name as the -n or --adaptername argument on the command line.')
	    __terminate__()
	
	if (options.buildnumber):
	    __buildnumber__ = options.buildnumber
	
	if (not __buildnumber__):
	    logger.error('ERROR: Cannot proceed without adapter build number as the -b or --buildnumber argument on the command line.')
	    __terminate__()
	    
	if (options.clearbuildnumber):
	    __clearbuildnumber__ = options.clearbuildnumber
	
	if (options.incrementbuildnumber):
	    __incrementbuildnumber__ = True
	
	if (options.override):
	    __override__ = True
	
	
    __dest__ = None
    if (options.dest):
	__dest__ = options.dest
	
    __flags__ = None
    if (options.flags):
	__flags__ = options.flags
    
    if (not __dest__):
	logger.error('ERROR.1: Cannot proceed without a valid fully qualified destination path name as the -d or --dest argument on the command line.')
	__terminate__()
    
    if (not __remotedebugger__):
	source_root = __normalize__(__source__.replace(os.path.dirname(__source__),''))
	logger.info('source_root is "%s".' % (source_root))
	source_bias = __source__.replace(source_root,'')
	logger.info('source_bias is "%s".' % (source_bias))
	__build_deploy__ = __normalize__('%s%s/build/deploy' % (__dest__,source_root))
	logger.info('__build_deploy__ is "%s".' % (__build_deploy__))
	__expected_jar__ = '%s.jar' % (__adaptername__)
	__source_build_deploy__ = __normalize__('%s/build/deploy' % (__source__))
	if (not os.path.exists(__source_build_deploy__)):
	    __source_build_deploy__ = __source__
	logger.info('__source_build_deploy__ is "%s".' % (__source_build_deploy__))
	__source_conf__ = __normalize__('%s/conf' % (__source__))
	if (not os.path.exists(__source_conf__)):
	    __source_conf__ = __source__
	logger.info('__source_conf__ is "%s".' % (__source_conf__))
    
    def handle_describe_xml_file():
	__has_expected_jar__ = False
	__found_jar__ = None
	__handled_expected_xml__ = False
	logger.info('Begin handling the describe.xml file.')
	for dirname,folders,files in _utils.walk(__source_build_deploy__):
	    logger.info('Begin first pass through folders in "%s" while handling the describe.xml file.' % (dirname))
	    for f in folders:
		_f_ = dirname+os.sep+f
		if (_f_.find('%sbuild%sdeploy%s' % (os.sep,os.sep,os.sep)) > -1):
		    if (__expected_jar__ in files):
			__has_expected_jar__ = True
			break
		    else:
			found_jars = [n for n in files if (n.find('.jar') > -1)]
			__found_jar__ = found_jars[0] if (len(found_jars) > 0) else __found_jar__
	    logger.info('Done with first pass through folders in "%s" while handling the describe.xml file.' % (dirname))
	for dirname,folders,files in _utils.walk(__source_conf__):
	    if ((not __handled_expected_xml__) and __incrementbuildnumber__ and (dirname.find('%sbuild%sdeploy%s' % (os.sep,os.sep,os.sep)) == -1)):
		logger.info('Begin second pass through files in "%s" while handling the describe.xml file.' % (dirname))
		for f in files:
		    if (f == 'describe.xml'):
			_f_ = dirname+os.sep+f
			_b_ = _f_+'.new'
			logger.info('Opening "%s".' % (_f_))
			fIn = open(_f_,'r')
			fOut = open(_b_,'w')
			logger.info('Opening "%s".' % (_b_))
			for l in fIn:
			    logger.info('Reading a line from "%s".' % (fIn.name))
			    if (l.find('<AdapterKind') > -1):
				so = SmartObject(dict([tuple(t.split('=')) for t in l.replace('<','').replace('>','').replace('AdapterKind ','').split(' ')]))
				if (so.version):
				    so.version = '%d' % (int(so.version.replace('"','').strip())+1)
				    if (not __override__) and (so.key.replace('"','') != __adaptername__):
					so.key = __adaptername__
					logger.warning('Seems like your describe.xml file has a problem with the key field of the AdapterKind tag; the key should match the adaptername and this has been changed for you.')
				    d = so.asPythonDict()
				    v = ['%s="%s"' % (k,v) for k,v in d.iteritems()]
				    l = '<AdapterKind %s>' % (' '.join(v))
				    l = l.replace('""','"')
			    l = l.rstrip()
			    if (len(l) > 0):
				print >>fOut, l
			    logger.info('Writing a line into "%s".' % (fOut.name))
			fOut.flush()
			fOut.close()
			logger.info('Closing "%s".' % (fOut.name))
			fIn.close()
			logger.info('Closing "%s".' % (fIn.name))
			
			os.remove(_f_)
			logger.info('Removed "%s".' % (_f_))
			os.rename(_b_, _f_)
			logger.info('Renamed "%s" --> "%s".' % (_b_, _f_))
			__handled_expected_xml__ = True
			break
		logger.info('Done with second pass through files in "%s" while handling the describe.xml file.' % (dirname))
	logger.info('Done handling the describe.xml file.')
	return __has_expected_jar__, __found_jar__, __handled_expected_xml__
    
    if (not __remotedebugger__):
	has_expected_jar, found_jar, handled_expected_xml = handle_describe_xml_file()
	if (_isVerbose):
	    logger.info('INFO: has_expected_jar=%s' % (has_expected_jar))
	    logger.info('INFO: found_jar=%s' % (found_jar))
	    logger.info('INFO: handled_expected_xml=%s' % (handled_expected_xml))
	
	if (not has_expected_jar):
	    logger.error('ERROR: Cannot proceed because there is no jar for the adapter name per the -n or --adaptername argument on the command line.  The expected jar should be %s however found %s instead.' % (__expected_jar__,found_jar))
	    __terminate__()
    
    if (_isVerbose):
	if (__ip__ is not None):
	    logger.info('ip is %s' % (__ip__))
	if (__port__ is not None):
	    logger.info('port is %s' % (__port__))
	if (__username__ is not None):
	    logger.info('username is %s' % (__username__))
	if (__password__ is not None):
	    logger.info('password is %s' % (__password__))
	if (__source__ is not None):
	    logger.info('source is %s' % (__source__))
	if (__dest__ is not None):
	    logger.info('dest is %s' % (__dest__))
	if (__copypaktofolder__ is not None):
	    logger.info('copypaktofolder is %s' % (__copypaktofolder__))
	if (__adapterpakfilebuilder__ is not None):
	    logger.info('adapterpakfilebuilder is %s' % (__adapterpakfilebuilder__))
	if (__adaptername__ is not None):
	    logger.info('adaptername is %s' % (__adaptername__))
	if (__buildnumber__ is not None):
	    logger.info('buildnumber is %s' % (__buildnumber__))
	if (__clearbuildnumber__ is not None):
	    logger.info('clearbuildnumber is %s' % (__clearbuildnumber__))
	if (__incrementbuildnumber__ is not None):
	    logger.info('incrementbuildnumber is %s' % (__incrementbuildnumber__))
	if (__override__ is not None):
	    logger.info('override is %s' % (__override__))
	if (__remotedebugger__ is not None):
	    logger.info('remotedebugger is %s' % (__remotedebugger__))
	if (__flags__ is not None):
	    logger.info('flags is %s' % (__flags__))
	if (_isExperimental is not None):
	    logger.info('experimental is %s' % (_isExperimental))
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

    __adapterpakfilebuilder_home__ = '%s/%s' % (__adapterpakfilebuilder__,__adapterpakfilebuilder_symbol__)
	    
    def __upload_pakbuilder__():
	#########################################
	logger.warning('Cannot locate the "%s" directory on your Linux box so trying to upload this for you.' % (__adapterpakfilebuilder_home__))
	zips = [f for f in __zips__ if (f.find('%s%s.zip'%(os.sep,__adapterpakfilebuilder_symbol__)) > -1)]
	logger.info('DEBUG: zips=%s' % (zips))
	if (len(zips) > 0):
	    adapterpakfilebuilder_home = os.path.splitext(zips[0])[0]
	    logger.info('DEBUG: adapterpakfilebuilder_home=%s' % (adapterpakfilebuilder_home))
	    if (not os.path.exists(adapterpakfilebuilder_home)):
		logger.info('DEBUG: os.makedirs("%s")' % (adapterpakfilebuilder_home))
		os.makedirs(adapterpakfilebuilder_home)
	    ##################################
	    __dstname__ = os.path.dirname(__adapterpakfilebuilder_home__) #+'/__test__/'
	    dstname = __dstname__+os.path.basename(zips[0])
	    logger.info('DEBUG: Preparing to upload "%s" to "%s".' % (zips[0],dstname))
	    sftp = __sftp__()
	    cmd = 'mkdir %s' % (os.path.dirname(dstname))
	    responses = sftp.exec_command(cmd)
	    logger.info(cmd)
	    logger.info('\n'.join(responses))
	    ##################################
	    logger.info('Uploading "%s" --> "%s".' % (zips[0],dstname))
	    sftp = __sftp__()
	    client = sftp.getSFTPClient
	    client.put(zips[0], dstname, callback=__callback__)

	    sftp = __sftp__()
	    cmd = 'ls -la %s' % (__dstname__)
	    responses = sftp.exec_command(cmd)
	    logger.info(cmd)
	    logger.info('\n'.join(responses))
	    lines = [l for l in responses if (l.find('cannot access') > -1) or (l.lower().find('no such file or directory') > -1)]
	    if (len(lines) > 0):
		logger.warning('Cannot locate the newly uploaded file "%s".' % (dstname))
	    else:
		logger.info('Found the newly uploaded file "%s".' % (dstname))

		sftp = __sftp__()
		cmd = 'which unzip'
		responses = sftp.exec_command(cmd)
		logger.info(cmd)
		logger.info('\n'.join(responses))
		lines = [l for l in responses if (l.find('which: no unzip in') > -1)]
		if (len(lines) > 0):
		    logger.warning('Cannot locate the unzip command.')
		else:
		    logger.info('Found the unzip command.')

		    sftp = __sftp__()
		    cmd = 'unzip %s -d %s' % (dstname,__adapterpakfilebuilder__)
		    responses = sftp.exec_command(cmd)
		    logger.info(cmd)
		    logger.info('\n'.join(responses))
	    ##################################
    
    logger.info('BEGIN:')
    #########################################################################
    if (__remotedebugger__):
	__comparefiles_bash_script__ = '''
#!/bin/bash

if [ -f "$1" ]; then 
    echo "$1 exists."
else
    echo "Cannot locate $1. Aborting."
    exit 1
fi

if [ -f "$2" ]; then 
    echo "$2 exists."
else
    echo "Cannot locate $2. Aborting."
    exit 1
fi

d=$(diff $1 $2)
if [ $? -eq 0 ]; then
  echo Same
else
  echo Different
fi	'''
	#########################################################################
	logger.info('REMOTE DEBUGGER:')
	sftp = __sftp__()
	cmd = 'find / -iname %s | grep %s' % (os.path.basename(__dest__),__dest__)
	responses = sftp.exec_command(cmd)
	logger.info(cmd)
	logger.info('%s' % ('='*40))
	for l in responses:
	    logger.info(l)
	logger.info('%s' % ('='*40))
	lines = [l for l in responses if (len(l.strip()) > 0) if (len(l.strip().split('/')) > 1)]
	logger.info('DEBUG: len(lines)=%s.' % (len(lines)))
	if (len(lines) == 0):
	    logger.warning('Cannot proceed without a valid destination which should be something like "collector/wrapper.conf" as the -d or --dest argument on the command line.  Either the IP Address is not for the Analytics VM or the ANalytics VM has become corrupted.')
	else:
	    fname = lines[0]
	    logger.info('Using "%s" for the wrapper.conf file.' % (fname))

	    import datetime
	    today = datetime.datetime.now()
	    ts = '%s%s%s%s%s%s' % (today.year,today.month,today.day,today.hour,today.minute,today.second)
	    
	    wrapper_conf_backup_name = '%s.backup.%s' % (fname,ts)
	    
	    sftp = __sftp__()
	    cmd = 'cp %s %s' % (fname,wrapper_conf_backup_name)
	    responses = sftp.exec_command(cmd)
	    logger.info(cmd)
	    logger.info('\n'.join(responses))
	    
	    tpath = _utils.tempFile(os.path.basename(__home_directory__), useTemporaryFile=True)
	    logger.info('DEBUG: tpath=%s' % (tpath))

	    sname = '%s%scomparefiles.sh' % (os.path.expanduser('~'),os.sep)
	    fOut = open(sname,'w')
	    print >>fOut, __comparefiles_bash_script__
	    fOut.flush()
	    fOut.close()
	    
	    sftp = __sftp__()
	    cmd = 'echo ${HOME}'
	    responses = sftp.exec_command(cmd)
	    logger.info(cmd)
	    logger.info('\n'.join(responses))
	    lines = [l for l in responses if (len(l.strip()) > 0) if (len(l.strip().split('/')) > 1)]
	    if (len(lines) == 0):
		logger.warning('Cannot proceed without a valid Home directory for the user who is being used as the user context for this program. This should never happen unless your Linux box is broken.')
	    else:
		__linux_home__ = lines[0] # '/tmp'
	    
		sname_dest = '%s/%s' % (__linux_home__,os.path.basename(sname))
		logger.info('(+++) scp put.1 "%s" --> "%s".' % (sname, sname_dest))

		sftp = __sftp__()
		cmd = 'rm %s' % (sname_dest)
		responses = sftp.exec_command(cmd)
		logger.info(cmd)
		logger.info('\n'.join(responses))

		sftp = __sftp__()
		sftp.put(sname, sname_dest,callback=__callback__)

		sftp = __sftp__()
		cmd = 'ls -la %s' % (sname_dest)
		responses = sftp.exec_command(cmd)
		logger.info(cmd)
		logger.info('\n'.join(responses))
		lines = [l for l in responses if (l.find('cannot access') > -1) or (l.lower().find('no such file or directory') > -1)]
		if (len(lines) > 0):
		    logger.warning('Camnnot continue unless "%s" exists and it should under programmatic control however this is not the case.' % (sname_dest))
		    __terminate__()

		sftp = __sftp__()
		cmd = 'ls -la %s' % (sname_dest)
		responses = sftp.exec_command(cmd)
		logger.info(cmd)
		logger.info('\n'.join(responses))
		lines = [l for l in responses if (l.find('cannot access') > -1) or (l.lower().find('no such file or directory') > -1)]
		if (len(lines) > 0):
		    logger.warning('Camnnot continue unless "%s" exists and it should under programmatic control however this is not the case.' % (sname_dest))
		    __terminate__()

		sftp = __sftp__()
		cmd = 'chmod +x %s' % (sname_dest)
		responses = sftp.exec_command(cmd)
		lines = []
		logger.debug('1. __is_response_iterable__(responses)=%s' % (__is_response_iterable__(responses)))
		if (__is_response_iterable__(responses)):
		    logger.debug('2. type(responses[0])=%s' % (type(responses[0])))
		    lines = responses[0].split('\n')
		elif (not __is_response_iterable_empty__(responses)):
		    logger.debug('3. type(responses)=%s' % (type(responses)))
		    lines = responses.split('\n')
		else:
		    logger.debug('4. type(responses)=%s' % (type(responses)))
		logger.debug('5. __is_response_iterable__(responses)=%s' % (__is_response_iterable__(responses)))
		lines = [l.strip() for l in lines if (len(l.strip()) > 0)]
		logger.info(cmd)
		logger.info('\n'.join(responses))

		sftp = __sftp__()
		cmd = 'cat %s' % (sname_dest)
		responses = sftp.exec_command(cmd)
		logger.info(cmd)
		logger.info('\n'.join(responses))
		lines = [l for l in responses if (l.find('cannot access') > -1) or (l.lower().find('no such file or directory') > -1)]
		if (len(lines) > 0):
		    logger.warning('Camnnot continue unless "%s" exists and it should under programmatic control however this is not the case.' % (sname_dest))
		    __terminate__()

		sftp = __sftp__()
		cmd = '%s %s %s' % (sname_dest,fname,wrapper_conf_backup_name)
		responses = sftp.exec_command(cmd)
		__lines__ = [r.split('\n') for r in responses] if (__is_response_iterable__(responses)) else responses.split('\n')
		lines = []
		for l in __lines__:
		    for ll in l:
			lines.append(ll.strip())
		lines = [l.strip() for l in lines if (len(l.strip()) > 0)]
		errors = [l.strip() for l in lines if (l.strip().find('Aborting') > -1)]
		sames = [l.strip() for l in lines if (l.strip().find('Same') > -1)]
		logger.info(cmd)
		logger.info('\n'.join(responses))

		logger.debug('len(errors)=%s' % (len(errors)))
		if (len(errors) > 0):
		    logger.warning('1. Cannot proceed unless "%s" and "%s" are the same file at this time.' % (fname,wrapper_conf_backup_name))
		    __terminate__()
		    
		logger.debug('len(sames)=%s' % (len(sames)))
		if (len(sames) == 0):
		    logger.warning('2. Cannot proceed unless "%s" and "%s" are the same file at this time.' % (fname,wrapper_conf_backup_name))
		    __terminate__()
		    
		if (os.path.exists(sname)):
		    logger.debug('os.remove("%s")' % (sname))
		    os.remove(sname)
		    
		sftp = __sftp__()
		cmd = 'rm %s' % (sname_dest)
		responses = sftp.exec_command(cmd)
		logger.info(cmd)
		logger.info('\n'.join(responses))
	
		####################################################################
		## cat wrapper.conf to console and download.
		#####################################################################
		try:
		    sftp = __sftp__()
		    client = sftp.getSFTPClient
		    content = client.read(sftp,fname)
		    local_fname = '%s%s%s' % (os.path.expanduser('~'),os.sep,os.path.basename(fname))
		    fOut = open(local_fname,'w')
		    print >> fOut, content
		    fOut.flush()
		    fOut.close()
		    logger.info('INFO: "%s" <-- "%s"' % (local_fname, fname))
		except paramiko.paramiko.ChannelException:
		    logger.warning('Cannot proceed without a valid wrapper.conf file for the collector and it appears the target machine has been locked-down for SCP. Sorry.')
		    __terminate__()

		#sftp = __sftp__()
		#cmd = 'cat %s' % (fname)
		#responses = sftp.exec_command(cmd)
		#__lines__ = lines = responses
		#lines = [l.strip() for l in lines if (len(l.strip()) > 0)]
		#errors = [l.strip() for l in lines if (l.strip().find('No such file or directory') > -1)]
		#logger.info(cmd)
		#logger.info('\n'.join(responses))
		#if (len(errors) > 0):
		    #logger.warning('Cannot proceed without a valid wrapper.conf file for the collector.')
		    #__terminate__()
    
		#####################################################################
		### write wrapper.conf to local file
		######################################################################
		#local_fname = '%s%s%s' % (os.path.expanduser('~'),os.sep,os.path.basename(fname))
		#fOut = open(local_fname,'w')
		#for l in __lines__:
		    #print >>fOut, l.rstrip()
		#fOut.flush()
		#fOut.close()
		#logger.info('INFO: "%s" <-- "%s"' % (local_fname, fname))
    
		####################################################################
		## parse and correct wrapper.conf
		#####################################################################
		from wrapper_conf_handler import parse_and_resequence
    
		__new_lines__ = parse_and_resequence(local_fname)
    
		local_wrapper_conf_new_name = '%s.new.%s' % (local_fname,ts)
    
		fOut = open(local_wrapper_conf_new_name,'w')
		print >>fOut, __new_lines__
		fOut.flush()
		fOut.close()
		
		####################################################################
		## upload to remote
		#####################################################################
    
		sftp = __sftp__()
		responses = sftp.put(local_wrapper_conf_new_name, fname,callback=__callback__)
		logger.info('SCP "%s" --> "%s"' % (local_wrapper_conf_new_name, fname))
		logger.debug('\n'.join(responses))
		
		####################################################################
		## restart collector
		#####################################################################
		
		logger.info('Done with remotedebugger setup !!!')
	#########################################################################
    else:
	logger.info('PAKBUILDER:')
	__count__ = 0
	while (1):
	    sftp = __sftp__()
	    cmd = 'ls -la %s' % (__dest__)
	    responses = sftp.exec_command(cmd)
	    logger.info(cmd)
	    logger.info('\n'.join(responses))
	    lines = [l for l in responses if (l.find('cannot access') > -1) or (l.lower().find('no such file or directory') > -1)]
	    if (len(lines) > 0):
		__count__ += 1
		if (__count__ > 1):
		    logger.warning('1. Cannot proceed without a valid fully qualified and valid dest path name as the -d or --dest argument on the command line.')
		    break
		sftp = __sftp__()
		cmd = 'mkdir %s' % (__dest__)
		responses = sftp.exec_command(cmd)
		logger.info(cmd)
		logger.info('\n'.join(responses))
	    else:
		break
	sftp = __sftp__()
	cmd = 'ls -la %s' % (__dest__)
	responses = sftp.exec_command(cmd)
	logger.info(cmd)
	logger.info('\n'.join(responses))
	lines = [l for l in responses if (l.find('cannot access') > -1) or (l.lower().find('no such file or directory') > -1)]
	if (len(lines) > 0):
	    logger.warning('2. Cannot proceed without a valid fully qualified and valid dest path name as the -d or --dest argument on the command line.')
	else:
	    __count__ = 0
	    while (1):
		sftp = __sftp__()
		cmd = 'ls -la %s' % (__adapterpakfilebuilder__)
		responses = sftp.exec_command(cmd)
		logger.info(cmd)
		logger.info('\n'.join(responses))
		lines = [l for l in responses if (l.find('cannot access') > -1) or (l.lower().find('no such file or directory') > -1)]
		if (len(lines) > 0):
		    __count__ += 1
		    if (__count__ > 1):
			logger.warning('1. Cannot proceed without a valid fully qualified and valid %s path name as the -a or --adapterpakfilebuilder argument on the command line.' % (__adapterpakfilebuilder_symbol__))
			break
		    __upload_pakbuilder__()
		else:
		    break
	    #####################################################
	    __count__ = 0
	    while (1):
		sftp = __sftp__()
		cmd = 'ls -la %s/%s' % (__adapterpakfilebuilder__,__adapterpakfilebuilder_symbol__)
		responses = sftp.exec_command(cmd)
		logger.info(cmd)
		logger.info('\n'.join(responses))
		lines = [l for l in responses if (l.find('cannot access') > -1) or (l.lower().find('no such file or directory') > -1)]
		if (len(lines) > 0):
		    __count__ += 1
		    if (__count__ > 1):
			logger.warning('2. Cannot proceed without a valid fully qualified and valid %s path name as the -a or --adapterpakfilebuilder argument on the command line.' % (__adapterpakfilebuilder_symbol__))
			break
		    __upload_pakbuilder__()
		else:
		    break
	    #####################################################
	    sftp = __sftp__()
	    cmd = 'ls -la %s' % (__adapterpakfilebuilder__)
	    responses = sftp.exec_command(cmd)
	    logger.info(cmd)
	    logger.info('\n'.join(responses))
	    lines = [l for l in responses if (l.find('cannot access') > -1) or (l.lower().find('no such file or directory') > -1)]
	    if (len(lines) > 0):
		logger.warning('Cannot proceed without a valid fully qualified and valid %s path name as the -a or --adapterpakfilebuilder argument on the command line.' % (__adapterpakfilebuilder_symbol__))
	    else:
		lines = [l for l in responses if (l.find(__adapterpakfilebuilder_symbol__) > -1)]
		if (len(lines) == 0):
		    logger.warning('Cannot proceed without a valid fully qualified and valid %s path name as the -a or --adapterpakfilebuilder argument on the command line; cannot find the %s directory in "%s".' % (__adapterpakfilebuilder_symbol__,__adapterpakfilebuilder_symbol__,__adapterpakfilebuilder__))
		else:
		    dirname = os.path.basename(__source__)
		    logger.info('dirname=%s' % (dirname))
		    sftp = __sftp__()
		    cmd = 'ls -la %s/%s' % (__dest__,dirname)
		    responses = sftp.exec_command(cmd)
		    logger.info(cmd)
		    logger.info('\n'.join(responses))
		    lines = [l for l in responses if (l.find('cannot access') > -1) or (l.lower().find('no such file or directory') > -1)]
		    if (len(lines) == 0):
			sftp = __sftp__()
			cmd = 'rm -rfv %s/%s/*' % (__dest__,dirname)
			responses = sftp.exec_command(cmd)
			logger.info(cmd)
			logger.info('\n'.join(responses))
		    dstname = __denormalize__(__dest__+''+source_root)
		    sftp = __sftp__()
		    cmd = 'mkdir %s' % (dstname)
		    responses = sftp.exec_command(cmd)
		    logger.info(cmd)
		    logger.info('\n'.join(responses))
		    ########################################################################
		    ioTimeAnalysis.ioBeginTime(__pakbuilder_eclipse_project_tar_symbol__)
		    __tar_dest__ = '%s%s%s.tar.gz' % (os.path.dirname(__source__),os.sep,os.path.basename(__source__))
		    logger.info('INFO: tar %s --> %s' % (__source__, __tar_dest__))
		    tarutils.tar_to_file_or_folder(__source__, __tar_dest__,compression=tarutils.TarCompressionTypes.gz)
		    ioTimeAnalysis.ioEndTime(__pakbuilder_eclipse_project_tar_symbol__)
		    ########################################################################
		    if (not __use_tar__):
			ioTimeAnalysis.ioBeginTime(__pakbuilder_eclipse_project_upload_symbol__)
			for dirname,folders,files in _utils.walk(__source__):
			    for f in folders:
				dstname = __denormalize__(__dest__+''+dirname.replace(source_bias,'')+'/'+f)
				sftp = __sftp__()
				cmd = 'mkdir %s' % (dstname)
				responses = sftp.exec_command(cmd)
				logger.info(cmd)
				logger.info('\n'.join(responses))
			for dirname,folders,files in _utils.walk(__source__):
			    for f in files:
				src = dirname+os.sep+f
				dstname = __denormalize__(__dest__+''+dirname.replace(source_bias,'')+'/'+f)
				logger.info('%s --> %s' % (src,dstname))
				sftp = __sftp__()
				responses = sftp.put(src, dstname, callback=__callback__)
				logger.debug('\n'.join(responses))
			ioTimeAnalysis.ioEndTime(__pakbuilder_eclipse_project_upload_symbol__)
		    ########################################################################
		    ioTimeAnalysis.ioBeginTime(__pakbuilder_eclipse_project_tar_upload_symbol__)
		    dstname = __denormalize__(__dest__+'/'+os.path.basename(__tar_dest__))
		    logger.info('INFO: tar upload %s --> %s' % (__tar_dest__, dstname))
		    sftp = __sftp__()
		    responses = sftp.put(__tar_dest__, dstname, callback=__callback__)
		    logger.debug('\n'.join(responses))
		    ioTimeAnalysis.ioEndTime(__pakbuilder_eclipse_project_tar_upload_symbol__)
		    ########################################################################
		    if (__use_tar__):
			########################################################################
			ioTimeAnalysis.ioBeginTime(__pakbuilder_eclipse_project_untar_symbol__)
			sftp = __sftp__()
			cmd = 'tar -zxvf %s -C %s' % (dstname,__dest__)
			responses = sftp.exec_command(cmd)
			logger.info(cmd)
			logger.info('\n'.join(responses))
			ioTimeAnalysis.ioEndTime(__pakbuilder_eclipse_project_untar_symbol__)
			########################################################################
		    fname = '%s/adapter-installer-conf/adapter-config.properties' % (__adapterpakfilebuilder_home__)
		    sftp = __sftp__()
		    cmd = 'ls -la %s' % (__adapterpakfilebuilder_home__)
		    responses = sftp.exec_command(cmd)
		    logger.info(cmd)
		    logger.info('\n'.join(responses))
		    lines = [l for l in responses if (l.find('cannot access') > -1) or (l.lower().find('no such file or directory') > -1)]
		    if (len(lines) > 0):
			pass
		    __original_buildnumber__ = __buildnumber__
		    if (__incrementbuildnumber__):
			logger.info('Automatically adjusting the buildnumber for you based on the last build.')
			sftp = __sftp__()
			cmd = 'cat %s' % (fname)
			responses = sftp.exec_command(cmd)
			lines = responses[0].split('\n') if (__is_response_iterable__(responses)) else responses.split('\n')
			lines = [l.strip() for l in lines if (l.find('ADAPTER_BUILD_NUMBER=') > -1)]
			if (len(lines) > 0):
			    __buildnumber__ = int(lines[0].split('=')[-1])+1
			logger.info(cmd)
			logger.info('\n'.join(responses))
		    if (__clearbuildnumber__):
			logger.info('Clearing the buildnumber back to %s.' % (__original_buildnumber__))
			__buildnumber__ = __original_buildnumber__
		    logger.info('buildnumber is %s' % (__buildnumber__))
		    #########################################
		    tname = os.path.dirname(__source__)+os.sep+'adapter-config.properties'
		    fOut = open(tname,'w')
		    print >> fOut, '''
	ADAPTER_LOCATION=%s%s/build/deploy
	ADAPTER_NAME=%s
	ADAPTER_BUILD_NUMBER=%s
	''' % (__dest__,__denormalize__(source_root),__adaptername__,__buildnumber__)
		    fOut.flush()
		    fOut.close()
		    responses = sftp.put(tname, fname, callback=__callback__)
		    logger.debug('\n'.join(responses))
		    
		    # check for and install rpmbuilder !!!
		    
		    __re__ = re.compile(r".*no\s*ant\s*in.*", re.DOTALL | re.MULTILINE)
	
		    sftp = __sftp__()
		    cmd = 'which ant'
		    responses = sftp.exec_command(cmd)
		    logger.info(cmd)
		    logger.info('\n'.join(responses))
		    lines = [l for l in responses if (__re__.match(l))]
		    lines = [l for l in lines if (len(l) > 0)]
		    __ant__ = None
		    if (len(lines) > 0):
			logger.warning('1. Cannot proceed without ant and it seems your Linux box does not have one installed.')
			logger.info('Installing ant and java, of course, if necessary.')
			try:
			    from ant_installer import install_ant
			    install_ant(__sftp__, logger, callback=__callback__)
			except Exception, ex:
			    logger.error('1. Cannot proceed unless ant has been successfully installed.')
			    logger.exception(_utils.formattedException(details=ex))
			    __terminate__()
		    else:
			sftp = __sftp__()
			cmd = 'find %s -iname ant' % (responses[0].split(':')[-1].strip())
			responses = sftp.exec_command(cmd)
			logger.info(cmd)
			logger.info('\n'.join(responses))
			lines = [l for l in responses if (l.find('/bin/ant') > -1)]
			if (len(lines) == 0):
			    logger.warning('2. Cannot proceed without ant and it seems your Linux box does not have one installed or the installation may have become corrupt.')
			else:
			    __ant__ = lines[0].strip()
			    logger.info('Found ant in %s' % (__ant__))
	    
			    sftp = __sftp__()
			    cmd = 'cd %s/%s; %s -buildfile %s/%s/adapter-installer-conf/adapter-build.xml build.pak' % (__adapterpakfilebuilder__,__adapterpakfilebuilder_symbol__,__ant__,__adapterpakfilebuilder__,__adapterpakfilebuilder_symbol__)
			    responses = sftp.exec_command(cmd)
			    logger.info(cmd)
			    logger.info('\n'.join(responses))
			    lines = [l for l in responses if (l.find('BUILD SUCCESSFUL') > -1)]
			    if (len(lines) == 0):
				logger.warning('Cannot proceed without a successful build.')
			    else:
				sftp = __sftp__()
				cmd = 'ls -la %s/%s' % (__adapterpakfilebuilder__,__adapterpakfilebuilder_symbol__)
				responses = sftp.exec_command(cmd)
				logger.info(cmd)
				logger.info('\n'.join(responses))
				pakname = '%s-%s.pak' % (__adaptername__,__buildnumber__)
				logger.info('Looking for %s' % (pakname))
				lines = [l for l in responses if (l.find(pakname) > -1)]
				if (len(lines) == 0):
				    logger.warning('Cannot proceed without the pak file named %s.' % (pakname))
				else:
				    local_pakname = os.path.dirname(__source__)+os.sep+pakname
				    try:
					if (os.path.exists(__copypaktofolder__)):
					    local_pakname = __copypaktofolder__+os.sep+pakname
					    logger.info('Chaning the location of the resulting PAK file to "%s".' % (__copypaktofolder__))
				    except:
					logger.warning('You might consider using the -c option to make it easier to find your pak file once it has been built or you can find it in "%s".' % (os.path.dirname(__source__)))
				    remote_pakname = '%s/%s/%s' % (__adapterpakfilebuilder__,__adapterpakfilebuilder_symbol__,pakname)
				    logger.info('Downloading %s --> %s' % (remote_pakname,local_pakname))
				    client.get(remote_pakname,local_pakname,callback=__callback__)
    #########################################################################
    logger.info('END!')
    
    sftp.close()

    if (_isVerbose):
	ioTimeAnalysis.ioEndTime(__pakbuilder_symbol__)
	ioTimeAnalysis.ioTimeAnalysisReport()
