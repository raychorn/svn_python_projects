import re
import os, sys, stat, platform
from time import localtime, asctime
from vyperlogix import misc
from vyperlogix.decorators import TailRecursive
from vyperlogix.enum.Enum import Enum
from vyperlogix.misc import ObjectTypeName
from vyperlogix.classes.SmartObject import SmartObject

class DaysOfWeek(Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6

class FileFolderSearchOptions(Enum):
    none = 0
    callback_files = 2**0
    callback_folders = 2**1
    skip_svn = 2**2

class DeCamelCaseMethods(Enum):
    default = 2**0
    force_lower_case = 2**1

isBeingDebugged = False if (not os.environ.has_key('WINGDB_ACTIVE')) else int(os.environ['WINGDB_ACTIVE']) == 1
isVerbose = False

isUsingWindows = (sys.platform.lower().find('win') > -1) and (os.name.lower() == 'nt')
isUsingMacOSX = (sys.platform.lower().find('darwin') > -1) and (os.name.find('posix') > -1) and (not isUsingWindows)
isUsingLinux = (sys.platform.lower().find('linux') > -1) and (os.name.find('posix') > -1) and (not isUsingWindows) and (not isUsingMacOSX)
isNotUsingLocalTimeConversions = not isUsingWindows
isUsingLocalTimeConversions = not isNotUsingLocalTimeConversions

__code_library_name__ = 'vyperlogix'

splice = lambda line,start,newStr,end:line[:start] + newStr + line[end:]

def terminate(reason):
    from vyperlogix.process.killProcByPID import killProcByPID
    if (reason):
        print >> sys.stderr, reason
    killProcByPID(os.getpid())

def os_platform():
    true_platform = os.environ['PROCESSOR_ARCHITECTURE']
    try:
        true_platform = os.environ["PROCESSOR_ARCHITEW6432"]
    except KeyError:
        pass
    return true_platform

def is_os_64bit():
    return platform.machine().endswith('64')

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def getWindowsLogicalDrives():
    if (isUsingWindows):
        import win32api
        return [d for d in win32api.GetLogicalDriveStrings().split("\x00")]
    return []

def getCurrentWindowsLogicalDrives():
    if (isUsingWindows):
        return [d for d in getWindowsLogicalDrives() if (len(d) > 0) and (os.path.isdir(d))]
    return []

def __hasVyperLogixLibraryLoadedIn__(container=sys.path):
    fpath = None
    try:
        paths = [f > -1 for f in container if str(f).find(__code_library_name__)]
        fpath = paths[0] if (len(paths) > 0) else None
    except:
        pass
    return fpath
def __hasVyperLogixLibraryLoaded():
    return __hasVyperLogixLibraryLoadedIn__(container=sys.path)
def hasVyperLogixLibraryLoadedIn(container=sys.path):
    bool = False
    try:
        bool = (__hasVyperLogixLibraryLoadedIn__(container=container) is not None)
    except:
        pass
    return bool
def hasVyperLogixLibraryLoaded():
    return hasVyperLogixLibraryLoadedIn(container=sys.path)
hasNotVyperLogixLibraryLoaded = not hasVyperLogixLibraryLoaded()

def getVyperLogixLibraryPath(top):
    for root, dirs, files in os.walk(top, topdown=True):
        fpath = __hasVyperLogixLibraryLoadedIn__(container=files)
        if (fpath is not None):
            return fpath
    return None

def containsVyperLogixLibrary(top):
    for root, dirs, files in os.walk(top, topdown=True):
        if (hasVyperLogixLibraryLoadedIn(container=files)):
            return True
    return False

seconds_per_hour = 60 * 60
seconds_per_day = seconds_per_hour * 24

isComputerAllowed = True

utf8 = lambda s:str(unicode(s).encode("utf-8"))

utf16 = lambda s:str(unicode(s).encode("utf-16"))

__invalid_dos_filename_chars__ = ['/','\\','?','%','*',':','|','"',"'",'>','<',' ','.']

ascii_only = lambda s:''.join([ch for ch in s if (ord(ch) >= 32) and (ord(ch) <= 127)])

ascii_valid_dos_filename_chars = lambda s:''.join([ch for ch in ascii_only(s) if (ch not in __invalid_dos_filename_chars__)])

alpha_numeric_only = lambda s:''.join([ch for ch in str(s) if (str(ch).isalnum())])

non_alpha_numeric_only = lambda s:''.join([ch for ch in str(s) if (not str(ch).isalnum())])

numerics_only = lambda s:''.join([ch for ch in str(s) if (str(ch).isdigit())])

numericals_only = lambda s:''.join([ch for ch in str(s) if (str(ch).isdigit()) or (ch in ['.'])])

quote_it = lambda arg:'"' if (not str(arg).isdigit()) and ( (not isinstance(arg,(list,tuple))) and (not lists.isDict(arg)) ) else ''

is_floating_digits = lambda s:(len(s.split('.')) == 2) and (all([len(t) == len(numerics_only(t)) for t in s.split('.')]))

__regex_valid_ip__ = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"

__regex_valid_ip_and_port__ = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):([0-9]{1,5})"

is_valid_ip = lambda value:ObjectTypeName.typeClassName(re.compile(__regex_valid_ip__, re.MULTILINE).match(value)) == '_sre.SRE_Match'

is_valid_ip_and_port = lambda value:ObjectTypeName.typeClassName(re.compile(__regex_valid_ip_and_port__, re.MULTILINE).match(value)) == '_sre.SRE_Match'

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

from vyperlogix.hash import lists
windows_modes = ['S_IREAD','S_IWRITE']
all_modes = lists.HashedLists({'S_ISUID':stat.S_ISUID,
                               'S_ISGID':stat.S_ISGID,
                               'S_ENFMT':stat.S_ENFMT,
                               'S_ISVTX':stat.S_ISVTX,
                               'S_IREAD':stat.S_IREAD,
                               'S_IWRITE':stat.S_IWRITE,
                               'S_IEXEC':stat.S_IEXEC,
                               'S_IRWXU':stat.S_IRWXU,
                               'S_IRUSR':stat.S_IRUSR,
                               'S_IWUSR':stat.S_IWUSR,
                               'S_IXUSR':stat.S_IXUSR,
                               'S_IRWXG':stat.S_IRWXG,
                               'S_IRGRP':stat.S_IRGRP,
                               'S_IWGRP':stat.S_IWGRP,
                               'S_IXGRP':stat.S_IXGRP,
                               'S_IRWXO':stat.S_IRWXO,
                               'S_IROTH':stat.S_IROTH,
                               'S_IWOTH':stat.S_IWOTH,
                               'S_IXOTH':stat.S_IXOTH
                               })
if (sys.platform == 'win32'):
    retire = set(all_modes.keys()) - set(windows_modes)
    for k in retire:
        del all_modes[k]
_all_modes = lists.HashedLists(all_modes.asDict(insideOut=True,isCopy=True))

windows_mask = 0
for item in windows_modes:
    v = all_modes[item]
    if (isinstance(v,list)):
        for _item in v:
            windows_mask |= _item
    else:
        windows_mask |= v

parse_key_value_pairs_as_dict = lambda params:lists.HashedLists2(dict([tuple(t) for t in [p.split('=') for p in params.split('\n') if (len(p) > 0)] if (len(t) == 2)]))

def is_x64():
    return 'PROGRAMFILES(X86)' in os.environ

def GetProgramFiles32():
    if is_x64():
        return os.environ['PROGRAMFILES(X86)']
    else:
        return os.environ['PROGRAMFILES']

def GetProgramFiles64():
    if is_x64():
        return os.environ['PROGRAMW6432']
    else:
        return None

is_x86 = not is_x64

def any_non_ascii(blob):
    for ch in blob:
        try:
            if (ord(ch) < 32) or (ord(ch) > 127):
                return True
        except:
            break
    return False

is_any_non_ascii = lambda s:any_non_ascii(s)

def utf_to_str(blob):
    try:
        return utf8(blob)
    except:
        try:
            return utf16(blob)
        except:
            pass
    return str(blob)

def _hex_ascii(blob,size=20,ascii_only=False):
    from vyperlogix.misc import hex_ascii
    io = hex_ascii.dumps(utf_to_str(blob),size=size,ascii_only=ascii_only)
    return io.getvalue()

def hex_ascii(blob,size=20,ascii_only=False):
    '''outout a traditional blob as a hex-ascii block of data - to be used when other methods (utf-8 or utf-16) fail'''
    return _hex_ascii(utf_to_str(blob), size=size, ascii_only=ascii_only)

def is_ip_address_valid(ip):
    '''127.0.0.1 is the general form of an IP address'''
    if (is_valid_ip(ip) or is_valid_ip_and_port(ip)):
	if (is_valid_ip_and_port(ip)):
	    toks1 = ip.split(':')
	    toks2 = toks1[0].split('.')
	    return (len(toks2) == 4) and all([str(n).isdigit() for n in list(tuple(toks2+[toks1[-1]]))])
	elif (is_valid_ip(ip)):
	    toks = ip.split('.')
	    return (len(toks) == 4) and all([str(n).isdigit() for n in toks])
    return False

