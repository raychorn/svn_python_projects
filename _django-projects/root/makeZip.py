#!/usr/bin/env python
import zipfile
import os, sys
import re
from distutils import util

fpath = r'Z:\python projects\@lib'
try:
    i = sys.path.index(fpath)
except:
    i = -1
if (i > -1):
    print 'Removing "%s" from sys.path.' % (fpath)
    del sys.path[i]
sys.path.insert(0,fpath)

from vyperlogix.misc import _utils
try:
    from vyperlogix.lists.ListWrapper import ListWrapper
except Exception, details:
    info_string = _utils.formattedException(details=details)
    print >>sys.stderr, info_string
    print 'BEGIN:'
    for p in sys.path:
	print >>sys.stderr, p
    print 'END!'

from vyperlogix.misc import jsmin
from vyperlogix import misc
from vyperlogix.misc.ReportTheList import reportTheList
from vyperlogix.hash import lists

from vyperlogix.misc import threadpool

from vyperlogix.zip.getZipFilesAnalysis import getZipFilesAnalysis2

from vyperlogix import zip

StringIO = _utils.stringIO

_Q_ = threadpool.ThreadQueue(100)

d_sio = lists.HashedLists2()

_use_zipper = True

_root = os.path.dirname(sys.argv[0])
if (not os.path.exists(_root)):
    _root = os.path.abspath(os.curdir)

print '_root is "%s".' % (_root)

_root_ = _root

rx = re.compile('[.]svn')
rxLog = re.compile('log')
rxPop = re.compile('pop')
rxZip = re.compile('[.]zip')
rxDb = re.compile('[.]db')

skip_list = ['django-trunk','sample-site-with-templates','google_code']

django_token = '%sdjango%s' % (os.sep,os.sep)

_delayed_removes = []
_delayed_commits = {}

def addFileToZip(top,_zip,filename,useNoPath=False,fOut=sys.stdout):
    print >>fOut, 'ZIP Adding (%s) to (%s)' % (filename,_zip.filename)
    f_base = filename.replace('.pyo','.pyc').replace(top,'')
    f_base = f_base if (not useNoPath) else os.path.basename(f_base)
    if (f_base.startswith(django_token)):
	f_base = f_base.replace(django_token,os.sep)
    _zip.write(filename,f_base)

def _commitTarget(cmds):
    from vyperlogix.process import Popen

    cmds = cmds if (misc.isList(cmds)) else [cmds]
    reportTheList(cmds,'Commands')
    buf = StringIO()
    shell = Popen.Shell(cmds,isExit=True,isWait=True,isVerbose=True,fOut=buf)
    print buf.getvalue()
    print '-'*40
    print

def commitTarget(target):
    has_svn = False
    x1 = _utils.searchForFolderNamed('.svn',top=target,callback=None,options=_utils.FileFolderSearchOptions.none)
    print '%s :: (+++) x1 is "%s".' % (misc.funcName(),x1)
    if (len(x1) == 0):
	x2 = _utils.searchForFolderNamed('_svn',top=target,callback=None,options=_utils.FileFolderSearchOptions.none)
	print '%s :: (+++) x2 is "%s".' % (misc.funcName(),x2)
	if (len(x2) > 0):
	    has_svn = True
    else:
	has_svn = True
    print 'has_svn is %s' % (has_svn)
    if (has_svn):
	cmd1 = 'svn add --quiet --force .'
	cmd2 = 'svn commit --non-interactive -m "Automated Commit on %s" .' % (_utils.timeStampLocalTime())
	if (not _delayed_commits.has_key(target)):
	    print '%s :: "%s" --> cmd1 is "%s".' % (misc.funcName(),target,cmd1)
	    print '%s :: "%s" --> cmd2 is "%s".' % (misc.funcName(),target,cmd2)
	    _delayed_commits[target] = [cmd1,cmd2]
	else:
	    print '%s :: Cannot add "%s".' % (misc.funcName(),target)
    else:
	print '%s :: SVN is not present in "%s".' % (misc.funcName(),target)

