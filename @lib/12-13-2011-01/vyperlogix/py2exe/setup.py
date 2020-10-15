'''
http://crazedmonkey.com/blog/python/pkg_resources-with-py2exe.html
'''
import re
import sys
import datetime
import platform

from distutils.core import setup

import py2exe
import os, glob, fnmatch  

from py2exe.build_exe import py2exe as build_exe

from vyperlogix import misc
from vyperlogix.enum.Enum import Enum
from vyperlogix.misc import ObjectTypeName
from vyperlogix.iterators.dict import dictutils
from vyperlogix.classes.SmartObject import SmartObject

__packages_bucket__ = []

__regex_libname__ = re.compile(r"(?P<libname>.*)_2_7\.zip", re.MULTILINE)

def handle_frozen_bootstrap(verbose=False):
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


def copy_extensions_for_media_collector(self, extensions):
    build_exe.copy_extensions(self, extensions)

    libs = 'libs'
    full = os.path.join(self.collect_dir, libs)
    print 'DEBUG: copy_extensions_for_media_collector.1 --> full=%s' % (full)
    if not os.path.exists(full):
	self.mkpath(full)

    for f in glob.glob('libs/*'):
	name = os.path.basename(f)
	dest = os.path.join(full, name)
	print 'DEBUG: copy_extensions_for_media_collector.2 --> source=%s, dest=%s' % (f, dest)
	self.copy_file(f, dest)
	self.compiled_files.append(os.path.join(libs, name))

def copy_extensions_for_zips_collector(self, extensions):
    build_exe.copy_extensions(self, extensions)

    zips = 'zips'
    full = os.path.join(self.collect_dir, zips)
    print 'DEBUG: copy_extensions_for_zips_collector.1 --> full=%s' % (full)
    if not os.path.exists(full):
	self.mkpath(full)

    for f in glob.glob('zips/*'):
	name = os.path.basename(f)
	dest = os.path.join(full, name)
	print 'DEBUG: copy_extensions_for_zips_collector.2 --> source=%s, dest=%s' % (f, dest)
	self.copy_file(f, dest)
	self.compiled_files.append(os.path.join(zips, name))
	
def is_file_embeddable_document(filename):
    __is__ = False
    if (filename.endswith('README')):
	__is__ = True
    elif (filename.endswith('README.txt')):
	__is__ = True
    elif (filename.endswith('README.md')):
	__is__ = True
    if (filename.endswith('LICENSE')):
	__is__ = True
    return __is__

def copy_extensions_for_docs_collector(self, extensions):
    build_exe.copy_extensions(self, extensions)

    full = self.collect_dir
    print 'DEBUG: copy_extensions_for_docs_collector.1 --> full=%s' % (full)

    for f in glob.glob('*'):
	if (is_file_embeddable_document(f)):
	    name = os.path.basename(f)
	    dest = os.path.join(full, name)
	    print 'DEBUG: copy_extensions_for_docs_collector.2 --> source=%s, dest=%s' % (f, dest)
	    self.copy_file(f, dest)
	    self.compiled_files.append(name)
	
class MediaCollector(build_exe):
    def copy_extensions(self, extensions):
	copy_extensions_for_media_collector(self, extensions)