def eat_leading_token_if_empty(url,delim='/'):
    toks = [t for t in url.split(delim) if (len(t) > 0)]
    return '/'.join(toks)

def get_dict_as_pairs(toks):
    try:
        from vyperlogix.iterators.iterutils import itergroup
        n = len(toks)
        i = int(n / 2) * 2
        d = lists.HashedLists2(dict([t for t in itergroup(toks[n-i:],2)]))
        if ((n % 2) != 0):
            d = lists.HashedLists2({toks[0]:lists.HashedLists2(d.asDict())})
        return d
    except:
        return lists.HashedLists2({})

def splits(s, seps):
    res = [s]
    for sep in seps:
        s, res = res, []
        for seq in s:
            res += seq.split(sep)
    return res

def asMessage(reason):
    from vyperlogix import misc
    return '(%s) %s.' % (misc.callersName(),reason)

def getVersionNumber():
    import sys
    return int(''.join(sys.version.split()[0].split('.')))

def cleanup_sqlautocode(fname):
    '''Cleans-up the sqlautocode process by removing all those "\r" chars that get in the way of consuming the code.'''
    from vyperlogix import misc
    fIn = open(fname,'r')
    ext = fname.split('.')[-1]
    fOut = open(fname.replace(ext,ext+'_bak'),'w')
    _count = 0
    try:
        while (1):
            l = fIn.readline()
            if (l == ''):
                break
            toks = l.split('\r')
            fOut.writelines([''.join(toks)])
            _count += 1
    finally:
        fOut.flush()
        fOut.close()
        fIn.close()
        print '%s :: Processed %d lines.' % (misc.funcName(),_count)
        os.remove(fIn.name)
        os.rename(fOut.name,fIn.name)
        print '%s :: Done !' % (misc.funcName())

def does_path_exist_conclusively(fpath):
    import re
    import os, sys
    import tempfile

    __re__ = re.compile(r"<DIR>\s*(?P<folder>\w*)", re.MULTILINE)

    __dirname__ = os.path.dirname(tempfile.NamedTemporaryFile().name)

    __is__ = False
    __fname__ = '%s\\test.txt' % (__dirname__)
    __cmd__ = 'dir "%s" > "%s" 2>&1' % (fpath,__fname__)
    os.system(__cmd__)
    content = readFileFrom(__fname__)
    __m__ = __re__.search(content)
    if (__m__):
	so = SmartObject(__m__.groupdict())
	if (fpath.find('%s%s'%(os.sep,so.folder))):
	    __is__ = True
    if (os.path.exists(__fname__)):
	os.remove(__fname__)
    return __is__

def safely_remove(fname_or_dirname):
    if (os.path.isdir(fname_or_dirname)):
        files = [os.sep.join([fname_or_dirname,f]) for f in os.listdir(fname_or_dirname)]
        for f in files:
            os.remove(f)
    else:
        if (os.path.exists(fname_or_dirname)):
            os.remove(fname_or_dirname)

def safely_mkdir(fpath='.',dirname='logs'):
    _path = os.path.abspath(os.sep.join([fpath,dirname]))
    if (not os.path.exists(_path)):
        try:
            os.mkdir(_path)
        except:
            os.makedirs(_path)
    return _path

def safely_mkdir_logs(fpath='.'):
    return safely_mkdir(fpath=fpath,dirname='logs')

def getFloatVersionNumber():
    import sys
    v = sys.version.split()[0].split('.')
    v.insert(1,'.')
    return float(eval(''.join(v)))

def getProgramName():
    return os.path.basename(sys.argv[0]).split('.')[0]

def getComputerName():
    import socket
    return socket.gethostbyname_ex(socket.gethostname())[0]

def isComputerAllowed(domain_name):
    '''domain_name is either a name (string) or list of names...'''
    from vyperlogix import misc
    global _isComputerAllowed
    domain_names = domain_name if (misc.isList(domain_name)) else [domain_name]
    cname = getComputerName().lower()
    _isComputerAllowed = (any([cname.find(c.lower()) > -1 for c in domain_names]))
    return _isComputerAllowed

def listify(maybe_list):
    """
    Ensure that input is a list, even if only a list of one item
    @maybeList: Item that shall join a list. If Item is a list, leave it alone
    """
    try:
        return list(maybe_list)
    except:
        return list(str(maybe_list))

    return maybe_list

def failUnlessEqual(first, second, msg=None):
    """Fail if the two objects are unequal as determined by the '=='
       operator.
    """
    if not first == second:
        raise AssertionError, (msg or '%r != %r' % (first, second))

def failIfEqual(first, second, msg=None):
    """Fail if the two objects are equal as determined by the '=='
       operator.
    """
    if first == second:
        raise AssertionError, (msg or '%r == %r' % (first, second))

def booleanize(data):
    return True if str(data).lower() in ['true','1','yes'] else False

def environ_copy():
    _env = {}
    for k,v in os.environ.iteritems():
        _env[k] = v
    return _env

def expandEnvMacro(p):
    toks = p.split(os.sep)
    _toks = []
    for t in toks:
        if (t.startswith('%') and t.endswith('%')):
            _t = t.replace('%','')
            if (os.environ.has_key(_t)):
                t = os.environ[_t]
        _toks.append(t)
    return os.sep.join(_toks)

def homeFolder():
    """ home folder for current user """
    f = os.path.abspath(os.curdir)
    toks = f.split(os.sep)
    if (sys.platform == 'win32'):
        t = toks[0:2]
    else:
        t = toks[0:3]
    return os.sep.join(t)

def containsSvnFolders(top):
    import re
    svn_regex = re.compile('[._]svn')
    for root, dirs, files in os.walk(top, topdown=True):
        if (svn_regex.search(root)):
            return True
    return False

def _searchForFileOrFolderNamed(fname,top='/',isFile=False,callback=None,options=FileFolderSearchOptions.none):
    """ Search for a folder of a specific name """
    import re
    _target = '.'+fname.split('.')[-1]
    svn_regex = re.compile('[._]svn')
    for root, dirs, files in os.walk(top, topdown=True):
        if (options.value & FileFolderSearchOptions.skip_svn.value) and (svn_regex.search(root)):
            continue
        if (options.value & FileFolderSearchOptions.callback_folders.value) and (callable(callback)):
            try:
                callback(root)
            except Exception, details:
                import sys
                print >>sys.stderr, formattedException(details=details)
        if (not isFile):
            if (fname in dirs):
                return os.sep.join([root,fname])
        else:
            if (fname in files):
                return os.sep.join([root,fname])
            elif (fname.startswith('*.')):
                for f in files:
                    if (options.value & FileFolderSearchOptions.callback_files.value) and (callable(callback)):
                        try:
                            callback(root, files)
                        except Exception, details:
                            import sys
                            print >>sys.stderr, formattedException(details=details)
                    if (f.endswith(_target)):
                        return os.sep.join([root,f])
    return ''

def searchForFolderNamed(fname,top='/',callback=None,options=FileFolderSearchOptions.none):
    """ Search for a folder of a specific name """
    return _searchForFileOrFolderNamed(fname,top,False,callback=None,options=options)

def searchForFileNamed(fname,top='/',callback=None,options=FileFolderSearchOptions.none):
    """ Search for a folder of a specific name, fname can contain '*.typ' to search for a file based on a wildcard. """
    return _searchForFileOrFolderNamed(fname,top,True,callback=callback,options=options)

def formatDate_YYYY():
    return '%Y'

def formatDate_MMYYYY():
    return '%m-%Y'

def formatDate_YYYYMMDD_dashes():
    return '%Y-%m-%d'

def formatDate_MMDDYYYY_dashes():
    return '%m-%d-%Y'

def formatDate_MMDDYYYY_slashes():
    return '%m/%d/%Y'

def formatTimeStr():
    return '%Y-%m-%dT%H:%M:%S.000Z'

def formatApacheDateTimeStr():
    return '%d/%b/%Y:%H:%M:%S'

def formatSimpleTimeStr():
    return '%H:%M:%S'

def formatSimpleTime12Str():
    return '%I:%M:%S'

def formatAMPMStr():
    return '%p'

def formatAmazonS3DateTimeStr():
    return '%s %s %s' % (formatDate_MMDDYYYY_slashes(),formatSimpleTimeStr(),formatAMPMStr())

def formatAmazonS3DateTime12Str():
    return '%s %s %s' % (formatDate_MMDDYYYY_slashes(),formatSimpleTime12Str(),formatAMPMStr())

def _formatTimeStr():
    return '%Y-%m-%dT%H:%M:%S'

def _formatShortTimeStr():
    return '%Y-%m-%dT%H:%M'

def formatSalesForceTimeStr():
    return '%Y-%m-%dT%H:%M:%S'

def format_mySQL_DateTimeStr():
    '''2008-11-28 09:52:00'''
    return '%Y-%m-%d %H:%M:%S'

def format_PHPDateTimeStr():
    '''11.28.2008 09:52:00'''
    return '%m.%d.%Y %H:%M:%S'

def formatDjangoDateTimeStr():
    '''01 May 2009 15:26:41 GMT'''
    return u"%d %b %Y %H:%M:%S %Z"

