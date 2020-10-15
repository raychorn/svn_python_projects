#
#  hot-backup.py: perform a "hot" backup of a Subversion repository
#                 and clean any old Berkeley DB logfiles after the
#                 backup completes, if the repository backend is
#                 Berkeley DB.
#
#  Subversion is a tool for revision control. 
#  See http://subversion.tigris.org for more information.
#    
# ====================================================================
# Copyright (c) 2000-2007 CollabNet.  All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.  The terms
# are also available at http://subversion.tigris.org/license-1.html.
# If newer versions of this license are posted there, you may use a
# newer version instead, at your option.
#
# This software consists of voluntary contributions made by many
# individuals.  For exact contribution history, see the revision
# history and logs, available at http://subversion.tigris.org/.
# ====================================================================

# ====================================================================
# Defects:
# (1). Not tossing out old backups to reduce disk space.
# (2). Not moving backups into the carbonite folder.
# (3). Not tossing-out old carbonite backups to reduce space.
# ====================================================================
# AWS Commands
# aws ls __vyperlogix_svn_backups__/backups
# aws delete __vyperlogix_svn_backups__/backups/repo1-14761.tar.gz
#
# $HeadURL$
# $LastChangedDate$
# $LastChangedBy$
# $LastChangedRevision$

######################################################################

import sys, os, getopt, stat, string, re, time, shutil
import traceback
import math

#print 'BEGIN:'
#for f in sys.path:
    #print f
#print 'END!'

import locale

locale.setlocale(locale.LC_ALL, "")

format_with_commas = lambda value:locale.format('%d', int(value), True)

from vyperlogix.enum.Enum import Enum

from vyperlogix import misc
from vyperlogix.process import Popen
from vyperlogix.misc import _utils
from vyperlogix.hash.lists import HashedFuzzyLists, HashedFuzzyLists2

from vyperlogix.process.shell import SmartShell

from vyperlogix.lists.ListWrapper import ListWrapper

from vyperlogix.aws.s3 import S3Shell
from vyperlogix.classes.SmartObject import SmartFuzzyObject

__is_platform_not_linux = sys.platform.count('linux') == 0
if (__is_platform_not_linux):
    from vyperlogix import oodb
else:
    print 'ERROR: Hey, this program won\'t run in anything but Windows !!!  Wake-up already !!!'
from vyperlogix.hash import lists
from vyperlogix.classes import SmartObject

from vyperlogix.crypto import XTEAEncryption

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix.misc import ioTimeAnalysis

normalize = lambda f:str(f).replace(os.sep,'/')

__pid__ = None

_iv = XTEAEncryption.iv(_utils.getProgramName())

s_passPhrase = [110,111,119,105,115,116,104,101,116,105,109,101,102,111,114,97,108,108,103,111,111,100,109,101,110,116,111,99,111,109,101,116,111,116,104,101,97,105,100,111,102,116,104,101,105,114,99,111,117,110,116,114,121]
_passPhrase = ''.join([chr(ch) for ch in s_passPhrase])

__url__ = 'www.vyperlogix.com'

__s3_bucketName__ = '__vyperlogix_svn_backups__'

# Try to import the subprocess mode.  It works better then os.popen3
# and os.spawnl on Windows when spaces appear in any of the svnadmin,
# svnlook or repository paths.  os.popen3 and os.spawnl are still used
# to support Python 2.3 and older which do not provide the subprocess
# module.  have_subprocess is set to 1 or 0 to support older Python
# versions that do not have True and False.
try:
    import subprocess
    have_subprocess = 1
except ImportError:
    have_subprocess = 0

######################################################################
# Global Settings

class ArchiveTypes(Enum):
    none = ''
    gz = 'tar.gz'
    bz2 = 'tar.bz2'
    zip = 'zip'
    ezip = 'ezip' # XTEAEncryption using Hex
    bzip = 'bzip' # blowfish
    xzip = 'xzip'
    z7 = '7z'

class BackupTypes(Enum):
    A = 0
    Alt = 0
    Alternate = 0
    Primary = 1
    Pri = 1
    P = 1
is_type_alternate = lambda value:(value in [BackupTypes.A,BackupTypes.Alt,BackupTypes.Alternate])

is_string_valid = lambda s:misc.isStringValid(s)

def other_backup_type(t):
    if (is_type_alternate(t)):
	return BackupTypes.Primary
    return BackupTypes.Alternate

######################################################################
# Helper functions

def fname_comparator(a, b):
    a_num = a.split('-')[-1]
    b_num = b.split('-')[-1]
    print 'DEBUG: a=%s, b=%s' % (a,b)
    return -1 if (a_num < b_num) else 0 if (a_num == b_num) else 1

def date_comparator(a, b):
    a_statinfo = os.stat(a)
    b_statinfo = os.stat(b)
    print 'DEBUG: a=%s, b=%s' % (a,b)
    return -1 if (a_statinfo.st_mtime < b_statinfo.st_mtime) else 0 if (a_statinfo.st_mtime == b_statinfo.st_mtime) else 1

def s3_date_comparator(a, b):
    '''a and b are both key objects that have metadata'''
    try:
	val = -1 if (a.metadata['ST_MTIME'].split('=')[0] < b.metadata['ST_MTIME'].split('=')[0]) else 0 if (a.metadata['ST_MTIME'].split('=')[0] == b.metadata['ST_MTIME'].split('=')[0]) else 1
    except Exception, ex:
	info_string = _utils.formattedException(details=ex)
	print >>sys.stderr, info_string
	val = 0 # just call them equal in case of a problem...
    return val

def s3_files_list_date_comparator(a, b):
    '''a and b are both key objects that have last_modified properties'''
    a_dt = None
    a_s = ''
    try:
	a_dt = _utils.getFromNativeTimeStamp(a.last_modified)
	a_s = a.last_modified
    except:
	try:
	    a_s = '%s %s' % (a.date,a.time)
	    a_dt = _utils.getFromDateTimeStr(a_s,format=_utils.formatAmazonS3DateTimeStr())
	except:
	    pass
    b_dt = None
    b_s = ''
    try:
	b_dt = _utils.getFromNativeTimeStamp(b.last_modified)
	b_s = b.last_modified
    except:
	try:
	    b_s = '%s %s' % (b.date,b.time)
	    b_dt = _utils.getFromDateTimeStr(b_s,format=_utils.formatAmazonS3DateTimeStr())
	except:
	    pass
    try:
	val = -1 if (a_dt < b_dt) else 0 if (a_dt == b_dt) else 1
	print 'DEBUG (%s) val=(%s) --> a_dt=%s (%s), b_dt=%s (%s)' % (misc.funcName(),val,a_dt,a_s,b_dt,b_s)
    except Exception, ex:
	info_string = _utils.formattedException(details=ex)
	print >>sys.stderr, info_string
	val = 0 # just call them equal in case of a problem...
    return val

def comparator(a, b):
    # We pass in filenames so there is never a case where they are equal.
    regexp = re.compile("-(?P<revision>[0-9]+)(-(?P<increment>[0-9]+))?")
    matcha = regexp.search(a)
    matchb = regexp.search(b)
    reva = int(matcha.groupdict()['revision']) if (matcha) else 0
    revb = int(matchb.groupdict()['revision']) if (matchb) else 0
    if (reva < revb):
        return -1
    elif (reva > revb):
        return 1
    else:
        inca = matcha.groupdict()['increment'] if (matcha) else 0
        incb = matchb.groupdict()['increment'] if (matchb) else 0
        if not inca:
            return -1
        elif not incb:
            return 1;
        elif (int(inca) < int(incb)):
            return -1
        else:
            return 1