class VyperLogixLibraryCollector(build_exe):
    compiled_excludes = []
    def copy_extensions(self, extensions):
        build_exe.copy_extensions(self, extensions)

	import vyperlogix # required for the filename...
	from vyperlogix.misc import _utils
	
	dirname = os.path.dirname(os.path.dirname(vyperlogix.__file__))
	print 'VyperLogixLibraryCollector.%s.1 --> dirname=%s' % (misc.callersName(),dirname)

	has_vyperlogix_lib = False
	print 'VyperLogixLibraryCollector.%s.2 --> BEGIN: compiled_files' % (misc.callersName())
	for f in self.compiled_files:
	    if (not has_vyperlogix_lib) and (f.find('vyperlogix%s' % (os.sep)) > -1):
		has_vyperlogix_lib = True
		print 'VyperLogixLibraryCollector.%s.3 --> has_vyperlogix_lib=%s' % (misc.callersName(),has_vyperlogix_lib)
	    print f
	print 'VyperLogixLibraryCollector.%s.4 --> END!!! compiled_files' % (misc.callersName())
	print '\n'
	
	__files__ = []
	__packages_bucket2__ = [n.lower() for n in __packages_bucket__]
	was_vyperlogix_lib_included = False
	print 'VyperLogixLibraryCollector.%s.5 --> __packages_bucket2__=%s' % (misc.callersName(),__packages_bucket2__)
	for top,dirs,files in _utils.walk(dirname):
	    for f in files:
		m = __regex_libname__.match(f)
		#print 'VyperLogixLibraryCollector.%s.6 --> f=%s, m=%s' % (misc.callersName(),f,m)
		if (m):
		    __g__ = SmartObject(m.groupdict())
		    __isVyperlogix__ = (vyperlogix.__file__.lower().find(__g__.libname.lower()) > -1)
		    __isPackage__ = (__g__.libname.lower() in __packages_bucket2__)
		    __is__ = (__isPackage__ or ( (not has_vyperlogix_lib) and (__isVyperlogix__) ) )
		    print 'VyperLogixLibraryCollector.%s.7 --> __isPackage__=%s, has_vyperlogix_lib=%s, __isVyperlogix__=%s, __is__=%s' % (misc.callersName(),__isPackage__,has_vyperlogix_lib,__isVyperlogix__,__is__)
		    if (__is__):
			__files__.append(os.sep.join([top,f]))
			if (not was_vyperlogix_lib_included):
			    was_vyperlogix_lib_included = __isVyperlogix__
			print 'VyperLogixLibraryCollector.%s.8 --> __files__=%s' % (misc.callersName(),__files__)
	files = __files__
	print 'VyperLogixLibraryCollector.%s.9 --> files=%s' % (misc.callersName(),files)
	print 'VyperLogixLibraryCollector.%s.10 --> vyperlogix.__file__=%s' % (misc.callersName(),vyperlogix.__file__)
	print 'VyperLogixLibraryCollector.%s.11 --> has_vyperlogix_lib=%s, was_vyperlogix_lib_included=%s' % (misc.callersName(),has_vyperlogix_lib,was_vyperlogix_lib_included)
	
	for f in files:
	    print 'VyperLogixLibraryCollector.%s.12 --> package=%s' % (misc.callersName(),f)
	    if (os.path.exists(f)):
		fname = os.path.basename(f)
		print 'VyperLogixLibraryCollector.%s.13 --> package fname=%s' % (misc.callersName(),fname)
		full = os.path.join(self.collect_dir, fname)
		print 'VyperLogixLibraryCollector.%s.14 --> copy_file source=%s dest=%s' % (misc.callersName(),f,full)
		self.copy_file(f,full)
		print 'VyperLogixLibraryCollector.%s.15 --> compiled_files.append --> %s' % (misc.callersName(),os.path.basename(full))
		self.compiled_files.append(os.path.basename(full))
	print '%s\n' % ('='*40)
	    
	__files__ = [os.path.basename(f).split('_')[0] for f in files]
	retirees = []
	print 'VyperLogixLibraryCollector.%s.20 --> BEGIN: compiled_files' % (misc.callersName())
	print 'VyperLogixLibraryCollector.%s.21 --> VyperLogixLibraryCollector.compiled_excludes=%s' % (misc.callersName(),VyperLogixLibraryCollector.compiled_excludes)
	for f in self.compiled_files:
	    m = [f.replace('/',os.sep).startswith(__f__+os.sep) for __f__ in __files__ if (not f.startswith('vyperlogix'+os.sep))]
	    if (any(m)):
		print 'VyperLogixLibraryCollector.%s.22 --> retirees.append(%s)' % (misc.callersName(),f)
		retirees.append(f)
	    m = [f.replace('/',os.sep).find(__f__+os.sep) > -1 for __f__ in VyperLogixLibraryCollector.compiled_excludes]
	    if (any(m)):
		print 'VyperLogixLibraryCollector.%s.23 --> retirees.append(%s)' % (misc.callersName(),f)
		retirees.append(f)
	    print f
	print 'VyperLogixLibraryCollector.%s.24 --> END!!! compiled_files' % (misc.callersName())
	print '\n'
	
	print 'VyperLogixLibraryCollector.%s.30 --> BEGIN: retirees' % (misc.callersName())
	for f in retirees:
	    print f
	print 'VyperLogixLibraryCollector.%s.31 --> END!!! retirees' % (misc.callersName())
	print '\n'
	
	print 'VyperLogixLibraryCollector.%s.40 --> (+++) Before Retirement Party self.compiled_files has %s items' % (misc.callersName(),len(self.compiled_files))
	self.compiled_files = [f for f in self.compiled_files if (f not in retirees)]
	print 'VyperLogixLibraryCollector.%s.41 --> (+++) After Retirement Party self.compiled_files has %s items' % (misc.callersName(),len(self.compiled_files))
	print '\n'

	print 'VyperLogixLibraryCollector.%s.50 --> BEGIN: compiled_files' % (misc.callersName())
	for f in self.compiled_files:
	    print f
	print 'VyperLogixLibraryCollector.%s.51 --> END!!! compiled_files' % (misc.callersName())
	print '\n'

class VyperLogixLibraryMediaCollector(VyperLogixLibraryCollector):
    def copy_extensions(self, extensions):
	print 'DEBUG: VyperLogixLibraryMediaCollector.1'
	copy_extensions_for_media_collector(self, extensions)
	VyperLogixLibraryCollector.copy_extensions(self, extensions)

class VyperLogixLibraryDocsMediaCollector(VyperLogixLibraryCollector):
    def copy_extensions(self, extensions):
	print 'DEBUG: VyperLogixLibraryMediaCollector.1'
	copy_extensions_for_media_collector(self, extensions)
	copy_extensions_for_docs_collector(self, extensions)
	VyperLogixLibraryCollector.copy_extensions(self, extensions)

class VyperLogixLibraryDocsCollector(VyperLogixLibraryCollector):
    def copy_extensions(self, extensions):
	print 'DEBUG: VyperLogixLibraryZipsCollector.1'
	copy_extensions_for_docs_collector(self, extensions)
	VyperLogixLibraryCollector.copy_extensions(self, extensions)

class VyperLogixLibraryZipsCollector(VyperLogixLibraryCollector):
    def copy_extensions(self, extensions):
	print 'DEBUG: VyperLogixLibraryZipsCollector.1'
	copy_extensions_for_zips_collector(self, extensions)
	VyperLogixLibraryCollector.copy_extensions(self, extensions)

class VyperLogixLibraryDocsZipsCollector(VyperLogixLibraryCollector):
    def copy_extensions(self, extensions):
	print 'DEBUG: VyperLogixLibraryZipsCollector.1'
	copy_extensions_for_zips_collector(self, extensions)
	copy_extensions_for_docs_collector(self, extensions)
	VyperLogixLibraryCollector.copy_extensions(self, extensions)

def extract(zipfilepath, extractiondir):
    import zipfile
    zip = zipfile.ZipFile(zipfilepath)
    zip.extractall(path=extractiondir)

    #find_data_files('libs', '*') + \
    #find_data_files('docs','*') + \
    
class CommandLineTypes(Enum):
    py2exe = 1
    pywin32 = 2
    custom = 4
    
