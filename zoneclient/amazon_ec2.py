import os, sys
import platform

__isDebugging__ = False

isUsingWindows = (sys.platform.lower().find('win') > -1) and (os.name.lower() == 'nt')
isUsingMacOSX = (sys.platform.lower().find('darwin') > -1) and (os.name.find('posix') > -1) and (not isUsingWindows)
isUsingLinux = (sys.platform.lower().find('linux') > -1) and (os.name.find('posix') > -1) and (not isUsingWindows) and (not isUsingMacOSX)

__code_library_name__ = 'vyperlogix'

def __hasVyperLogixLibraryLoadedIn__(top=None,container=sys.path,isDebug=__isDebugging__):
    fpath = None
    try:
        paths = [f for f in container if str(f).find(__code_library_name__) > -1]
        if (isDebug):
            print >> sys.stderr, '__hasVyperLogixLibraryLoadedIn__.1.DEBUG: __hasVyperLogixLibraryLoadedIn__--> paths=%s' % (paths)
        fpath = os.sep.join([top,paths[0]]) if (len(paths) > 0) else None
        if (isDebug):
            print >> sys.stderr, '__hasVyperLogixLibraryLoadedIn__.2.DEBUG: __hasVyperLogixLibraryLoadedIn__--> fpath=%s' % (fpath)
        fpath = fpath if (fpath) and (os.path.exists(fpath)) and (os.path.isfile(fpath)) else None
        if (isDebug):
            print >> sys.stderr, '__hasVyperLogixLibraryLoadedIn__.3.DEBUG: __hasVyperLogixLibraryLoadedIn__--> fpath=%s' % (fpath)
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
        isStopping = False #(root == '/usr/local/cargochief')
        if (__isDebugging__):
            print >> sys.stderr, 'getVyperLogixLibraryPath.1.DEBUG: root=%s' % (root)
        fpath = __hasVyperLogixLibraryLoadedIn__(top=root,container=files,isDebug=isStopping)
        if (__isDebugging__):
            print >> sys.stderr, 'getVyperLogixLibraryPath.2.DEBUG: fpath=%s' % (fpath)
        if (isStopping):
            print >> sys.stderr, 'getVyperLogixLibraryPath.3.DEBUG: files=%s' % (files)
            return fpath
        if (fpath is not None):
            return fpath
    return None

if (__isDebugging__):
    print >> sys.stderr, '1.DEBUG: isUsingLinux=%s' % (isUsingLinux)
if (isUsingLinux):
    fpath = None
    if (__isDebugging__):
        print >> sys.stderr, '2.DEBUG: hasNotVyperLogixLibraryLoaded=%s' % (hasNotVyperLogixLibraryLoaded)
    if (hasNotVyperLogixLibraryLoaded):
        fpath = __hasVyperLogixLibraryLoaded()
        if (__isDebugging__):
            print >> sys.stderr, '3.DEBUG: fpath=%s' % (fpath)
    if (fpath is not None) and (os.path.exists(fpath)) and (os.path.isfile(fpath)):
        sys.path.insert(0,fpath)
    else:
        fpath = getVyperLogixLibraryPath('/')
        if (__isDebugging__):
            print >> sys.stderr, '4.DEBUG: fpath=%s' % (fpath)
        if (fpath is not None) and (os.path.exists(fpath)) and (os.path.isfile(fpath)):
            sys.path.insert(0,fpath)
        else:
            print >> sys.stderr, '5.ERROR: Cannot proceed without the %s Library' % (__code_library_name__)
            sys.exit(1)

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.hash.lists import HashedLists2

from vyperlogix.process import Popen
from vyperlogix.netinfo import getupnetips

from vyperlogix.sockets import traceroute

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

__ip__ = '169.254.169.254'

__urlLocal__ = 'http://%s/latest/meta-data/local-ipv4' % (__ip__)
__urlPublic__ = 'http://%s/latest/meta-data/public-ipv4' % (__ip__)