def get_youngest_revision():
    """Examine the repository REPO_DIR using the svnlook binary
  specified by SVNLOOK, and return the youngest revision."""

    if have_subprocess:
        p = subprocess.Popen([svnlook, 'youngest', repo_dir],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        infile, outfile, errfile = p.stdin, p.stdout, p.stderr
    else:
        infile, outfile, errfile = os.popen3(svnlook + " youngest " + repo_dir)

    stdout_lines = outfile.readlines()
    stderr_lines = errfile.readlines()
    outfile.close()
    infile.close()
    errfile.close()

    if stderr_lines:
        raise Exception("Unable to find the youngest revision for repository '%s'"
                        ": %s" % (repo_dir, string.rstrip(stderr_lines[0])))

    return string.strip(stdout_lines[0])

######################################################################
# Main

from vyperlogix.decorators import onexit

@onexit.onexit
def on_exit():
    try:
	try:
	    if (__pid__ is not None):
		from vyperlogix.process import killProcByPID
		killProcByPID(p.pid)
	except KeyboardInterrupt, SystemExit:
	    pass
	finally:
	    __pid__ = None
    except:
	pass

def walk_and_collect_files_from(_target_path_,topdown=True,onerror=None,rejecting_re=None):
    _files_ = {}
    try:
	for folder,dirs,files in _utils.walk(_target_path_, topdown=topdown, onerror=onerror, rejecting_re=rejecting_re):
	    for f in files:
		_files_[f] = os.sep.join([folder,f])
    except:
	pass
    return _files_
	    
def restore_secured_backup(restore_path,repo_path,passPhrase,isVerbose=False,isMultiUnzipper=False,sevenZ=None):
    if (os.path.exists(restore_path)):
	print >>sys.stdout, 'Your --restore of "%s" exists.' % (restore_path)
	if (os.path.isfile(restore_path)):
	    from vyperlogix.zip import secure
	    fext = os.path.splitext(restore_path)
	    if (fext[-1] == '.bzip'):
		if (not os.path.exists(repo_path)) or (not os.path.isdir(repo_path)):
		    _utils.makeDirs(repo_path)
		print >>sys.stdout, 'BEGIN --restore of "%s" into "%s".' % (restore_path,repo_path)
		secure.unzipper(restore_path,repo_path,archive_type=secure.ZipType.bzip,passPhrase=passPhrase,isMultiUnzipper=isMultiUnzipper,sevenZ=sevenZ)
		print >>sys.stdout, 'END --restore of "%s" into "%s".' % (restore_path,repo_path)

		#### DEVELOPMENT +++ ####################################################################
		print >>sys.stdout, 'BEGIN: (VERIFY)'
		from vyperlogix.svn.svnadmin import SVNAdminShell
		from vyperlogix.classes.SmartObject import SmartFuzzyObject
		def __callback101__(svnadmin):
		    print >>sys.stdout, 'BEGIN :: __callback101__ (VERIFY)'
		    for item in svnadmin.data:
			print >>sys.stdout, 'item = %s' % (item)
		    print >>sys.stdout, 'END :: __callback101__ (VERIFY)'
		def __onExit101__(svnadmin):
		    print >>sys.stdout, 'BEGIN :: __onExit101__ (VERIFY)'
		    for item in svnadmin.data:
			print >>sys.stdout, 'item = %s' % (item)
		    print >>sys.stdout, 'END :: __onExit101__ (VERIFY)'
		svnAdmin = SVNAdminShell(callback=__callback101__,onExit=__onExit101__,svnadmin=svnadmin,sysout=sys.stdout)
		svnAdmin.verify(repo_path)
		print >>sys.stdout, 'END  (VERIFY) !!!'
		#### DEVELOPMENT +++ ####################################################################
	    else:
		print >>sys.stdout, 'ERROR: Cannot restore the file named "%s" because it has an unrestorable file extension of "%s".' % (restore_path,fext[-1])
	else:
	    print >>sys.stdout, 'ERROR: Your --restore of "%s" exists but is NOT a file so nothing more can be done at this time.' % (restore_path)

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()
	
    oBuf = _utils.stringIO()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
            '--test':'test some stuff.',
	    '--skip':'skip the actual backup process.',
            '--skipZiptest':'skip the ziptest process.',
            '--servicerecovery':'handle the service restart for tntdrive.',
            #'--multiUnzipper':'unzipper uses threaded process.',
            '--use7zip':'try using 7zip when it is avaialble otherwise not.',
	    '--specific':'consider only those backups that match the currently selected method otherwise consider them all.',
	    '--restore=?':'must be a valid archive file that can be restored (bzip).',
            '--oldest':'choose the oldest file from S3.',
            '--newest':'choose the newest file from S3.',
            '--output=?':'must be a valid output file (stdout and stderr).',
	    '--archive-type=?':'must be a valid archive type.',
	    '--num-backups=?':'the number of backups to keep locally.',
	    '--repo-path=?':'path to the SVN repo.',
	    '--backup-dir=?':'path to the folder where backups are to be placed, this folder can reside on a resource accessible by SSH+SFTP.',
            '--aws_access_key=?':'Amazon aws_access_key.',
            '--aws_secret_access_key=?':'Amazon aws_secret_access_key.',
            '--bucket=?':'S3 bucket name.',
            '--bucket_size=?':'S3 bucket size expressed as the number of items to keep - the rest are trashed during each run.',
            '--nocleanup':'do not perform any cleanup actions (used for debugging).',
	    '--carbonite=?':'path to the carbonite folder.',
	    '--carbonite-alt=?':'alternate path to the carbonite folder.',
	    '--carbonite-hours=?':'the number of hours between carbonite backups.',
	    '--carbonite-files=?':'the number of files to maintain in carbonite backups.',
	    '--carbonite-optimize=?':'(1/True) once the file is copied into the carbonite folder the source is removed to free-up disk-space.',
	    '--carbonite-schedule=?':'schedule for issuing carbonite backups ?type=Primary&days=M-F&hours=0-20&type=Alt&days=Sa-Su&hours=*.',
	    '--username=?':'username for SSH if using a folder path from a foreign resource otherwise leave this blank.',
	    '--password=?':'password for SSH if using a folder path from a foreign resource otherwise leave this blank.',
            '--workfile=?':'path to the commands file (C:\Program Files (x86)\@utils\svnHotBackups\commands.cmd).',
	    }
    __args__ = Args.SmartArgs(args)
    
    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = __args__.programName

	_archive_type_ = lambda val:ArchiveTypes(val)
	
	_stdout = sys.stdout

	_isVerbose = __args__.get_var('isVerbose',Args._bool_,False)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isVerbose=%s' % (_isVerbose)
	_isDebug = __args__.get_var('isDebug',Args._bool_,False)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isDebug=%s' % (_isDebug)
	_isTest = __args__.get_var('isTest',Args._bool_,False)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isTest=%s' % (_isTest)
	_isSkip = __args__.get_var('isSkip',Args._bool_,False)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isSkip=%s' % (_isSkip)
	_isSkipZiptest = __args__.get_var('isSkipZiptest',Args._bool_,False)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isSkipZiptest=%s' % (_isSkipZiptest)
	_isUse7zip = __args__.get_var('isUse7zip',Args._bool_,False)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isUse7zip=%s' % (_isUse7zip)
	#_isMultiUnzipper = __args__.get_var('isMultiUnzipper',Args._bool_,False)
	#if (_isVerbose):
	    #print >>_stdout, 'DEBUG: _isMultiUnzipper=%s' % (_isMultiUnzipper)
	_isSpecific = __args__.get_var('isSpecific',Args._bool_,False)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isSpecific=%s' % (_isSpecific)
	_isNocleanup = __args__.get_var('isNocleanup',Args._bool_,False)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isNocleanup=%s' % (_isNocleanup)
	_isHelp = __args__.get_var('isHelp',Args._bool_,False)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isHelp=%s' % (_isHelp)
	    
	_isServicerecovery = __args__.get_var('isServicerecovery',Args._bool_,False)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isServicerecovery=%s' % (_isServicerecovery)

	if (_isHelp):
	    ppArgs()
	    sys.exit()

	__archive_type_default = 'none'
	__archive_type = __args__.get_var('archive-type',_archive_type_,__archive_type_default)
	    
	try:
	    if (__archive_type is None):
		__archive_type = __archive_type_default
		l =  [item.name for item in  ArchiveTypes._items_]
		print >>_stdout, 'Invalid --archive-type of "%s"; must be one of "%s" instead.' % (__archive_type,l)
	except:
	    __archive_type = __archive_type_default
	_archive_type = __archive_type
	
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _archive_type=%s' % (_archive_type)

	num_backups = __args__.get_var('num-backups',Args._int_,int(os.environ.get("SVN_HOTBACKUP_BACKUPS_NUMBER", 64)))
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: num_backups=%s' % (num_backups)
	
	_repo_path = __args__.get_var('repo-path',Args._str_,'')
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _repo_path=%s' % (_repo_path)
	    
	_restore_path = __args__.get_var('restore',Args._str_,'')
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _restore_path=%s' % (_restore_path)
	    
	_isOldest = __args__.get_var('isOldest',Args._bool_,False)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isOldest=%s' % (_isOldest)

	_isNewest = __args__.get_var('isNewest',Args._bool_,not _isOldest)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isNewest=%s' % (_isNewest)
	    
	if (not _isOldest) and (not _isNewest):
	    _isNewest = True
	    
	_backup_dir = __args__.get_var('backup-dir',Args._str_,'')
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _backup_dir=%s' % (_backup_dir)
	    
	_output_path = __args__.get_var('output',Args._str_,None)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _output_path=%s' % (_output_path)

	_aws_access_key = __args__.get_var('aws_access_key',Args._str_,'')
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _aws_access_key=%s' % (_aws_access_key)

	_aws_secret_access_key = __args__.get_var('aws_secret_access_key',Args._str_,'')
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _aws_secret_access_key=%s' % (_aws_secret_access_key)

	_bucket_name = __args__.get_var('bucket',Args._str_,__s3_bucketName__)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _bucket_name=%s' % (_bucket_name)
	__s3_bucketName__ = _bucket_name
	
	bucket_size = __args__.get_var('bucket_size',Args._int_,int(os.environ.get("SVN_HOTBACKUP_S3_BUCKET_SIZE", 5)))
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: bucket_size=%s' % (bucket_size)

	_carbonite = __args__.get_var('carbonite',Args._str_,'')
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _carbonite=%s' % (_carbonite)
	    
	_carbonite_alt = __args__.get_var('carbonite-alt',Args._str_,'')
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _carbonite_alt=%s' % (_carbonite_alt)

	_is_carbonite = os.path.exists(_carbonite)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _is_carbonite=%s' % (_is_carbonite)
	    
	_workfile = __args__.get_var('workfile',Args._str_,'C:\Program Files (x86)\@utils\svnHotBackups\commands.cmd')
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _workfile=%s' % (_workfile)
	    
	wfHandle = open(_workfile,'w')
	print >>wfHandle, '@echo on\n'
	
	__output__ = None
	__stdout = sys.stdout
	__stderr = sys.stderr
	print >>_stdout, 'DEBUG.1: _output_path=%s' % (_output_path)
	if (_output_path is None):
	    _output_path = os.path.abspath('logs')
	    
	toks = [t for t in os.path.splitext(_output_path) if (len(t) > 0)]
	if (len(toks) ==1):
	    toks.append('.txt')

	__progName = os.path.splitext(_progName)[0]
	_toks = toks[0].replace(os.sep,'/').replace('//','/').split('/')
	if (_toks[-1].find(__progName) == -1):
	    _toks.append(__progName+'-'+_utils.timeStampForFileName())
	toks[0] = '/'.join(_toks)
	    
	_output_path = ''.join(toks)

	_utils._makeDirs(os.path.dirname(_output_path))
	    
	print >>_stdout, 'DEBUG.1a: _output_path=%s' % (_output_path)

	__output__ = open(_output_path,mode='w')

	if (not _isDebug):
	    print >>sys.stdout, oBuf.getvalue()
	    
	if (not _utils.isBeingDebugged):
	    sys.stdout = sys.stderr = __output__
	    
	# how do we know we are doing a restore and not a backup ???

	#### DEBUGGING PURPOSES ONLY ####################################################################
	print >>sys.stdout, 'DEBUG: _isVerbose=%s, _isTest=%s' % (_isVerbose,_isTest)
	if (_isVerbose) and (False):
	    print >>sys.stdout, 'BEGIN:'
	    from vyperlogix.aws.s3 import S3Shell
	    from vyperlogix.classes.SmartObject import SmartFuzzyObject
	    keyNamePrefix = 'testing'
	    bucketName = '%s/%s'%(__s3_bucketName__,keyNamePrefix)
	    keyname = 'programming-test-php-08-23-2012.zip'
	    _should_see_in_files_list_ = ['testing/To-Do.txt']
	    def __callback1__(s3):
		print >>sys.stdout, 'BEGIN :: __callback1__ (LIST)'
		_num_seen_ = 0
		for f in s3.files:
		    _f_ = SmartFuzzyObject(f)
		    print _f_.prettyPrint()
		    for fname in _should_see_in_files_list_:
			if (_f_.name.find(fname) > -1):
			    _num_seen_ += 1
		_is_problem1_ = (len(_should_see_in_files_list_) != len(s3.files))
		_is_problem2_ = (_num_seen_ != len(_should_see_in_files_list_))
		_is_problem3_ = (len(s3.files) != _num_seen_)
		_is_problem_ = (_is_problem1_) or (_is_problem2_) or (_is_problem3_)
		assert not _is_problem_, 'WARNING :: Your logic seems to be in error here...'
		print >>sys.stdout, 'END :: __callback1__ (LIST)'
	    def __callback2__(s3,lines=None):
		global _should_see_in_files_list_
		print >>sys.stdout, 'BEGIN :: __callback2__ (PUT)'
		print >>sys.stdout, '_should_see_in_files_list_ --> %s' % (_should_see_in_files_list_)
		if (misc.isList(lines)):
		    misc.append(_should_see_in_files_list_,lines)
		    _should_see_in_files_list_ = list(set(_should_see_in_files_list_))
		    print '_should_see_in_files_list_ --> %s' % (_should_see_in_files_list_)
		print >>sys.stdout, 'END :: __callback2__ (PUT)'
	    def __callback3__(s3,lines=None,items=None):
		global _should_see_in_files_list_
		print >>sys.stdout, 'BEGIN :: __callback3__ (DELETE)'
		print >>sys.stdout, '_should_see_in_files_list_ --> %s' % (_should_see_in_files_list_)
		if (misc.isList(lines)):
		    _should_see_in_files_list_ = list(set(_should_see_in_files_list_) - set(lines))
		    print >>sys.stdout, '_should_see_in_files_list_ --> %s' % (_should_see_in_files_list_)
		print >>sys.stdout, 'END :: __callback3__ (DELETE)'
	    def __onExit1__(s3):
		print >>sys.stdout, 'BEGIN :: __onExit1__'
		def __onExit2__(s3):
		    print >>sys.stdout, 'BEGIN :: __onExit2__ after (PUT)'
		    def __onExit3__(s3):
			print >>sys.stdout, 'BEGIN :: __onExit3__ (DELETE)'
			def __onExit4__(s3):
			    print >>sys.stdout, 'BEGIN :: __onExit4__'
			    print >>sys.stdout, 'END :: __onExit4__'
			s3 = S3Shell(bucketName,_aws_access_key,_aws_secret_access_key,callback=__callback1__,onExit=__onExit4__,sysout=sys.stdout)
			s3.list()
			print >>sys.stdout, 'END :: __onExit3__(DELETE)'
		    def __onExit5__(s3):
			print >>sys.stdout, 'BEGIN :: __onExit5__'
			def __onExit6__(s3):
			    print >>sys.stdout, 'BEGIN :: __onExit6__'
			    def __onExit7__(s3):
				print >>sys.stdout, 'BEGIN :: __onExit7__'
				print >>sys.stdout, 'END :: __onExit7__'
			    s3 = S3Shell(bucketName,_aws_access_key,_aws_secret_access_key,callback=__callback1__,onExit=__onExit7__,sysout=sys.stdout)
			    s3.list()
			    print >>sys.stdout, 'END :: __onExit6__'
			s3 = S3Shell(bucketName,_aws_access_key,_aws_secret_access_key,callback=__callback3__,onExit=__onExit6__,sysout=sys.stdout)
			s3.delete(__s3_bucketName__,'%s/%s'%(keyNamePrefix,keyname),callback=__callback3__)
			print >>sys.stdout, 'END :: __onExit5__'
		    s3 = S3Shell(bucketName,_aws_access_key,_aws_secret_access_key,callback=__callback1__,onExit=__onExit5__,sysout=sys.stdout)
		    s3.list()
		    print >>sys.stdout, 'END :: __onExit2__ after (PUT)'
		s3 = S3Shell(bucketName,_aws_access_key,_aws_secret_access_key,callback=__callback2__,onExit=__onExit2__,sysout=sys.stdout)
		s3.put(bucketName,"J:\@8\%s" % (keyname))
		print >>sys.stdout, 'END :: __onExit1__'
	    s3 = S3Shell(bucketName,_aws_access_key,_aws_secret_access_key,callback=__callback1__,onExit=__onExit1__,sysout=sys.stdout)
	    s3.list()
	    print >>sys.stdout, 'END !!!'
	#### DEBUGGING PURPOSES ONLY ####################################################################

	_carbonite_hours = __args__.get_var('carbonite-hours',Args._int_,int(os.environ.get("CARBONITE_HOURS", 12)))
	if (_isVerbose):
	    print >>sys.stdout, 'DEBUG: _carbonite_hours=%s' % (_carbonite_hours)
	_carbonite_files = __args__.get_var('carbonite-files',Args._int_,int(os.environ.get("CARBONITE_FILES", 60)))
	if (_isVerbose):
	    print >>sys.stdout, 'DEBUG: _carbonite_files=%s' % (_carbonite_files)

	_carbonite_optimize = __args__.get_var('carbonite-optimize',Args._bool_true_,True,is_filter=True)
	if (_isVerbose):
	    print >>sys.stdout, 'DEBUG: _carbonite_optimize=%s' % (_carbonite_optimize)
	
	__carbonite_schedule = __args__.get_var('carbonite-schedule',Args._dict_,HashedFuzzyLists({ }))
	if (_isVerbose):
	    print >>sys.stdout, 'DEBUG: __carbonite_schedule=%s' % (__carbonite_schedule)

	ioTimeAnalysis.initIOTime(__name__)
	ioTimeAnalysis.ioBeginTime(__name__)
	
	try: # ?type1=Primary&days1=M-F&hours1=0-20&type2=Alt&days2=Sa-Su&hours2=*
	    from vyperlogix import sets
	    def choose_schedule_days_options(_dict_):
		try:
		    specs = dict([(k,_utils.days_range(misc._unpack_(v)['days'])) for k,v in _dict_.iteritems() if (misc._unpack_(v)['days'])])
		except:
		    specs = dict()
		__specs__ = {}
		_specs_ = specs.values()
		for k,v in specs.iteritems():
		    specs[k] = [v,list(sets.diff(_specs_,v))]
		if (len(specs) == 2):
		    _keys = misc.sortCopy(specs.keys())
		    _a_ = dict({_keys[0]:_keys[-1],_keys[-1]:_keys[0]})
		    for k,v in specs.iteritems():
			for n in v[-1]:
			    __specs__['%d'%(n)] = _a_[k]
		return HashedFuzzyLists2(__specs__)
	    def proper_backup_type(d):
		_type_ = d['type'] if (d.has_key('type')) else None
		_l_ = ListWrapper([i.name for i in BackupTypes._items_])
		try:
		    _i_ = _l_.findFirstContaining(_type_.name)
		except:
		    _i_ = _l_.findFirstContaining(_type_)
		return BackupTypes._items_[_i_] if (_i_ > -1) else None
	    def map_schedule_days(days,_sched_):
		for k,v in days.iteritems():
		    d = misc._unpack_(_sched_[v]).asDict()
		    dR = _utils.days_range(d['days']) if (d.has_key('days')) else []
		    hR = ListWrapper(_utils.hours_range(d['hours']) if (d.has_key('hours')) else [])
		    t = proper_backup_type(d)
		    del days[k]
		    days[k] = {'days':dR,'hours':hR,'type':t}
		_d_ = HashedFuzzyLists()
		for k,v in days.iteritems():
		    d = v
		    dR = d['days'] if (d.has_key('days')) else []
		    hR = ListWrapper(d['hours'] if (d.has_key('hours')) else [])
		    t = proper_backup_type(d)
		    for dd in dR:
			for hh in xrange(0,24):
			    _f_ = hR.findFirstMatching(hh)
			    kk = '%d.%d'%(dd,hh)
			    if (_d_.has_key(kk)):
				del _d_[kk]
			    if (_f_ > -1):
				_d_[kk] = t
			    else:
				_d_[kk] = other_backup_type(t)
			pass
		    pass
		return _d_
	    _d_ = choose_schedule_days_options(__carbonite_schedule)
	    _map_ = map_schedule_days(_d_,HashedFuzzyLists(__carbonite_schedule.asDict()))
	    _day_ = _utils.day_of_week()
	    _s_ = _d_['%d'%(_day_.value)]
	    if (misc.isDict(_s_)):
		_s_['_day_'] = _day_
		__carbonite_schedule = _s_
	except Exception, ex:
	    info_string = _utils.formattedException(details=ex)
	    print >>sys.stderr, info_string
	    __carbonite_schedule = None
	_carbonite_schedule = __carbonite_schedule
	if (_isVerbose):
	    print >>sys.stdout, 'DEBUG: _carbonite_schedule=%s' % (_carbonite_schedule)
	
	_username = __args__.get_var('username',Args._str_,'')
	if (_isVerbose):
	    print >>sys.stdout, 'DEBUG: _username=%s' % (_username)
	_password = __args__.get_var('password',Args._str_,'')
	if (_isVerbose):
	    print >>sys.stdout, 'DEBUG: _password=%s' % (_password)
	
	svnlook = ''
	
	_program_name = _utils.getProgramName()
	if (_isVerbose):
	    print >>sys.stdout, 'DEBUG: _program_name=%s' % (_program_name)
	
	_data_path = _utils.appDataFolder(os.sep.join([__url__,_program_name]))
	_utils._makeDirs(_data_path)
	_dbx_name = oodb.dbx_name('%s_settings.dbx' % (_program_name),_data_path)
	print >>sys.stdout, '(DEBUG) _dbx_name=%s' % (_dbx_name)
	dbx = oodb.PickledFastCompressedHash2(_dbx_name,has_bsddb=oodb.__has_bsddb)
	    
	__7z__ = ''
	try:
	    if (dbx.has_key('svnlook')):
		_svnlook = dbx['svnlook']
		svnlook = '' if (not os.path.exists(_svnlook)) else _svnlook
	    if (_isUse7zip) and (dbx.has_key('7z')):
		sevenZ = dbx['7z']
		__7z__ = '' if (not misc.isStringValid(sevenZ)) or (not os.path.exists(sevenZ)) else sevenZ
	finally:
	    dbx.close()
		
	if (_isVerbose):
	    print >>sys.stdout, 'DEBUG: _isSkip=%s' % (_isSkip)

	if (not os.path.exists(svnlook)):
	    print >>sys.stdout, 'Searching for svnlook.'
	    svnlook = _utils.findUsingPath(r"@SVN_BINDIR@/svnlook")
	    
	if (misc.isStringValid(svnlook)) and (os.path.exists(svnlook)):
	    print >>sys.stdout, 'Found svnlook at "%s".' % (svnlook)
	    root = os.path.dirname(svnlook)
	    svnadmin_fname = os.sep.join([root,'svnadmin.exe'])
	    if (os.path.exists(svnadmin_fname)):
		svnadmin = svnadmin_fname
	    else:
		print >>sys.stdout, 'Searching for svnadmin.'
		svnadmin = _utils.findUsingPath(r"@SVN_BINDIR@/svnadmin") # Path to svnadmin utility
		if (misc.isStringValid(svnlook)) and (os.path.exists(svnlook)):
		    print >>sys.stdout, 'Found svnadmin at "%s".' % (svnadmin)
		else:
		    print >>sys.stdout, 'Could not find svnadmin at "%s", cannot proceed. Install SVN Admin functions and try again.' % (svnadmin)
		    sys.exit()
	else:
	    print >>sys.stdout, 'Could not find svnlook at "%s", cannot proceed. Install SVN Admin functions and try again.' % (svnlook)
	    sys.exit()
		
	########################################################
	__7z__ = ''
	if (_isUse7zip) or (1):
	    if (_isVerbose):
		print >>sys.stdout, 'DEBUG: __7z__=%s, misc.isStringValid("%s")=%s, os.path.exists("%s")=%s' % (__7z__,__7z__,misc.isStringValid(__7z__),__7z__,os.path.exists(__7z__))
	    if (not misc.isStringValid(__7z__)) or (not os.path.exists(__7z__)):
		print >>sys.stdout, 'Searching for 7z.exe'
		__7z__ = _utils.findUsingPath(r"@PATH@/7z.exe")
	    
	    if (_isVerbose):
		print >>sys.stdout, 'DEBUG: __7z__=%s, misc.isStringValid("%s")=%s, os.path.exists("%s")=%s' % (__7z__,__7z__,misc.isStringValid(__7z__),__7z__,os.path.exists(__7z__))
	    if (misc.isStringValid(__7z__)) and (os.path.exists(__7z__)):
		print >>sys.stdout, 'Found 7z.exe at "%s".' % (__7z__)
	    else:
		print >>sys.stdout, 'Could not find 7z.exe at "%s", cannot proceed. Install 7Zip and try again or live with the default encryption in ZipFile' % (__7z__)
	########################################################
    
	dbx = oodb.PickledFastCompressedHash2(_dbx_name,has_bsddb=oodb.__has_bsddb)
	try:
	    if (dbx.has_key('svnlook')):
		del dbx['svnlook']
	    dbx['svnlook'] = svnlook
	    if (dbx.has_key('7z')):
		del dbx['7z']
	    dbx['7z'] = __7z__
	finally:
	    dbx.close()
		
	################################################################################################### +++
	if (os.path.exists(_restore_path)) and (misc.isStringValid(_repo_path)):
	    restore_secured_backup(_restore_path,_repo_path,_passPhrase,isVerbose=_isVerbose)
	    if (isVerbose):
		print >>sys.stdout, "DEBUG: That's all folks..."
	    sys.exit()
	###################################################################################################
	    
	archive_type = _archive_type
	
	# Path to repository
	if (not os.path.exists(_repo_path)):
	    print >>sys.stdout, 'Your --repo-path of "%s" does not exist.' % (_repo_path)
	    if (_isVerbose):
		print >>sys.stdout, 'DEBUG: Cannot continue...'
	    sys.exit()
	repo_dir = _repo_path.replace(os.sep,'/')
	repo = os.path.basename(os.path.abspath(repo_dir))
	
	# Added to the filename regexp, set when using --archive-type.
	ext_re = ""
	
	# Do we want to create an archive of the backup
	if archive_type:
	    # Additionally find files with the archive extension.
	    ext_re = "(" + re.escape(archive_type) + ")?"
	else:
	    print >>sys.stdout, "Unknown archive type '%s'.\n\n" % archive_type
	    ppArgs()
	    sys.exit(2)
	    
	print >>sys.stdout, 'DEBUG:  _restore_path=%s' % (_restore_path)
	print >>sys.stdout, 'DEBUG:  _repo_path=%s' % (_repo_path)
	print >>sys.stdout, 'DEBUG:  _backup_dir=%s' % (_backup_dir)
	if (1):
	    _isUsingSFTP = False
	    backup_dir = _backup_dir
	    if (not _isSkip):
		print >>sys.stdout, "Beginning hot backup of '"+ repo_dir + "'."
		
		### Step 1: get the youngest revision.
		
		try:
		    youngest = get_youngest_revision()
		except Exception, e:
		    print >>sys.stderr, str(e)
		    sys.exit(1)
		
		print >>sys.stdout, "Youngest revision is", youngest
		
		### Step 2: Find next available backup path
		
		youngest_repo = repo + "-" + youngest
		
		# Where to store the repository backup.  The backup will be placed in
		# a *subdirectory* of this location, named after the youngest
		# revision.
		print >>sys.stdout, "DEBUG.1: _backup_dir is '%s' and it %s." % (_backup_dir,'exists' if (os.path.exists(_backup_dir)) else 'does NOT exist')
		if (os.path.exists(_backup_dir)):
		    backup_dir = _backup_dir
		else:
		    _utils._makeDirs(_backup_dir)
		    print >>sys.stdout, "DEBUG.2: _backup_dir is '%s' and it %s." % (_backup_dir,'exists' if (os.path.exists(_backup_dir)) else 'does NOT exist')
		    if (os.path.exists(_backup_dir)):
			backup_dir = _backup_dir
		    else:
			backup_dir = os.sep.join([_data_path,youngest_repo])
			_utils._makeDirs(backup_dir)
		print >>sys.stdout, "DEBUG.3: _isUsingSFTP is '%s'." % (_isUsingSFTP)
		
		backup_subdir = normalize(os.path.join(backup_dir, youngest_repo))
		
		# If there is already a backup of this revision, then append the
		# next highest increment to the path. We still need to do a backup
		# because the repository might have changed despite no new revision
		# having been created. We find the highest increment and add one
		# rather than start from 1 and increment because the starting
		# increments may have already been removed due to num_backups.
		
		regexp = re.compile("^" + repo + "-" + youngest + "(-(?P<increment>[0-9]+))?" + ext_re + "$")
		directory_list = [f for f in os.listdir(backup_dir) if (not f.endswith('.zip'))]
		young_list = filter(lambda x: regexp.search(x), directory_list)
		if young_list:
		    young_list.sort(comparator)
		    increment = regexp.search(young_list.pop()).groupdict()['increment']
		    if increment:
			backup_subdir = os.path.join(backup_dir, repo + "-" + youngest + "-" + str(int(increment) + 1))
		    else:
			backup_subdir = os.path.join(backup_dir, repo + "-" + youngest + "-1")
		    for item in young_list:
			f = os.path.join(backup_dir, item)
			if (os.path.exists(f)):
			    try:
				os.remove(f)
			    except:
				pass
		
		### Step 3: Ask subversion to make a hot copy of a repository.
		###         copied last.
		
		def perform_disk_space_check_and_cleanup(target_path):
		    _result = True
		    print >>sys.stdout, 'DEBUG: BEGIN: perform_disk_space_check_and_cleanup() in target_path="%s".' % (target_path)
		    if (os.path.exists(target_path)) and (os.path.isdir(target_path)):
			tp = os.path.dirname(target_path)
			tf = os.path.splitext(target_path.replace(tp,''))[0]+'.'
			print >>sys.stdout, 'DEBUG: tp="%s", tf="%s".' % (tp,tf)
			try:
			    _files_ = [f for f in [os.path.join(tp,n) for n in os.listdir(tp)] if (os.path.isfile(f))]
			    _files_.sort(date_comparator)
			    
			    if (len(_files_) > 1):
				print >>sys.stdout, 'BEGIN:'
				for n in _files_:
				    print >>sys.stdout, '%s' % (n)
				    if (n.find(tf) > -1):
					print >>sys.stdout, 'FOUND - NO NEED TO BACKUP THIS TIME !!!'
					_result = False # no need to backup because the file seems to exist...
					break
				    print >>sys.stdout, '%s (%s)' % (n,_result)
				print >>sys.stdout, 'END!!!'
			    else:
				print >>sys.stdout, 'DOING THE BACKUP DUE TO A LACK OF FILES !!!'
			except Exception, ex:
			    print >>sys.stdout, _utils.formattedException(details=ex)
		    print >>sys.stdout, 'DEBUG: END! perform_disk_space_check_and_cleanup() --> (%s) in "%s".' % (_result,target_path)
		    return _result
		
		archive_path = '' # initialize in case the backup doesn't run... otherwise exception happens.
		
		#if (_isDebug):
		    #print >> sys.stderr, 'DEBUG: Exiting now...'
		    #sys.exit(status=101)
			
		_process_the_backup = not _isDebug
		print >>sys.stdout, "1. _process_the_backup=%s" % (_process_the_backup)
		print >>sys.stdout, 'backup_subdir is "%s".' % (backup_subdir)
		if (not _isNocleanup):
		    _process_the_backup = perform_disk_space_check_and_cleanup(backup_subdir)
		    print >>sys.stdout, "2. _process_the_backup=%s" % (_process_the_backup)
		if (_process_the_backup):
		    #################################################################################
		    print >>sys.stdout, "Verify repository in '" + repo_dir + "'..."
		    if have_subprocess:
			p = subprocess.Popen([svnadmin, "verify", repo_dir])
			print >>sys.stdout, 'subprocess is %s or "%s".' % (p.pid,str(p))
			__pid__ = p.pid
			try:
			    p.wait()
			    err_code = p.returncode
			except KeyboardInterrupt, SystemExit:
			    if (_isDebug):
				from vyperlogix.process import killProcByPID
				killProcByPID(p.pid)
				raise
			finally:
			    __pid__ = None
		    else:
			err_code = -1
			print >>sys.stdout, 'ERROR.1: Which version of the runtime are you using anyway ?!?'
		    #################################################################################
		    if err_code != 0:
			print >>sys.stdout, "Unable to backup the repository."
			sys.exit(err_code)
		    else:
			print >>sys.stdout, "Backing up repository to '" + backup_subdir + "'..."
			print >>wfHandle, '%s\n' % (' '.join(['"%s"'%(svnadmin), "hotcopy", '"%s"'%(repo_dir), '"%s"'%(backup_subdir), "--clean-logs"]))

		    def perform_cleanup(target_path):
			fpath = target_path
			print >>sys.stdout, 'DEBUG: BEGIN: perform_cleanup() in "%s" --> "%s".' % (target_path,fpath)
			if (os.path.exists(fpath)) and (os.path.isdir(fpath)):
			    _cmd_ = 'rmdir /S /Q "%s"' % (fpath)
			    print >>wfHandle, '%s\n' % (_cmd_)

			    _cmd_ = 'del d:/temp/repo*.tmp'
			    print >>wfHandle, '%s\n' % (_cmd_)

			print >>sys.stdout, 'DEBUG: END! perform_cleanup() in "%s".' % (target_path)
		    
		    _utils.makeDirs(backup_subdir)
		    ### Step 4: Make an archive of the backup if required.
		    if archive_type and (len(archive_type) > 0):
			archive_path = backup_subdir + ('.' if (archive_type.find('.') == -1) else '') + archive_type
			err_msg = ""
		
			print >>sys.stdout, "Archiving backup to '%s' (%s)..." % (archive_path,archive_type)
			print >>sys.stdout, "(???) ArchiveTypes.gz=(%s), ArchiveTypes.bz2=(%s)..." % (ArchiveTypes.gz,ArchiveTypes.bz2)
			if (archive_type == ArchiveTypes.gz) or (archive_type == ArchiveTypes.bz2):
			    try:
				import tarfile
				print >>sys.stdout, "tarfile.open('%s', 'w:%s')" % (archive_path,archive_type)
				tar = tarfile.open(archive_path, 'w:' + archive_type)
				try:
				    print >>sys.stdout, "tar.add('%s', '%s')" % (backup_subdir,os.path.basename(backup_subdir))
				    tar.add(backup_subdir, os.path.basename(backup_subdir))
				finally:
				    print >>sys.stdout, "tar.close()"
				    tar.close()
			    except ImportError, e:
				err_msg = "Import failed: " + str(e)
				err_code = -2
			    except tarfile.TarError, e:
				err_msg = "Tar failed: " + str(e)
				err_code = -3
			    finally:
				print >>sys.stdout, "(1) DEBUG: About to perform_cleanup() in '%s' using _isNocleanup=(%s)." % (backup_subdir,_isNocleanup)
				if (not _isNocleanup):
				    perform_cleanup(backup_subdir)
		
			elif (archive_type):
			    try:
				if (os.path.exists(__7z__)):
				    archive_path = backup_subdir + '.7z'

				    __zip_target__ = archive_path.replace(backup_dir,_carbonite).replace('/','\\')
				    _cmd_ = ['"%s"'%(__7z__), "a", "-t7z", "-mx9", "-wd:\\temp", "-p%s"%(_passPhrase), '"%s"'%(__zip_target__), '"%s"'%(backup_subdir.replace('/','\\'))]
				    cmd_str = ' '.join(_cmd_)
				    print >>wfHandle, '%s\n' % (cmd_str)
				    
				    if (__zip_target__.find(_carbonite_alt) == -1):
					_cmd_ = 'xcopy "%s" "%s" /v /y' % (__zip_target__, _carbonite_alt)
					print >>wfHandle, '%s\n' % (_cmd_)
					
				    __re__ = re.compile(r"(?P<repo>repo[0-9]+)\W(?P<revision>[0-9]+)\W7z\Wtmp", re.MULTILINE)
				    __files__ = ['/'.join(['d:/temp',f]) for f in os.listdir('d:/temp/') if (__re__.match(f))]
				    for f in __files__:
					_cmd_ = 'del "%s"' % (f.replace('/',os.sep))
					print >>wfHandle, '%s\n' % (_cmd_)

				    _cmd_ = 'rmdir /S /Q "%s"' % (backup_subdir)
				    print >>wfHandle, '%s\n' % (_cmd_)

				    _cmd_ = 'C:\\'
				    print >>wfHandle, '%s\n' % (_cmd_)
				    
				    _cmd_ = 'cd "C:\\Program Files (x86)\\@utils\\svnHotBackups"'
				    print >>wfHandle, '%s\n' % (_cmd_)
				    
				    _cmd_ = 'START "remove-oldest" /SEPARATE /HIGH "remove-oldest.cmd" END'
				    print >>wfHandle, '%s\n' % (_cmd_)
				else:
				    from vyperlogix.zip import secure
				    print >>sys.stdout, "(???) ArchiveTypes.zip=(%s), ArchiveTypes.ezip=(%s), ArchiveTypes.xzip=(%s), ArchiveTypes.bzip=(%s)..." % (ArchiveTypes.zip,ArchiveTypes.ezip,ArchiveTypes.xzip,ArchiveTypes.bzip)
				    if (archive_type == ArchiveTypes.zip):
					secure.zipper(backup_subdir,archive_path,archive_type=secure.ZipType.zip,passPhrase=_passPhrase,sevenZ=__7z__ if (_isUse7zip) else '',fOut=sys.stdout)
				    elif (archive_type == ArchiveTypes.ezip):
					secure.zipper(backup_subdir,archive_path,archive_type=secure.ZipType.ezip,_iv=_iv,passPhrase=_passPhrase,sevenZ=__7z__ if (_isUse7zip) else '',fOut=sys.stdout)
				    elif (archive_type == ArchiveTypes.xzip):
					secure.zipper(backup_subdir,archive_path,archive_type=secure.ZipType.xzip,passPhrase=_passPhrase,sevenZ=__7z__ if (_isUse7zip) else '',fOut=sys.stdout)
				    elif (archive_type == ArchiveTypes.bzip):
					secure.zipper(backup_subdir,archive_path,archive_type=secure.ZipType.bzip,passPhrase=_passPhrase,sevenZ=__7z__ if (_isUse7zip) else '',fOut=sys.stdout)
				    elif (archive_type == ArchiveTypes.z7):
					secure.zipper(backup_subdir,archive_path,archive_type=secure.ZipType.z7,passPhrase=_passPhrase,sevenZ=__7z__ if (_isUse7zip) else '',fOut=sys.stdout)
			    except ImportError, e:
				err_msg = "Import failed: " + str(e)
				err_code = -4
			    except Exception, e:
				err_msg = "General Failure: " + _utils.formattedException(details=e)
				err_code = -5
			    finally:
				print >>sys.stdout, "(2) DEBUG: About to perform_cleanup() using _isNocleanup=(%s)." % (_isNocleanup)
				if (not _isNocleanup):
				    perform_cleanup(backup_subdir)
		
			if err_code != 0:
			    print >>sys.stdout, "Unable to create an archive for the backup.\n" + err_msg
			    sys.exit(err_code)
	    
	    ### Step 5: finally, remove all repository backups other than the last
	    ###         NUM_BACKUPS.
		
	    _isNotUsingSFTP = False
	    print >>sys.stdout, 'DEBUG: num_backups is "%s"' % (num_backups)
	    if num_backups > 0:
		def __cleanup_space__(fpath):
		    regexp = re.compile(r"(?P<reponame>.*)-(?P<revision>[0-9]+(-[0-9]+)?)\.(?P<ftype>.*)")
		    directory_list = os.listdir(fpath)
    
		    old_list = filter(lambda x: regexp.search(x), directory_list)
		    old_list.sort(comparator)
		    _n_ = max(0,len(old_list)-num_backups)
		    print >>sys.stdout, 'DEBUG: There are %d backups in "%s" with %d expected at-most.' % (_n_,fpath,num_backups)
		    if (_n_ > 0):
			print >>sys.stdout, 'DEBUG: Ignoring these "%s".' % (old_list[_n_:])
			del old_list[_n_:]
			print >>sys.stdout, 'DEBUG: There are now %d in the list to delete.' % (len(old_list))
			for item in old_list:
			    old_backup_item = os.path.join(fpath, item)
			    print >>sys.stdout, "Removing old backup %s" % (old_backup_item)

			    _cmd_ = 'del "%s"' % (old_backup_item)
			    print >>wfHandle, '%s\n' % (_cmd_)
			    
		__cleanup_space__(backup_dir)
		s_begin = time.time()
		sleep_interval = 5
		while (1):
		    try:
			__cleanup_space__(_carbonite)
			break
		    except WindowsError, details:
			if (_isServicerecovery):
			    try:
				from vyperlogix.services import _win32service
				service = ['tntdrive'][0]
				print 'Checking for %s' % (service)
				__service__ = _win32service.get_service_containing(service)
				__has__ = __service__ is not None
				print '%s %s%s' % ('Has' if (__has__) else 'Does not have',service,' (%s)'%(__service__.State if (__has__) else ''))
				if (not __has__):
				    print >> sys.stderr, 'ERROR: Cannot recover from the tnt drive service problem, because there is no driver...'
				    break
				print '%s is %s' % (__service__.Name,__service__.State)
				if (str(__service__.State).lower().find('running') > -1):
				    print '%s is Stopping' % (__service__.Name)
				    __service__.StopService()
				    print 'Sleeping...'
				    time.sleep(sleep_interval)
				print '%s is Starting' % (__service__.Name)
				__service__.StartService()
				print 'Sleeping...'
				time.sleep(sleep_interval)
				s_elapsed = time.time() - s_begin
				print 's_elapsed=%s' % (s_elapsed)
				if (s_elapsed > 60):
				    print >> sys.stderr, 'ERROR: Cannot recover from the tnt drive service problem, because the %s service cannot be controlled...' % (service)
				    break
				sleep_interval += 5
			    except ImportError:
				print >> sys.stderr, 'ERROR: Cannot recover from the tnt drive service problem, because the _win32service module cannot be imported...'
				break
			else:
			    print >> sys.stderr, 'EXCEPTION: %s' % (_utils.formattedException(details=details))
		
	    def cleanUpCarbination(fpath):
		_date_comparator = fname_comparator
		print >>sys.stdout, 'DEBUG:  _is_carbonite is "%s"' % (_is_carbonite)
		if (_is_carbonite):
		    files = [os.sep.join([fpath,f]) for f in os.listdir(fpath)]
		files.sort(_date_comparator)
		print >>sys.stdout, 'BEGIN:'
		for f in files:
		    print >>sys.stdout, '%s' % (f)
		print >>sys.stdout, 'END!!!'
		dt = time.time()
		_files = []
		_fprefix = _repo_path.split(os.sep)[-1]
		for f in files:
		    _bool_ = f.find(_fprefix) > -1
		    print >>sys.stdout, 'cleanUpCarbination->DEBUG.1: %s :: "%s".startswith("%s")=%s' % (misc.funcName(),f,_fprefix,_bool_)
		    if (_bool_):
			print >>sys.stdout, 'cleanUpCarbination->DEBUG.2:  _is_carbonite is "%s"' % (_is_carbonite)
			if (_is_carbonite):
			    statinfo = os.stat(f)
			    t = statinfo.st_mtime
			secs = dt - t
			hours = secs / 3600
			print >>sys.stdout, 'cleanUpCarbination->DEBUG.3: %s.1 f=%s' % (misc.funcName(),f)
			print >>sys.stdout, 'cleanUpCarbination->DEBUG.4: %s.2 secs=%s, hours=%s' % (misc.funcName(),secs,hours)
			_files.append(SmartObject.SmartFuzzyObject({'hours':hours,'secs':secs,'t':t,'fname':f}))
		print >>sys.stdout, 'cleanUpCarbination->DEBUG.5: %s.3 fpath=%s, len(_files)=%s' % (misc.funcName(),fpath,len(_files))
		if (len(_files) > _carbonite_files):
		    edge = -1 if (_files[-1].hours < _files[0].hours) else 0
		    print >>sys.stdout, 'cleanUpCarbination->DEBUG.6:  %s.4 edge=%s because last is %s and first is %s.' % (misc.funcName(),edge,_files[-1].hours,_files[0].hours)
		    if (edge == -1):
			print >>sys.stdout, '%s.5 reversed !' % (misc.funcName())
			misc.reverse(_files)
		    if (edge != -1):
			_beginning_ = _carbonite_files
			_ending_ = len(_files)
		    else:
			_beginning_ = 0
			_ending_ = len(_files) - _carbonite_files
		    print >>sys.stdout, 'cleanUpCarbination->DEBUG.6a: _beginning_=%s, _ending_=%s, len(_files)=%s' % (_beginning_,_ending_,len(_files))
		    print >>sys.stdout, 'BEGIN:'
		    for f in _files:
			print >>sys.stdout, '%s' % (f)
		    print >>sys.stdout, 'END!!!'
		    for f in _files[_beginning_:_ending_]:
			print >>sys.stdout, 'cleanUpCarbination->DEBUG.7: %s.6 unlink(%s)' % (misc.funcName(),f.fname)
			print >>sys.stdout, 'cleanUpCarbination->DEBUG.8: _is_carbonite _is_carbonite is "%s"' % (_is_carbonite)
			print >>sys.stdout, 'cleanUpCarbination->DEBUG.9: _is_carbonite is "%s"' % (_is_carbonite)
			if (_is_carbonite):
			    print >>sys.stdout, 'cleanUpCarbination->DEBUG.10: os.unlink("%s")' % (f.fname)
			    _cmd_ = 'del "%s"' % (f.fname)
			    print >>wfHandle, '%s' % (_cmd_)
	    
	    print >>sys.stdout, 'DEBUG: _carbonite=%s, archive_path=%s' % (_carbonite,archive_path)
	    print >>sys.stdout, 'DEBUG: _is_carbonite is "%s", os.path.exists("%s") is "%s"' % (_is_carbonite,archive_path,os.path.exists(archive_path))
	    if (_is_carbonite) and (os.path.exists(archive_path)):
		_date_comparator = fname_comparator
		if (_is_carbonite):
		    directory_list = [os.sep.join([_carbonite,f]) for f in os.listdir(_carbonite) if (str(f).find(repo) > -1)]
		directory_list.sort(_date_comparator)
		is_time_to_carbonite = True
		print >>sys.stdout, 'DEBUG: len(directory_list)=%s' % (len(directory_list))
		_directory_list = []
		dt = time.time()
		print >>sys.stdout, 'DEBUG:  _is_carbonite is "%s"' % (_is_carbonite)
		for f in directory_list:
		    if (_is_carbonite):
			statinfo = os.stat(f)
			t = statinfo.st_mtime
		    secs = dt - t
		    hours = secs / 3600
		    print >>sys.stdout, 'DEBUG: 2.1 f=%s' % (f)
		    print >>sys.stdout, 'DEBUG: 2.2 secs=%s, hours=%s' % (secs,hours)
		    _directory_list.append(SmartObject.SmartFuzzyObject({'hours':hours,'secs':secs,'t':t,'f':f}))
		print >>sys.stdout, 'BEGIN: (_directory_list)'
		for f in _directory_list:
		    print >>sys.stdout, '%s' % (str(f))
		print >>sys.stdout, 'END!!! (_directory_list)'
		
		print >>sys.stdout, 'DEBUG:  Calling cleanUpCarbination() !!!'
		cleanUpCarbination(_carbonite_target)

	ioTimeAnalysis.ioEndTime(__name__)
	ioTimeAnalysis.ioTimeAnalysisReport(fOut=sys.stdout)
	
	print >>wfHandle, 'echo "Done !!!"\n'
	wfHandle.flush()
	wfHandle.close()

	def __callback__(ss,data=None):
	    global __begin__
	    if (data) and (misc.isString(data)) and (len(data) > 0):
		print 'BEGIN:'
		print 'data=%s' % (data)
		print 'END !'
	    return

	def __onExit__(ss):
	    print '__onExit__'
	
	__cmd__ = '"%s"'%(_workfile)
	print >>sys.stdout, '__cmd__="%s".' % (__cmd__)

	ss = SmartShell(__cmd__,callback=__callback__,isDebugging=True,onExit=__onExit__,sysout=sys.stdout)
	ss.execute()

	if (not _utils.isBeingDebugged):
	    if (__output__):
		__output__.flush()
		__output__.close()
		
	    if (__stdout):
		sys.stdout = __stdout
    
	    if (__stderr):
		sys.stderr = __stderr

	    import os
	    from vyperlogix.process import killProcByPID
	    pid = os.getpid()
	    killProcByPID.killProcByPID(pid)

