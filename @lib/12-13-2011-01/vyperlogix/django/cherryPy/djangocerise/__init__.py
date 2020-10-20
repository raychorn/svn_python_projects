__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
import os, sys
import logging
import signal

from optparse import OptionParser

from vyperlogix.misc import ReportTheList
from vyperlogix.misc import ObjectTypeName
from vyperlogix.lists import ListWrapper
from vyperlogix.misc import _utils

from vyperlogix.daemon.daemon import Log

from vyperlogix.process import Popen
StringIO = _utils.stringIO

try:
    # This fails if TurboGears is installed because TurboGears wants to use CherryPy version 2...
    from cherrypy.wsgiserver import CherryPyWSGIServer as Server
    print >>sys.stderr, 'Imported the installed %s' % (Server.version)
except ImportError, details:
    try:
        from cherrypy3.wsgiserver import CherryPyWSGIServer as Server
        print >>sys.stderr, 'Imported the installed %s' % (Server.version)
    except ImportError, details:
        info_string = _utils.formattedException(details)
        print >>sys.stderr, 'Import of installed CherryPy Failed, retrying from the vyperlogix library.\n%s' % (info_string)
        try:
            from vyperlogix.sockets.CherryPyWSGIServer import CherryPyWSGIServer as Server
            print >>sys.stderr, 'Imported the vyperlogix library %s' % (Server.version)
        except ImportError, details:
            info_string = _utils.formattedException(details)
            print >>sys.stderr, 'Import of CherryPy from vyperlogix library failed, retrying the older verson of CherryPy from the vyperlogix library.\n%s' % (info_string)
            try:
                from vyperlogix.sockets.wsgi.wsgiserver import CherryPyWSGIServer as Server
                print >>sys.stderr, 'Imported the older version of %s' % (Server.version)
            except ImportError, details:
                info_string = _utils.formattedException(details)
                print >>sys.stderr, 'ERROR: Cannot use the %s command because cannot import CherryPyWSGIServer from the known sources.\n%s' % (__name__,info_string)
                sys.exit(0)

from django.core.handlers.wsgi import WSGIHandler
# Django related import are performed after the loading of the
# configuration as we need to set the DJANGO_SETTINGS_MODULE
# environment variable which comes from the config.

def change_uid_gid(uid, gid=None):
    """Try to change UID and GID to the provided values.
    UID and GID are given as names like 'nobody' not integer.

    Src: http://mail.mems-exchange.org/durusmail/quixote-users/4940/1/
    """
    if not os.geteuid() == 0:
        # Do not try to change the gid/uid if not root.
        return
    (uid, gid) = get_uid_gid(uid, gid)
    os.setgid(gid)
    os.setuid(uid)

def get_uid_gid(uid, gid=None):
    """Try to change UID and GID to the provided values.
    UID and GID are given as names like 'nobody' not integer.

    Src: http://mail.mems-exchange.org/durusmail/quixote-users/4940/1/
    """
    import pwd, grp
    uid, default_grp = pwd.getpwnam(uid)[2:4]
    if gid is None:
        gid = default_grp
    else:
        try:
            gid = grp.getgrnam(gid)[2]            
        except KeyError:
            gid = default_grp
    return (uid, gid)

def chown_pid_log(optons,uid, gid=None):
    if not os.geteuid() == 0:
        # Do not try to change the gid/uid if not root.
        return
    (uid, gid) = get_uid_gid(uid, gid)
    if os.path.exists(options.PIDFILE):
        os.chown(options.PIDFILE, uid, gid)
    os.chown(options.LOGFILE, uid, gid)

