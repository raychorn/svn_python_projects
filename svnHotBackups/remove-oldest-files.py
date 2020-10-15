import re
import os, sys

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
        print '1. libname=%s' % (libname)
        data = zip.read(libname)
        fpath = os.sep.join([__dirname__,os.path.splitext(libname)[0]])
        __is__ = False
        if (not os.path.exists(fpath)):
            print '2. os.mkdir("%s")' % (fpath)
            os.mkdir(fpath)
        else:
            fsize = os.path.getsize(fpath)
            print '3. fsize=%s' % (fsize)
            print '4. f.file_size=%s' % (f.file_size)
            if (fsize != f.file_size):
                __is__ = True
                print '5. __is__=%s' % (__is__)
        fname = os.sep.join([fpath,libname])
        if (not os.path.exists(fname)) or (__is__):
            print '6. fname=%s' % (fname)
            file = open(fname, 'wb')
            file.write(data)
            file.flush()
            file.close()
        __module__ = fname
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
    

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.misc._utils import does_path_exist_conclusively

from vyperlogix.classes.SmartObject import SmartObject

def mtime(a):
    return os.stat(a).st_mtime

def date_comparator(a, b):
    a_statinfo = os.stat(a)
    b_statinfo = os.stat(b)
    print 'DEBUG: a=%s, b=%s' % (a,b)
    return -1 if (a_statinfo.st_mtime < b_statinfo.st_mtime) else 0 if (a_statinfo.st_mtime == b_statinfo.st_mtime) else 1

if (__name__ == '__main__'):
    def ppArgs():
        pArgs = [(k,args[k]) for k in args.keys()]
        pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
        pPretty.pprint()

    args = {'--help':'show some help.',
            '--verbose':'output more stuff.',
            '--debug':'debug some stuff, works like dryrun.',
            '--dryrun':'dryrun, makes no changes (see also --debug).',
            '--folder=?':'folder path.',
            '--num=?':'num to keep after files have been retired.',
            '--days=?':'number of days file has to be from today to be retired.',
            '--oldest':'retire oldest or newest by default.',
            }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
        ppArgs()
    else:
        _progName = __args__.programName

        _isVerbose = __args__.get_var('isVerbose',misc.isBooleanString,False)
        _isDebug = __args__.get_var('isDebug',misc.isBooleanString,False)
	_isDryrun = __args__.get_var('isDryrun',misc.isBooleanString,False)
        _isHelp = __args__.get_var('isHelp',misc.isBooleanString,False)

	_isDryrun = _isDebug or _isDryrun
	
        print 'DEBUG: _isVerbose=%s' % (_isVerbose)
        print 'DEBUG: _isDebug=%s' % (_isDebug)
	print 'DEBUG: _isDryrun=%s' % (_isDryrun)
        print 'DEBUG: _isHelp=%s' % (_isHelp)

        if (_isHelp):
            ppArgs()
            sys.exit()

	__path__ = os.path.abspath('logs')
        _folder = __args__.get_var('folder',misc.isString,__path__)
        __path__ = _folder

	_num = __args__.get_var('num',Args._int_,30)

	_days = __args__.get_var('days',Args._int_,30)

	_isOldest = __args__.get_var('isOldest',misc.isBooleanString,False)

        print 'DEBUG.1: __path__=%s' % (__path__)
	print 'DEBUG.2: _num=%s' % (_num)
	print 'DEBUG.3: _days=%s' % (_days)
	print 'DEBUG.4: _isOldest=%s' % (_isOldest)
	
	import time
	import datetime
	from time import mktime
	from datetime import timedelta
	now = time.time()
	dt = datetime.datetime.fromtimestamp(now)
	delta = timedelta(days=_days)
	past = dt - delta
	
	__is__ = os.path.exists(__path__)
	if (not __is__):
	    __is__ = does_path_exist_conclusively(__path__)

        if (__is__):
            if (os.path.isdir(__path__)):
                __count__ = 0
                __retirees__ = []
                print 'DEBUG.5: __path__=%s' % (__path__)
                for top, dirs, files in _utils.walk(__path__, topdown=True, onerror=None, rejecting_re=None):
                    if (top == __path__):
                        for f in files:
                            fname = os.sep.join([top, f])
			    t = mtime(fname)
			    fdt = datetime.datetime.fromtimestamp(t)
			    if (fdt < past):
				print '"%s" (%s).' % (fname,t)
				__retirees__.append(fname)
                    else:
                        break
		__retirees__.sort(date_comparator)
		if (_isDebug):
		    for f in __retirees__:
			try:
			    if (os.path.exists(f) or does_path_exist_conclusively(f)) and (os.path.isfile(f)):
				print '"%s" (%s).' % (f,mtime(f))
			    else:
				print 'DEBUG.6: Cannot locate "%s" or is not a file.' % (f)
			except Exception, ex:
			    print 'WARNING: %s' % (_utils.formattedException(details=ex))
		#__is__ = True if (len(__retirees__) >= _num) else False
		__is__ = True if (len(__retirees__) > 0) else False
                print 'DEBUG.7: There are %s files, %s to retire.' % (len(__retirees__),0 if (not __is__) else (_num - len(__retirees__)))
		if (__is__):
		    print 'BEGIN:'
		    for f in __retirees__:
			try:
			    if (os.path.exists(f) or does_path_exist_conclusively(f)) and (os.path.isfile(f)):
				print '"%s" (%s).' % (f,mtime(f))
				if (not _isDryrun):
				    print 'Removing "%s".' % (f)
				    os.unlink(f)
			    else:
				print 'DEBUG.8: Cannot locate "%s" or is not a file.' % (f)
			except Exception, ex:
			    print 'WARNING: %s' % (_utils.formattedException(details=ex))
                print 'END!'
            else:
                print 'WARNING: Looks like "%s" is not a directory.' % (__path__)
        else:
            print 'WARNING: Cannot determine the location of "%s".' % (__path__)
