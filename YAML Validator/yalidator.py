import os
import sys
import time

import re
import zipfile
import logging

import json
import yaml

__normalize__ = lambda fp:fp.replace('/',os.sep) if (fp) else fp
__denormalize__ = lambda fp:fp.replace(os.sep,'/') if (fp) else fp

__version__ = '1.0.0.0'
name = 'yalidator%s' % (__version__)

if (__name__ == '__main__'):
    ### BEGIN: LOGGING ###############################################################
    logger = logging.getLogger(name)
    logger.setLevel = logging.INFO
    logging.basicConfig(level=logger.level)
    
    stderr_log_handler = logging.StreamHandler()
    logger.addHandler(stderr_log_handler)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fpath = os.path.dirname(sys.argv[0])
    fpath = fpath if (len(fpath) > 0) else os.path.expanduser('~/logs')
    try:
	if (not os.path.exists(fpath)):
	    os.makedirs(fpath)
    except Exception, ex:
	print >> sys.stderr, '%s' % (ex)
    fpath = __normalize__(fpath)
    log_fname = '%s/%s_%s.log' % (fpath,name,time.time())
    log_fname = __normalize__(log_fname)
    file_log_handler = logging.FileHandler(log_fname)
    file_log_handler.setFormatter(formatter)
    logger.addHandler(file_log_handler)
    stderr_log_handler.setFormatter(formatter)
    stderr_log_handler.setLevel = logger.level
    
    print 'DEBUG: Logging to "%s".' % (log_fname)
    logger.info('yalidator v%s' % (__version__))
    ### END: LOGGING ##################################################################
    
    from optparse import OptionParser
    
    parser = OptionParser("usage: %prog [options]")
    parser.add_option('-i', '--input', dest='input', help="specify the input file name (expects a YAML file)")
    parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
   
    if (len(sys.argv) == 1):
	sys.argv.append('-h')
    
    options, args = parser.parse_args()
    
    __use_tar_for_project_uploads_ = True # this will be made into a real feature in the next release however for now we need to validate this works.    
    
    _isVerbose = False
    if (options.verbose):
	_isVerbose = True
    logger.info('DEBUG: _isVerbose=%s' % (_isVerbose))
    
    __input__ = None
    if (options.input):
	__input__ = options.input
    logger.info('DEBUG: __input__=%s' % (__input__))
    
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
    if (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__")):
	import pkg_resources
    
	__regex_libname__ = re.compile(r"(?P<libname>.*)_2_7\.zip", re.MULTILINE)
	
	my_file = pkg_resources.resource_stream('__main__',sys.executable)
    
	import tempfile
	__dirname__ = os.path.dirname(tempfile.NamedTemporaryFile().name)
    
	zip = zipfile.ZipFile(my_file)
	files = [z for z in zip.filelist]
	for f in files:
	    try:
		libname = f.filename
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
			if (fsize != f.file_size):
			    __is__ = True
		    fname = os.sep.join([fpath,__normalize__(libname)])
		    if (not os.path.exists(fname)) or (__is__):
			fp = os.path.dirname(fname)
			if (not os.path.exists(fp)):
			    os.makedirs(fp)
			file = open(fname, 'wb')
			file.write(data)
			file.flush()
			file.close()
		    if (__regex_libname__.match(f.filename)):
			__module__ = fname
		
			import zipextimporter
			zipextimporter.install()
			sys.path.insert(0, __module__)
			
			__imported__ = True
			__zips__.append(fname)
	    except Exception, details:
		logger.exception('EXCEPTION: %s\n%s' % (details,formattedException(details=details)))
    else:
	fpath = os.path.abspath('./zips')
	if (os.path.exists(fpath)):
	    for f in [ff for ff in os.listdir(fpath) if (str(os.path.splitext(ff)[-1]).lower() == '.zip')]:
		fname = os.sep.join([fpath,f])
		__zips__.append(fname)
    
    import atexit
    @atexit.register
    def __terminate__():
	import os, signal
	pid = os.getpid()
	os.kill(pid,signal.SIGTERM)
    
    from vyperlogix.daemon.daemon import Log
    from vyperlogix.daemon.daemon import CustomLog
    from vyperlogix.logging import standardLogging
    
    from vyperlogix import misc
    from vyperlogix.misc import _utils
    
    __yalidator_symbol__ = 'yalidator'
    
    if (_isVerbose):
	from vyperlogix.misc import ioTimeAnalysis
	ioTimeAnalysis.initIOTime(__yalidator_symbol__)
	ioTimeAnalysis.ioBeginTime(__yalidator_symbol__)
    
    if (_isVerbose):
	if (__input__ is not None):
	    logger.info('input is %s' % (__input__))
    
    logger.info('BEGIN:')
    #########################################################################

    __is__ = os.path.exists(__input__) and os.path.isfile(__input__)
    logger.info('__is__ is %s' % (__is__))
    
    fIn = sys.stdin
    if (__is__):
	fIn = open(__input__)
    else:
	logger.warning('Nothing to do.')
	__terminate__()

    try:
	doc = yaml.load(fIn)
    except Exception, details:
	doc = {'value':'FAILED'}
	logger.error('FAILED:  Please correct your YAML and try again. Check for TABS and Special Chars.')
	logger.exception('EXCEPTION: %s\n%s' % (details,formattedException(details=details)))
	print >> sys.stderr, '='*40
    __json__ = json.dumps(doc, indent=4, sort_keys=True)
    print >> sys.stdout, __json__

    if (__is__):
	fIn.close()

    #########################################################################
    logger.info('END!')
    
    if (_isVerbose):
	ioTimeAnalysis.ioEndTime(__yalidator_symbol__)
	ioTimeAnalysis.ioTimeAnalysisReport()