def formatSalesForceDateStr():
    return '%Y-%m-%d'

def formatMySQLDateTimeStr():
    return '%d-%b-%Y %H:%M:%S'

def formatSalesForceDateTimeStr():
    return '%d-%b-%Y %H:%M:%S'

def formatShortDateTimeStr():
    '''Jun 12 04:41'''
    return '%b %d %y %I:%M'

def formatShortDateStr():
    '''Jun 12 2008'''
    return '%b %d %y'

def formatShortBlogDateStr():
    '''Wed, 12 Jun 2008'''
    return '%A, %d %B %Y'

def formatSimpleBlogTimeStr():
    return '%I:%M %p'

def formatMetaHeaderExpiresOn():
    return '%a, %d %b %Y %H:%M:%S'

def formatMetaHeaderExpiresOnZ():
    return '%a, %d %b %Y %H:%M:%S %Z'

def reformatSalesForceTimeStr(sTime):
    toks = sTime.split('T')
    toks[-1] = toks[-1].split('.')[0]
    return "%sT%s.000Z" % tuple(toks) # yyyy-MM-ddTHH:mm:ss.SSSZ

def getDatetimeFromApexDatetime(value):
    try:
        return getFromDateTimeStr(value.isoformat().split('+')[0],formatSalesForceTimeStr())
    except:
        pass
    return value

def getSimpleDateFromApexDatetime(value):
    try:
        return value.isoformat().split('+')[0].split('T')[0]
    except:
        pass
    return value

def reformatSalesForceDateStrAsMMDDYYYY(sDate,useSlashes=True):
    from vyperlogix import misc
    sDate = sDate if (misc.isString(sDate)) else str(sDate)
    ts = getFromDateTimeStr(sDate,format=formatSalesForceDateStr())
    _fmt = formatDate_MMDDYYYY_slashes if (useSlashes) else formatDate_MMDDYYYY_dashes
    return getAsSimpleDateStr(ts,fmt=_fmt())

def parms_dict_from_url(s_url):
    '''This function converts a URL that has parms to the right of the "?" into a dict.'''
    try:
        return lists.HashedLists2(dict([tuple(t.split('=')) for t in s_url.split('?')[-1].split('&')]))
    except ValueError, details:
        return lists.HashedLists2()

def parse_parms_from_url(url):
    '''This function converts a URL that has parms to the right of the "?" into a dict.'''
    return parms_dict_from_url(url)

def parse_url_parms(parms):
    from vyperlogix.iterators import iterutils

    items = [t for t in parms.split('?')[-1].split('=')]
    return SmartObject(dict([n for n in iterutils.itergroup(items,2)]))

def utcDelta():
    import datetime, time
    _uts = datetime.datetime.utcfromtimestamp(time.time())
    _ts = datetime.datetime.fromtimestamp(time.time())
    # This time conversion fails under Linux for some odd reason so let's just stick with UTC when this happens.
    _zero = datetime.timedelta(0)
    return _zero if (isNotUsingLocalTimeConversions) else (_uts - _ts if (_uts > _ts) else _ts - _uts)

def localFromUTC(utc):
    d = utcDelta()
    return utc - d

def timeDeltaAsSeconds(td):
    from datetime import timedelta
    if (isinstance(td,timedelta)):
        return float(td.seconds) + float(td.days * 86400) + (float(td.microseconds) / (10**6))
    else:
        logging.warning('Unable to convert timedelta to seconds due to type mismatch, type "%s" should be "%s".' % (type(td),timedelta))
    return -1

def timeDeltaAsReadable(td):
    from vyperlogix import misc
    from datetime import timedelta
    if (isinstance(td,timedelta)):
        secs = timeDeltaAsSeconds(td)
        x = secs / 86400
        days = int(x)
        x = (x - days) * 86400
        x = x / 3660
        hours = int(x)
        x = (x - hours) * 3660
        x = x / 60
        mins = int(x)
        x = (x - mins) * 60
        secs = int(x)
        d = '%d days ' % (days)
        return '%s%d hour%s %d minute%s %d second%s' % (d if (days > 0) else '',hours,'s' if (hours > 1) else '',mins,'s' if (mins > 1) else '',secs,'s' if (secs > 1) else '')
    else:
        logging.warning('Unable to use timedelta due to type mismatch, type "%s" should be "%s".' % (type(td),timedelta))
    return str(td)

def getFromApexDateTime(apex_date_time,fmt=formatSalesForceDateTimeStr()):
    dt = getFromSalesForceDateTimeStr(str(apex_date_time))
    dt = localFromUTC(dt)
    return getAsDateTimeStr(dt,fmt=fmt)

def getFromDateTimeStr(ts,format=_formatTimeStr()):
    from datetime import datetime
    try:
        return datetime.strptime(ts,format)
    except ValueError:
        return datetime.strptime('.'.join(ts.split('.')[0:-1]),format)

def getFromDateStr(ts,format=_formatTimeStr()):
    return getFromDateTimeStr(ts,format=format)

def getFromSimpleDateStr(ts):
    _fmt = formatDate_MMDDYYYY_dashes() if (ts.find('-') > -1) else formatDate_MMDDYYYY_slashes()
    return getFromDateTimeStr(ts,format=_fmt).date()

def getFromSalesForceDateStr(ts):
    _fmt = formatSalesForceTimeStr()
    return getFromDateTimeStr(ts.split('+')[0],format=_fmt).date()

def getFromSalesForceDateTimeStr(ts):
    _fmt = formatSalesForceTimeStr()
    return getFromDateTimeStr(ts.split('+')[0],format=_fmt)

def days_timedelta(num_days=0):
    import datetime
    return datetime.timedelta(num_days)

def strip_time_from_datetime(dt):
    '''Normalizes the datetime to be the date beginning at midnight.'''
    import datetime
    tm = dt.time()
    delta = datetime.timedelta(days=0, hours=tm.hour, minutes=tm.minute, seconds=tm.second)
    return (dt - delta)

def today_localtime(_timedelta=None,begin_at_midnight=False):
    dt = getFromNativeTimeStamp(timeStampLocalTime())
    begin_at_midnight = False if (not isinstance(begin_at_midnight,bool)) else begin_at_midnight
    if (begin_at_midnight):
        dt = strip_time_from_datetime(dt)
    try:
        if (_timedelta is not None):
            return dt - _timedelta
    except Exception, details:
        info_string = formattedException(details=details)
        print >>sys.stderr, info_string
    return dt

def datetime_as_seconds(dt):
    import time
    return time.mktime(dt.timetuple())

def utc_datetime_as_seconds(now=None):
    import datetime
    now = datetime.datetime.utcnow() if (now is None) else now
    return datetime_as_seconds(now)

def today_localtime_as_seconds():
    ts = today_localtime()
    return datetime_as_seconds(ts)

def today_utctime():
    import datetime
    ts = today_localtime_as_seconds()
    _uts = datetime_as_seconds(datetime.datetime.utcfromtimestamp(ts))
    tstamp = getAsDateTimeStrFromTimeSeconds(_uts)
    return getFromNativeTimeStamp(tstamp,format=_formatTimeStr())

def todayForSalesForce_localtime(_timedelta=None,begin_at_midnight=False):
    '''begin_at_midnight = True when the goal is to make the date begin at midnight otherwise the local time is used.'''
    dt = today_localtime(_timedelta=_timedelta,begin_at_midnight=begin_at_midnight)
    return reformatSalesForceTimeStr(dt.isoformat())

def truncate_if_necessary(s,max_width=40):
    if (max_width > -1):
        elipsis = '...'
        l_elipsis = len(elipsis)
        normalized_width = max_width - l_elipsis
        is_truncating = s > normalized_width
        return s[0:normalized_width].replace(elipsis,'') + '...' if (is_truncating) else ''
    return s

def isStrDate(ts,format=formatSalesForceDateStr()):
    try:
        dt = getFromDateTimeStr(ts,format=format)
        return True
    except ValueError:
        pass
    return False

def getAsSimpleDateStr(dt,fmt=formatDate_MMDDYYYY_slashes()):
    return dt.strftime(fmt)

def getAsDateTimeStr(value, offset=0,fmt=_formatTimeStr()):
    """ return time as 2004-01-10T00:13:50.000Z """
    import sys,time
    import types
    from datetime import datetime

    strTypes = (types.StringType, types.UnicodeType)
    numTypes = (types.LongType, types.FloatType, types.IntType)
    if (not isinstance(offset,strTypes)):
        if isinstance(value, (types.TupleType, time.struct_time)):
            return time.strftime(fmt, value)
        if isinstance(value, numTypes):
            secs = time.gmtime(value+offset)
            return time.strftime(fmt, secs)

        if isinstance(value, strTypes):
            try: 
                value = time.strptime(value, fmt)
                return time.strftime(fmt, value)
            except Exception, details: 
                info_string = formattedException(details=details)
                print >>sys.stderr, 'ERROR :: getDateTimeTuple Could not parse "%s".\n%s' % (value,info_string)
                secs = time.gmtime(time.time()+offset)
                return time.strftime(fmt, secs)
        elif (isinstance(value,datetime)):
            from datetime import timedelta
            if (offset is not None):
                value += timedelta(offset)
            ts = time.strftime(fmt, value.timetuple())
            return ts
    else:
        print >>sys.stderr, 'ERROR :: offset must be a numeric type rather than string type.'
