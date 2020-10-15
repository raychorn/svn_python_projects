import os
import sys
import re
import compileall
from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint
from vyperlogix.win import winreg
from vyperlogix.hash import lists
from vyperlogix.misc import ObjectTypeName
from vyperlogix.zip import getZipFilesAnalysis
from vyperlogix.zip import copyZipFile
import random
import traceback

import cython_templates
import distutils_templates

__copyright__ = """\
(c). Copyright 1990-2014, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

_isHelp = False
_isVerbose = False
_isEgg = False
_isNosource = False
_ignore = []
_isNoCleanup = False
_isExt = False

_version = _utils.getVersionNumber()
_isVersion23 = (_version >= 230) and (_version <= 239)
_isVersion25 = (_version >= 250) and (_version <= 259)

_progName = ''

_setupPy_name = 'setup.py'
_EggBatch_name = 'make-egg.cmd'

_pythonEXE_name = 'python.exe'

_EggBatch_lines = ['@echo off'] # 'cd "#libdest#"'

_EggBatch_contents = '%s -O "#libroot#\\setup.py" bdist_egg'
_EggBatch_contents_nosource = '%s --exclude-source-files'

_EggBatch_options = [_EggBatch_contents,_EggBatch_contents_nosource]

def EggBatch_options(p):
    m1 = _EggBatch_contents % (p)
    l = [m1,_EggBatch_contents_nosource % (m1)]
    print '%s :: %s' % (misc.funcName(),l)
    return l

_rootKeyName = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'

random.seed()

from vyperlogix.crypto.Encryptors import *

_encryptor_method = Encryptors.none

_source_less_types = ['pyc', 'pyo']
_ext_types = ['pyd']
_source_types = ['py']
_acceptable_types = list(set(_source_less_types + _source_types + _ext_types))
_source_less_types_all = list(set(_source_less_types + _ext_types))

def os_sep_from_path(path):
    if (not path.startswith(os.sep)):
	return os.sep
    return ''

def updateEggsHistory(root,fname):
    subKey = winreg.get_key(root, _progName, winreg.KEY.ALL_ACCESS)
    if ('eggs' not in subKey.keys):
	subKey.values['eggs'] = winreg.solve('')
    l = subKey.values['eggs'].split(',')
    if (fname not in l):
	l.append(fname)
    subKey.values['eggs'] = winreg.solve(','.join(l))
    print 'Egg History=[%s]' % subKey.values['eggs']

# T0-Do: +++
#         1). Oragami Folding Technique + Random Bit 7 unset based on all set.
#         2). Remove the _blowfish argument - make it _method from an Enumeration.
#         3). Remove blowfish completely - try XTEA to see if that works.
#         4). Naming convention for the encoded file, e for encoded and x for XTEA.

def makeEggEncrypted(fname,zipPrefix='EGG-INFO/'):
    import zipfile
    
    def _checkTypes(t):
	global _source_types
	global _source_less_types
	global _source_less_types_all
	_any_sourceless = (len([_t for _t in _source_less_types_all if (_t in t)]) > 0)
	_all_sourceful = (len([_t for _t in _source_types if (_t in t)]) > 0)
	return (len(t) == 1) or (_any_sourceless) or (_all_sourceful) or ( (len(zipPrefix) > 0) and (f.startswith(zipPrefix)) )
    
    def _adjustTypes(t):
	global _encryptor_method
	global _source_less_types
	if (_encryptor_method != Encryptors.none):
	    t = list(set(t)-set(_source_less_types))
	return t
    
    def _adjustContents(fType,fName,fContents,d_analysis):
	global _encryptor_method
	global _source_less_types_all
	if (fType not in _source_less_types_all) and (not fName.startswith(zipPrefix)):
	    if (_encryptor_method == Encryptors.simple):
		fContents = encryptSimple(fContents)
	return fContents
    
    def _postProcess(tmpFolder,zip,newZip,d_analysis):
	global _encryptor_method
	try:
	    _zipPrefix = zipPrefix.replace('/','')
	    _signature = '/'.join([_zipPrefix,'signature'])
	    sigName = os.sep.join([tmpFolder,_signature.replace('/',os.sep)])
	    sigFh = open(sigName,'w')
	    sigFh.write(str(_encryptor_method).split('=')[-1])
	    sigFh.flush()
	    sigFh.close()
	    newZip.write( sigName,_signature, zipfile.ZIP_DEFLATED)
	except:
	    pass
	finally:
	    try:
		os.remove(sigName)
	    except:
		pass
	    
    def _cleanup(fname,newName):
	if (os.path.exists(fname)) and (os.path.exists(newName)):
	    targetFolder = os.path.dirname(fname)
	    targetFname = os.sep.join([targetFolder,'e%s'%(os.path.basename(fname))])
	    _utils.copyFile(newName,targetFname)
	else:
	    print >>sys.stderr, 'WARNING: Cannot copy the Encrypted Egg from "%s" to the target-folder of "%s".' % (fname,targetFname)
	pass
    
    copyZipFile.copyZipFile(fname,checkTypes=_checkTypes,adjustTypes=_adjustTypes,adjustContents=_adjustContents,postProcess=_postProcess,cleanup=_cleanup,zipPrefix=zipPrefix,acceptable_types=['py'])

def performSanityCheckOnEggs(root,eggs):
    #import zipfile
    #from vyperlogix.misc import collectFromPath
    
    #_root = os.sep.join(root.split(os.sep)[0:-1])
    #d_files = collectFromPath.collectFilesFromPath(_root)
    #_unacceptable_folder_prefixes = ['%sbuild%s' % (os.sep,os.sep),'%sdist%s' % (os.sep,os.sep),'%smake-egg.cmd' % (os.sep),'%ssetup.py' % (os.sep),'%ssetup.pyc' % (os.sep),'%ssetup_helper.py' % (os.sep),'%ssetup_helper.pyc' % (os.sep)]
    #for k,v in d_files.iteritems():
	#d_files[k] = None
	#_k = k.replace(_root,'')
	#if not any([n for n in _unacceptable_folder_prefixes if (_k.startswith(n))]):
	    #d_files[_k] = v
    #src_analysis = getZipFilesAnalysis.getZipFilesAnalysis(d_files,_acceptable_types=_acceptable_types)
    #for egg in eggs:
	#_eggName = os.sep.join([root,egg])
	#_zip = zipfile.ZipFile(_eggName,'r',zipfile.ZIP_DEFLATED)
	#egg_analysis = getZipFilesAnalysis.getZipFilesAnalysis(_zip,prefix='EGG_INFO/',_acceptable_types=_acceptable_types)
	#_zip.close()
	#_zip = zipfile.ZipFile(_eggName,'a',zipfile.ZIP_DEFLATED)
	#try:
	    #for k,v in egg_analysis.iteritems():
		#for nv in v[0]:
		    #kv = '.'.join([k,nv])
		    #src = d_files[kv]
		    #if (src):
			#_src = src.replace(_root,'').replace(os.sep,'/')[1:]
			#_zip.write(src,_src,zipfile.ZIP_DEFLATED)
		    #pass
		#pass
	#finally:
	    #_zip.close()
    return

def layAnEgg(regroot,fname):
    if (_isVerbose):
	print 'BEGIN: "%s".' % fname
    _cwd = os.path.abspath(os.curdir)
    _root = os.path.dirname(fname)
    os.chdir(_root)
    _details = _utils.spawnProcessWithDetails(fname)
    os.chdir(_cwd)
    if (_isVerbose):
	print 'END! "%s".' % (fname)
	print 'cwd=[%s]' % (_cwd)
	print '='*80
	print _utils.readFileFrom(fname)
	print '-'*80
	print _details
	print '='*80
    _dist = os.sep.join([_root,'dist'])
    if (os.path.exists(_dist)):
	files = [f for f in os.listdir(_dist) if f.endswith('.egg')]
	#performSanityCheckOnEggs(_dist,files)
	for f in files:
	    _src = os.sep.join([_dist,f])
	    _dst = os.sep.join([_cwd,f])
	    try:
		if (os.path.exists(_dst)):
		    os.remove(_dst)
		_utils.copyFile(_src,_dst)
		if (_isVerbose):
		    print 'Copied "%s" to "%s".' % (_src,_dst)
		# +++ - Here we convert the ZIP Egg into an Encrypted Egg one file at a time from the Egg (ZIP)
		if (_encryptor_method != Encryptors.none):
		    if (_isVerbose):
			print 'makeEggEncrypted "%s".' % (_dst)
		    makeEggEncrypted(_dst)
	    except IOError, details:
		_reason = 'Disk may be full or the directory "%s" may have the wrong permissions.' % (os.path.dirname(_dst))
		if (sys.platform == 'win32'):
		    _reason += ' If your OS is Vista then you may wish to run this program using Admin rights.'
		print >>sys.stderr, '%s :: Reason: %s' % (details,_reason)
		exc_info = sys.exc_info()
		info_string = '\n'.join(traceback.format_exception(*exc_info))
		print >>sys.stderr, info_string
	    except:
		exc_info = sys.exc_info()
		info_string = '\n'.join(traceback.format_exception(*exc_info))
		print >>sys.stderr, info_string
	    try:
		updateEggsHistory(regroot,os.path.basename(_dst))
	    except:
		pass
    if (not _isNoCleanup):
	_utils.removeAllFilesUnder(_root)
    pass

def postProcessEgg(_cwd,fname,isSplitOff=True,isPrune=False):
    import zipfile
    ignore_prefix = 'EGG-INFO/'
    sources_fname = '%sSOURCES.txt' % (ignore_prefix)
    toplevel_fname = '%stop_level.txt' % (ignore_prefix)
    ignore_files = ['setup.py']
    ignore_patterns = [ignore_prefix.lower(),'.pyc','.pyo']
    
    def _adjustContents(fType,fName,fContents,d_analysis):
	def adjustedFileList(d):
	    new_list = []
	    for k,v in d.iteritems():
		for ext in v:
		    _fname = '.'.join([k,ext])
		    if (_fname not in ignore_files) and not any([(_fname.lower().find(p) > -1) for p in ignore_patterns]):
			new_list.append(_fname)
	    return new_list
	
	if (fName.lower() == sources_fname.lower()):
	    new_list = adjustedFileList(d_analysis)
	    fContents = '\n'.join(new_list)
	elif (fName.lower() == toplevel_fname.lower()):
	    new_list = list(set([f.split('/')[0] for f in adjustedFileList(d_analysis)]))
	    fContents = '\n'.join(new_list)
	return fContents
    
    def _cleanup(fname,newName):
	if (os.path.exists(fname)) and (os.path.exists(newName)):
	    targetFolder = os.path.dirname(fname)
	    if (isSplitOff):
		targetFname = os.sep.join([targetFolder,'ext%s'%(os.path.basename(fname))])
		_utils.copyFile(newName,targetFname)
	    elif (isPrune):
		os.remove(fname)
		if (os.path.splitdrive(newName)) == (os.path.splitdrive(fname)):
		    os.rename(newName,fname)
		else:
		    _utils.copyFile(newName,fname)
		    os.remove(newName)
	else:
	    print >>sys.stderr, 'WARNING: Cannot %s the Encrypted Egg from "%s" to the target-folder of "%s".' % ('copy' if (isSplitOff) else 'prune',fname,targetFname)
	pass
    
    def _adjustAnalysis(d_analysis):
	if (lists.isDict(d_analysis)):
	    d = lists.HashedLists2(d_analysis.asDict())
	    if (isSplitOff):
		keys = [k for k in d_analysis.keys() if (k.startswith('ext/')) or (k.startswith('EGG-INFO/'))]
		keys_to_remove = list(set(d_analysis.keys()) - set(keys))
	    elif (isPrune):
		keys_to_remove = [k for k in d_analysis.keys() if (k.startswith('ext/'))]
	    for k in keys_to_remove:
		del d[k]
	    return d
	return d_analysis
    
    try:
	_fname = os.sep.join([_cwd,os.path.basename(fname)])
	copyZipFile.copyZipFile(_fname,adjustAnalysis=_adjustAnalysis,cleanup=_cleanup,adjustContents=_adjustContents,zipPrefix='EGG-INFO/')
    except:
        exc_info = sys.exc_info()
        info_string = '\n'.join(traceback.format_exception(*exc_info))
	print >>sys.stderr, info_string
	pass

def postProcessEggs():
    _cwd = os.path.abspath(os.curdir)
    _eggs = [f for f in os.listdir(_cwd) if (os.path.isfile(f)) and (os.path.splitext(f)[-1] == '.egg')]
    if (len(_eggs) == 2):
	e_egg = [f for f in _eggs if (f.startswith('e'))][0]
	n_egg = [f for f in _eggs if (not f.startswith('e'))][0]
	# n_egg - split-off ext/ and EGG-INFO/ into an egg named extBLAH-BLAH.egg.
	postProcessEgg(_cwd,n_egg,isSplitOff=True,isPrune=False)
	# e_egg - prune ext/ and EGG-INFO/ from the egg. (reverse the logic for n_egg - keep everything but the stuff n_egg keeps)
	postProcessEgg(_cwd,e_egg,isSplitOff=False,isPrune=True)
	# n_egg - split-off ext/ but not EGG-INFO/ into an egg named BLAH-BLAH.egg.
	postProcessEgg(_cwd,n_egg,isSplitOff=False,isPrune=True)
	pass
    else:
	if (_isVerbose):
	    print 'WARNING: Cannot determine the list of eggs to work with - cannot post-process eggs.'

def updateAddOrRemoveProgramStrings(root, op='ADD'):
    op = str(op).upper()
    if (op == 'ADD'):
	try:
	    subKey = winreg.get_key(root, _progName, winreg.KEY.ALL_ACCESS)
	    subKey.values['HelpLink'] = winreg.solve('mailto:support@vyperlogix.com')
	    subKey.values['URLUpdateInfo'] = winreg.solve('http://www.pypi.info')
	    subKey.values['NoModify'] = winreg.solve(1)
	    subKey.values['NoRepair'] = winreg.solve(1)
	    subKey.values['Publisher'] = winreg.solve('Vyper Logix Corp.')
	except:
	    pass
    elif (op == 'REMOVE'):
	root.remove(_progName)

def main(libroot,libdest,isEgg,isNosource,ignore,isExt):
    _reg_root = winreg.get_key(winreg.HKEY.LOCAL_MACHINE, _rootKeyName, winreg.KEY.ALL_ACCESS)
    updateAddOrRemoveProgramStrings(_reg_root)
    _destTarget = libroot.split(os.sep)[-1]
    _destFolder = os.sep.join([libdest,_destTarget])
    if (not os.path.exists(_destFolder)):
	_utils._makeDirs(_destFolder)
    _files = []
    _dirs = []
    _reFilter = __reFilter = '[._]svn' 
    if (not isinstance(ignore,list)):
	ignore = [ignore]
    if (ignore) or (len(ignore) > 0):
	for ig in ignore:
	    if (len(ig) > 0):
		_reFilter += '|%s' % os.sep.join([ig.split(os.sep)[-1]])
    c_fileFilter = ['.pyx']
    _fileFilter = ['.py','.pyc'] + c_fileFilter
    _rx=re.compile(_reFilter)
    rejecting_re=re.compile(__reFilter)
    try:
	compileall.compile_dir(libroot, rx=_rx, force=True, quiet=not _isVerbose)
    except SyntaxError, details:
	print >>sys.stderr, 'WARNING :: Unable to compile due to "%s".' % details
    _re = re.compile(r"\.pyo", re.IGNORECASE)
    _utils.removeAllFilesUnder(libroot,matching_re=_re,rejecting_re=rejecting_re)
    _utils.removeAllFilesUnder(_destFolder)
    for root, dirs, files in _utils.walk(libroot, topdown=True, rejecting_re=rejecting_re):
	if (not _rx.search(root)) and (not any([root.find(ig) > -1 for ig in ignore])):
	    _root = root.split(os.sep)[-1]
	    _dname = os.sep.join([_destFolder,_root])
	    _dirs.append(_dname)
	    _isInRoot = (root == libroot)
	    c_files = []
	    for f in files:
		if (_isInRoot and f.startswith('setup') and f.endswith('.py')) or (any([f.endswith(_f) for _f in _fileFilter])):
		    _fnameIn = os.sep.join([root,f])
		    _fToks = _fnameIn.split(os.sep)
		    _fSuffix = os.sep.join(_fToks[_fToks.index(_destTarget)+1:])
		    _fnameOut = os.sep.join([_destFolder,_fSuffix])
		    _rootOut = os.sep.join([_destFolder,os.path.dirname(_fSuffix)])
		    _files.append(_fnameOut)
		    if (any([f.endswith(_f) for _f in c_fileFilter])):
			c_files.append(_fnameOut)
		    try:
			_utils.copyFile(_fnameIn,_fnameOut)
		    except IOError, details:
			_reason = 'Disk may be full or the directory "%s" may have the wrong permissions.' % (os.path.dirname(_fnameOut))
			if (sys.platform == 'win32'):
			    _reason += ' If your OS is Vista then you may wish to run this program using Admin rights.'
			print >>sys.stderr, '%s :: Reason: %s' % (details,_reason)
	    if (len(c_files) > 0):
		_build_files = []
		fList = [os.sep.join([_rootOut,_f]) for _f in os.listdir(_rootOut) if (_f.lower().find('setup.') > -1)]
		for _f in fList:
		    os.remove(_f)
		_ExtensionName = root.split(os.sep)[-1]
		fName = os.sep.join([_rootOut,'setup.py'])
		_build_files.append(fName)
		fOut = open(fName,'w')
		fOut.writelines(cython_templates.template1)
		for _f in c_files:
		    fOut.writelines(cython_templates.template2 % (_ExtensionName,os.path.basename(_f)))
		fOut.writelines(cython_templates.template3 % (_ExtensionName))
		fOut.flush()
		fOut.close()

		_python_path = _utils.validatePathEXE_using_environ()
		
		if (len(_python_path) > 0):
		    fName = os.sep.join([_rootOut,'build.cmd'])
		    _build_files.append(fName)
		    fOut = open(fName,'w')
		    fOut.writelines(cython_templates.cmd_template % (_python_path))
		    fOut.flush()
		    fOut.close()
		    _chdir = os.getcwd()
		    os.chdir(_rootOut)
		    _utils.spawnProcessWithDetails(fName)
		    os.chdir(_chdir)
		else:
		    print >>sys.stderr, 'ERROR : Cannot build "%s" in "%s".' % (c_files,_rootOut)
		    
		for n in _build_files:
		    if (os.path.exists(n)):
			os.remove(n)

		c_files = []
		pass
    if (isEgg):
	_libdest = libdest
	_files = os.listdir(libdest)
	_filesDir = os.sep.join([_libdest,_files[0] if (len(_files) > 0) else ''])
	if (len(_files) == 1) and (os.path.isdir(_filesDir)):
	    _libdest = _filesDir
	_setupPy = os.sep.join([_libdest,_setupPy_name])
	if (not os.path.exists(_setupPy)):
	    fOut = open(_setupPy,'w')
	    fOut.writelines("longdesc = '''%s'''" % distutils_templates.longdesc)
	    fOut.writelines('')
	    fOut.writelines(distutils_templates.template1)
	    fOut.flush()
	    fOut.close()
	    pass
	if (not os.path.exists(_EggBatch_name)):
	    _fname = os.sep.join([_libdest,_EggBatch_name])
	    fOut = open(_fname,'w')
	    fOut.writelines('\n'.join(_EggBatch_lines))
	    fOut.write('\n')
	    _i = 1
	    if (not isNosource):
		_i = 0
	    fOut.writelines('\n'.join([_EggBatch_options[_i]]))
	    fOut.flush()
	    fOut.close()
	    if (isEgg):
		layAnEgg(_reg_root,_fname)
	    if (isExt):
		postProcessEggs()
	    pass
	pass
    
if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(main)
    
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'displays this help text.',
	    '--nocleanup':'perform cleanup or not.',
	    '--verbose':'output more stuff.',
	    '--egg':'make-egg on the target.',
	    '--ext':'split ext files from the main Egg into a separate egg also remote ext from encrpted egg.',
	    '--nosource':'eggs laid without source.',
	    '--libroot=?':'path to root of the library.',
	    '--libdest=?':'path to root of the destination for the library.',
	    '--ignore=?':'[item,item] or [%libroot%\item,item] list of folders to ignore, such as archives or the like.',
	    '--enc=?':'specifies the encryption model being used, one of %s.' % str(Encryptors)}
    _argsObj = Args.Args(args)
    if (_isVerbose):
	print '_argsObj=(%s)' % str(_argsObj)

    _isHelp = False
    try:
	if _argsObj.booleans.has_key('isHelp'):
	    _isHelp = _argsObj.booleans['isHelp']
    except:
	_isHelp = False

    if ( (len(sys.argv) == 1) or (_isHelp) ):
	ppArgs()
    else:
	_progName = _argsObj.programName
	_isVerbose = False
	try:
	    if _argsObj.booleans.has_key('isVerbose'):
		_isVerbose = _argsObj.booleans['isVerbose']
	except:
	    _isVerbose = False

	_isEgg = False
	try:
	    if _argsObj.booleans.has_key('isEgg'):
		_isEgg = _argsObj.booleans['isEgg']
	except:
	    _isEgg = False

	_isExt = False
	try:
	    if _argsObj.booleans.has_key('isExt'):
		_isExt = _argsObj.booleans['isExt']
	except:
	    _isExt = False

	_isNosource = False
	try:
	    if _argsObj.booleans.has_key('isNosource'):
		_isNosource = _argsObj.booleans['isNosource']
	except:
	    _isNosource = False
	
	_isNoCleanup = False
	try:
	    if _argsObj.booleans.has_key('isNocleanup'):
		_isNoCleanup = _argsObj.booleans['isNocleanup']
	except:
	    _isNoCleanup = False

	_encryptor_method = Encryptors.none
	try:
	    if _argsObj.arguments.has_key('enc'):
		_encryptor_method = Encryptors(_argsObj.arguments['enc'])
		_encryptor_method = _encryptor_method if (str(_encryptor_method) in Encryptors) else Encryptors.none
	except:
	    _encryptor_method = Encryptors.none
	    
	try:
	    if _argsObj.arguments.has_key('libroot'):
		p = _argsObj.arguments['libroot']
		_lib_root = os.path.abspath(_utils.expandMacro(p,os.environ)[0])
	    else:
		_lib_root = ''
	except:
	    _lib_root = ''

	try:
	    if _argsObj.arguments.has_key('libdest'):
		p = _argsObj.arguments['libdest']
		_lib_dest = os.path.abspath(_utils.expandMacro(p,os.environ)[0])
	    else:
		_lib_dest = ''
	except:
	    _lib_dest = ''
	    
	__isUsingTmp = False
	if (len(_lib_dest) == 0):
	    _lib_dest = _utils.tempFile(random.randint(0,2**31))
	    __isUsingTmp = True
	    if (not os.path.exists(_lib_dest)):
		os.mkdir(_lib_dest)

	try:
	    if _argsObj.arguments.has_key('ignore'):
		p = _argsObj.arguments['ignore']
		p = ''.join((''.join(p.split('[')[-1])).split(']')[0])
		toks = [os.sep.join([_utils.expandMacro(s,_argsObj.arguments)[0] for s in t.split(os.sep)]) for t in p.split(',')]
		_ignore = toks
	    else:
		_ignore = []
	except:
	    _ignore = []
	
	if (_isNosource) and (_encryptor_method != Encryptors.none):
	    _isNosource = False
	    print >>sys.stderr, 'When --enc=? is used --nosource is not allowed, therefore --nosource has been reversed.'

	_EggBatch_lines = [_utils.expandMacro(f.replace('#','%'),_argsObj.arguments)[0] for f in _EggBatch_lines]
	    
	p = _utils.validatePathEXE(fname=_pythonEXE_name,verbose=_isVerbose)
	if (len(p) > 0):
	    _EggBatch_options = EggBatch_options(p)
	else:
	    import sys
	    print 'WARNING :: Unable to locate the "%s" executable, it was not found on the PATH or PYTHONPATH.' % (_pythonEXE_name)
	    sys.exit(1)
	    
	_EggBatch_options = [_utils.expandMacro(f.replace('#','%'),_argsObj.arguments)[0] for f in _EggBatch_options]

	if (not os.path.exists(_lib_dest)):
	    os.mkdir(_lib_dest)
	    
	if (os.path.exists(_lib_root)):
	    fpath = os.path.dirname(sys.argv[0])
	    if (not os.path.exists(fpath)) or (fpath.find(os.sep) == -1):
		fpath = os.path.abspath(fpath)
	    _crc = _utils.crc32(fpath, isVerbose=False, isObfuscated=True)
	    #print '(***) %s, crc32=%s' % (fpath,_crc)
	    
	    if (_lib_dest in _ignore):
		_ignore = [item for item in _ignore if (item != _lib_dest)]
	    main(_lib_root, _lib_dest, _isEgg, _isNosource, _ignore, _isExt)

	    if (__isUsingTmp) and (not _isNoCleanup):
		_utils.removeAllFilesUnder(_lib_dest)
		if (os.path.exists(_lib_dest)):
		    os.rmdir(_lib_dest)
		if (_isVerbose):
		    print 'Removed the temporary folder "%s".' % (_lib_dest)
	else:
	    print 'ERROR :: Unable to launch this program using the arguments as listed below because "%s" does not exist.' % (_lib_root)
	    ppArgs()
	    print str(sys.argv)