@threadpool.threadify(_Q_)
def handle_folder(dname):
    _top_ = dname
    toks = dname.split(os.sep)
    dname = toks[-1]
    
    if (d_sio[dname] is None):
	d_sio[dname] = StringIO()
    
    _zipName_prefix = '%s' % (dname)
    zipName = '%s.zip' % (_zipName_prefix)
    
    zipName = os.path.join(os.sep.join(toks[0:-1]),zipName)
    if (os.path.exists(zipName)):
	os.remove(zipName)
    try:
	zp = zipfile.ZipFile( zipName, 'w', zipfile.ZIP_DEFLATED)
	d_ignore_roots = lists.HashedLists2()
	for root, dirs, files in os.walk(_top_):
	    if (rx.search(root) == None) and (not root.endswith('%slogs' % (os.sep))) and (not root.endswith('@projects')):
		if (len(dirs) > 1) and ('django' in dirs):
		    for n in [d for d in dirs if (d != 'django')]:
			d_ignore_roots[os.sep.join([root,n])] = n
		    for n in [f for f in files]:
			d_ignore_roots[os.sep.join([root,n])] = n
		if (any([root.find(k) > -1 for k in d_ignore_roots.keys()])):
		    continue
		py_files = [os.sep.join([root,f]) for f in files if (f.endswith('.py'))]
		print >>d_sio[dname], 'Compiling (%s) %s' % (root,py_files)
		util.byte_compile(py_files,optimize=2,force=1)
		compiled_file = lambda f:f.replace('.py','.pyo') if (os.path.exists(f.replace('.py','.pyo'))) else f
		py_files = [(f,compiled_file(f)) for f in py_files]
		d = dict(py_files)
		set_files = set(d.keys())
		for f,p in py_files:
		    addFileToZip(_top_,zp,p,fOut=d_sio[dname])
		s = set([f for f in files if (not f.endswith('.py')) and (not f.endswith('.pyc')) and (not f.endswith('.pyo')) and (not f.endswith('.cmd')) and (not f.endswith('.wpr')) and (f != 'Django-Commands.txt') ]) - set_files
		for f in list(s):
		    fname = os.sep.join([root,f])
		    if (d_ignore_roots[fname]):
			continue
		    addFileToZip(_top_,zp,fname,fOut=d_sio[dname])
		#print >>d_sio[dname], '(+++) _top_ is "%s".' % (_top_)
		_target = os.path.join(_top_,'django')
		commitTarget(_target if (os.path.exists(_target)) else _top_)
		print >>d_sio[dname], '%s' % ('-'*80)
	print >>d_sio[dname], '%s\n' % ('='*80)
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>d_sio[dname], 'Error in ZIP processing.\n%s' % (info_string)
    finally:
	try:
	    zp.close()
	    sz = _utils.fileSize(zp.filename)
	    if (sz == 0):
		print 'Close Empty %s' % (zp.filename)
		zp.close()
		_delayed_removes.append(zp.filename)
	    else:
		zp = zipfile.ZipFile( zipName, 'r')
		try:
		    toks = _top_.split(os.sep)
		    _deployments = os.path.join(_top_,'deployments')
		    print '_deployments is "%s".' % (_deployments)
		    if (os.path.exists(_deployments)):
			_deployment = os.path.join(_deployments,'%s_deployment' % (toks[-1]))
			print '_deployment is %s' % (_deployment)
			if (os.path.exists(_deployment)) and (_utils.containsSvnFolders(_deployment)):
			    print '%s --> %s\n' % (zp.filename,_deployment)
			    _analysis = getZipFilesAnalysis2(zp)
			    #lists.prettyPrint(_analysis,title='_analysis',fOut=sys.stdout)
			    d_files = _utils.filesAsDict(_deployment,deBias=True,asZip=True)
			    #lists.prettyPrint(d_files,title='d_files',fOut=sys.stdout)
			    _d_files = lists.HashedLists2(d_files.asDict())
			    for k in _analysis.keys():
				if (_d_files.has_key(k)):
				    del _d_files[k]
			    for k in _d_files.keys():
				fpath = os.path.join(_deployment,k.replace('/',os.sep))
				if (os.path.exists(fpath)):
				    print '(-) %s' % (fpath)
				    os.remove(fpath)
			    #lists.prettyPrint(_d_files,title='_d_files',fOut=sys.stdout)
			    print 'BEGIN: zip.unZipInto %s -> %s' % (zp.filename,_deployment)
			    zip.unZipInto(zp,_deployment,isVerbose=True)
			    print 'END!   zip.unZipInto %s -> %s\n' % (zp.filename,_deployment)
			    commitTarget(_deployment)
			else:
			    print '(+++) _deployment (%s) does not exist or does not contain .svn folders' % (_deployment)
		finally:
		    print 'Close %s' % (zp.filename)
		    zp.close()
		    _delayed_removes.append(zp.filename)
	    print d_sio[dname].getvalue()
	    del d_sio[dname]
	except Exception, details:
	    print _utils.formattedException(details=details)
	finally:
	    pass

def main():
    if (_use_zipper):
	dnames = []
	_top = _root_
	while (len(dnames) <= 1):
	    dnames = [f for f in os.listdir(_top) if (rx.search(f) == None) and (os.path.isdir(os.sep.join([_top,f]))) and (f not in skip_list) ]
	    if (len(dnames) == 1):
		_top = os.path.join(_top,dnames[0])
	for dname in dnames:
	    handle_folder(os.path.join(_top,dname))
    
	print '_Q_.join() !'
	_Q_.join()
	print '_delayed_removes :: There are %s in the list.' % (len(_delayed_removes))
	for f in _delayed_removes:
	    print 'Delayed Remove "%s".' % (f)
	    os.remove(f)
	print '='*80
	print
    
	print '_delayed_commits'
	for k,v in _delayed_commits.iteritems():
	    print 'Delayed Commit'
	    cmds = ['cd "%s"' % (k)]
	    for item in v:
		cmds.append('%s' % (item))
	    _commitTarget(cmds)
	print '='*80
	print
    
    if (False):
	try:
	    source = r'Z:\python projects\_django-media_source'
	    dest = r'Z:\python projects\_django-media'
	    for root, dirs, files in os.walk(source):
		if (rx.search(root) == None):
		    for f in files:
			_source = os.sep.join([root,f])
			_dest = os.sep.join([dest,os.sep.join(_source.replace(source,'').split(os.sep)[1:])])
			if (f.endswith('.js')):
			    _utils.makeDirs(_dest)
			    print 'Minifying %s --> %s' % (_source,_dest)
			    jsm = jsmin.JavascriptMinify()
			    fIn = open(_source,'r')
			    fOut = open(_dest,'w')
			    try:
				jsm.minify(fIn, fOut)
			    finally:
				fOut.flush()
				fOut.close()
			elif (rxDb.search(os.path.splitext(_source)[-1]) == None):
			    _utils.copyFile(_source,_dest)
	except Exception, details:
	    info_string = _utils.formattedException(details=details)
	    print 'Error in Minifying process.\n%s' % (info_string)
    else:
	print 'Not Minifying JavaScripts...'
	    
    print 'Done !'

from vyperlogix.misc import _psyco
_psyco.importPsycoIfPossible(func=main)
main()
sys.exit(0)