def do_setup(program_name=None,company_name=None,product_name=None,description=None,product_copyright=None,icon=None,product_version=None,service_module=None,cmdline_style=CommandLineTypes.py2exe,cmdline_extra=None,minimum_python_version=2.7,dist_dir='./dist',includes=[],excludes=[],packages=[],extra_packages=[],extra_modules=[],packagedir={},datafiles=[],data_files=[],compiled_excludes=[],dll_excludes=[],initialize_datafiles=False,callback=None,minion=None,collector=VyperLogixLibraryCollector):
    global __version__, __v__, __v_v__
    
    if (not program_name) or (not company_name) or (not product_name) or (not description) or (not icon) or (not product_version):
	if (not program_name):
	    print >>sys.stderr, 'ERROR: Cannot proceed without program_name.'
	if (not company_name):
	    print >>sys.stderr, 'ERROR: Cannot proceed without company_name.'
	if (not product_name):
	    print >>sys.stderr, 'ERROR: Cannot proceed without product_name.'
	if (not description):
	    print >>sys.stderr, 'ERROR: Cannot proceed without description.'
	if (not icon):
	    print >>sys.stderr, 'ERROR: Cannot proceed without icon.'
	if (not product_version):
	    print >>sys.stderr, 'ERROR: Cannot proceed without product_version.'
	return
    __program_name__ = program_name
    __company_name__ = company_name
    __product_name__ = product_name
    __product_description__ = description
    __product_version__ = product_version
    __year__ = datetime.date.today().year
    __product_copyright__ = product_copyright if (product_copyright) else "(c).Copyright %s %s (See the LICENSE file for the details, when applicable)" % (__year__,__company_name__)
    __icon__ = icon
    
    from vyperlogix import misc
    __is_service__ = misc.isStringValid(service_module)

    toks = platform.python_version().split('.')
    if (len(toks) > 2):
	while (len(toks) > 2):
	    toks.pop()
    __version__ = float('.'.join(toks))

    __v__ = '%1.1f'%(__version__)
    __v_v__ = __v__.replace('.','_')

    if __version__ < minimum_python_version:
	sys.exit('ERROR: Sorry, python %s is required for this application.' % (minimum_python_version))

    def get_libdate_for(fpath):
	import os
	from vyperlogix.misc import _utils
    
	__callback__ = lambda top,dirs,f:True if (not f.endswith('.pyc')) and (not f.endswith('.pyo')) else False
	allfiles = _utils.get_allfiles_from(fpath,callback=__callback__,topdown=True,followlinks=True)
	allfiles = filter(os.path.isfile, allfiles)
	allfiles.sort(key=lambda x: os.path.getmtime(x))
    
	return os.path.getmtime(allfiles[-1])
	
    def rebuild_libs_if_necessary(fpath):
	import os
	from vyperlogix.misc import _utils
	from vyperlogix.process import Popen
    
	__cwd__ = os.getcwd()
	__vyperlogix__ = os.path.join(__cwd__,'libs','vyperlogix_%s.zip'%(__v_v__))
	__has_vyperlogix__ = os.path.exists(__vyperlogix__)
	if (not __has_vyperlogix__):
	    lib_base = os.path.dirname(fpath)
	    __vyperlogix__ = os.path.join('%s/dist_%s'%(lib_base,__v__),'vyperlogix_%s.zip'%(__v_v__))
	    __has_vyperlogix__ = os.path.exists(__vyperlogix__)
	    __target__ = os.path.join(__cwd__,'libs')
	else:
	    __target__ = __vyperlogix__
    
	libdate = latest = get_libdate_for(fpath)
	#print '(+++) __has_vyperlogix__=%s' % (__has_vyperlogix__)
	if (__has_vyperlogix__):
	    libdate = os.path.getmtime(__vyperlogix__)
	else:
	    __vyperlogix__ = os.path.join(os.path.dirname(fpath),'dist_%s'%(__v__),'vyperlogix_%s.zip'%(__v__.replace('.','_')))
	    __has_vyperlogix__ = os.path.exists(__vyperlogix__)
	    if (__has_vyperlogix__):
		libdate = os.path.getmtime(__vyperlogix__)
	#print '(+++) latest=%s, libdate=%s, (not __has_vyperlogix__)=%s, (latest > libdate)=%s' % (latest,libdate,(not __has_vyperlogix__),(latest > libdate))
	__is__ = (not __has_vyperlogix__) or (latest > libdate) 
	#print '(+++) __is__=%s' % (__is__)
	if (1):
	    __fpath__ = os.path.dirname(fpath)
	    __vyperlogix__ = os.path.join(__fpath__,'dist_%s'%(__v__),'vyperlogix_%s.zip'%(__v__.replace('.','_')))
	    __command__ = os.path.join(__fpath__,'compile%s.cmd'%(__v__))
	    __command_egg__ = os.path.join(__fpath__,'compile-egg%s.cmd'%(__v__))
	    __has_vyperlogix__ = os.path.exists(__fpath__)
	    __has_command__ = os.path.exists(__command__)
	    #print '(+++) __has_vyperlogix__=%s' % (__has_vyperlogix__)
	    if (__has_vyperlogix__) and (__has_command__):
		__compiles__ = []

		ioBuf = _utils.stringIO()
		dirName = os.path.dirname(__command__).replace(os.sep,'/')
		cmd = 'cd "%s"' % (dirName)
		fOut = open('compile.cmd','w')
		print >>fOut, '@echo on\n'
		print >>fOut, 'cd "%s"\n' % (dirName)
		print >>fOut, '%s\n' % (os.path.splitdrive(dirName)[0])
		if (__is__):
		    print 'Compile "%s"...' % (__vyperlogix__)
		    print >>fOut, 'START "%s" /SEPARATE /HIGH "%s" END\n' % (os.path.splitext(os.path.basename(__command__))[0],os.path.basename(__command__))
		else:
		    print 'INFO: No need to compile %s into ZIP.' % (__vyperlogix__)
		
		__compiles__.append(os.path.basename(__command__))
		
		if (misc.isDict(packagedir)):
		    from vyperlogix.lists.ListWrapper import ListWrapper
		    handled_eggs = []
		    print '(+++)  __packages_bucket__=%s' % (__packages_bucket__)
		    for k,v in packagedir.iteritems():
			print '(+++)  %s=%s' % (k,v)
			print '(+++) os.path.exists("%s")=%s' % (v,os.path.exists(v))
			print '(+++) os.path.isdir("%s")=%s' % (v,os.path.isdir(v))
			p = '%s/EGG-INFO'%(os.path.dirname(v).replace(os.sep,'/'))
			print '(+++) p=%s' % (p)
			__files__ = []
			if (not os.path.exists(p)):
			    __files__ = [f for f in os.listdir(os.path.dirname(p)) if ( (os.path.splitext(f)[0].find(k) > -1) or (os.path.splitext(f)[0].find(os.path.basename(v)) > -1) ) and (os.path.splitext(f)[-1].lower() == '.egg-info')]
			    print '(+++) __files__=%s' % (__files__)
			print '(+++) "%s".endswith(\'.egg\')=%s' % (os.path.dirname(v),os.path.dirname(v).endswith('.egg'))
			so = SmartObject()
			if (os.path.exists(v)) and (os.path.isdir(v)) and ( ( (os.path.exists(p) and (os.path.dirname(v).endswith('.egg')) ) or (len(__files__) > 0) ) ):
			    __dirname__ = os.path.dirname(__vyperlogix__)
			    if (os.path.exists(__dirname__) and os.path.isdir(__dirname__)):
				print '(+++).1 vyperlogix target path=%s' % (__dirname__)
				for f in os.listdir(__dirname__):
				    mm = __regex_libname__.match(f)
				    if (mm) and (mm.groupdict().get('libname',None) == k):
					lpath = os.sep.join([__dirname__,f])
					dt = os.path.getmtime(lpath)
					so.libpath = lpath
					so.datetime = dt
					so.libdate = dt
				print '(+++).2 so=%s' % (str(so))
			    else:
				print 'WARNING: Cannot determine if the egg "%s" has been compiled into a ZIP or not.' % (k)
				print '(+++) egg source path=%s' % (v)
			    if (os.path.exists(v) and os.path.isdir(v)):
				so.libdate = get_libdate_for(v)
				print '(+++).3 so.libdate=%s' % (so.libdate)
			    else:
				print 'WARNING: Cannot determine if the egg "%s" has source files or not in "%s".' % (k,v)
			    print '(+++).4 so.datetime=%s isNone=(%s), so.libdate=%s isGreater=%s' % (so.datetime,(so.datetime is None),so.libdate,(so.libdate > so.datetime))
			    if (so.datetime is None) or (so.libdate > so.datetime):
				print '(+++).5 Schedule the compile... for %s from "%s".' % (k,v)
				print >>fOut, 'START "%s" /SEPARATE /HIGH %s "%s" %s END\n' % (os.path.splitext(os.path.basename(__command_egg__))[0],os.path.basename(__command_egg__),v,k)
				__compiles__.append(os.path.basename(__command_egg__))
			    else:
				print 'INFO: No need to compile the egg "%s" because it has already been compiled from source at "%s".' % (k,v)
			    __packages_bucket__.append(k)
			    handled_eggs.append(k)
		    print '(+++)  __packages_bucket__=%s' % (__packages_bucket__)
		    print '(+++)  handled_eggs=%s' % (handled_eggs)
		    l = ListWrapper(packages)
		    for k in handled_eggs:
			print '(+++)  del "%s"' % (packagedir[k])
			del packagedir[k]
			i = l.findFirstMatching(k)
			print '(+++)  k=%s' % (k)
			print '(+++)  i=%s' % (i)
			if (i > -1):
			    print '(+++)  del "%s"' % (packages[i])
			    del packages[i]
			    l = ListWrapper(packages)
		
		fOut.flush()
		fOut.close()
		Popen.Shell(fOut.name, shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=ioBuf)
		print >>sys.stdout, ioBuf.getvalue()
		
		#print '(+++) __vyperlogix__=%s' % (__vyperlogix__)
		dirname = os.path.dirname(os.path.dirname(__vyperlogix__)) #str(os.sep.join([os.path.dirname(os.path.dirname(__vyperlogix__)),'compile%s.log'%(v)]))

		from vyperlogix.win import WinProcesses
		p = WinProcesses.WinProcesses()
		
		import time
		s_begin = time.time()
		while (1):
		    #__l__ = [pr for pr in p.listProcNames() if (any([pr.find(os.path.splitext(c)[0]) > -1 for c in __compiles__])) or (pr.find('cmd') > -1) or (pr.find('python') > -1)]
		    #print '(+++) __l__=%s' % (__l__)
		    __re__ = re.compile(r"compile.*\.log", re.MULTILINE)
		    #print '(+++) dirname=%s' % (dirname)
		    files = ['/'.join([dirname,f]) for f in os.listdir(dirname) if (__re__.match(f))]
		    #print '(+++) files=%s' % (files)

		    __files__ = []
		    for f in files:
			_f_ = os.path.splitext(os.path.basename(f))[0]
			toks = _f_.split('_')
			if (len(toks) > 1):
			    del toks[1]
			    _f_ = ''.join([t for t in toks if (len(t) > 0)])
			#print '(+++) _f_=%s' % (_f_)
			#print '(+++) __compiles__=%s' % (__compiles__)
			if (_f_+'.cmd' in __compiles__):
			    __files__.append(f)
			    #print '(+++) __files__=%s' % (__files__)
			print
		    files = __files__
		    #print '(+++) files=%s' % (files)
		    
		    d_done = {}
		    d_errors = {}
		    
		    __re__ = re.compile(r"\[\s*Errno\s*\d*\]", re.MULTILINE)
		    #print '(+++) len(files)=%s, len(__compiles__)=%s' % (len(files),len(__compiles__))
		    if (len(files) == len(__compiles__)):
			for fname in files:
			    #print >>sys.stderr, '(+++) os.path.exists("%s")=%s' % (fname,os.path.exists(fname))
			    if (os.path.exists(fname)):
				#print >>sys.stderr, '(+++) fname=%s' % (fname)
				results = _utils.readFileFrom(fname)
				__matches2__ = results.find('Done !\n\nEND !') > -1
				#print >>sys.stderr, '(+++) __matches2__=%s' % (__matches2__)
				if (__matches2__):
				    d_done[fname] = __matches2__
				    print sys.stdout, results
				    __matches__ = __re__.match(results)
				    #print >>sys.stderr, '(+++) __matches__=%s' % (__matches__)
				    if (__matches__):
					d_errors[fname] = __matches__
					print >>sys.stderr, 'WARNING: Required Compile Failed in "%s".' % (fname)
			    else:
				print >>sys.stderr, 'WARNING: Cannot locate "%s".' % (fname)
			#print >>sys.stderr, '(+++) len(d_done.keys())=%s' % (len(d_done.keys()))
			#print >>sys.stderr, '(+++) len(d_errors.keys())=%s' % (len(d_errors.keys()))
			#print >>sys.stderr, '(+++) len(__compiles__)=%s' % (len(__compiles__))
			if ((len(d_done.keys())+len(d_errors.keys())) == len(__compiles__)):
			    print >>sys.stderr, 'INFO: Seems like the compile jobs have completed.'
			    break

		    s_end = time.time()
		    s_et = s_end - s_begin
		    print '(+++) s_et=%s' % (s_et)
		    if (s_et > 300):
			break
	    else:
		print >>sys.stderr, 'Missing "%s" or missing "%s" or missing "%s".' % (__vyperlogix__,__command__,__command_egg__)
	__has_vyperlogix__ = os.path.exists(__vyperlogix__)
	print >>sys.stderr, 'INFO: __vyperlogix__=%s' % (__vyperlogix__)
	print >>sys.stderr, 'INFO: __has_vyperlogix__=%s' % (__has_vyperlogix__)
	return

    import vyperlogix # required for the path information from the module...
    from vyperlogix import misc
    from vyperlogix.misc import _utils
    _utils.removeAllFilesUnder(os.path.abspath(r'.\build'))
    _utils.removeAllFilesUnder(os.path.abspath(dist_dir))
    #_utils.removeAllFilesUnder(os.path.abspath(r'.\libs'))
    lib_base = os.path.dirname(vyperlogix.__file__) if (os.path.isfile(vyperlogix.__file__)) else vyperlogix.__file__
    rebuild_libs_if_necessary(lib_base)

    normalize = lambda *args:os.path.normpath(os.path.join(*args))
    def find_data_files(srcdir, *wildcards, **kw):
	print '(+++).0 srcdir=%s, wildcards=%s, **kw=%s' % (srcdir,wildcards,kw)
	if (isinstance(srcdir,tuple)):
	    wildcards = srcdir[-1]
	    srcdir = srcdir[0]
	    print '(+++).1 srcdir=%s, wildcards=%s' % (srcdir,wildcards)
	def walk_helper(arg, dirname, files):
	    if '.svn' in dirname:
		return
	    names = []
	    lst, wildcards = arg
	    for wc in wildcards:
		wc_name = normalize(dirname, wc)
		for f in files:
		    filename = normalize(dirname, f)
    
		    if fnmatch.fnmatch(filename, wc_name) and (not os.path.isdir(filename)) and (not is_file_embeddable_document(os.path.basename(filename))):
			names.append(filename)
	    if names:
		lst.append( (dirname, names ) )
    
	file_list = []
	recursive = kw.get('recursive', True)
	print '(+++).3 recursive=%s' % (recursive)
	if recursive:
	    os.path.walk(srcdir, walk_helper, (file_list, wildcards))
	else:
	    walk_helper((file_list, wildcards),
		        srcdir,
		        [os.path.basename(f) for f in glob.glob(normalize(srcdir, '*'))])
	print '(+++).2 file_list=%s' % (file_list)
	return file_list[0] if (file_list and misc.isList(file_list)) else file_list

    __packages__ =      [] if (not misc.isList(packages)) else packages
    __datafiles__ = [ ('.', ['run.cmd']) ] if (not initialize_datafiles and os.path.exists(os.path.abspath('./run.cmd'))) else []
    print '(1). __datafiles__=%s' % (__datafiles__)
    
    if (os.path.exists(__program_name__+'.py')):
	print '(+++) --> source=%s' % (__program_name__+'.py')

    def handle_service_file(key,fname):
	fOut = open(fname,'w')
	print >> fOut, '@echo off\n'
	print >> fOut, 'echo %COMPUTERNAME%\n'
	print '(@@@).cmdline_style = %s' % (cmdline_style)
	if (cmdline_style == CommandLineTypes.py2exe):
	    if (os.path.splitext(key)[0] == 'start'):
		print >> fOut, 'net start %s\n' % (__program_name__)
	    elif (os.path.splitext(key)[0] == 'stop'):
		print >> fOut, 'net stop %s\n' % (__program_name__)
		print >> fOut, 'taskkill /F /IM %s\n' % (__program_name__)
	    elif (os.path.splitext(key)[0] == 'restart'):
		print >> fOut, 'net stop %s\n' % (__program_name__)
		print >> fOut, 'net start %s\n' % (__program_name__)
	    else:
		print >> fOut, '%s -%s\n' % (__program_name__,os.path.splitext(key)[0])
		if (os.path.splitext(key)[0] == 'remove'):
		    print >> fOut, 'taskkill /F /IM %s\n' % (__program_name__)
	elif (cmdline_style == CommandLineTypes.custom):
	    print >> fOut, '%s %s %s\n' % (__program_name__,cmdline_extra,os.path.splitext(key)[0])
	    if (os.path.splitext(key)[0] == 'remove'):
		print >> fOut, 'taskkill /F /IM %s\n' % (__program_name__)
	fOut.flush()
	fOut.close()
    
    __service_files__ = {}
    __service_files__['install.cmd'] = None
    __service_files__['remove.cmd'] = None
    __service_files__['start.cmd'] = None
    __service_files__['stop.cmd'] = None
    __service_files__['restart.cmd'] = None

    try:
	for df in datafiles:
	    dfp = os.path.abspath(df[0])
	    _l_ = []
	    if (not misc.isTuple(df)):
		l = df.replace(os.sep,'/').split('/')
		df = tuple([os.sep.join(l[0:-1]),l[-1]])
	    print '(@@@).1 df[1:]=%s' % (df[1:])
	    for dfl in df[1:]:
		for f in [os.sep.join([dfp,f]) for f in dfl]:
		    if (os.path.exists(f) and os.path.isfile(f) and (not is_file_embeddable_document(os.path.basename(f)))):
			print '(@@@).2 __is_service__=%s' % (__is_service__)
			if (__is_service__):
			    for ff in __service_files__.keys():
				print '(@@@).3 "%s".find("%s")=%s' % (f,os.sep+ff,f.find(os.sep+ff) > -1)
				if (f.find(os.sep+ff) > -1):
				    handle_service_file(ff,f)
				    print '(@@@).4 special-service-file=%s' % (f)
			_l_.append(f)
	    __datafiles__.append(tuple([df[0],_l_]))
    except Exception, ex:
	print >> sys.stderr, _utils.formattedException(details=ex)
    try:
	for df in data_files:
	    __df__ = find_data_files(df)
	    if (len(__df__) > 0):
		__datafiles__.append(__df__)
    except Exception, ex:
	print >> sys.stderr, _utils.formattedException(details=ex)
    print '(2). __datafiles__=%s' % (__datafiles__)
    __excludes__ = ["pywin", "pywin.debugger", "pywin.debugger.dbgcon",
	        "pywin.dialogs", "pywin.dialogs.list", 'MySQLdb' ] # , "vyperlogix", 'paramiko'
    for exc in excludes:
	if (exc not in __excludes__):
	    __excludes__.append(exc)
    __excludes__ = list(set(__excludes__))
    
    __dll_excludes__ = ['w9xpopen.exe', "mswsock.dll", "MSWSOCK.dll", "powrprof.dll", '_mysql.pyd', 'LIBEAY32.dll', '_ssl.pyd']

    for exc in dll_excludes:
	if (exc not in __dll_excludes__):
	    __dll_excludes__.append(exc)
    __dll_excludes__ = list(set(__dll_excludes__))
    
    __includes__ = ['web', 'web.wsgiserver', 'web.contrib',  'web.http', 'bisect',
	        'M2Crypto', 
	        'email',
	        'email.base64mime',
	        'email.charset',
	        'email.encoders',
	        'email.errors',
	        'email.feedparser',
	        'email.generator',
	        'email.header',
	        'email.iterators',
	        'email.message',
	        'email.parser',
	        'email.quoprimime',
	        'email.utils',
	        'email._parseaddr',
	        'email.mime', 
	        'email.mime.application', 
	        'email.mime.audio', 
	        'email.mime.base', 
	        'email.mime.image', 
	        'email.mime.message', 
	        'email.mime.multipart', 
	        'email.mime.nonmultipart', 
	        'email.mime.text' 
	        ]
    for inc in includes:
	if (inc not in __includes__):
	    __includes__.append(inc)
    __includes__ = list(set(__includes__))
    
    VyperLogixLibraryCollector.compiled_excludes = list(set(VyperLogixLibraryCollector.compiled_excludes)-set(compiled_excludes))+compiled_excludes
    print 'DEBUG: (+++) VyperLogixLibraryCollector.compiled_excludes=%s' % (VyperLogixLibraryCollector.compiled_excludes)

    if (misc.isList(extra_packages)):
	try:
	    # py2exe 0.6.4 introduced a replacement modulefinder.
	    # This means we have to add package paths there, not to the built-in
	    # one.  If this new modulefinder gets integrated into Python, then
	    # we might be able to revert this some day.
	    try:
		import py2exe.mf as modulefinder
	    except ImportError:
		import modulefinder
	    if ('win32com' in extra_packages):
		import win32com
		for p in win32com.__path__[1:]:
		    modulefinder.AddPackagePath("win32com", p)
		if (misc.isList(extra_modules)):
		    if (len(extra_modules) == 0):
			extra_modules.append("win32com.shell")
			extra_modules.append("win32com.mapi")
		    for extra in extra_modules:
			__import__(extra)
			m = sys.modules[extra]
			for p in m.__path__[1:]:
			    modulefinder.AddPackagePath(extra, p)
	except ImportError:
	    # no build path setup, no worries.
	    pass

    def include_additional_text_into(source):
	source = source + '\n'
	if (os.path.exists('README')):
	    source += ''.join(_utils.readFileFrom('README'))
	elif (os.path.exists('README.txt')):
	    source += ''.join(_utils.readFileFrom('README.txt'))
	elif (os.path.exists('README.md')):
	    source += ''.join(_utils.readFileFrom('README.md'))
	if (os.path.exists('LICENSE')):
	    source += ''.join(_utils.readFileFrom('LICENSE'))
	return source
    
    try:
	if (__is_service__):
	    class Target:
		def __init__(self, **kw):
		    self.__dict__.update(kw)
		    # for the versioninfo resources
		    self.version = __product_version__                  # build.py magic comment
		    self.company_name = __company_name__
		    self.copyright = __product_copyright__
		    self.name = __product_name__
		    self.description = __product_description__
	    
	    manifest_template = '''
	    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	    <assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
	    <assemblyIdentity
		version="5.0.0.0"
		processorArchitecture="x86"
		name="%(prog)s"
		type="win32"
	    />
	    <description>%(prog)s Program</description>
	    <dependency>
		<dependentAssembly>
		    <assemblyIdentity 
		        type="win32" 
		        name="Microsoft.VC90.CRT" 
		        version="9.0.21022.8" 
		        processorArchitecture="x86" 
		        publicKeyToken="1fc8b3b9a1e18e3b"
		        language="*"
		    />
		</dependentAssembly>
	    </dependency>
	    </assembly>
	    '''
	    RT_MANIFEST = 24
	    #print 'DEBUG: cmdline_style=%s' % (cmdline_style)
	    __cmdline_style__ = CommandLineTypes.pywin32.name
	    #print 'DEBUG: __cmdline_style__=%s' % (__cmdline_style__)
	    try:
		__cmdline_style__ = cmdline_style.name
	    except:
		__cmdline_style__ = cmdline_style
	    #print 'DEBUG: __cmdline_style__=%s' % (__cmdline_style__)
	    windows_service = Target(
		# used for the versioninfo resource
		description = __product_description__,
		# What to build
		modules = [ service_module ],
		cmdline_style = __cmdline_style__,
		other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog=service_module))],
		dest_base = service_module,
		icon_resources = [(0, __icon__)]
	    )
	    setup(
		name=__program_name__,
		version=__product_version__,                            # build.py magic comment
		package_dir = packagedir,
		description=__product_description__,
		packages = __packages__,
	    
		options = {"py2exe": {"compressed": True,
		                      "optimize": 2,
		                      "ascii": False,
		                      "bundle_files": 1,
		                      "includes": __includes__,
		                      "excludes": __excludes__,
		                      'dist_dir': os.path.abspath(dist_dir),
		                      "dll_excludes": __dll_excludes__,
		                      }
		           },
		zipfile = None,
		data_files = __datafiles__,
		cmdclass = {"py2exe": collector},
		service = [ windows_service ],    
	    )
	else:
	    class Target:
		def __init__(self, **kw):
		    self.__dict__.update(kw)
		    # for the versioninfo resources
		    self.version = __product_version__                  # build.py magic comment
		    self.company_name = __company_name__
		    self.copyright = __product_copyright__
		    self.name = __product_name__
		    self.script = '%s.py' % (__program_name__)
		    self.description = include_additional_text_into(__product_description__)
	    
	    windows_console = Target(
		description = include_additional_text_into(__product_description__),
		modules = [ __program_name__ ],
		cmdline_style = cmdline_style.name if (ObjectTypeName.typeName(cmdline_style).find('Enum.EnumMetaClass') > -1) else cmdline_style,
		dest_base = __program_name__,
		icon_resources = [(0, __icon__)]
	    )

	    setup(
		name=__program_name__,
		version=__product_version__,                            # build.py magic comment
		package_dir = packagedir,
		description=include_additional_text_into(__product_description__),
		packages = __packages__,
	    
		options = {"py2exe": {"compressed": True,
		                      "optimize": 2,
		                      "ascii": False,
		                      "bundle_files": 1,
		                      "includes": __includes__,
		                      "excludes": __excludes__,
		                      'dist_dir': os.path.abspath(dist_dir),
		                      "dll_excludes": __dll_excludes__,
		                      }
		           },
		zipfile = None,
		data_files = __datafiles__,
		cmdclass = {"py2exe": collector},
		console = [windows_console],
	    )
    finally:
	if (hasattr(minion, '__class__') and hasattr(minion, 'callback') and hasattr(minion,'__data__')):
	    #from vyperlogix.misc import ObjectTypeName
	    callback = minion.callback
	    so = minion.__data__
	    print >> sys.stdout, 'DEBUG: so.__class__=%s' % (so.__class__)
	    so.program_name = __program_name__
	    so.company_name = __company_name__
	    so.product_name = __product_name__
	    so.description = include_additional_text_into(__product_description__)
	    so.product_version = __product_version__
	    so.product_copyright = __product_copyright__
	    so.icon = __icon__
	if (callable(callback)):
	    try:
		callback(dist_dir)
	    except Exception, ex:
		print >> sys.stderr, 'EXCEPTION: %s' % (_utils.formattedException(details=ex))

