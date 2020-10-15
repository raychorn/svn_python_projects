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

from vyperlogix.daemon.daemon import Log
from vyperlogix.daemon.daemon import CustomLog
from vyperlogix.logging import standardLogging

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.lists.ListWrapper import ListWrapper

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

parser = OptionParser("usage: %prog filename [options]")
parser.add_option('-l', '--lowercase', dest='lowercase', help="lowercase (default)", action="store_true")
parser.add_option('-u', '--uppercase', dest='uppercase', help="uppercase (default)", action="store_true")
parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")

options, args = parser.parse_args()

_isVerbose = False
if (options.verbose):
    _isVerbose = True

_isUpperCase = True
if (options.lowercase):
    _isUpperCase = False

_logging = logging.INFO
_console_logging = logging.INFO
standardLogging.standardLogging(logFileName,_level=_logging,console_level=_console_logging,isVerbose=_isVerbose)

logger = logging.getLogger('')

if (_isVerbose):
    logger.info('password is %s' % (__password__))

def hashfile(filepath,isUpperCase=True):
    import hashlib, os, sys
    sha1 = hashlib.sha1()
    if (os.path.exists(filepath)) and (os.path.isfile(filepath)):
        f = open(filepath, 'rb')
        try:
            sha1.update(f.read())
        finally:
            f.close()
    else:
        raise IOError('No filepath was specified')
    response = sha1.hexdigest()
    return response.upper() if (isUpperCase) else response

logger.info('BEGIN:')
if (os.path.exists(args[0])) and (os.path.isfile(args[0])):
    print hashfile(args[0],isUpperCase=_isUpperCase)
logger.info('END!')

