from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.win import links

from vyperlogix.misc import ObjectTypeName

from vyperlogix.misc import threadpool
_Q_ = threadpool.ThreadQueue(1000)

from vyperlogix.django import django_utils
from vyperlogix.classes.SmartObject import SmartFuzzyObject
from vyperlogix.misc import _utils

from vyperlogix.json import json_to_python
from vyperlogix.xml.xml_utils import xml_to_json, python_to_xml

from vyperlogix.xml.XMLJSON import python_to_json

from vyperlogix.lists import ListWrapper
from vyperlogix.hash.lists import HashedLists

from vyperlogix.enum.Enum import Enum

import os, sys
import random

import uuid

import logging

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

import tempfile, shutil, os, time

try:
    import subprocess
    have_subprocess = 1
except ImportError:
    have_subprocess = 0

class Options(Enum):
    none = 0
    djangoappengine = 2^0

@threadpool.threadify(_Q_)
def _threaded_copyFile(src,dst,func=None,verbose=False,use_logging=False,no_shell=False):
    _utils.copyFile(_src_f_,_dst_f_,verbose=_isVerbose,use_logging=_isVerbose,no_shell=True,num_threads=len(_Q_))

def find_svn_tools():
    svnlook = None
    svnadmin = None
    if (not os.path.exists(svnlook)):
	print 'Searching for svnlook.'
	svnlook = _utils.findUsingPath(r"@SVN_BINDIR@/svnlook")
	    
    if (svnlook is not None) and (os.path.exists(svnlook)):
	print 'Found svnlook at "%s".' % (svnlook)
	root = os.path.dirname(svnlook)
	svnadmin_fname = os.sep.join([root,'svnadmin.exe'])
	if (os.path.exists(svnadmin_fname)):
	    svnadmin = svnadmin_fname
	else:
	    print 'Searching for svnadmin.'
	    svnadmin = _utils.findUsingPath(r"@SVN_BINDIR@/svnadmin")
	    if (svnlook is not None) and (os.path.exists(svnlook)):
		print 'Found svnadmin at "%s".' % (svnadmin)
	    else:
		print 'Could not find svnadmin at "%s", cannot proceed. Install SVN Admin functions and try again.' % (svnadmin)
    else:
	print 'Could not find svnlook at "%s", cannot proceed. Install SVN Admin functions and try again.' % (svnlook)
    return svnlook,svnadmin

def copy_files_from_possible_svn_project(top,target,ignores=[]):
    import re
    svn_regex = re.compile('[._]svn')
    svnlook = svnadmin = None
    _isSVN = _utils.containsSvnFolders(top)
    if (_isSVN):
	svnlook,svnadmin = find_svn_tools()
	if (svnadmin):
	    if have_subprocess:
		# make this an export command... ???
		p = subprocess.Popen([svnadmin, "hotcopy", repo_dir, backup_subdir, "--clean-logs"])
		print 'subprocess is %s or "%s".' % (p.pid,str(p))
		__pid__ = p.pid
	    else:
		from vyperlogix.process import Popen
		if (_utils.isUsingWindows):
		    # make this an export command... ???
		    Popen.Shell('echo F | XCOPY "%s" "%s" /Q /V /C /Y /I' % (src,dst), shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=sys.stdout)
		else:
		    # make this an export command... ???
		    Popen.Shell('cp -f %s %s' % (src,dst), shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=sys.stdout)
    # determine if the scaffold is controled by SVN and if so - 
    #    handle the export using svnadmin if present or use this method as a fall-back.
    for root, dirs, files in _utils.walk(top,rejecting_re=svn_regex):
	for f in files:
	    _src_f_ = os.sep.join([root,f])
	    _bias = os.sep.join(root.replace(top,'').split(os.sep)[1:])
	    _dst_f_ = os.sep.join([target,_bias,f])
	    if (_isThreaded):
		_threaded_copyFile(_src_f_,_dst_f_,verbose=_isVerbose,use_logging=_isVerbose,no_shell=True)
	    else:
		_utils.copyFile(_src_f_,_dst_f_,verbose=_isVerbose,use_logging=_isVerbose,no_shell=True)
	for f in dirs:
	    if (f not in ignores):
		_dst_ = os.sep.join([target,f])
		_utils._makeDirs(_dst_)
		if (_isVerbose):
		    logging.info('%s.1 makeDirs "%s".' % (misc.funcName(),_dst_))
	    pass
	pass