import os, sys

__isExe__ = lambda f:(os.path.splitext(str(f))[-1].lower() == '.exe')
__isTrash__ = lambda f:(str(f).lower().find('w9xpopen.exe') > -1)

class CallbackException(Exception):
    pass

class Py2EXEUtils():
    def __init__(self,target,isExe=__isExe__,isTrash=__isTrash__,isZIP=False):
	self.target = target
	self.isExe = isExe
	self.isTrash = isTrash
	self.isZIP = isZIP
	self.isNonExe = lambda f:(not self.isTrash(f)) and (not self.isExe(f))
	self.__data__ = SmartObject()
	self.regex1 = re.compile(r"\{\{\S*(?P<name>.*)\S*\}\}", re.DOTALL | re.MULTILINE)
	
    def normalize(self,f,dist,t):
	from vyperlogix.lists.ListWrapper import ListWrapper
	n1 = os.path.dirname(f.replace(dist,t))
	if (f.startswith(dist)):
	    fl = ListWrapper(f.split(os.sep))
	    i = fl.findFirstMatching('dist')
	    if (i > -1):
		i -= 1
		ft1 = os.sep.join(fl[0:i+1])
		ft2 = os.sep.join(fl[i:])
		return f.replace(ft1,t)
	return f
    
    def __normalize__(self,dest,target):
	bias = ''
	__dest__ = dest if (os.path.isdir(dest)) else os.path.dirname(dest)
	print '(%s).1 --> dest=%s' % (misc.funcName(),__dest__)
	toks = [str(t).lower() for t in __dest__.split(os.sep) if (len(t) > 0)]
	print '(%s).2 --> toks=%s' % (misc.funcName(),toks)
	if ('dist' in toks):
	    bias = os.sep+'dist'
	    print '(%s).3 --> bias=%s' % (misc.funcName(),bias)
	return dest.replace(target+bias,'')
	
    def callback(self,dist_dir):
	raise CallbackException('Invalid use of abstract method.')
    
    def process_templates(self,fpath,product_version=None):
	if (os.path.exists(fpath) and os.path.isfile(fpath)):
	    fIn = open(fpath,'r')
	    fOut = open(fpath+'.new', mode='w')
	    __is_dirty__ = False
	    #print >>sys.stdout, 'DEBUG: fpath=%s' % (fpath)
	    #print >>sys.stdout, 'DEBUG: self.__data__=%s' % (self.__data__)
	    for aLine in fIn:
		aLine = aLine.rstrip()
		#print >>sys.stdout, 'DEBUG: aLine=%s' % (aLine)
		matches = self.regex1.search(aLine)
		#print >>sys.stdout, 'DEBUG: matches=%s' % (matches)
		if (matches and matches.groupdict() and matches.groupdict().has_key('name')):
		    #print >>sys.stdout, 'DEBUG: matches=%s, matches.groupdict()=%s' % (matches,matches.groupdict())
		    for k,v in matches.groupdict().iteritems():
			v = str(v).strip()
			#print >>sys.stdout, 'DEBUG: self.__data__["%s"]=%s' % (v,self.__data__[v])
			if (self.__data__[v]):
			    aLine = aLine.replace('{{ %s }}' % (v),self.__data__[v])
			    #print >>sys.stdout, 'DEBUG: --> aLine=%s' % (aLine)
			    __is_dirty__ = True
		print >>fOut, aLine
	    fIn.close()
	    fOut.flush()
	    fOut.close()
	    #print >> sys.stdout, 'DEBUG: __is_dirty__=%s' % (__is_dirty__)
	    if (__is_dirty__):
		#print >> sys.stdout, 'DEBUG: fpath=%s, fOut.name=%s' % (fpath,fOut.name)
		os.remove(fpath)
		#print >> sys.stdout, 'DEBUG: os.remove("%s")' % (fpath)
		os.rename(fOut.name,fpath)
		#print >> sys.stdout, 'DEBUG: os.rename("%s","%s")' % (fOut.name,fpath)
	    else:
		os.remove(fOut.name)

