'''
http://crazedmonkey.com/blog/python/pkg_resources-with-py2exe.html
'''
import sys
import platform

from distutils.core import setup

import py2exe
import os, glob, fnmatch  

from py2exe.build_exe import py2exe as build_exe

import vyperlogix

class MediaCollector(build_exe):
    def copy_extensions(self, extensions):
        build_exe.copy_extensions(self, extensions)

        libs = 'libs'
        full = os.path.join(self.collect_dir, libs)
        if not os.path.exists(full):
            self.mkpath(full)

        for f in glob.glob('libs/*'):
            name = os.path.basename(f)
            self.copy_file(f, os.path.join(full, name))
            self.compiled_files.append(os.path.join(libs, name))

class VyperLogixLibraryCollector(build_exe):
    def copy_extensions(self, extensions):
        build_exe.copy_extensions(self, extensions)

	v = '%1.1f'%(__version__)
	v_v = v.replace('.','_')
	__vyperlogix__ = os.path.join('J:/@Vyper Logix Corp/@Projects/python-projects/@lib/12-13-2011-01/dist_%s'%(v),'vyperlogix_%s.zip'%(v_v))
	__has_vyperlogix__ = os.path.exists(__vyperlogix__)
	if (__has_vyperlogix__):
	    fname = os.path.basename(__vyperlogix__)
	    full = os.path.join(self.collect_dir, fname)
	    self.copy_file(__vyperlogix__,full)
	    self.compiled_files.append(os.path.basename(full))


def extract(zipfilepath, extractiondir):
    import zipfile
    zip = zipfile.ZipFile(zipfilepath)
    zip.extractall(path=extractiondir)

#datafiles = datafiles + find_data_files('Microsoft.VC90.CRT', '*.*')

    #find_data_files('libs', '*') + \
    #find_data_files('docs','*') + \
    
