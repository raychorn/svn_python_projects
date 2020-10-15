__copyright__ = """\
(c). Copyright 1990-2008, Vyper Logix Corp., 

                   All Rights Reserved.

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

__version__ = "0.2.1.2"

import os, sys
import signal

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import BaseHTTPServer, select, socket, SocketServer, urlparse

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.misc import ReportTheList

from vyperlogix.process import Popen

from vyperlogix.daemon.daemon import Log
from vyperlogix.daemon.daemon import EchoLog

from vyperlogix.classes.CooperativeClass import Cooperative

from vyperlogix.lists.ListWrapper import CircularList

from vyperlogix.sockets.proxies.TinyHTTPProxy import VyperProxy
from vyperlogix.sockets.proxies.TinyHTTPProxy import start_VyperProxy

from vyperlogix.misc import ObjectTypeName

from vyperlogix.zlib import zlibCompressor

def save_pid(fOut,pid):
    if (fOut.closed):
	fOut = open(fOut.name,'a')
    try:
	print >>fOut, '%d' % (pid)
    finally:
	fOut.flush()
	fOut.close()

def main():
    from sys import argv
    import sys
    allowed = []
    deletes = {}
    for i in xrange(1,len(argv)):
        if (argv[i] in ['-h', '--help']):
            print argv[0], "[port [allowed_client_name ...]]"
            sys.exit(1)
        elif (argv[i] in ['--hosts']):
            try:
                hosts = argv[i+1].split(',')
                print >>sys.stderr, '%s %s %s' % (argv[0],argv[i],hosts)
                VyperProxy.remotes = CircularList(hosts)
                deletes[i] = argv[i]
                deletes[i+1] = argv[i+1]
            except Exception, details:
                info_string = _utils.formattedException(details=details)
                print >>sys.stderr, info_string
        elif (argv[i] in ('--allowed')):
            try:
                name = argv[i+1]
                client = socket.gethostbyname(name)
                allowed.append(client)
                print "Accept: %s (%s)" % (client, name)
                VyperProxy.allowed_clients = allowed
                deletes[i] = argv[i]
                deletes[i+1] = argv[i+1]
            except Exception, details:
                info_string = _utils.formattedException(details=details)
                print >>sys.stderr, info_string
        elif (argv[i] in ('--django')):
            try:
                z = argv[i+1]
                print 'z is "%s".' % (z)
		_django,_django_port,_django_num = tuple(z.split(','))
		_django = _django.replace('/',os.sep)
		_django_port = int(_django_port)
		_django_num = int(_django_num)
		commands = []
		for k in xrange(_django_port,_django_port+_django_num):
		    s = '"%s" %d' % (_django,k)
		    commands.append(s)
		#print commands
		buffers = []
		shells = []
		for cmd in commands:
		    sio = StringIO()
		    buffers.append(sio)
		    p = Popen.Shell([cmd],env=None,fOut=sio,isExit=False,isWait=False,isVerbose=True)
		    #print >>sys.stderr, 'pid=%d' % (p.proc.pid)
		    save_pid(_pidFile,p.proc.pid)
		    shells.append(p)
		    #print >>sys.stderr, sio.getvalue()
                deletes[i] = argv[i]
                deletes[i+1] = argv[i+1]
            except Exception, details:
                info_string = _utils.formattedException(details=details)
                print >>sys.stderr, info_string
                #print >>sys.stderr, 'i=%d' % (i)
		#ReportTheList.reportTheList(argv,'argv',fOut=sys.stderr)
    if (len(allowed) == 0):
        print >>sys.stderr, "Any clients will be served..."
    for k,v in deletes.iteritems():
        argv[k] = None
    while (argv[len(argv)-1] is None):
	argv.pop()
    #ReportTheList.reportTheList(argv,'start_VyperProxy --> argv',fOut=sys.stderr)
    start_VyperProxy()

def signal_handler(self, sig, stack):
    """Handle the signal sent to the daemon."""
    if sig == signal.SIGUSR1:
        pass
    elif sig == signal.SIGHUP:
        print >>sys.stderr, "%s :: Should reload itself." % (misc.funcName())
    elif sig == signal.SIGTERM:
        logger.close()
        print >>sys.stderr, "%s :: SIGTERM: stop the server." % (misc.funcName())
        sys.exit(0)
    else:
        print >>sys.stderr, "%s :: SIG: %s." % (misc.funcName(),str(sig))
        
if (__name__ == '__main__'):
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)

    _root_ = os.path.dirname(sys.argv[0])
    _log_path = os.path.join(_root_,'logs')
    _pid_path = os.path.join(_root_,'pid')
    
    _utils._makeDirs(_log_path)

    _utils.removeAllFilesUnder(_pid_path)
    _utils._makeDirs(_pid_path)
    
    _logFile = open(os.path.join(_log_path, '%s_%s.txt' % (os.path.basename(sys.argv[0]),_utils.timeStampLocalTime(format=_utils.formatSalesForceDateTimeStr()).replace(' ','_').replace(':','_'))),'w')
    logger = EchoLog(_logFile)

    _pidFile = open(os.path.join(_pid_path, 'pid_%s.txt' % (_utils.timeStampLocalTime(format=_utils.formatSalesForceDateTimeStr()).replace(' ','_').replace(':','_'))),'w')
    
    try:
        signal.signal(signal.SIGTERM, signal_handler)    
    except AttributeError:
        print >>sys.stderr, 'WARNING: signal.SIGTERM is not supported.'
        
    sys.stderr = logger
    
    pid = os.getpid()
    #print >>sys.stderr, 'pid=%d.' % (pid)
    save_pid(_pidFile,pid)
    
    try:
        main()
    except Exception, details:
        info_string = _utils.formattedException(details=details)
        print >>sys.stderr, info_string