# END getAsDateTimeStr

def getDayOfYear(dt):
    try:
        return int(dt.strftime("%j"))
    except:
        return -1

def getWeekday(dt):
    try:
        return int(dt.strftime("%w"))
    except:
        return -1

def getWeekdayName(dt):
    try:
        return dt.strftime("%a")
    except:
        return ''

def getFullWeekdayName(dt):
    try:
        return dt.strftime("%A")
    except:
        return ''

def getMonthName(dt):
    try:
        return dt.strftime("%B")
    except:
        return ''

def isWorkWeekDay(dt):
    return (getWeekday(dt) not in [0,6])

def time_to_secs(s):
    hms = s.split(":")     # [hh, mm, ss]
    secs = 0
    for t in hms[0:3]:
        secs = secs * 60 + int(t)
    return secs

def secs_to_time(secs):
    hms = ['00','00','00']
    while secs:
        hms.append('%02d' % (secs % 60))
        secs = secs // 60
    return ":".join(hms[(len(hms)-3):])

def timeSeconds(month=-1,day=-1,year=-1,format=formatSalesForceTimeStr()):
    """ get number of seconds """
    import time, datetime
    fromSecs = datetime.datetime.fromtimestamp(time.time())
    s = getAsDateTimeStr(fromSecs,fmt=format)
    _toks = s.split('T')
    toks = _toks[0].split('-')
    if (month > -1):
        toks[0] = '%02d' % (month)
    if (day > -1):
        toks[1] = '%02d' % (day)
    if (year > -1):
        toks[-1] = '%04d' % (year)
    _toks[0] = '-'.join(toks)
    s = 'T'.join(_toks)
    fromSecs = getFromDateStr(s,format=format)
    return time.mktime(fromSecs.timetuple())

def dateTime(month=-1,day=-1,year=-1,format=formatSalesForceTimeStr()):
    """ dateTime from month,day,time """
    import time, datetime
    fromSecs = datetime.datetime.fromtimestamp(time.time())
    s = getAsDateTimeStr(fromSecs,fmt=format)
    _toks = s.split('T')
    toks = _toks[0].split('-')
    if (month > -1):
        toks[0] = '%02d' % (month)
    if (day > -1):
        toks[1] = '%02d' % (day)
    if (year > -1):
        toks[-1] = '%04d' % (year)
    _toks[0] = '-'.join(toks)
    s = 'T'.join(_toks)
    return getFromDateStr(s,format=format)

def daysInMonth(month=-1,year=-1,format=formatSalesForceTimeStr()):
    """ days in Month """
    import datetime, time
    dt = dateTime(month=month+1,day=1,year=year,format=formatDate_MMDDYYYY_dashes())
    _minus1 = datetime.timedelta(-1)
    dt += _minus1
    return dt.day

def _day_of_week(_date=None):
    from datetime import date
    return date.weekday(date.today() if (not misc.isDate(_date)) else _date)

def day_of_week():
    dow = _day_of_week()
    return DaysOfWeek(dow)

def days_of_week(func=None):
    if (not callable(func)):
        func = lambda item:item
    return [func(item) for item in DaysOfWeek._items_]

def hour_of_day():
    import time
    return time.localtime()[3]

def days_range(spec):
    from vyperlogix.lists.ListWrapper import ListWrapper
    normalize = lambda name,num:str(name).capitalize()[0:num] if (misc.isString(name)) else name
    _days_ = misc.sortCopy(dict([(i,i) for i in list(set(days_of_week(func=lambda item:item.value)))]).keys())
    toks = spec.split('-')
    n = max(len(toks[0]),len(toks[-1]))
    days = ListWrapper([normalize(DaysOfWeek(i).name,n) for i in _days_])
    dowFirst = days.findFirstMatching(toks[0],callback=lambda name,s_search:normalize(name,n) == s_search,returnIndexes=True)
    dowLast = days.findFirstMatching(toks[-1],callback=lambda name,s_search:normalize(name,n) == s_search,returnIndexes=True)
    return [i for i in _days_[dowFirst:dowLast+1]]

def day_in_range(spec,dow):
    _r_ = days_range(spec)
    return dow in _r_

def hours_range(spec):
    from vyperlogix.lists.ListWrapper import ListWrapper
    normalize = lambda value:int(numerics_only(str(value)))
    spec = '0-23' if (spec == '*') else spec
    toks = [normalize(i) for i in spec.split('-')]
    return [i for i in xrange(toks[0],toks[-1])]

def timeSecondsFromTimeStamp(ts):
    """ get number of seconds """
    import time
    return time.mktime(ts.timetuple())

def timeStamp(tsecs=0,format=_formatTimeStr(),useLocalTime=isUsingLocalTimeConversions):
    """ get standard timestamp """
    useLocalTime = isUsingLocalTimeConversions if (not isinstance(useLocalTime,bool)) else useLocalTime
    secs = 0 if (not useLocalTime) else -utcDelta().seconds
    tsecs = tsecs if (tsecs > 0) else timeSeconds()
    t = tsecs+secs
    return getAsDateTimeStr(t if (tsecs > abs(secs)) else tsecs,fmt=format)

def getAsDateTimeStrFromTimeSeconds(secs,useLocalTime=isUsingLocalTimeConversions):
    return timeStamp(tsecs=secs,useLocalTime=useLocalTime)

def dateFromSeconds(ts,format=_formatTimeStr(),useLocalTime=isUsingLocalTimeConversions):
    useLocalTime = isUsingLocalTimeConversions if (not isinstance(useLocalTime,bool)) else useLocalTime
    ts = timeStamp(tsecs=ts,format=format,useLocalTime=useLocalTime)
    return getFromDateTimeStr(ts)

def timeStampForFileName(format=_formatTimeStr(),useLocalTime=isUsingLocalTimeConversions,delimiters=('_','')):
    ''' delimiters is a tuple that contains the replacement for 'T' and replacement for ':' in that order. '''
    import sys
    from vyperlogix import misc
    try:
        delimiters = delimiters if (isinstance(delimiters,tuple)) and (len(delimiters) == 2) else (delimiters,'')
        if (':' not in delimiters):
            useLocalTime = isUsingLocalTimeConversions if (not isinstance(useLocalTime,bool)) else useLocalTime
            return timeStamp(format=format,useLocalTime=useLocalTime).replace('T',delimiters[0]).replace(':',delimiters[-1])
        else:
            print >>sys.stderr, '%s :: Invalid use of delimiters parameter, cannot use ":" as a delimiter, double-check your work.' % (misc.funcName())
    except:
        print >>sys.stderr, '%s :: Invalid use of parameters, double-check your work.' % (misc.funcName())
    return None

def only_float_digits(aString):
    aString = str(aString)
    return ''.join([ch for ch in aString if (ch.isdigit()) or (ch in ['.','+','-'])])

def _float(aString):
    aString = only_float_digits(aString)
    return float(aString)

def only_digits(aString):
    aString = str(aString)
    return ''.join([ch for ch in aString if (ch.isdigit())])

def _int(aString):
    aString = only_digits(aString)
    return int(aString)

def isTimeStamp(ts):
    tests = [str(t).isdigit() or (t in ['_','-']) for t in ts]
    return (all(tests))

def isTimeStampForFileName(ts):
    return isTimeStamp(ts)

def isNativeTimeStamp(ts):
    tests = [str(t).isdigit() or (t in ['-','T',':']) for t in ts]
    return (all(tests))

def isNativeTimeStampForFileName(ts):
    return isNativeTimeStamp(ts)

def getFromNativeTimeStamp(ts,format=None):
    format = _formatTimeStr() if (format is None) else format
    if (':' not in ts):
        format = format.replace(':','')
    if ('T' not in ts):
        format = format.split('T')[0]
    return getFromDateTimeStr(ts,format=format)

def getFromTimeStampForFileName(ts):
    if (isTimeStampForFileName(ts)):
        toks = ts.split('_')
        t = toks[1:]
        if (len(t) == 1):
            tt = []
            for i in xrange(0,len(t[0]),2):
                tt.append(t[0][i:i+2])
            t = tt
        _ts = toks[0:1][0] + 'T' + ':'.join(t)
        return getFromDateTimeStr(_ts)
    elif (isNativeTimeStampForFileName(ts)):
        return getFromNativeTimeStamp(ts)
    else:
        return None

def isSometimeToday(ts):
    '''ts is a timeStamp in the form of a datetime object'''
    from vyperlogix import misc
    today = getFromNativeTimeStamp(timeStamp().split('T')[0])
    format = _formatTimeStr().split('T')[0]
    mm_dd_yyyy = getAsDateTimeStr(today,fmt=format)
    if (misc.isString(ts)):
        if (isNativeTimeStamp(ts)):
            other_day = getFromNativeTimeStamp(ts.split('T')[0])
        elif (isTimeStamp(ts)):
            other_day = getFromNativeTimeStamp(ts.split('_')[0])
        else:
            print >>sys.stderr, '(%s) :: Unknown format for "%s".' % (misc.funcName(),ts)
    else:
        other_day = ts
    other_mm_dd_yyyy = getAsDateTimeStr(other_day,fmt=format)
    return mm_dd_yyyy == other_mm_dd_yyyy

