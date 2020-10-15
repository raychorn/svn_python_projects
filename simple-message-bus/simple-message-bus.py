import re
import os, sys

import time

import win32file
import win32con

import logging

import tcpipbridge

_isVerbose = False # defined here to satisfy py2exe runtime issues.

__eof__ = '@@@EOF@@@'
__writer__ = None

__is_listener__ = False
listen_to_ip,listen_to_port = None,None

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

program_name = __name__ if (__name__ != '__main__') else os.path.splitext(os.path.basename(sys.argv[0]))[0]
LOG_FILENAME = './%s.log' % (program_name)
logger = logging.getLogger(program_name)
handler = logging.FileHandler(LOG_FILENAME)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler) 
print 'Logging to "%s".' % (handler.baseFilename)

ch = logging.StreamHandler()
ch_format = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(ch_format)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

logging.getLogger().setLevel(logging.DEBUG)

tcpipbridge.logger = logger


from vyperlogix.enum import Enum

from vyperlogix import misc
from vyperlogix.misc import threadpool

from vyperlogix.misc import _utils
from vyperlogix.classes.SmartObject import SmartObject

__Q_INPUT__ = threadpool.ThreadQueue(2)
__Q_OUTPUT__ = threadpool.ThreadQueue(2)

__Q1__ = threadpool.ThreadQueue(100)
__Q2__ = threadpool.ThreadQueue(100)

class Actions(Enum.Enum):
    UNKNOWN = -1
    Created = 1
    Deleted = 2
    Updated = 3
    Renamed_From = 4
    Renamed_To = 5

def __terminate__():
    import os
    from vyperlogix.process.killProcByPID import killProcByPID
    pid = os.getpid()
    killProcByPID(pid)

def report_changes(cflags):
    flags = []
    if (cflags & win32con.FILE_NOTIFY_CHANGE_FILE_NAME):
        flags.append('FILE_NOTIFY_CHANGE_FILE_NAME')
    if (cflags & win32con.FILE_NOTIFY_CHANGE_DIR_NAME):
        flags.append('FILE_NOTIFY_CHANGE_DIR_NAME')
    if (cflags & win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES):
        flags.append('FILE_NOTIFY_CHANGE_ATTRIBUTES')
    if (cflags & win32con.FILE_NOTIFY_CHANGE_SIZE):
        flags.append('FILE_NOTIFY_CHANGE_SIZE')
    if (cflags & win32con.FILE_NOTIFY_CHANGE_LAST_WRITE):
        flags.append('FILE_NOTIFY_CHANGE_LAST_WRITE')
    if (cflags & win32con.FILE_NOTIFY_CHANGE_SECURITY):
        flags.append('FILE_NOTIFY_CHANGE_SECURITY')
    print >> sys.stdout, 'INFO: %s' % ('FLAGS: %s --> %s' % (format(cflags,'b'),flags))

def date_comparator(a, b):
    a_statinfo = os.stat(a)
    b_statinfo = os.stat(b)
    print 'DEBUG: a=%s, b=%s' % (a,b)
    return -1 if (a_statinfo.st_mtime < b_statinfo.st_mtime) else 0 if (a_statinfo.st_mtime == b_statinfo.st_mtime) else 1

@threadpool.threadify(__Q_INPUT__)
def handle_changes(hDir,changes,watching,output=None,callback=None,is_running=True):
    _files_ = [f for f in [os.path.join(watching,n) for n in os.listdir(watching)] if (os.path.isfile(f))]
    _files_.sort(date_comparator)
    
    def __handle_file__(a,w,f,out=None):
	if (callable(callback)):
	    try:
		time.sleep(1) # mitigate a possible race condition - don't want to consume the file too quickly... LOL
		callback(a,w,f,output=out)
	    except Exception, ex:
		print >> sys.stderr, 'EXCEPTION: %s' % (_utils.formattedException(details=ex))
    
    for f in _files_:
	action = Actions.Created
	__handle_file__(action, watching, os.path.basename(f), out=output)

    while (is_running):
        for action,aFile in win32file.ReadDirectoryChangesW(hDir,1024,True,changes,None,None):
            action = Actions(action)
	    __handle_file__(action, watching, aFile, out=output)