def parse_options():
    """Return the run options for the server.

    It is merging options from command line and from the config python
    module. It sets and import the right stuff for Django.
    """
    parser = OptionParser()
    parser.add_option("--conf", "-c", dest="config",
                      help="load configuration from file",
                      action="store", default="config")
    parser.add_option("--host", "", dest="host",
                      help="specify the host as 127.0.0.1:80",
                      action="store", default="config")
    parser.add_option("--conf2", "", dest="config2",
                      help="load configuration from file",
                      action="store", default="config")
    parser.add_option("--host2", "", dest="host2",
                      help="specify the host as 127.0.0.1:443",
                      action="store", default="config")
    parser.add_option("--daemon", "-d", dest="daemon",
                      help="run as daemon.",
                      action="store", default="0")
    parser.add_option("--kill", "-k", dest="kill",
                      help="kill and clean.",
                      action="store", default="0")
    (cmd_options, args) = parser.parse_args()
    try:
        options = __import__(cmd_options.config)
    except ImportError, e:
        raise EnvironmentError, "Could not import settings '%s' (Is it on sys.path? Does it have syntax errors?): %s" % (cmd_options.config, e)
    os.environ["DJANGO_SETTINGS_MODULE"] = options.DJANGO_SETTINGS
    toks = cmd_options.host.split(':')
    _ip = toks[0]
    if (_utils.is_ip_address_valid(_ip)) and (options.IP_ADDRESS != _ip):
        print >>sys.stdout, 'INFO: Overriding options.IP_ADDRESS of "%s" with "%s".' % (options.IP_ADDRESS,_ip)
        options.IP_ADDRESS = toks[0]
    port = int(options.PORT)
    if (len(toks) == 2):
        port = int(toks[-1]) if (str(toks[-1]).isdigit()) else port
    if (int(options.PORT) != port) and (port >= 0) and (port <= 65535):
        print >>sys.stdout, 'INFO: Overriding options.PORT of "%s" with "%s".' % (options.PORT,port)
        options.PORT = port
    parts = list(os.path.splitext(options.LOGFILE))
    options.SERVER_NAME = '%s:%s' % (options.IP_ADDRESS,options.PORT)
    parts[0] += '_%s_%s' % (options.IP_ADDRESS.replace('.','_'),options.PORT)
    options.LOGFILE = ''.join(parts)
    cmd_options.daemon = True if (int(cmd_options.daemon)) else False
    cmd_options.kill = True if (int(cmd_options.kill)) else False
    options.cmd_options = cmd_options
    options.PIDFILE = options.PIDFILE.replace('{port}',options.SERVER_NAME.replace(':','-'))
    return options

