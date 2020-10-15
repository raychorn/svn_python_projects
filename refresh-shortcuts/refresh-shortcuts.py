import os, sys

import logging

_isVerbose = False # defined here to satisfy py2exe runtime issues.

verbose = False
import imp
if (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__")):
    import zipfile
    import pkg_resources

    import re
    __regex_libname__ = re.compile(r"(?P<libname>.*)_2_7\.zip", re.MULTILINE)

    my_file = pkg_resources.resource_stream('__main__',sys.executable)
    if (verbose):
        print '%s' % (my_file)

    import tempfile
    __dirname__ = os.path.dirname(tempfile.NamedTemporaryFile().name)

    zip = zipfile.ZipFile(my_file)
    files = [z for z in zip.filelist if (__regex_libname__.match(z.filename))]
    for f in files:
        libname = f.filename
        if (verbose):
            print '1. libname=%s' % (libname)
        data = zip.read(libname)
        fpath = os.sep.join([__dirname__,os.path.splitext(libname)[0]])
        __is__ = False
        if (not os.path.exists(fpath)):
            if (verbose):
                print '2. os.mkdir("%s")' % (fpath)
            os.mkdir(fpath)
        else:
            fsize = os.path.getsize(fpath)
            if (verbose):
                print '3. fsize=%s' % (fsize)
                print '4. f.file_size=%s' % (f.file_size)
            if (fsize != f.file_size):
                __is__ = True
                if (verbose):
                    print '5. __is__=%s' % (__is__)
        fname = os.sep.join([fpath,libname])
        if (not os.path.exists(fname)) or (__is__):
            if (verbose):
                print '6. fname=%s' % (fname)
            file = open(fname, 'wb')
            file.write(data)
            file.flush()
            file.close()
        __module__ = fname
        if (verbose):
            print '7. __module__=%s' % (__module__)

        if (verbose):
            print '__module__ --> "%s".' % (__module__)

        import zipextimporter
        zipextimporter.install()
        sys.path.insert(0, __module__)

    if (verbose):
        print 'BEGIN:'
        for f in sys.path:
            print f
        print 'END !!'
    
import atexit
@atexit.register
def __terminate__():
    import os, signal
    pid = os.getpid()
    os.kill(pid,signal.SIGTERM)

import simplejson

from vyperlogix.daemon.daemon import Log
from vyperlogix.daemon.daemon import CustomLog
from vyperlogix.logging import standardLogging

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.win import folders
from vyperlogix.win import windowsShortcuts

__version__ = '1.0.0.0'

### BEGIN: LOGGING ###############################################################
__cwd__ = os.path.expanduser("~")
name = _utils.getProgramName()
fpath = __cwd__
_log_path = _utils.safely_mkdir_logs(fpath=fpath)
_log_path = _utils.safely_mkdir(fpath=_log_path,dirname=_utils.timeStampLocalTimeForFileName(delimiters=('_','-'),format=_utils.formatSalesForceTimeStr()))
if (not os.path.exists(_log_path)):
    print >> sys.stderr, 'Logging path does not exist at "%s".' % (_log_path)
    __terminate__()

logFileName = os.sep.join([_log_path,'%s.log' % (name)])

print '(%s) :: Logging to "%s".' % (_utils.timeStampLocalTime(),logFileName)

_logging = logging.DEBUG
_console_logging = logging.DEBUG
standardLogging.standardLogging(logFileName,_level=_logging,console_level=_console_logging,isVerbose=_isVerbose)

logger = logging.getLogger('')

def does_nothing(root):
    return True

def requires_vcvatime(root):
    if (_isVerbose):
	logger.info('DEBUG: requires_vcvatime --> %s' % (root))
    return root.find('vcva-time') > -1

target_symbol = 'target'
start_in_symbol = 'start-in'
description_symbol = 'description'
icon_symbol = 'icon'
source_symbol = 'source'

__required_links__ = {
    'start-hpcs.cmd':{target_symbol:r'C:\workspaces\voyage\start-hpcs.cmd',start_in_symbol:r'C:\workspaces\voyage','top':r'C:\workspaces\voyage','lambda':does_nothing},
    'start-server.cmd':{target_symbol:r'C:\workspaces\voyage\start-server.cmd',start_in_symbol:r'C:\workspaces\voyage','top':r'C:\workspaces\voyage','lambda':does_nothing},
    'start-uim.cmd':{target_symbol:r'C:\workspaces\voyage\start-uim.cmd',start_in_symbol:r'C:\workspaces\voyage','top':r'C:\workspaces\voyage','lambda':does_nothing},
    'stop-all.cmd':{target_symbol:r'C:\workspaces\voyage\stop-all.cmd',start_in_symbol:r'C:\workspaces\voyage','top':r'C:\workspaces\voyage','lambda':does_nothing},
    'vcva-time':{target_symbol:r'C:\Program Files (x86)\_utils\vcva-time\run.cmd',start_in_symbol:r'C:\Program Files (x86)\_utils\vcva-time','top':r'C:\Program Files (x86)','lambda':requires_vcvatime}
}

shutdown_now_cmd_source = '''
@echo off

shutdown /s /f /t 1
'''

reboot_now_cmd_source = '''
@echo off

shutdown /r /f /t 1
'''

__required_commands__ = {
    'shutdown now !!!.cmd':{'source':shutdown_now_cmd_source},
    'reboot now !!!.cmd':{'source':reboot_now_cmd_source}
}

def locateFileByName(likethis,top='c:/',func=does_nothing):
    found = []
    for root, dirs, files in os.walk(top):
	if (root.find('.svn') == -1) and (func(root)):
	    if (_isVerbose):
		logger.info("%s..." % (root))
	    for f in files:
		if (str(f).lower() == str(likethis).lower()):
		    found.append(os.sep.join([root,f]))
		    break
    return found

def validate_required_link_targets(required):
    for k,v in required.iteritems():
	target = v.get(target_symbol,None)
	if (target):
	    fname = os.path.basename(target)
	    func = v.get('lambda',does_nothing)
	    top = v.get('top','C:\\')
	    found = locateFileByName(fname,top=top,func=func)
	    if (len(found) == 0):
		found = locateFileByName(fname,func=func)
		if (_isVerbose):
		    assert len(found) > 0, 'Check this out !!!'
	    v[target_symbol] = found[0] if (len(found) > 0) else v[target_symbol]
	    v[start_in_symbol] = os.path.dirname(v[target_symbol])
	    top = v[start_in_symbol]
	    required[k] = v

def locateShortcut(likethis,top=folders.Desktop()):
    shortcuts = []
    b_likethis = os.path.basename(likethis)
    for root, dirs, files in os.walk(top):
	for f in files:
	    if (_isVerbose):
		try:
		    logger.info(unicode(f).encode('utf-8'))
		except:
		    logger.info('WARNING: Cannot tell you about a file in %s due to some kind of issue with unicode.' % (root))
	    if (os.path.splitext(f)[-1] == '.lnk'):
		logger.debug('f=%s' % (f))
		_fname = os.sep.join([root,f])
		_path = windowsShortcuts.getPathFromShortcut(_fname)
		fname = os.path.basename(_path[0])
		logger.debug('likethis=%s, fname=%s --> likethis.find(fname)=%s' % (likethis,fname,likethis.find(fname)))
		if (b_likethis == fname):
		    shortcuts.append([_fname,_path[0]])
		    logger.debug('(+) %s --> shortcuts=%s' % ((_fname,_path[0]),shortcuts))
    return shortcuts

def locateShortcuts(required,top=folders.Desktop()):
    missing_shortcuts = []
    for k,v in required.iteritems():
	target = v.get(target_symbol,None)
	logger.debug('target=%s' % (target))
	if (target):
	    logger.debug('BEGIN: locateShortcut(%s, top=%s)' % (target,top))
	    shortcuts = locateShortcut(target, top=top)
	    logger.debug('END: locateShortcut(%s, top=%s) --> %s' % (target,top,shortcuts))
	    if (len(shortcuts) == 0):
		logger.debug('missing_shortcuts.append(%s)' % (k))
		missing_shortcuts.append(k)
    return missing_shortcuts

from simplejson import JSONEncoder
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if (callable(obj)):
            # `default` must return a python serializable
            # structure, the easiest way is to load the JSON
            # string produced by `serialize` and return it
            return {'callable':{'__name__':obj.__name__,description_symbol:str(obj)}}
        return JSONEncoder.default(self,obj)

if (__name__ == '__main__'):
    from optparse import OptionParser
    
    parser = OptionParser("usage: %prog [options]")
    parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
    parser.add_option("-w", "--write", action="store", type="string", dest="ofilename")
    parser.add_option("-i", "--input", action="store", type="string", dest="ifilename")
    
    options, args = parser.parse_args()
    
    _isVerbose = False
    if (options.verbose):
	_isVerbose = True
	
    if (options.ofilename):
	ofilename = os.path.abspath(options.ofilename)
	if (_isVerbose):
	    logger.info('ofilename is %s' % (ofilename))
	json = simplejson.dumps(__required_links__,cls=CustomJSONEncoder)
	fOut = open(ofilename, 'w')
	print >> fOut, json
	fOut.flush()
	fOut.close()
	_utils.terminate('Program complete.')
    elif (options.ifilename):
	ifilename = os.path.abspath(options.ifilename)
	if (_isVerbose):
	    logger.info('ifilename is %s' % (ifilename))
	fIn = open(ifilename, 'r')
	json = ''.join(fIn.readlines())
	fIn.close()
	__required_links__ = simplejson.loads(json)
	from vyperlogix.decorators.dictwalk import walk_into, DictWalkOptions

	@walk_into(__required_links__,options=DictWalkOptions.keys_and_values_and_top)
	def __callback__(item):
	    k,v,t = item
	    if (k == 'lambda') and (v.has_key('callable')):
		c = v.get('callable',None)
		if (c):
		    c = eval(c.get('__name__',None))
		    if (c):
			t[k] = c

    else:
	pass
    
    __desktop__ = 'C:/@6/Desktop' if (_utils.isBeingDebugged) else folders.Desktop()
    if (_isVerbose):
	logger.info('__desktop__ is %s' % (__desktop__))
    
    for k,v in __required_links__.iteritems():
	data = v
	if (data):
	    logger.info('Creating shortcut for %s in %s.' % (data, __desktop__))
	    targetPath = data.get(target_symbol,None)
	    workingPath = data.get(start_in_symbol,None)
	    description = data.get(description_symbol,k)
	    iconLocation = data.get(icon_symbol,None)
	    lnkPath = os.sep.join([__desktop__,k+'.lnk'])
	    if (not os.path.exists(lnkPath)):
		logger.info('makeWindowsShortcut("%s", "%s", "%s", "%s", "%s")' % (lnkPath, targetPath, workingPath, description, iconLocation))
		windowsShortcuts.makeWindowsShortcut(lnkPath, targetPath, workingPath, description, iconLocation)
	    else:
		logger.info('Cannot makeWindowsShortcut because it already exists as ("%s", "%s", "%s", "%s", "%s")' % (lnkPath, targetPath, workingPath, description, iconLocation))
    

    for k,v in __required_commands__.iteritems():
	data = v
	if (data):
	    logger.info('Creating command for %s in %s.' % (data, __desktop__))
	    fpath = os.sep.join([__desktop__,k])
	    if (not os.path.exists(fpath)):
		source = data.get(source_symbol,None)
		if (source):
		    logger.info('(+++) Writing source into "%s".' % (fpath))
		    _utils.writeFileFrom(fpath, source, mode='w')
		else:
		    logger.info('Cannot make the command because it has no source in the JSON file.')
	    else:
		logger.info('Cannot make the command because it already exists in "%s"' % (fpath))