@threadpool.threadify(__Q2__)
def ProcessFile(fpath,output=None):
    import socket
    global __writer__
    
    if (fpath and os.path.exists(fpath) and (os.path.isfile(fpath))):
	if (__writer__):
	    while (1):
		try:
		    __writer__.sendFile(fpath,__eof__=__eof__)
		    # To do: Ensure the file was received and stored at the other end however for now we simply assume that happened because no exceptions.
		    #os.remove(fpath)
		    break
		except socket.error:
		    print 'INFO: Restarting Socket Writer on %s:%s.' % (__writer__.ipAddress, __writer__.portNum)
		    __writer__ = tcpipbridge.SocketWriter(__writer__.ipAddress, __writer__.portNum,retry=__writer__.retry)
		    if (__is_listener__):
			__writer__.send('@@@address=%s:%s@@@' % (listen_to_ip,listen_to_port))
		except Exception, ex:
		    print >> sys.stderr, 'EXCEPTION: %s' % (_utils.formattedException(details=ex))
	else:
	    if (output and os.path.exists(output) and os.path.isdir(output)):
		try:
		    dest = os.sep.join([output,os.path.basename(fpath)])
		    _utils.copyFile(fpath, dest, no_shell=True)
		    print >> sys.stdout, 'DEBUG: PROCESS --> %s --> %s' % (fpath,dest)
		    if (os.path.exists(dest)):
			os.remove(fpath)
		except Exception, ex:
		    print >> sys.stderr, 'EXCEPTION: %s' % (_utils.formattedException(details=ex))

@threadpool.threadify(__Q1__)
def ProcessInputs(action,watching,fpath,output=None):
    fp = '/'.join([watching, fpath]).replace(os.sep,'/')
    if (action == Actions.Created):
	print >> sys.stdout, 'DEBUG: PROCESS --> INPUT (%s) --> %s' % (action,fp)
	ProcessFile(fp,output=output)
    else:
	print >> sys.stdout, 'DEBUG: IGNORE --> INPUT (%s) --> %s' % (action,fp)

