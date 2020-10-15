import sys
import os
if sys.platform != "win32":
    import fcntl
    import select
import gzip
import os.path
import _psyco
import _utils
import Args
import PrettyPrint

try:
    import bz2
    have_bz2 = True
except ImportError:
    have_bz2 = False

_isVerbose = False
_source = ''
_dest = ''
_keep = 999

# Path to svnadmin utility
svnadmin = r"@SVN_BINDIR@/svnadmin"

def exec_cmd(cmd, output=None, printerr=False):
    if sys.platform == "win32":
	return exec_cmd_win32(cmd, output, printerr)
    else:
	return exec_cmd_unix(cmd, output, printerr)

def exec_cmd_unix(cmd, output=None, printerr=False):
    try:
	proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=False)
    except:
	return (256, "", "Popen failed (%s ...):\n  %s" % (cmd[0], str(sys.exc_info()[1])))
    stdout = proc.stdout
    stderr = proc.stderr
    self.set_nonblock(stdout)
    self.set_nonblock(stderr)
    readfds = [ stdout, stderr ]
    selres = select.select(readfds, [], [])
    bufout = ""
    buferr = ""
    while len(selres[0]) > 0:
	for fd in selres[0]:
	    buf = fd.read(16384)
	    if len(buf) == 0:
		readfds.remove(fd)
	    elif fd == stdout:
		if output:
		    output.write(buf)
		else:
		    bufout += buf
	    else:
		if printerr:
		    print buf,
		else:
		    buferr += buf
	if len(readfds) == 0:
	    break
	selres = select.select(readfds, [], [])
    rc = proc.wait()
    if printerr:
	print ""
    return (rc, bufout, buferr)

def exec_cmd_win32(cmd, output=None, printerr=False):
    try:
	proc = Popen(cmd, stdout=PIPE, stderr=None, shell=False)
    except:
	return (256, "", "Popen failed (%s ...):\n  %s" % (cmd[0],
		str(sys.exc_info()[1])))
    stdout = proc.stdout
    bufout = ""
    buferr = ""
    buf = stdout.read(16384)
    while len(buf) > 0:
	if output:
	    output.write(buf)
	else:
	    bufout += buf
	buf = stdout.read(16384)
    rc = proc.wait()
    return (rc, bufout, buferr)

def removeFiles(top):
    for root, dirs, files in os.walk(top, topdown=False):
	for f in files:
	    os.remove(os.sep.join([root,f]))
	for d in dirs:
	    os.rmdir(os.sep.join([root,d]))

def keepBackups(top):
    d = {}
    removeNum = -1
    for root, dirs, files in os.walk(top, topdown=True):
	if (len(dirs) > _keep):
	    removeNum = len(dirs) - _keep
	for dirName in dirs:
	    st = os.stat(dirName)
	    d[st.st_ctime] = os.sep([root,dirName])
	k = ([k for k in d.keys()][_keep+1:]).sort()
	for nK in k:
	    removeFiles(d[nK])
	break

def main():
    args = {'--help':'displays this help text.','--verbose':'output more stuff.','--source=source or repos path':'path to the repository.','--dest=dest path':'path to the backup folder.','--keep=number':'number of backups to keep.'}
    _argsObj = Args.Args(args)
    print >>sys.stderr, '_argsObj=(%s)' % str(_argsObj)

    if ( (len(sys.argv) == 1) or (sys.argv[-1] == args.keys()[0]) ):
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    try:
	_isVerbose = _argsObj.booleans['isVerbose']
    except:
	_isVerbose = False

    try:
	_source = os.path.abspath(_argsObj.arguments['source'])
    except:
	pass

    try:
	_dest = os.path.abspath(_argsObj.arguments['dest'])
    except:
	pass
    
    try:
	_keep = int(_argsObj.arguments['keep'])
    except:
	pass
    
    if (len(_source) > 0) and (os.path.exists(_source)) and (len(_dest) > 0) and (_keep >= 0):
	if (not os.path.exists(_dest)):
	    os.mkdir(_dest)
	# determine how many backups have been taken ?
	# remove any old backups we cannot keep.
	keepBackups(_dest)
	# take hotcopy ()
	tstamp = _utils.timeStamp()
	dname = os.sep.join([_dest,tstamp])
	if (not os.path.exists(dname)):
	    os.mkdir(dname)
	_cmd = 'svnadmin hotcopy %s %s' % (_source,dname)
	exec_cmd(_cmd)
	# zip up the hotcopy
	# remove the hotcopy
	# move the zip file into the folder
	pass
    elif (len(_source) <= 0) or (not os.path.exists(_source)):
	print 'ERROR :: Invalid source repository path specified, "%s" will not work.' % (_source)
    elif (len(_dest) <= 0):
	print 'ERROR :: Invalid dest backup path specified, "%s" will not work.' % (_dest)
    
if (__name__ == '__main__'):
    if (_utils.getVersionNumber() >= 251):
        _psyco.importPsycoIfPossible()
        main()
    else:
	print 'You seem to be using the wrong version of Python, try using 2.5.1 or later rather than "%s".' % sys.version.split()[0]
