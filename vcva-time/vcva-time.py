import os
import sys
import time

import logging

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

    if (verbose):
        print 'BEGIN:'
        for f in sys.path:
            print f
        print 'END !!'
    
import atexit
@atexit.register
def __terminate__():
    import os, signal
    pid = os.getpid()
    os.kill(pid,signal.SIGTERM)

from vyperlogix import paramiko

from vyperlogix.daemon.daemon import Log
from vyperlogix.daemon.daemon import CustomLog
from vyperlogix.logging import standardLogging

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.lists.ListWrapper import ListWrapper

__version__ = '1.0.0.1'

### BEGIN: LOGGING ###############################################################
__cwd__ = os.path.expanduser("~")
name = _utils.getProgramName()
fpath = __cwd__
_log_path = _utils.safely_mkdir_logs(fpath=fpath)
_log_path = _utils.safely_mkdir(fpath=_log_path,dirname=_utils.timeStampLocalTimeForFileName(delimiters=('_','-'),format=_utils.formatSalesForceTimeStr()))
if (not os.path.exists(_log_path)):
    print >> sys.stderr, 'Logging path does not exist at "%s".' % (_log_path)
    __terminate__()

logFileName = os.sep.join([_log_path,'%s.log' % (name)])

print '(%s) :: Logging to "%s".' % (_utils.timeStampLocalTime(),logFileName)

from optparse import OptionParser

parser = OptionParser("usage: %prog ip-address [options]")
parser.add_option('-p', '--port', dest='port', help="VCVA host port, typically 22", action="store", type="int")
parser.add_option('-u', '--username', dest='username', help="VCVA username, typically root", action="store", type="string")
parser.add_option('-w', '--password', dest='password', help="VCVA password, typically Compaq123", action="store", type="string")
parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
parser.add_option('-d', '--delay', dest='delay', help="delay seconds", action="store", type="int")

options, args = parser.parse_args()

_isVerbose = False
if (options.verbose):
    _isVerbose = True

_logging = logging.INFO
_console_logging = logging.INFO
standardLogging.standardLogging(logFileName,_level=_logging,console_level=_console_logging,isVerbose=_isVerbose)

logger = logging.getLogger('')

__ip__ = None #'16.83.121.123'
if (len(args) > 0):
    __ip__ = args[0] if (_utils.is_ip_address_valid(args[0])) else None

normalize = lambda items:[s for s in [''.join(ll[0:ll.findFirstMatching('#') if (ll.findFirstMatching('#') > -1) else len(ll)]).strip() for ll in [ListWrapper(l) for l in items if (len(l) > 0)]] if (len(s) > 0)]
    
if (not misc.isStringValid(__ip__)):
    c_opt_defaults = {'5.5':r"C:\opt\serenity-client\server\configuration",'5.1':r"C:\opt\serenity-client\server\config"}
    for k,v in c_opt_defaults.iteritems():
        fpath = os.sep.join([v,'client.properties'])
        #print '(+++).1 "%s" exists ?' % (fpath)
        if (os.path.exists(fpath)):
            #print '(+++).2 "%s" exists !!!' % (fpath)
            fIn = open(fpath,'r')
            for line in fIn:
                #print '(+++).3 line=%s' % (line)
                l = ''.join(normalize(line))
                #print '(+++).4 l=%s' % (l)
                toks = [str(t).strip() for t in l.split('=')]
                #print '(+++).5 is "%s" --> "ls.url" ?' % (toks[0])
                if (toks[0].lower() == 'ls.url'):
                    toks2 = toks[-1].split(r"\:")
                    #print '(+++).6 toks2=%s' % (toks2)
                    __ip__ = toks2[1].replace('//','')
                    #print '(+++).7 __ip__=%s' % (__ip__)
            fIn.close()
    
if (not misc.isStringValid(__ip__)):
    logger.error('ERROR: Cannot proceed without a valid ip address that must be the first argument before any options.')
    __terminate__()

logger.info('VCVA-Time v%s' % (__version__))

__port__ = 22
if (options.port):
    __port__ = options.port

__username__ = 'root'
if (options.username):
    __username__ = options.username

__password__ = 'Compaq123'
if (options.password):
    __password__ = options.password
    
__delay__ = 10
if (options.delay):
    __delay__ = int(str(options.delay))
        
if (_isVerbose):
    logger.info('ip is %s' % (__ip__))
    logger.info('port is %s' % (__port__))
    logger.info('username is %s' % (__username__))
    logger.info('password is %s' % (__password__))
    logger.info('delay is %s' % (__delay__))

__home_directory__ = os.path.expanduser("~")

__ssh_directory__ = os.sep.join([__home_directory__,'ssh'])
if (not os.path.exists(__ssh_directory__)):
    os.makedirs(__ssh_directory__)
__ssh_known_hosts__ = os.sep.join([__ssh_directory__,'known_hosts'])
if (not os.path.exists(__ssh_known_hosts__)):
    fOut = open(__ssh_known_hosts__,'w')
    print >> fOut, ''
    fOut.flush()
    fOut.close()

sftp = paramiko.ParamikoSFTP(__ip__,int(__port__),__username__,password=__password__,callback=None,use_manual_auth=True,auto_close=False,logPath=logFileName if (_isVerbose) else None)

cmd = 'date'
responses = sftp.exec_command(cmd)

__zones__ = ['PST','PDT','MST','MDT','CST','CDT','EST','EDT']
__zoneNames__ = dict([('P','Pacific'),('M','Mountain'),('C','Central'),('E','Eastern')])
__zones2__ = [tz.replace('ST',' Standard Time').replace('DT',' Daylight Time') for tz in __zones__]
for i in xrange(len(__zones2__)):
    __zones2__[i] = '%s%s'% (__zoneNames__.get(__zones2__[i][0],''),__zones2__[i][1:])

logger.info('BEGIN:')
for r in responses:
    tests = ListWrapper([r.find(' %s '%(tz)) > -1 for tz in __zones__])
    has_us_timezone = any(tests)
    tzone = None
    if (has_us_timezone):
        i = tests.findFirstMatching(True)
        if (i > -1):
            tzone = __zones__[i]
            tzone2 = __zones2__[i]
            r = r.replace(tzone,tzone2)
    logger.info('r=%s' % (r))
    dt = _utils.getFromDateStr(r,format='%a %b %d %H:%M:%S %Z %Y')
    __dt__ = _utils.getFromNativeTimeStamp(_utils.timeStampLocalTime())
    delta = max(dt,__dt__) - min(dt,__dt__)
    logger.info('%s --> %s' % (r, dt))
    if (delta.total_seconds() > 120):
        cmd2 = 'date -s "%s"' % (_utils.getAsDateTimeStr(__dt__,fmt='%d %b %Y %H:%M:%S'))
        responses2 = sftp.__reopen__().exec_command(cmd2)
        for rr in responses2:
            logger.info(rr)
        logger.info('New time set !!!')
    else:
        logger.info('Local Time is within %s second%s of VCVA time, no need to adjust at this time.' % (delta.total_seconds(),'s' if ( (delta.total_seconds() == 0) or (delta.total_seconds() > 1) ) else ''))
logger.info('END!')

sftp.close()