def do_setup(program_name=None,company_name=None,product_name=None,description=None,icon=None,product_version=None,is_service=False,minimum_python_version=2.7):
    global __version__
    
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
    __product_copyright__ = "Copyright 2013 %s" % (__company_name__)
    __icon__ = icon

    toks = platform.python_version().split('.')
    if (len(toks) > 2):
	while (len(toks) > 2):
	    toks.pop()
    __version__ = float('.'.join(toks))
    if __version__ < minimum_python_version:
	sys.exit('ERROR: Sorry, python %s is required for this application.' % (minimum_python_version))

    def rebuild_libs_if_necessary(fpath):
	import os
	from vyperlogix.misc import _utils
	from vyperlogix.process import Popen
    
	allfiles = []
	for top,dirs,files in os.walk(fpath,topdown=True,followlinks=True):
	    print top
	    for f in files:
		if (not f.endswith('.pyc')) and (not f.endswith('.pyo')):
		    allfiles.append(os.path.join(top,f))
	allfiles = filter(os.path.isfile, allfiles)
	allfiles.sort(key=lambda x: os.path.getmtime(x))
    
	v = '%1.1f'%(__version__)
	v_v = v.replace('.','_')
    
	__cwd__ = os.getcwd()
	__vyperlogix__ = os.path.join(__cwd__,'libs','vyperlogix_%s.zip'%(v_v))
	__has_vyperlogix__ = os.path.exists(__vyperlogix__)
	if (not __has_vyperlogix__):
	    lib_base = os.path.dirname(fpath)
	    __vyperlogix__ = os.path.join('%s/dist_%s'%(lib_base,v),'vyperlogix_%s.zip'%(v_v))
	    __has_vyperlogix__ = os.path.exists(__vyperlogix__)
	    __target__ = os.path.join(__cwd__,'libs')
	else:
	    __target__ = __vyperlogix__
    
	libdate = latest = os.path.getmtime(allfiles[-1])
	if (__has_vyperlogix__):
	    libdate = os.path.getmtime(__vyperlogix__)
	else:
	    __vyperlogix__ = os.path.join(os.path.dirname(fpath),'dist_%s'%(v),'vyperlogix_%s.zip'%(v.replace('.','_')))
	    __has_vyperlogix__ = os.path.exists(__vyperlogix__)
	    if (__has_vyperlogix__):
		libdate = os.path.getmtime(__vyperlogix__)
	if (latest > libdate):
	    print 'Compile "%s"...' % (__vyperlogix__)
    
	    v = '%1.1f'%(__version__)
	    __fpath__ = os.path.dirname(fpath)
	    __vyperlogix__ = os.path.join(__fpath__,'dist_%s'%(v),'vyperlogix_%s.zip'%(v.replace('.','_')))
	    __command__ = os.path.join(__fpath__,'compile%s.cmd'%(v))
	    __has_vyperlogix__ = os.path.exists(__fpath__)
	    __has_command__ = os.path.exists(__command__)
	    if (__has_vyperlogix__) and (__has_command__):
		ioBuf = _utils.stringIO()
		dirName = os.path.dirname(__command__).replace(os.sep,'/')
		cmd = 'cd "%s"' % (dirName)
		fOut = open('compile.cmd','w')
		print >>fOut, '@echo on\n'
		#print >>fOut, '%s\n' % (cmd)
		print >>fOut, '"%s/%s"\n' % (dirName,os.path.basename(__command__))
		fOut.flush()
		fOut.close()
		Popen.Shell(fOut.name, shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=ioBuf)
		print >>sys.stdout, ioBuf.getvalue()
		fname = str(os.sep.join([os.path.dirname(os.path.dirname(__vyperlogix__)),'compile%s.log'%(v)]))
		if (os.path.exists(fname)):
		    import re
		    print >>sys.stderr, 'fname=%s' % (fname)
		    results = _utils.readFileFrom(fname)
		    print sys.stdout, results
		    __re__ = re.compile(r"\[\s*Errno\s*\d*\]", re.MULTILINE)
		    if __re__.match(results):
			print >>sys.stderr, 'WARNING: Stopping due to an error.'
		else:
		    print >>sys.stderr, 'WARNING: Cannot locate "%s".' % (fname)
	    else:
		print >>sys.stderr, 'Missing "%s" or missing "".' % (__vyperlogix__,__command__)
	__has_vyperlogix__ = os.path.exists(__vyperlogix__)
	print >>sys.stderr, 'INFO: __vyperlogix__=%s' % (__vyperlogix__)
	print >>sys.stderr, 'INFO: __has_vyperlogix__=%s' % (__has_vyperlogix__)
	#if (__has_vyperlogix__):
	    #t = __target__ if (os.path.isdir(__target__)) else os.path.dirname(__target__)
	    #print >>sys.stderr, 'INFO(1): t=%s' % (t)
	    #t = os.sep.join([t,'libs'])
	    #print >>sys.stderr, 'INFO: extract %s --> %s' % (__vyperlogix__,t)
	    #_utils.removeAllFilesUnder(t)
	    #_utils.makeDirs(t)
	    #extract(__vyperlogix__,t)
	    #_utils.copyFile(__vyperlogix__,__target__)
	return

    from vyperlogix import misc
    from vyperlogix.misc import _utils
    _utils.removeAllFilesUnder(os.path.abspath(r'.\build'))
    _utils.removeAllFilesUnder(os.path.abspath(r'.\dist'))
    _utils.removeAllFilesUnder(os.path.abspath(r'.\libs'))
    lib_base = os.path.dirname(vyperlogix.__file__) if (os.path.isfile(vyperlogix.__file__)) else vyperlogix.__file__
    rebuild_libs_if_necessary(lib_base)

    normalize = lambda *args:os.path.normpath(os.path.join(*args))
    def find_data_files(srcdir, *wildcards, **kw):
	def walk_helper(arg, dirname, files):
	    if '.svn' in dirname:
		return
	    names = []
	    lst, wildcards = arg
	    for wc in wildcards:
		wc_name = normalize(dirname, wc)
		for f in files:
		    filename = normalize(dirname, f)
    
		    if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
			names.append(filename)
	    if names:
		lst.append( (dirname, names ) )
    
	file_list = []
	recursive = kw.get('recursive', True)
	if recursive:
	    os.path.walk(srcdir, walk_helper, (file_list, wildcards))
	else:
	    walk_helper((file_list, wildcards),
		        srcdir,
		        [os.path.basename(f) for f in glob.glob(normalize(srcdir, '*'))])
	return file_list
    #pkgs =      ['Crypto' ]
    pkgs =      []
    datafiles = [ ('.', ['run.cmd']) ]
    excludes = ["pywin", "pywin.debugger", "pywin.debugger.dbgcon",
	        "pywin.dialogs", "pywin.dialogs.list", "vyperlogix", 'paramiko', 'MySQLdb' ]
    
    includes = ['web', 'web.wsgiserver', 'web.contrib',  'web.http',
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
    if (is_service):
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
	windows_service = Target(
	    # used for the versioninfo resource
	    description = __product_description__,
	    # What to build
	    modules = [ __program_name__ ],
	    cmdline_style = 'pywin32',
	    other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog=__program_name__))],
	    dest_base = __program_name__,
	    icon_resources = [(0, __icon__)]
	)
	setup(
	    name=__program_name__,
	    version=__product_version__,                            # build.py magic comment
	    package_dir = {
	        #'Crypto':'C:\\Python27\\Lib\\site-packages\\Crypto'
	        },
	    description=__product_description__,
	    packages = pkgs,
	
	    options = {"py2exe": {"compressed": True,
	                          "optimize": 2,
	                          "ascii": False,
	                          "bundle_files": 1,
	                          "includes": includes,
	                          "excludes": excludes,
	                          'dist_dir': os.path.abspath('./dist'),
	                          "dll_excludes": ['w9xpopen.exe', "mswsock.dll", "MSWSOCK.dll", "powrprof.dll", '_mysql.pyd', 'LIBEAY32.dll', '_ssl.pyd'],
	                          }
	               },
	    zipfile = None,
	    data_files = datafiles,
	    cmdclass = {"py2exe": VyperLogixLibraryCollector},
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
		self.description = __product_description__
	
	windows_console = Target(
            description = __product_description__,
            modules = [ __program_name__ ],
            cmdline_style = 'pywin32',
            dest_base = __program_name__,
            icon_resources = [(0, __icon__)]
	)

	setup(
	    name=__program_name__,
	    version=__product_version__,                            # build.py magic comment
	    package_dir = {
	        'Crypto':'C:\\Python27\\Lib\\site-packages\\Crypto'
	        },
	    description=__product_description__,
	    packages = pkgs,
	
	    options = {"py2exe": {"compressed": True,
	                          "optimize": 2,
	                          "ascii": False,
	                          "bundle_files": 1,
	                          "includes": includes,
	                          "excludes": excludes,
	                          'dist_dir': os.path.abspath('./dist'),
	                          "dll_excludes": ['w9xpopen.exe', "mswsock.dll", "MSWSOCK.dll", "powrprof.dll", '_mysql.pyd', 'LIBEAY32.dll', '_ssl.pyd'],
	                          }
	               },
	    zipfile = None,
	    data_files = datafiles,
	    cmdclass = {"py2exe": VyperLogixLibraryCollector},
	    console = [windows_console],
	)
