__copyright__ = """\
(c). Copyright 2013, Ray C Horn, All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !
"""
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

from vyperlogix.classes import SmartObject

from vyperlogix.lists.ListWrapper import ListWrapper

__version__ = '1.0.0.0'

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

parser = OptionParser("usage: %prog [options]")
parser.add_option('-1', '--fence1', dest='fence1', help="Fence1 expressed as Lat,Lng,Radius", action="store", type="string")
parser.add_option('-2', '--fence2', dest='fence2', help="Fence2 expressed as Lat,Lng,Radius", action="store", type="string")
parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
parser.add_option('-b', '--bearing', dest='bearing', help="bearing in decimal degrees", action="store", type="float")
parser.add_option('-d', '--distance', dest='distance', help="distance in decimal miles per step.", action="store", type="float")
parser.add_option('-s', '--steps', dest='steps', help="number of steps.", action="store", type="int")
parser.add_option('-x', '--experimental', dest='experimental', help="experimental - validates all fences can be crossed or traversed.", action="store_true")

options, args = parser.parse_args()

_isVerbose = False
if (options.verbose):
    _isVerbose = True
    
_isExperimental = False
if (options.experimental):
    _isExperimental = True

_logging = logging.INFO
_console_logging = logging.INFO
standardLogging.standardLogging(logFileName,_level=_logging,console_level=_console_logging,isVerbose=_isVerbose)

logger = logging.getLogger('')

logger.info('GPS-Fences v%s' % (__version__))

__fence1__ = None
if (options.fence1):
    __fence1__ = options.fence1

__fence2__ = None
if (options.fence2):
    __fence2__ = options.fence2

__bearing__ = 90.0
if (options.bearing):
    __bearing__ = options.bearing

__distance__ = 0.1
if (options.distance):
    __distance__ = options.distance

__steps__ = 5
if (options.steps):
    __steps__ = options.steps

if (_isVerbose):
    logger.info('fence1 is %s' % (__fence1__))
    logger.info('fence2 is %s' % (__fence2__))
    logger.info('bearing is %s' % (__bearing__))
    logger.info('distance is %s' % (__distance__))
    logger.info('steps is %s' % (__steps__))
    logger.info('isExperimental is %s' % (_isExperimental))

logger.info('BEGIN:')

normalize = lambda fence:[float(str(t).strip()) for t in str(fence).strip().split(',')]

d = normalize(__fence1__)
f1 = SmartObject.SmartObject({'lat':d[0],'lng':d[1],'radius':d[-1] if (len(d) == 3) else 0})

d = normalize(__fence2__)
f2 = SmartObject.SmartObject({'lat':d[0],'lng':d[1],'radius':d[-1] if (len(d) == 3) else 0})

from geopy import Point
from geopy.distance import distance, VincentyDistance

f1.pt = Point(f1.lat,f1.lng,0)
f2.pt = Point(f2.lat,f2.lng,0)
pt1 = Point(f1.lat,f1.lng,0)

if (not _isExperimental):
    steps = []
    
    logger.info('='*20)
    for aStep in xrange(1,__steps__+1):
        if (_isVerbose):
            logger.info('Step is %s.' % (aStep))
        pt1 = VincentyDistance(miles=__distance__).destination(pt1, __bearing__)
        if (_isVerbose):
            logger.info('pt1 is "%s"' % (pt1))
        
        dist1 = VincentyDistance(f1.pt,pt1).meters
        if (_isVerbose):
            logger.info('dist1 is "%s"' % (dist1))
        __is__ = dist1 < f1.radius
        logger.info('%s f1.' % ('INSIDE' if (__is__) else 'OUTSIDE'))
        __outward1__ = None
        if (len(steps) > 1):
            __outward1__ = dist1 > steps[-1].dist1
        if (_isVerbose):
            if (__outward1__ is not None):
                logger.info('Moving %s relative to f1.' % ('IN' if (not __outward1__) else 'OUT'))
            else:
                logger.info('Cannot determine relative movement to f1.')
        
        dist2 = VincentyDistance(f2.pt,pt1).meters
        if (_isVerbose):
            logger.info('dist2 is "%s"' % (dist2))
        __is__ = dist2 < f2.radius
        logger.info('%s f2.' % ('INSIDE' if (__is__) else 'OUTSIDE'))
        __outward2__ = None
        if (len(steps) > 1):
            __outward2__ = dist2 > steps[-1].dist2
        if (_isVerbose):
            if (__outward2__ is not None):
                logger.info('Moving %s relative to f2.' % ('IN' if (not __outward2__) else 'OUT'))
            else:
                logger.info('Cannot determine relative movement to f2.')
    
        vector = SmartObject.SmartObject({'dist1':dist1,'dist2':dist2})
        
        steps.append(vector)
    
        logger.info('='*20)
else:
    analysis = SmartObject.SmartObject()
    for bearing in xrange(0,360):
        analysis[bearing] = SmartObject.SmartObject()
        for aStep in xrange(1,__steps__+1):
            if (_isVerbose):
                logger.info('Step is %s.' % (aStep))
                logger.info('Bearing is %s.' % (bearing))
            pt1 = VincentyDistance(miles=__distance__).destination(pt1, bearing)
            if (_isVerbose):
                logger.info('pt1 is "%s"' % (pt1))
            
            dist1 = VincentyDistance(f1.pt,pt1).meters
            if (not analysis[bearing].inside_f1):
                analysis[bearing].inside_f1 = dist1 < f1.radius
            
            dist2 = VincentyDistance(f2.pt,pt1).meters
            if (not analysis[bearing].inside_f2):
                analysis[bearing].inside_f2 = dist2 < f1.radius
                
            if (analysis[bearing].inside_f1 and analysis[bearing].inside_f2):
                logger.info('Crossed all fences for bearing %s !!!' % (bearing))
                break

        if ( (not analysis[bearing].inside_f1) or (not analysis[bearing].inside_f2)):
            logger.info('Did NOT Cross all fences for bearing %s !!!' % (bearing))
        
logger.info('END!')