def make_djangoappengine_project():
    '''
    <project-target>/autoload
    <project-target>/dbindexer
    <project-target>/django
    <project-target>/djangoappengine
    <project-target>/djangotoolbox
    <project-target>/filetransfers (edit the settings.py file)
    <project-target>/search        (edit the settings.py file)
    
    (1). Create the scaffold for the project.
    (2). Create the Symbolic Links.
    (3). Make sure the scaffold is usable with settings.py properly adjusted.
    '''
    _folder_names = ['autoload','dbindexer','django','djangoappengine','djangotoolbox','filetransfers','search']
    _sources_ = [os.sep.join([_fpath_source,f]) for f in _folder_names]
    _source_checks = [os.path.exists(f) for f in _sources_]
    _has_sources = all(_source_checks)
    if (_has_sources):
	if (os.path.exists(_fpath_scaffold)):
	    if (_fpath_target != _fpath_scaffold):
		if (os.path.exists(_fpath_target)) and (os.path.isdir(_fpath_target)):
		    copy_files_from_possible_svn_project(_fpath_scaffold,_fpath_target,ignores=_folder_names)
		pass
	    _targets_ = [os.sep.join([_fpath_target,f]) for f in _folder_names]
	    for i in xrange(0,len(_targets_)):
		s = _sources_[i]
		t = _targets_[i]
		if (not os.path.exists(t)):
		    if (_isVerbose):
			logging.info('%s.1 CreateSymbolicLink "%s" --> "%s".' % (misc.funcName(),s,t))
		    links.CreateSymbolicLink(t,s)
	elif (_isVerbose):
	    logging.error('%s.1 Cannot locate "%s", are you sure you know what you are doing ?' % (misc.funcName(),_fpath_scaffold))
    else:
	_missing_sources = []
	for i in xrange(0,len(_source_checks)):
	    if (not _source_checks[i]):
		_missing_sources.append(_sources_[i])
	logging.error('%s.2 Missing one or more of "%s", are you sure you know what you are doing ?' % (misc.funcName(),_missing_sources))
    pass

def make_nonrel_project():
    logging.info('%s BEGIN: ' % (misc.funcName()))
    if (os.path.exists(_fpath_source)):
	if (not os.path.exists(_fpath_target)):
	    _utils._makeDirs(_fpath_target)
	if (os.path.exists(_fpath_target)):
	    if (_option):
		if (_option == Options.djangoappengine):
		    make_djangoappengine_project()
		else:
		    logging.info('%s.1 Nothing to do at this time...' % (misc.funcName()))
	    else:
		logging.warning('%s.2 Cannot understand option of "%s", are you sure you know what you are doing ?' % (misc.funcName(),_option))
	else:
	    logging.warning('%s.3 Cannot access "%s", are you sure you have specified the correct path ?' % (misc.funcName(),_fpath_target))
    else:
	logging.warning('%s.4 Cannot access "%s", are you sure you have specified the correct path ?' % (misc.funcName(),_fpath_source))
    logging.info('%s END! ' % (misc.funcName()))

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
	    '--profiler':'use profiler.',
	    '--threaded':'use threads.',
	    '--source=?':'source folder fully qualified path.',
	    '--target=?':'target folder fully qualified path.',
	    '--scaffold=?':'scaffold folder fully qualified path (typically points to "...\_django-nonrel-projects\django-nonrel-testapp").',
	    '--option=?':'One of %s.' % ([t.name for t in Options._items_]),
	    }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = __args__.programName
	
	_isVerbose = __args__.get_var('isVerbose',bool,False)
	_isDebug = __args__.get_var('isDebug',bool,False)
	_isHelp = __args__.get_var('isHelp',bool,False)
	_isProfiler = __args__.get_var('isProfiler',bool,False)
	_isThreaded = __args__.get_var('isThreaded',bool,False)

	_fpath_target = __args__.get_var('target',misc.isString,'')
	_fpath_source = __args__.get_var('source',misc.isString,'')
	
	_fpath_scaffold = __args__.get_var('scaffold',misc.isString,'')

	_option = Options(__args__.get_var('option',misc.isString,''))
	
	logging.basicConfig(level=logging.DEBUG,
		            format='%(asctime)s %(levelname)-8s %(message)s',
		            datefmt=_utils.formatMySQLDateTimeStr()
		            )
	
	if (_isProfiler):
	    import cProfile
	    cProfile.run('make_nonrel_project()')
	else:
	    make_nonrel_project()
	
        