class CopyFilesToTarget(Py2EXEUtils):
    def callback(self,dist_dir):
	import zipfile
	from vyperlogix import misc
	from vyperlogix.misc import _utils
	dist_dir = os.path.abspath(dist_dir.replace('/',os.sep))
	print '(%s).1 --> dist_dir=%s' % (misc.funcName(),dist_dir)
	if (not os.path.exists(self.target)) or (not os.path.isdir(self.target)):
	    print '(DEBUG) Making dirs --> %s' % (self.target)
	    os.makedirs(self.target)
	if (self.isZIP):
	    print '(DEBUG) dist_dir=%s, self.target=%s' % (dist_dir,self.target)
	    toks = [t for t in dist_dir.split(os.sep) if (len(t) > 0)][0:-1]
	    print '(DEBUG) toks=%s' % (toks)
	    zf_name = os.sep.join([self.target,toks[-1]+'.zip'])
	    print '(DEBUG) zf_name=%s' % (zf_name)
	    zf = zipfile.PyZipFile(zf_name, mode='w')
	if (os.path.exists(self.target)) and (os.path.isdir(self.target)):
	    if (os.path.exists(dist_dir)):
		#files = [os.sep.join([dist_dir,f]) for f in os.listdir(dist_dir)]
		files_d = _utils.filesAsDict(dist_dir)
		files = [os.path.abspath(f) for f in dictutils.flatten(files_d)]
		print '(%s).2 --> files=%s' % (misc.funcName(),files)
		#print '(%s).2a --> files_d=%s' % (misc.funcName(),files_d)
		#print '(%s).2b --> fd=%s' % (misc.funcName(),fd)
		nonexes = [f for f in files if (self.isNonExe(f))]
		exes = [f for f in files if (f not in nonexes) and (not self.isTrash(f))]
		others = list(set(files) - set(exes) - set(nonexes))
		print '(%s).3 --> exes=%s' % (misc.funcName(),exes)
		if (len(exes) == 1):
		    print '(%s).4 --> exes=%s' % (misc.funcName(),exes)
		    for f in exes:
			_f_ = os.path.abspath(f)
			dest = self.normalize(f,dist_dir,self.target)
			print '(%s).5 --> _utils.copyFile("%s","%s",verbose=True)' % (misc.funcName(),_f_,dest)
			if (not os.path.exists(os.path.dirname(dest))):
			    _utils.makeDirs(dest)
			_utils.copy_binary_files_by_chunks(_f_,dest)
			if (self.isZIP):
			    t = self.__normalize__(dest,self.target)
			    print '(%s).5a --> _f_=%s, t=%s' % (misc.funcName(),_f_,t)
			    zf.write(_f_, t)
			assert(_utils.fileSize(_f_) == _utils.fileSize(dest))
		print '(%s).6 --> nonexes=%s' % (misc.funcName(),nonexes)
		for f in nonexes:
		    _f_ = os.path.abspath(f)
		    if (os.path.exists(_f_)):
			if os.path.isfile(_f_):
			    dest = self.normalize(f,dist_dir,self.target)
			    print '(%s).7 --> _utils.copyFile("%s","%s",verbose=True)' % (misc.funcName(),_f_,dest)
			    #print '(%s).7a --> os.path.isfile("%s"))=%s' % (misc.funcName(),dest,os.path.isfile(dest))
			    #print '(%s).7b --> os.path.exists("%s")=%s' % (misc.funcName(),os.path.dirname(dest),os.path.exists(os.path.dirname(dest)))
			    if (not os.path.exists(os.path.dirname(dest))):
				_utils.makeDirs(dest)
			    _utils.copy_binary_files_by_chunks(_f_,dest)
			    self.process_templates(dest)
			    if (self.isZIP):
				t = self.__normalize__(dest,self.target)
				print '(%s).7a --> _f_=%s, t=%s' % (misc.funcName(),_f_,t)
				zf.write(dest,t)
			    assert(_utils.fileSize(_f_) == _utils.fileSize(dest))
		    else:
			print '(%s).8 WARNING --> _f_ is "%s" and seems to be inaccessible as a file that could be copied, it was not copied however.' % (misc.funcName(),_f_)
		print '(%s).9 --> others=%s' % (misc.funcName(),others)
		for f in others:
		    _f_ = os.path.abspath(f)
		    dest = self.normalize(f,dist_dir,self.target)
		    print '(%s).10 --> remove("%s")' % (misc.funcName(),_f_)
		    if (os.path.exists(_f_)):
			os.remove(_f_)
		    else:
			print >> sys.stderr, 'WARNING: Nothing to do remove cuz "%s" does not seem to exist.' % (_f_)
		    print '(%s).11 --> remove("%s")' % (misc.funcName(),dest)
		    if (os.path.exists(dest)):
			os.remove(dest)
		    else:
			print >> sys.stderr, 'WARNING: Nothing to do remove cuz "%s" does not seem to exist.' % (dest)
		if (self.isZIP):
		    zf.close()
	    else:
		print >> sys.stderr, 'WARNING: Nothing to do cuz "%s" does not seem to exist or is not a directory.' % (dist_dir)
	else:
	    print >> sys.stderr, 'WARNING: Nothing to do cuz "%s" does not seem to exist or is not a directory.' % (self.target)


if (__name__ == '__main__'):
    import os, sys
    dist_dir = r"J:\@Vyper Logix Corp\@Projects\python-projects\windows-cron-service\dist"
    nonexes = ['.\\dist\\restart.cmd', '.\\dist\\install.cmd', '.\\dist\\Microsoft.VC90.CRT\\msvcp90.dll', '.\\dist\\Microsoft.VC90.CRT\\msvcr90.dll', '.\\dist\\stop.cmd', '.\\dist\\remove.cmd', '.\\dist\\start.cmd', '.\\dist\\Microsoft.VC90.CRT\\msvcm90.dll', '.\\dist\\Microsoft.VC90.CRT\\Microsoft.VC90.CRT.manifest', '.\\dist\\service_config.json']
    nonexes = [f.replace('.\\dist\\',dist_dir+os.sep) for f in nonexes]
    n_nonexes = [normalize(f,dist_dir,r"c:\@vm1") for f in nonexes]
    print n_nonexes
    