def timeStampLocalTime(tsecs=0,format=_formatTimeStr()):
    """ get standard timestamp adjusted to local time """
    return timeStamp(tsecs=tsecs,format=format,useLocalTime=isUsingLocalTimeConversions)

def timeStampLocalTimeForFileName(format=_formatTimeStr(),delimiters=('_','')):
    ''' delimiters is a tuple that contains the replacement for 'T' and replacement for ':' in that order. '''
    return timeStampForFileName(format=format,useLocalTime=isUsingLocalTimeConversions,delimiters=delimiters)

def timeStampSalesForce(offset_secs=None):
    """ get sales force timestamp using UTC """
    is_offset_secs_invalid = False
    if (offset_secs is not None):
        try:
            v = eval('%s' % (offset_secs))
        except ValueError:
            is_offset_secs_invalid = True
    return timeStamp(tsecs=timeSeconds() + (0 if (offset_secs is None) or (is_offset_secs_invalid) else offset_secs),format=formatSalesForceTimeStr(),useLocalTime=False)

def timeStampSimple(format=formatDate_MMDDYYYY_slashes(),useLocalTime=False):
    """ get simple timestamp using UTC """
    return timeStamp(tsecs=timeSeconds(),format=format,useLocalTime=useLocalTime)

def timeStampApache(useLocalTime=True):
    return timeStampSimple(format=formatApacheDateTimeStr(),useLocalTime=useLocalTime) + ' %04d' % ((utcDelta().seconds / 3600) * 100)

def timeStampMySQL(useLocalTime=True):
    return timeStampSimple(format=formatMySQLDateTimeStr(),useLocalTime=useLocalTime)

def callersContext():
    """ get context of caller of a function """
    import sys
    return sys._getframe(2).f_code

def logPrint(s):
    """ log a line to a file """
    from vyperlogix import misc
    if (sys.platform == 'win32'):
        logPath = 'log'
    else:
        logPath = searchForFolderNamed('log',homeFolder())
    tstamp = timeStamp()
    folder = ''.join(tstamp.split('T')[0]).replace(':','-').replace('.','_')
    if (os.path.exists(logPath) == False):
        os.mkdir(logPath)
    logPath = os.sep.join([logPath,'details'])
    if (os.path.exists(logPath) == False):
        os.mkdir(logPath)
    logPath = os.sep.join([logPath,folder])
    if (os.path.exists(logPath) == False):
        os.mkdir(logPath)
    logFile = '%s.log' % (os.sep.join([logPath,sys.argv[0].split(os.sep)[-1]]).replace('.','_'))
    fOut = open(logFile,'a')
    fOut.write('%s::%s -- %s\n' % (tstamp,misc.callersName(),s))
    fOut.flush()
    fOut.close()
# END logPrint

def read_lines_simple(aFileName,mode):
    fIn = open(aFileName,mode)
    try:
        lines = [line.strip() for line in fIn.readlines() if (len(line.strip()) > 0)]
    finally:
        fIn.close()
    return lines

def _readFileFrom(fname,mode='r'):
    '''read-raw and return the lines via a list'''
    fIn = open(fname,mode)
    try:
        lines = fIn.readlines()
        return lines
    finally:
        fIn.close()
    return []

def readFileFrom(fname,mode='r',noCRs=False):
    '''mode='rb' then noCRs is not used otherwise the content is treated like text with line delimiters'''
    fIn = open(fname,mode)
    try:
        if (mode.find('b') == -1):
            lines = fIn.readlines()
            ch = '' if (noCRs) else '\n'
            if (noCRs):
                lines = [l.strip() for l in lines]
            data = ch.join(lines)
        else:
            data = fIn.read()
    finally:
        fIn.close()
    return data

def readFileFromGenerator(fname,mode='r'):
    '''mode='rb' then noCRs is not used otherwise the content is treated like text with line delimiters'''
    fIn = open(fname,mode)
    try:
        if (mode.find('b') == -1):
	    line = '<top>'
	    while (misc.isStringValid(line)):
		line = fIn.readline()
		if (misc.isStringValid(line)):
		    yield line
		else:
		    break
        else:
            yield fIn.read()
    finally:
        fIn.close()

def readBinaryFileFrom(fname):
    return readFileFrom(fname,mode='rb')

def writeFileFrom(fname,contents,mode='w'):
    dname = os.path.dirname(fname)
    safely_mkdir(fpath=dname,dirname='')
    fOut = open(fname,mode)
    try:
        fOut.write(contents)
    finally:
        fOut.flush()
        fOut.close()

def filesAsDict(top,deBias=False,asZip=False):
    import re
    svn_regex = re.compile('[._]svn')
    d = lists.HashedLists2()
    for root, dirs, files in walk(top, topdown=True, rejecting_re=svn_regex):
        for f in files:
            _fname = os.sep.join([root,f])
            if (deBias):
                _fname = _fname.replace(top,'')
            if (asZip):
                _fname = '/'.join([t for t in _fname.replace(os.sep,'/').split('/') if (len(t) > 0)])
            d[_fname] = _fname
    return d

def analysisFromFilesDict(d):
    '''Performs a detailed analysis to determine the common parts of all the file paths.
    Useful in determining the bias of a heap of paths.
    The bias is that which appears in all the files equally.
    Knowing the bias can help us compare the contents of a zip file with the contents of a folder tree on a file-by-file basis.
    '''
    d_analysis = lists.HashedLists()
    for k,v in d.iteritems():
        toks = k.split(os.sep)
        bias = []
        for t in toks[0:-1]:
            bias.append(t)
            d_analysis[os.sep.join(bias)] = v
    to_be_retired = []
    for k,v in d_analysis.iteritems():
        if (not all([(kk.find(k) > -1) for kk in d_analysis.keys()])):
            to_be_retired.append(k)
    return d_analysis

__is_numerical__ = lambda item:len(only_digits(str(item))) == len(str(item))

def _noSQLComments(fname):
    import re
    _re_ = re.compile(r"('(''|[^'])*')|[\t\r\n]|(--[^\r\n]*)|(/\*[\w\W]*?(?=\*/)\*/)", re.MULTILINE)
    if (os.path.exists(fname)):
        _bytes = readBinaryFileFrom(fname)
        _matches_ = [m for m in _re_.finditer(_bytes)]
        if (len(_matches_) > 0):
            _toks = list(os.path.splitext(fname))
            _toks_ = misc.copy(_toks)
            _toks_[0] += '-original'
            _fname = ''.join(_toks_)
            if (not isBeingDebugged):
                copyFile(fname,_fname)
            _toks_ = misc.copy(_toks)
            _toks_[0] += '-comments'
            _fnameComments = ''.join(_toks_)
        _comments_ = []
        while (len(_matches_) > 0):
            _m_ = _matches_.pop()
            _start_ = _m_.start()
            _end_ = _m_.end()
            _s_ = _bytes[_start_:_end_]
            _s1_ = _s_.find('/*')
            _s2_ = _s_.find('*/')
            _s3_ = _s_.find('--')
            if (_s_.isspace()) or ((_s1_ > -1) and (_s2_ > -1) and (_s1_ < _s2_)) or (_s3_ > -1):
                _comments_.insert(0,_s_)
                _bytes = (_bytes[0:_start_] if (_start_ > 0) else '') + _bytes[_end_:]
        writeFileFrom(_fnameComments,''.join(_comments_))
        writeFileFrom(_fname,_bytes)

def _crc32(fname,crc=None):
    import binascii
    _crc = crc if (__is_numerical__(crc)) else 0
    if (os.path.exists(fname)):
        _bytes = readBinaryFileFrom(fname)
        _crc = binascii.crc32(_bytes,_crc)
    return _crc

def crc32(top, isVerbose=False, isObfuscated=False):
    '''Walk the files and compute the crc from the bytes in the files...'''
    from vyperlogix.products import keys
    crc = 0
    for root, dirs, files in walk(top, topdown=True, rejecting_re=None):
        for f in files:
            _fname = os.sep.join([root,f])
            if (isVerbose):
                print '%s' % (_fname)
            crc = _crc32(_fname)
    return crc if (not isObfuscated) else keys._encode('%d' % (crc))

def stringIO(*args, **kwargs):
    try:
        from cStringIO import StringIO as StringIO
    except ImportError:
        try:
            from StringIO import StringIO as StringIO
        except ImportError:
            pass
    return StringIO(*args, **kwargs)

__symbol_InternetShortcut__ = '[InternetShortcut]'

def parse_InternetShortcut(fname):
    _url = ''
    if (fname.lower().endswith('.url')):
        if (os.path.exists(fname)):
            fIn = open(fname, 'rb')
            try:
                bytes = fIn.read()
            finally:
                fIn.close()
            l_bytes = bytes.split('\r\n')
            if (l_bytes[0] == __symbol_InternetShortcut__):
                toks = ''.join(l_bytes[1:]).split('=')
                toks = ''.join(toks[1:]).split('http://')
                _url = ','.join(['http://%s' % (t) for t in toks])
    return _url