class Runner:
    """Runner class.

    Store some basic info like the server instance so the signal
    handling methods can easily access it.
    """

    def __init__(self):
        """Initialize the server."""
        self.server = None
        # Get the options
        self.options = parse_options()
        #
        # Logging stuff.
        #
        logging.basicConfig(filename=self.options.LOGFILE, format='%(asctime)s %(levelname)s %(message)s')
        log = logging.getLogger("webserver.py")
        if self.options.DEBUG:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(getattr(logging, self.options.LOGLEVEL.upper()))
            
        self.logger = Log(open(self.options.LOGFILE,'a'))
    
        if (self.options.cmd_options.kill):
            if (sys.platform == 'win32'):
                log.info("Platform is %s but daemon procs run in Unix or Linux but not %s." % (sys.platform,sys.platform))
            else:
                if os.path.exists(self.options.PIDFILE):
                    s_pid = _utils.readFileFrom(self.options.PIDFILE,mode='r',noCRs=True)[0]
                    try:
                        _pid = int(s_pid)
                    except:
                        _pid = -1
                    if (_pid > -1):
                        buf = StringIO()
			cmd = 'kill -9 %s' % (_pid)
                        shell = Popen.Shell([cmd],isExit=True,isWait=True,isVerbose=True,fOut=buf)
                        lines = ListWrapper.ListWrapper([l for l in buf.getvalue().split('\n') if (len(l.strip()) > 0)])
			ReportTheList.reportTheList(lines,cmd,fOut=sys.stdout)
			self.clean()
                    else:
                        log.info("PID file exists: %s, webserver is apparently running but the PID is not a number because it is %s of type %s, exiting." % self.options.PIDFILE,s_pid,ObjectTypeName.typeClassName(s_pid))
                else:
                    log.info("PID file does NOT exist: %s, webserver is apparently NOT running, exiting." % self.options.PIDFILE)
        elif (self.options.RUN_AS_DAEMON) or (self.options.cmd_options.daemon):
            log.info("Run as daemon")
            # do the UNIX double-fork magic, see Stevens' "Advanced
            # Programming in the UNIX Environment" for details (ISBN 0201563177)
            if os.path.exists(self.options.PIDFILE):
                log.info("PID file exists: %s, webserver already running, exiting" % self.options.PIDFILE)
                sys.exit(1)
            try:
                pid = os.fork()
                if pid > 0:
                    # exit first parent
                    sys.exit(0)
            except OSError, e:
                log.debug("Fork #1 failed: %d (%s)" % (e.errno, e.strerror))
                sys.exit(1)
            # decouple from parent environment
            os.chdir(self.options.DAEMON_RUN_DIR)   #don't prevent unmounting....
            os.setsid()
            os.umask(0)
            # do second fork
            try:
                pid = os.fork()
                if pid > 0:
                    # exit from second parent, print eventual PID before
                    open(self.options.PIDFILE,'w').write("%d"%pid)
                    chown_pid_log(self.options,self.options.SERVER_USER, self.options.SERVER_GROUP)
                    sys.exit(0)
            except OSError, e:
                log.debug("Fork #2 failed: %d (%s)" % (e.errno, e.strerror))
                sys.exit(1)
        # Start the daemon main loop

    def clean(self):
        """Clean the PID file"""
        if (self.options.RUN_AS_DAEMON) or (self.options.cmd_options.daemon):
            try:
                os.remove(self.options.PIDFILE)
            except Exception, e:
                log = logging.getLogger("webserver.py")
                log.debug("Can't clean PID file: %s" % self.options.PIDFILE)
                log.debug(str(e))

    def main(self):
        """Real main loop of the daemon."""
        log = logging.getLogger("webserver.py")        
        if self.options.RUN_AS_DAEMON:
            #ensure the that the daemon runs a normal user
            change_uid_gid(self.options.SERVER_USER, self.options.SERVER_GROUP)
        if self.options.DJANGO_SERVE_ADMIN:
            from django.core.servers.basehttp import AdminMediaHandler
            app = AdminMediaHandler(WSGIHandler())
        else:
            app = WSGIHandler()
	try:
	    if (self.options.SERVER_VERSION):
		Server.version = '%s+%s' % (self.options.SERVER_VERSION,Server.version)
	except AttributeError:
	    Server.version = 'DjangoCerise+%s' % (Server.version)
        self.server = Server((self.options.IP_ADDRESS, self.options.PORT),
                             app, self.options.SERVER_THREADS, self.options.SERVER_NAME)
        if self.options.SSL:
            self.server.ssl_certificate = self.options.SSL_CERTIFICATE
            self.server.ssl_private_key = self.options.SSL_PRIVATE_KEY
        try:
            signal.signal(signal.SIGUSR1, self.signal_handler)
        except AttributeError:
            print >>sys.stderr, 'WARNING: signal.SIGUSR1 is not supported.'
        try:
            signal.signal(signal.SIGHUP, self.signal_handler)
        except AttributeError:
            print >>sys.stderr, 'WARNING: signal.SIGHUP is not supported.'
        try:
            signal.signal(signal.SIGTERM, self.signal_handler)    
        except AttributeError:
            print >>sys.stderr, 'WARNING: signal.SIGTERM is not supported.'
        try:
            info_string = "Start the %s server on %s:%s logging to %s" % (__name__,self.options.IP_ADDRESS, str(self.options.PORT),self.options.LOGFILE)
            print >>sys.stdout, info_string
            log.info(info_string)
            sys.stderr = self.logger
            sys.stdout = self.logger
            self.server.start()
        except KeyboardInterrupt:
            self.server.stop()
            log.debug("KeyboardInterrupt: stop the server")
            self.clean()

    def signal_handler(self, sig, stack):
        """Handle the signal sent to the daemon."""
        if sig == signal.SIGUSR1:
            pass
        elif sig == signal.SIGHUP:
            log.debug("Should reload itself.")
        elif sig == signal.SIGTERM:
            self.server.stop()
            log.debug("SIGTERM: stop the server")
            self.clean()
            sys.exit(0)
        else:
            log.debug("SIG: %s" % str(sig))