__urls__ = [__urlLocal__,__urlPublic__]

__hops__ = HashedLists2()

__hops__[__ip__] = traceroute.TraceRoute(__ip__).hops

print '%s (%d hops)' % (__ip__,__hops__[__ip__])

ifaces = [i for i in getupnetips.localifs() if (i[-1] != '127.0.0.1')]
print 'DEBUG: ifaces=%s' % (ifaces)
if (len(ifaces) > 0) and (len(ifaces[-1]) > 0):
    _ip = ifaces[-1][-1]

import urllib2
for __url__ in __urls__:
    response = urllib2.urlopen(__url__)
    _default_ip = response.read()
    _ip = _default_ip
    __hops__[_ip] = traceroute.TraceRoute(_ip).hops
    print '%s --> %s (%d hops)' % (__url__,_ip,__hops__[_ip])

def ppArgs():
    pArgs = [(k,args[k]) for k in args.keys()]
    pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
    pPretty.pprint()

if (__name__ == '__main__'):
    args = {'--help':'show some help.',
            '--verbose':'output more stuff.',
            '--debug':'debug some stuff.',
            '--test':'test some stuff.',
            '--username=?':'username for zoneedit.',
            '--password=?':'password for zoneedit.',
            '--domain=?':'domain for zoneedit.',
            }
    _argsObj = Args.Args(args)

    if (len(sys.argv) == 1):
        ppArgs()
    else:
        _progName = _argsObj.programName
        _isVerbose = False
        try:
            if _argsObj.booleans.has_key('isVerbose'):
                _isVerbose = _argsObj.booleans['isVerbose']
        except Exception, e:
            info_string = _utils.formattedException(details=e)
            print info_string
            _isVerbose = False

        _isDebug = False
        try:
            if _argsObj.booleans.has_key('isDebug'):
                _isDebug = _argsObj.booleans['isDebug']
        except:
            pass

        _isTest = False
        try:
            if _argsObj.booleans.has_key('isTest'):
                _isTest = _argsObj.booleans['isTest']
        except:
            pass

        _isHelp = False
        try:
            if _argsObj.booleans.has_key('isHelp'):
                _isHelp = _argsObj.booleans['isHelp']
        except:
            pass

        _username = ''
        try:
            __username = _argsObj.arguments['username'] if _argsObj.arguments.has_key('username') else _username
        except Exception, e:
            info_string = _utils.formattedException(details=e)
            print info_string
        _username = __username

        _password = ''
        try:
            __password = _argsObj.arguments['password'] if _argsObj.arguments.has_key('password') else _password
        except Exception, e:
            info_string = _utils.formattedException(details=e)
            print info_string
        _password = __password

        _domain = ''
        try:
            __domain = _argsObj.arguments['domain'] if _argsObj.arguments.has_key('domain') else _domain
        except Exception, e:
            info_string = _utils.formattedException(details=e)
            print info_string
        _domain = __domain

        _zoneclientPy = 'zoneclient.py'
        _fpath = os.sep.join([os.path.abspath('.'),_zoneclientPy])
        if (_isDebug):
            print >> sys.stderr, 'DEBUG: _fpath=%s' % (_fpath)
        if (os.path.exists(_fpath)) and (os.path.isfile(_fpath)):
            _cmd_ = 'python zoneclient.py -v%s -a %s %s %s %s' % (' -t' if (_isTest) else '',_ip,_username,_password,_domain)
            if (_isDebug):
                print >> sys.stderr, 'DEBUG: _fpath=%s' % (_fpath)
            if (_isDebug):
                print >> sys.stderr, 'DEBUG: _cmd_=%s' % (_cmd_)
            print Popen.Shell(_cmd_, shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=sys.stdout)
        else:
            print >> sys.stderr, 'ERROR: Cannot proceed without %s which seems to be missing.' % (_fpath)