def formattedException(details='',depth=None,delims='\n'):
    from vyperlogix import misc
    return misc.formattedException(details=details,_callersName=misc.callersName(),depth=depth,delims=delims)

def spawnProcessWithDetails(progPath,env=None,shell=False,fOut=None,pWait=True):
    """ spawn a background process with environment and shell options, when pWait is False the process object is returned """
    import subprocess
    import logging

    try:
        if (not fOut):
            _details_symbol = os.path.abspath('@details')
            if (not os.path.exists(_details_symbol)):
                os.mkdir(_details_symbol)
            _fOut = open('%s_%s.txt' % (os.sep.join([_details_symbol,'.'.join(timeStamp().replace(':','').split('.')[0:-1])]),os.path.basename(progPath).replace('.','_')),'w')
            logFname = _fOut.name
        elif (os.path.isdir(fOut)):
            _details_symbol = os.path.abspath(fOut)
            _fOut = open('%s_%s.txt' % (os.sep.join([_details_symbol,'.'.join(timeStamp().replace(':','').split('.')[0:-1])]),os.path.basename(progPath).replace('.','_')),'w')
            logFname = _fOut.name
        else:
            _fOut = fOut
    except:
        _fOut = fOut
    e = os.environ if env == None else env
    _isError = False
    _details = ''
    try:
        p = subprocess.Popen([progPath], env=e, stdout=_fOut, shell=shell)
        if (pWait):
            p.wait()
        else:
            return p
    except Exception, details:
        from vyperlogix import misc
        _isError = True
        _details = misc.formattedException(details=details)
        logging.warning('ERROR in "%s" caused "%s".' % (progPath,_details))
    if (_fOut != fOut):
        _fOut.flush()
        _fOut.close()
        if (not _isError):
            _details = readFileFrom(logFname)
        if (os.path.exists(logFname)):
            try:
                os.remove(logFname)
            except Exception, details:
                from vyperlogix import misc
                _details = misc.formattedException(details=details)
                logging.warning('WARNING :: Unable to remove the "%s" file in "%s" due to a Windows Error which is "%s".' % (logFname,_details_symbol,details))
        if (os.path.exists(_details_symbol)):
            try:
                os.rmdir(_details_symbol)
            except Exception, details:
                from vyperlogix import misc
                _details = misc.formattedException(details=details)
                logging.warning('WARNING :: Unable to remove the "%s" folder in "%s" due to a Windows Error which is "%s".' % (logFname,os.curdir,details))
    return _details

def expandInSubstr(t,args={}):
    """ expand all occurences of a macro bounded by %item% with a value from the dict passed via args """
    x = 0
    while (x > -1):
        x = t.find('%')
        if (x > -1):
            y = t[x+1:].find('%')
            if (y > -1):
                xx = t[x+1:x+y+1]
                if (args.has_key(xx)):
                    _t = args[xx]
                    t = t.replace('%'+xx+'%',_t)
                    x = y+1
    return t

def expandMacro(p,args={}):
    """ expand a macro bounded by %item% with a value from the dict passed via args """
    toks = p.split(',')
    _toks = []
    for t in toks:
        if (t.startswith('%') and t.endswith('%')):
            _t = t.replace('%','')
            if (args.has_key(_t)):
                t = args[_t]
        else:
            t = expandInSubstr(t,args)
        _toks.append(t)
    return _toks

def args(*args,**kwargs):
    kw = []
    for k,v in kwargs.iteritems():
        q = quote_it(v)
        kw.append('%s=%s%s%s' % (k,q,v,q))
    value = '%s%s%s' % (','.join(['%s%s%s' % (quote_it(arg),arg,quote_it(arg)) for arg in args]),',' if (len(args) > 0) and (len(kw) > 0) else '',','.join(kw))
    return value