if (__name__ == '__main__'):
    from optparse import OptionParser
    
    class CustomOptionParser(OptionParser):
	def exit(self, status=0, msg=None):
	    if msg:
		sys.stderr.write(msg)
	    _utils.terminate('Program Complete.')

    if (len(sys.argv) == 1):
	sys.argv.insert(len(sys.argv), '-h')
    
    parser = CustomOptionParser("usage: %prog [options]")
    parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
    parser.add_option("-i", "--input", action="store", type="string", help="Fully qualified filesystem path or IP address.", dest="ipath")
    parser.add_option("-o", "--output", action="store", type="string", help="Fully qualified filesystem path or IP address.", dest="opath")
    parser.add_option("-d", "--dest", action="store", type="string", help="Fully qualified filesystem path for incoming files.", dest="dest")
    parser.add_option("-r", "--retry", action="store_true", help="Sets retry to True otherwise will not retry connection with Remote.", dest="retry")
    parser.add_option("-l", "--listen", action="store", type="string", help="IP address and port for listener, provides bidirectional communications.", dest="listener")
    
    options, args = parser.parse_args()
    
    _isVerbose = False
    if (options.verbose):
	_isVerbose = True
	
    __ipath__ = None
    if (options.ipath and (os.path.exists(options.ipath) and os.path.isdir(options.ipath)) or (_utils.is_valid_ip_and_port(options.ipath)) ):
	__ipath__ = options.ipath
	
    if (_isVerbose):
	print >> sys.stdout, 'INFO: input path is "%s".' % (__ipath__)
	
    __opath__ = None
    if (options.opath and (os.path.exists(options.opath) and os.path.isdir(options.opath)) or (_utils.is_valid_ip_and_port(options.opath)) ):
	__opath__ = options.opath
	
    __dest__ = None
    if (options.dest and (os.path.exists(options.dest) and os.path.isdir(options.dest)) ):
	__dest__ = options.dest
	    
    __retry__ = False
    if (options.retry):
	__retry__ = options.retry
		
    __listener__ = None
    if (options.listener and _utils.is_valid_ip_and_port(options.listener) ):
	__listener__ = options.listener
		
    if (_isVerbose):
	print >> sys.stdout, 'INFO: input path is "%s".' % (__ipath__)
	print >> sys.stdout, 'INFO: output path is "%s".' % (__opath__)
	print >> sys.stdout, 'INFO: dest path is "%s".' % (__dest__)
	print >> sys.stdout, 'INFO: retry is "%s".' % (__retry__)
	print >> sys.stdout, 'INFO: listener is "%s".' % (__listener__)

    __changes__ = 0
    __hDir__ = None
    
    #####################################################
    ##
    ## Establist a listener for a remote connection.
    ##
    #####################################################

    def __callback__(*args, **kwargs):
	print 'DEBUG.%s: args=%s, kwargs=%s' % (misc.funcName(),args,kwargs)
	new_dirname = args
	if (__dest__):
	    if (not os.path.exists(__dest__)):
		os.makedirs(__dest__)
	    if (len(args) > 0):
		new_dirname = args[0].replace(os.path.dirname(args[0]),__dest__)
	elif (__opath__):
	    if (not os.path.exists(__opath__)):
		os.makedirs(__opath__)
	    if (len(args) > 0):
		new_dirname = args[0].replace(args[0],__opath__)
	print 'DEBUG.%s: new_dirname=%s' % (misc.funcName(),new_dirname)
	return new_dirname
    
    def __callback2__(*args, **kwargs):
	__re1__ = re.compile("@@@delete=(?P<filename>.*)@@@", re.DOTALL | re.MULTILINE)
	data = args[0] if (misc.isIterable(args) and (len(args) > 0)) else args
	matches1 = __re1__.search(data)
	if (matches1):
	    f = matches1.groupdict().get('filename',None)
	    if (f):
		fpath = os.sep.join([__ipath__,f])
		if (os.path.exists(fpath) and os.path.isfile(fpath)):
		    print 'INFO: Removing "%s".' % (fpath)
		    os.remove(fpath)
	print 'DEBUG.%s: args=%s, kwargs=%s' % (misc.funcName(),args,kwargs)
	return None
    
    __is_listener__ = __listener__ and _utils.is_valid_ip_and_port(__listener__)
    __is_ipath__ = __ipath__ and _utils.is_valid_ip_and_port(__ipath__)
    if (__is_listener__) or (__is_ipath__):
	if (__is_listener__):
	    cb = __callback2__
	    listen_to_ip,listen_to_port = tcpipbridge.parse_ip_address_and_port(__listener__, default_ip='0.0.0.0', default_port=50555)
	elif (__is_ipath__):
	    cb = __callback__
	    listen_to_ip,listen_to_port = tcpipbridge.parse_ip_address_and_port(__ipath__, default_ip='0.0.0.0', default_port=55555)
	print 'INFO: Starting TCP/IP Bridge on %s:%s.' % (listen_to_ip, listen_to_port)
	tcpipbridge.startTCPIPBridge(listen_to_ip, listen_to_port, callback=cb,__eof__=__eof__)
    
    if (_utils.is_valid_ip_and_port(__opath__)):
	connect_to_ip,connect_to_port = tcpipbridge.parse_ip_address_and_port(__opath__, default_ip='0.0.0.0', default_port=55555)
	print 'INFO: Starting Socket Writer on %s:%s.' % (connect_to_ip, connect_to_port)
	__writer__ = tcpipbridge.SocketWriter(connect_to_ip, connect_to_port,retry=__retry__)
	
	if (__is_listener__):
	    __writer__.send('@@@address=%s:%s@@@' % (listen_to_ip,listen_to_port))
	
    if (__ipath__ and os.path.exists(__ipath__) and os.path.isdir(__ipath__)):
	print 'INFO: Beginning to look for changes appearing in "%s".' % (__ipath__)
	FILE_LIST_DIRECTORY = 0x0001
	__hDir__ = win32file.CreateFile (
            __ipath__,
            FILE_LIST_DIRECTORY,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS,
            None
        )
	#__changes__ = win32con.FILE_NOTIFY_CHANGE_FILE_NAME
	#__changes__ |= win32con.FILE_NOTIFY_CHANGE_DIR_NAME
	#__changes__ |= win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES
	#__changes__ |= win32con.FILE_NOTIFY_CHANGE_SIZE
	#__changes__ |= win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
	#__changes__ |= win32con.FILE_NOTIFY_CHANGE_SECURITY

	__changes__ = win32con.FILE_NOTIFY_CHANGE_FILE_NAME
	
	report_changes(__changes__)

	handle_changes(__hDir__, __changes__, __ipath__, output=__opath__, callback=ProcessInputs)
	
	while (1):
	    print >> sys.stdout, 'Sleeping...'
	    time.sleep(5)
	    print >> sys.stdout, 'Doing nothing...'
	    time.sleep(5)
    elif (__is_ipath__):
	print >> sys.stderr, 'INFO: Taking inputs from remote connection via TCP/IP Bridge.'
    else:
	print >> sys.stderr, 'WARNING: Cannot proceed without an input path, see the --input parameter.'
