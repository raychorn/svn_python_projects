import os
import sys
import time

import re

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
parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
parser.add_option('-n', '--nondestructive', dest='nondestructive', help="nondestructive", action="store_true")

options, args = parser.parse_args()

_isVerbose = _utils.isBeingDebugged
if (options.verbose):
    _isVerbose = True

_isNonDestructive = _utils.isBeingDebugged
if (options.nondestructive):
    _isNonDestructive = True

_logging = logging.INFO
_console_logging = logging.INFO
standardLogging.standardLogging(logFileName,_level=_logging,console_level=_console_logging,isVerbose=_isVerbose)

logger = logging.getLogger('')

if (_isVerbose):
    logger.info('nondestructive is %s' % (_isNonDestructive))

from vyperlogix.crypto.sha1 import hashfile
from vyperlogix.classes.SmartObject import SmartObject

__vmware_cdrom_iso__ = 'vmware.cdrom.iso'
__vmware_cdrom_iso_fix__ = '<rasd:ResourceSubType>vmware.cdrom.remotepassthrough</rasd:ResourceSubType>'

__re__ = re.compile("<rasd:ResourceSubType>(?P<data>.*)</rasd:ResourceSubType>")

__re2__ = re.compile(r"SHA1\((?P<fname>.*)\)\s*=\s*(?P<signature>\w*)")

logger.info('BEGIN:')
fname = args[0]
if (os.path.exists(fname)) and (os.path.isfile(fname)):
    if (_isNonDestructive):
        newDirName = os.path.dirname(fname)+'_fixed'
        _utils._makeDirs(newDirName)
        newFname = os.path.basename(fname)
    else:
        newDirName = os.path.dirname(fname)
        newFname = os.path.basename(fname)+'-backup'
    fnameOut = os.sep.join([newDirName,newFname])
    __is__ = False
    fOut = open(fnameOut,'w')
    try:
        for line in _utils.readFileFromGenerator(fname):
            matches = __re__.search(line)
            if (matches):
                so = SmartObject(matches.groupdict())
                if (so.data == __vmware_cdrom_iso__):
                    #line = line[:matches.start()] + __vmware_cdrom_iso_fix__ + line[matches.end():]
                    line = _utils.splice(line,matches.start(),__vmware_cdrom_iso_fix__,matches.end())
                    __is__ = True
            print >> fOut, line
    finally:
        fOut.flush()
        fOut.close()
    if (__is__):
        __files__ = []
        sha1 = hashfile(fnameOut,isUpperCase=True)
        fname_mf = os.sep.join([os.path.dirname(fname),os.path.splitext(os.path.basename(fname))[0]+'.mf'])
        if (os.path.exists(fname_mf)) and (os.path.isfile(fname_mf)):
            if (_isNonDestructive):
                newFname_mf = os.path.basename(fname_mf)
            else:
                newFname_mf = os.path.basename(fname_mf)+'-backup'
            fnameOut_mf = os.sep.join([newDirName,newFname_mf])
            fOut = open(fnameOut_mf,'w')
            try:
                for line in _utils.readFileFromGenerator(fname_mf):
                    matches = __re2__.search(line)
                    if (matches):
                        so = SmartObject(matches.groupdict())
                        if (os.path.splitext(so.fname)[-1].lower() == '.ovf'):
                            line = line.replace(so.signature,sha1)
                        else:
                            __files__.append(so.fname)
                    print >> fOut, line.strip()
            finally:
                fOut.flush()
                fOut.close()
        else:
            logger.info('NOTHING TO DO (Cannot locate the .MF file which is supposed to be in the same folder as the .OVF file.) !!!')
        for f in __files__:
            fname_src = os.sep.join([os.path.dirname(fname),os.path.basename(f)])
            if (os.path.exists(fname_src)) and (os.path.isfile(fname_src)):
                if (_isNonDestructive):
                    newFname_dst = os.path.basename(f)
                else:
                    newFname_dst = os.path.basename(f)+'-backup'
                fnameOut_dst = os.sep.join([newDirName,newFname_dst])
                logger.info('Copying "%s" to "%s".' % (fname_src,fnameOut_dst))
                _utils.copy_binary_files_by_chunks(fname_src,fnameOut_dst,chunk_size=65535)
                logger.info('Done copying "%s" to "%s".' % (fname_src,fnameOut_dst))
    else:
        logger.info('NOTHING TO DO (Your OVF file looks good, oddly enough.) !!!')
else:
    logger.info('NOTHING TO DO (Cannot locate the .OVF file from the command line.) !!!')
logger.info('END!')

