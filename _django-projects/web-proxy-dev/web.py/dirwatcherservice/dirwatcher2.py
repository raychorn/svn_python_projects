import os
import sys
import time

import logging

from vyperlogix.daemon.daemon import Log
from vyperlogix.logging import standardLogging

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.win import dirwatcher

__running__ = True

### BEGIN: LOGGING ###############################################################
name = _utils.getProgramName()
fpath = os.path.dirname(sys.argv[0])
_log_path = _utils.safely_mkdir_logs(fpath=fpath)
_log_path = _utils.safely_mkdir(fpath=_log_path,dirname=_utils.timeStampLocalTimeForFileName(delimiters=('_','-'),format=_utils.formatSalesForceTimeStr()))

logFileName = os.sep.join([_log_path,'%s.log' % (name)])

print '(%s) :: logFileName=%s' % (_utils.timeStampLocalTime(),logFileName)

from optparse import OptionParser

parser = OptionParser("usage: %prog [options]")
parser.add_option('-w', '--watching', dest='watching', help="watching folder path")
parser.add_option('-c', '--changes', dest='changes', help="changes (all)")
parser.add_option('--ll', '--loglevel', dest='loglevel', help="loglevel (INFO)")
parser.add_option('--cl', '--consoleloglevel', dest='consoleloglevel', help="consoleloglevel (INFO)")
parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")

options, args = parser.parse_args()

__watching__ = None
__changes__ = None
if (options.watching):
    __watching__ = options.watching if (os.path.exists(options.watching)) else None
else:
    print 'Nothing to do unless you watch a directory.'
    sys.exit(1)

if (options.changes):
    __changes__ = win32con.FILE_NOTIFY_CHANGE_FILE_NAME
    __changes__ |= win32con.FILE_NOTIFY_CHANGE_DIR_NAME
    __changes__ |= win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES
    __changes__ |= win32con.FILE_NOTIFY_CHANGE_SIZE
    __changes__ |= win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
    __changes__ |= win32con.FILE_NOTIFY_CHANGE_SECURITY
    
_logging = logging.INFO
if (options.loglevel):
    pass

_console_logging = logging.INFO
if (options.consoleloglevel):
    pass

_isVerbose = False
if (options.verbose):
    _isVerbose = True

standardLogging.standardLogging(logFileName,_level=_logging,console_level=_console_logging,isVerbose=_isVerbose)

def __callback__(self,action,fname):
    print 'CALLBACK: %s --> %s' % (action,fname)

if (os.path.exists(__watching__)):
    print 'Watching... "%s".' % (__watching__)
    watcher = dirwatcher.DirectoryWatcher(__watching__)
    watcher.execute(callback=__callback__)
    
    while (1):
        time.sleep(5)
else:
    print 'Nothing to do.'
    dirwatcher.__terminate__()