def walk(top, topdown=True, onerror=None, rejecting_re=None):
    from vyperlogix.misc import ObjectTypeName

    isRejectingRe = ObjectTypeName.typeClassName(rejecting_re) == '_sre.SRE_Pattern'

    try:
        names = [n for n in os.listdir(top) if (not isRejectingRe) or (isRejectingRe and not rejecting_re.search(n))]
    except os.error, err:
        if onerror is not None:
            onerror(err)
        return

    dirs, nondirs = [], []
    for name in names:
        if os.path.isdir(os.path.join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    if topdown:
        yield top, dirs, nondirs
    for name in dirs:
        path = os.path.join(top, name)
        if not os.path.islink(path):
            for x in walk(path, topdown, onerror, rejecting_re):
                yield x
    if not topdown:
        yield top, dirs, nondirs

def get_allfiles_from(fpath,callback=None,topdown=True,followlinks=True):
    import os
    allfiles = []
    for top,dirs,files in os.walk(fpath,topdown=topdown,followlinks=followlinks):
        for f in files:
            try:
                if (callable(callback) and (callback(top,dirs,f))):
                    allfiles.append(os.path.join(top,f))
            except Exception, ex:
                print formattedException(details=ex)
    return allfiles

def removeAllFilesUnder(top,rejecting_re=None,matching_re=None):
    """ remove all files under top including folders """
    from vyperlogix.misc import ObjectTypeName
    isMatchingRe = ObjectTypeName.typeClassName(matching_re) == '_sre.SRE_Pattern'
    for root, dirs, files in walk(top, topdown=False, rejecting_re=rejecting_re):
        for f in files:
            _fname = os.sep.join([root,f])
            if (not isMatchingRe):
                os.remove(_fname)
            elif (isMatchingRe) and (matching_re.search(_fname)):
                os.remove(_fname)
        if (not isMatchingRe) and (os.path.exists(root)) and (os.listdir(root) == []):
            try:
                os.rmdir(root)
            except Exception as details:
                print 'ERROR due to %s' % details
                pass

def handleAllFilesUnder(top,callback,rejecting_re=None,matching_re=None):
    """ handle all files under top not including folders """
    from vyperlogix.misc import ObjectTypeName
    isMatchingRe = ObjectTypeName.typeClassName(matching_re) == '_sre.SRE_Pattern'
    for root, dirs, files in walk(top, topdown=False, rejecting_re=rejecting_re):
        for f in files:
            _fname = os.sep.join([root,f])
            if (not isMatchingRe):
                if (callable(callback)):
                    callback(_fname)
            elif (isMatchingRe) and (matching_re.search(_fname)):
                if (callable(callback)):
                    callback(_fname)
        for d in dirs:
            _dname = os.sep.join([root,d])
            if (not isMatchingRe):
                if (callable(callback)):
                    callback(_dname)
            elif (isMatchingRe) and (matching_re.search(d)):
                if (callable(callback)):
                    callback(_dname)

def validatePathEXE(eVar=['PATH','PYTHONPATH'],fname='python.exe',verbose=False):
    """
    finds the specified fname from PATH.
    eVar can be a string or a list of strings that specify a path or list of paths.
    """
    from vyperlogix import misc
    eVar = eVar if (misc.isList(eVar)) else [eVar]
    for e in eVar:
        if (misc.isString(e)) and (os.environ.has_key(e)):
            toks = os.environ[e].split(';')
            for t in toks:
                f = searchForFileNamed(fname,t)
                if (verbose):
                    print '(%s)=[%s in %s]' % (f,fname,t)
                if (len(f) > 0):
                    return os.sep.join([t,fname])
    return ''

def validatePathEXE_using_environ(fname='python.exe'):
    _paths = sys.path
    fname = str(fname).lower()
    if (os.environ.has_key('PYTHONPATH')):
        _paths = os.environ['PYTHONPATH'].split(';')
        _top = '%s%s' % (':' if (sys.platform == 'win32') else '',os.sep)
        ex_paths = []
        for n in _paths:
            while (len(n) > 0) and (n[len(n)-2:] != _top):
                n = os.path.dirname(n)
                if (len(n) > 0) and (n[len(n)-2:] != _top):
                    ex_paths.append(n)
                else:
                    break
        _paths += ex_paths
    elif (os.environ.has_key('PATH')):
        _paths = os.environ['PATH'].split(';')
    _path = [n for n in _paths if (os.path.isdir(n)) and (os.path.exists(os.sep.join([n,fname])))]
    return '' if (len(_path) == 0) else _path[0]

def _makeDirs(_dirName):
    """ make all folders for a path, front to back, without considering the _dirName to be a fully qualified file path. """
    if (not os.path.exists(_dirName)):
        try:
            os.makedirs(_dirName)
        except:
            pass

def makeDirs(fname):
    """ make all folders for a path, front to back, fname is considered to be a fully qualified file path name rather than the name of a folder. """
    _dirName = fname if (os.path.isdir(fname)) else os.path.dirname(fname)
    _makeDirs(_dirName)

def dec2bin(x, digits=0): 
    oct2bin = ['000','001','010','011','100','101','110','111'] 
    binstring = [oct2bin[int(n)] for n in oct(x)] 
    return ''.join(binstring).lstrip('0').zfill(digits) 

st_normalize = lambda t:asctime(localtime(t))
s3_normalize = lambda t:timeStampLocalTime(tsecs=t,format=formatAmazonS3DateTimeStr())
s3_normalize12 = lambda t:timeStampLocalTime(tsecs=t,format=formatAmazonS3DateTime12Str())

def explain_stat(st,delim=',',asDict=False):
    normalize = lambda t:asctime(localtime(t))
    __is__ = ObjectTypeName.typeName(st) == 'nt.stat_result'
    __is_dict__ = misc.isDict(st)
    s = []
    if (__is_dict__):
        for k in st.keys():
            st[k.upper()] = st[k]
            del st[k]
    try:
        __ST_ATIME__ = st[stat.ST_ATIME] if (__is__) else st.get('ST_ATIME',0L) if (__is_dict__) else 0L
        val = tuple(['ST_ATIME','%s=%s'%(__ST_ATIME__,st_normalize(__ST_ATIME__))])
        if (asDict):
            s.append(val)
        else:
            s.append('%s is %s' % val)
    except Exception, ex:
        info_string = formattedException(details=ex)
        pass
    try:
        __ST_CTIME__ = st[stat.ST_CTIME] if (__is__) else st.get('ST_CTIME',0L) if (__is_dict__) else 0L
        val = tuple(['ST_CTIME','%s=%s'%(__ST_CTIME__,st_normalize(__ST_CTIME__))])
        if (asDict):
            s.append(val)
        else:
            s.append('%s is %s' % val)
    except Exception, ex:
        info_string = formattedException(details=ex)
        pass
    try:
        __ST_DEV__ = st[stat.ST_DEV] if (__is__) else st.get('ST_DEV',0L) if (__is_dict__) else 0L
        val = tuple(['ST_DEV',__ST_DEV__])
        if (asDict):
            s.append(val)
        else:
            s.append('%s is %s' % val)
    except:
        pass
    try:
        __ST_GID__ = st[stat.ST_GID] if (__is__) else st.get('ST_GID',0L) if (__is_dict__) else 0L
        val = tuple(['ST_GID',__ST_GID__])
        if (asDict):
            s.append(val)
        else:
            s.append('%s is %s' % val)
    except:
        pass
    try:
        __ST_INO__ = st[stat.ST_INO] if (__is__) else st.get('ST_INO',0L) if (__is_dict__) else 0L
        val = tuple(['ST_INO',__ST_INO__])
        if (asDict):
            s.append(val)
        else:
            s.append('%s is %s' % val)
    except:
        pass
    try:
        st_mode = st[stat.ST_MODE] if (__is__) else st.get('ST_MODE',0L) if (__is_dict__) else 0L
        _mode = stat.S_IMODE(st_mode)
        print '_mode (%d) --> %s' % (_mode,dec2bin(_mode))
        r_mode = 0
        a = []
        for k,v in _all_modes.iteritems():
            _k_ = int(k)
            _v_ = (_mode and _k_)
            print '%s and %s --> %s' % (_mode,_k_,_v_)
            if (_v_):
                a += v
                r_mode = r_mode or _k_
        val = tuple(['ST_MODE','%o or "%s"' % (r_mode,','.join(a))])
        if (asDict):
            s.append(val)
        else:
            s.append('%s is %s' % val)
    except Exception, details:
        print '%s' % (str(details))
        pass
    try:
        val = tuple(['ST_MTIME','%s=%s'%(st[stat.ST_MTIME],st_normalize(st[stat.ST_MTIME]))])
        if (asDict):
            s.append(val)
        else:
            s.append('%s is %s' % val)
    except Exception, ex:
        info_string = formattedException(details=ex)
        pass
    try:
        val = tuple(['ST_NLINK',st[stat.ST_NLINK]])
        if (asDict):
            s.append(val)
        else:
            s.append('%s is %s' % val)
    except:
        pass
    try:
        val = tuple(['ST_SIZE',st[stat.ST_SIZE]])
        if (asDict):
            s.append(val)
        else:
            s.append('%s is %s' % val)
    except:
        pass
    try:
        val = tuple(['ST_UID',st[stat.ST_UID]])
        if (asDict):
            s.append(val)
        else:
            s.append('%s is %s' % val)
    except:
        pass
    return delim.join(s) if (not asDict) else dict(s)

# Chmod recursively on a whole subtree
def chmod_tree(path, mode, mask):
    '''Chmod the tree at path'''
    def visit(arg, dirname, names):
        mode, mask = arg
        for name in names:
            fullname = os.path.join(dirname, name)
            if not os.path.islink(fullname):
                new_mode = (os.stat(fullname)[stat.ST_MODE] & ~mask) | mode
                m = '%o' % (new_mode)
                os.chmod(fullname, eval(m[len(m)-4:]))
    if (os.path.isfile(path)):
        path = os.path.dirname(path)
    os.path.walk(path, visit, (mode, mask))

# For clearing away read-only directories
def safe_rmtree(dirname, retry=0):
    '''Remove the tree at DIRNAME'''
    import shutil, time
    def rmtree(dirname):
        chmod_tree(dirname, 0666, 0666)
        shutil.rmtree(dirname)

    if (os.path.isfile(dirname)):
        dirname = os.path.dirname(dirname)

    if (sys.platform == 'win32'):
        m = stat.S_IREAD | stat.S_IWRITE
        chmod_tree(dirname, m, m)
        return removeAllFilesUnder(dirname)

    if not os.path.exists(dirname):
        return

    if retry:
        for delay in (0.5, 1, 2, 4):
            try:
                rmtree(dirname)
                break
            except:
                time.sleep(delay)
        else:
            rmtree(dirname)
    else:
        rmtree(dirname)

def locateRootContaining(top,fname):
    '''Locate a specific file using a recursive function that melts a path to nothing unless the file is found in the list of files at that level.'''
    while (1):
        d = dict([(k,os.sep.join([top,k])) for k in os.listdir(top)])
        if (d.has_key(fname)):
            return os.sep.join([top,fname])
        top = os.path.dirname(top)
        if (not os.path.exists(top)):
            break
    return None

def copyFile(src,dst,func=None,verbose=False,use_logging=False,no_shell=False):
    """ copies a binary file from src to dst """
    import types
    import math
    if (use_logging):
        import logging
    from vyperlogix import misc
    from vyperlogix.win import memoryUsage
    if (os.path.exists(src)):
	availRAM = 16384
        if (not no_shell) and (availRAM < 0):
            from vyperlogix.process import Popen
            if (isUsingWindows):
                Popen.Shell('echo F | XCOPY "%s" "%s" /Q /V /C /Y /I' % (src,dst), shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=sys.stdout)
            else:
                Popen.Shell('cp -f %s %s' % (src,dst), shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=sys.stdout)
        else:
            makeDirs(dst)
            fIn = open(src,'rb')
            fOut = open(dst,'wb')
            _failed = True
            try:
		try:
		    nBytes = 0
		    while (1):
			chunk = fIn.read(availRAM)
			l_chunk = len(chunk)
			nBytes += l_chunk
			if (l_chunk > 0):
			    fOut.write(chunk)
			if (l_chunk < availRAM):
			    if (verbose):
				info_string = '%s.2a :: Wrote %s bytes.' % (misc.funcName(),nBytes)
				if (use_logging):
				    logging.info(info_string)
				else:
				    print >>sys.stderr, info_string
			    break
		except Exception, ex:
		    print >> sys.stderr, 'EXCEPTION: %s' % (formattedException(details=ex))
            finally:
                fOut.flush()
                fOut.close()
                fIn.close()
                if (verbose):
                    info_string = '%s.3 :: Files Closed !' % (misc.funcName())
                    if (use_logging):
                        logging.info(info_string)
                    else:
                        print >>sys.stderr, info_string
    else:
        if (verbose):
            info_string = 'ERROR :: Cannot find the file named "%s".' % src
            if (use_logging):
                logging.warning(info_string)
            else:
                print >>sys.stderr, info_string

def copyFiles(src,dst,func=None,verbose=False):
    if (len(os.path.splitext(src)[-1]) > 1):
        _isdir = os.path.isdir(os.path.dirname(src))
    else:
        _isdir = os.path.isdir(src)
    if ((_isdir) and os.path.isdir(dst)):
        from vyperlogix.process import Popen
        if (isUsingWindows):
            Popen.Shell('XCOPY "%s" "%s" /S /E /Y' % (src,dst), shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=sys.stdout)
        else:
            Popen.Shell('cp -f -R %s %s' % (src,dst), shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=sys.stdout)
    else:
        copyFile(src,dst,func=None,verbose=False)

def read_in_chunks(infile, chunk_size=1024*64):
    chunk = infile.read(chunk_size)
    while chunk:
        yield chunk
        chunk = infile.read(chunk_size)

def copy_binary_files_by_chunks(source,dest,chunk_size=(1024*64)-1,callback=None):
    fIn = open(source,'rb')
    __is__ = callable(callback)
    if (not __is__):
	fOut = open(dest,'wb')
    else:
	callback(filename=source)
    try:
        for chunk in read_in_chunks(fIn):
	    if (not __is__):
		fOut.write(chunk)
	    else:
		try:
		    callback(chunk=chunk)
		except:
		    pass
    finally:
	if (not __is__):
	    fOut.flush()
	    fOut.close()
	else:
	    callback(eof=source)
        fIn.close()

def fileSize(fname):
    if (os.path.exists(fname)):
        st = os.stat(fname)
        return st.st_size
    return -1

def folderSize(fpath):
    '''Returns a tuple with (count,size_in_bytes)'''
    num = 0
    folder_size = 0
    for (path, dirs, files) in os.walk(fpath):
        for f in files:
            folder_size += os.path.getsize(os.path.join(path, f))
            num += 1
    return (num,folder_size)

def tempFile(prefix,useTemporaryFile=False):
    '''Get the name of a temp file based on where such files are being kept. See also appDataFolder() for a similar use.'''
    import tempfile as tfile
    from vyperlogix import misc
    common = ''
    prefix = str(prefix) if not misc.isString(prefix) else prefix
    if (os.environ.has_key('TEMP')):
        common = os.environ['TEMP']
    elif (os.environ.has_key('TMP')):
        common = os.environ['TMP']
    if (len(common) == 0) or (useTemporaryFile):
        f = tfile.TemporaryFile()
        common = os.path.abspath(os.sep.join(f.name.split(os.sep)[0:-1]))
        f.close()
    return os.sep.join([common,prefix])

def appDataFolder(prefix='',useTemporaryFile=True):
    '''Get the name of a temp file based on where application specific files are being kept.'''
    from vyperlogix import misc
    if (sys.platform == 'win32'):
        t = tempFile('',useTemporaryFile=useTemporaryFile)
        toks = [_t_ for _t_ in t.lower().split(os.sep) if (len(_t_.strip()) > 0)]
        if (len(toks) > 0):
            _popped_too_many = False
            _toks = misc.copy(toks)
            while (toks[-1].replace('location ','') != 'appdata'):
                toks.pop()
                if (len(toks) == 0):
                    _popped_too_many = True
                    break
            if (_popped_too_many):
                toks = misc.copy(_toks)
        if (misc.findFirstContaining(toks,'local') == -1):
            toks.append('local')
        if (len(prefix) > 0):
            toks.append(prefix)
        return os.sep.join(toks)
    return tempFile(prefix=prefix,useTemporaryFile=useTemporaryFile)

def _findUsingPath(t,p):
    import time,Queue
    from vyperlogix import misc

    Qs = {}
    q = Queue.Queue(100)

    def do_scan_for_file(target,top,statsDict,topdown=True):
        for root, dirs, files in os.walk(top,topdown=topdown):
            for f in files:
                if (f.split(os.sep)[-1] == target) or (f.find(target) > -1):
                    p = os.sep.join([root,f])
                    print '(+++).do_scan_for_file().1 q.put_nowait(%s)' % (p)
                    q.put_nowait(p)
                    print '(+++).do_scan_for_file().2 del statsDict["%s"]' % (top)
                    del statsDict[top]
                    return
        print '(+++).do_scan_for_file().3 del statsDict["%s"]' % (top)
        del statsDict[top]

    ptoks = p.split(';')
    if (len(ptoks) == 1):
        ptoks = p.split(':')
    ptoks = [p for p in ptoks if (len(p) > 0)]
    for i in xrange(len(ptoks)):
        f = ptoks[i]
        if (f.startswith('%') and f.endswith('%')):
            f = f.replace('%','')
            f = os.environ.get(f,None)
            ptoks[i] = f
    for drive in [d for d in getCurrentWindowsLogicalDrives()]:
        try:
            for dir in [os.path.join(drive,tt) for tt in os.listdir(drive) if (not tt.startswith('$')) and (tt.find('Program Files') > -1) and (os.path.isdir(os.path.join(drive,tt)))]:
                ptoks.append(dir)
        except WindowsError:
            pass
    ptoks = list(set(ptoks))
    for f in ptoks:
        if (misc.isStringValid(f)) and (os.path.exists(f)) and (os.path.isdir(f)):
            Qs[f] = 1
            do_scan_for_file(t,f,Qs)
    isDone = False
    while (not isDone):
        try:
            p = q.get_nowait()
        except:
            p = None
        print '(+++)._findUsingPath().1 Sleeping on "%s".' % (p)
        time.sleep(1)
        if (misc.isStringValid(p)):
            print '(+++)._findUsingPath().2 Return "%s".' % (p)
            return p
        isDone = (len(Qs) == 0)
    print '(+++)._findUsingPath().3 Return None.'
    return None

def findUsingPath(fname):
    '''Allows findUsingPath(r"@SVN_BINDIR@/svnlook") to be used as a way to execute a macro.'''
    from vyperlogix import misc
    toks = fname.split('/')
    t = toks[0]
    if (t.startswith('@')) and (t.endswith('@')) and (len(toks) > 1):
        tx = t.replace('@','')
        t = toks[1]
    else:
        try:
            tx = toks[1]
        except IndexError:
            tx = ''
    t += '.' if (sys.platform == 'win32') and (len(os.path.splitext(t)) == 1) else ''
    p = os.environ["PATH"] if (not os.environ.has_key(tx)) else os.environ[tx]
    tf = _findUsingPath(t,p)
    if (tf == None):
        try:
            p = os.environ["windir"]
            p = p.split(os.sep)[0]+os.sep
        except:
            p = '%s' % (os.sep)
        tf = _findUsingPath(t,p)
    return tf.replace(os.sep,'/')

def print_stderrout(msg):
    import sys
    print >>sys.stdout, msg
    print >>sys.stderr, msg

def strip(s):
    return ''.join([ch for ch in s if (ord(ch) != 0)]).strip()

def expand_template(string,context):
    s = string
    for k,v in context.iteritems():
        _k = '{{ %s }}' % (k)
        s = s.replace(_k,str(v))
    return s

def parseBetween(s,i,tok1,tok2):
    foundIt1 = -1
    for x in xrange(i,0,-1):
        if (s[x] == '?'):
            foundIt1 = x
            break
    foundIt2 = -1
    for x in xrange(i,len(s)):
        if (s[x] == '"'):
            foundIt2 = x
            break
    return foundIt1,foundIt2

def de_camel_case(stringAsCamelCase,delim=' ',method=DeCamelCaseMethods.default):
    """Adds spaces to a camel case string.  Failure to space out string returns the original string.
    >>> space_out_camel_case('DMLSServicesOtherBSTextLLC')
    'DMLS Services Other BS Text LLC'
    """
    import re
    from vyperlogix import misc

    def get_matches(subject):
        matches = [match for match in pattern.finditer(subject)]
        if (subject[0].isupper()) and (len(matches) > 0) and (matches[0].start() == 0):
            del matches[0]
        return matches

    if stringAsCamelCase is None:
        return None
    _stringAsCamelCase = stringAsCamelCase

    normalize = lambda s:s
    if (method == DeCamelCaseMethods.force_lower_case):
        normalize = lambda s:s.lower()

    is_lowerUpper = lambda group:group[0].islower() and group[-1].isupper()
    isUpper_lower = lambda group:group[0].isupper() and group[-1].islower()
    isUpperUpper = lambda group:group[0].isupper() and group[-1].isupper()
    is_lowerUpperUpper = lambda group:group[0].islower() and group[1].isupper() and group[1].isupper()

    pattern = re.compile('([a-z][A-Z][A-Z][_])|([A-Z][A-Z])|([a-z][A-Z])|([A-Z][a-z])')
    while (1):
        matches = get_matches(_stringAsCamelCase)
        if (len(matches) == 0):
            break
        aMatch = matches.pop()
        if (is_lowerUpper(aMatch.group())):
            b = (aMatch.group()[0:1] != '_')
            _stringAsCamelCase = _stringAsCamelCase[0:aMatch.start()] + aMatch.group()[0:1] + (delim if (b) else '') + aMatch.group()[1:].lower() + _stringAsCamelCase[aMatch.end():]
        elif (isUpper_lower(aMatch.group())):
            b = (_stringAsCamelCase[0:aMatch.start()][-1] != '_')
            _stringAsCamelCase = _stringAsCamelCase[0:aMatch.start()] + (delim if (b) else '') + aMatch.group().lower() + _stringAsCamelCase[aMatch.end():]
        elif (isUpperUpper(aMatch.group())):
            b = (aMatch.group()[0:1] != '_')
            _stringAsCamelCase = _stringAsCamelCase[0:aMatch.start()] + (delim if (b) else '') + aMatch.group()[0:1].lower() + aMatch.group()[1:].lower() + _stringAsCamelCase[aMatch.end():]
        elif (is_lowerUpperUpper(aMatch.group())):
            _stringAsCamelCase = _stringAsCamelCase[0:aMatch.start()] + aMatch.group()[0:1] + delim + aMatch.group()[1:].lower() + _stringAsCamelCase[aMatch.end():]
    return normalize(_stringAsCamelCase)

if (__name__ == '__main__'):
    tt = today_utctime()
    print tt
