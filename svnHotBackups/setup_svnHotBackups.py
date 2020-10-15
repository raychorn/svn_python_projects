from distutils.core import setup
import py2exe

from vyperlogix import misc
from vyperlogix.misc import _utils
import os, sys, traceback

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from vyperlogix.daemon.daemon import Log

_stdOut = sys.stdout

sys.stdout = Log(StringIO())

_console=[os.sep.join([os.getcwd(),'svnHotBackups.py'])]
_packages = [[f for f in sys.path if (f.endswith('@lib'))][0]]
_includes = ['win32api','win32file','win32con']
_excludes = []
#_excludes = ['Crypto.PublicKey._fastmath','Crypto.Util.winrandom','_pybsddb','bsddb3.dbutils', 'r_hmac', 'testdata', 'tests']

_root = os.path.abspath('.')
print >>sys.stderr, '_root is "%s" from "%s".' % (_root,sys.argv[0])

print >>sys.stderr, '_packages is "%s".' % (_packages)

_len_packages = len(_packages)
try:
    try:
        _root_ = os.path.abspath('.')
        print >>sys.stderr, 'Building...\n\tconsole is "%s"\n\tpackages is "%s"\n\tincludes is "%s"\n\texcludes is "%s".' % (_console,_packages,_includes,_excludes)
        setup(
            console=_console,
            packages=_packages,
            options = {"py2exe": {"compressed": 1,
                                  "optimize": 2,
                                  "ascii": 1,
                                  "bundle_files": 1,
                                  "includes": _includes,
                                  "excludes": _excludes,
                                  "dll_excludes": ["mswsock.dll", "MSWSOCK.dll", "powrprof.dll"],
                                  }
                       },
            zipfile = None,
        )
    except ImportError, details:
        print >>sys.stderr, 'ImportError: %s' % (details)
    except Exception, details:
        print >>sys.stderr, 'ERROR: %s' % (details)
        exc_info = sys.exc_info()
        info_string = _utils.asMessage('\n'.join(traceback.format_exception(*exc_info)))
        print >>sys.stderr, info_string
except Exception, details:
    print >>sys.stderr, 'ERROR: %s' % (details)
    exc_info = sys.exc_info()
    info_string = _utils.asMessage('\n'.join(traceback.format_exception(*exc_info)))
    print >>sys.stderr, info_string
finally:
    _stdout_log = os.sep.join([_root_,'stdout_%s.txt' % (_utils.timeStampForFileName())])
    _utils.writeFileFrom(_stdout_log,sys.stdout.f.getvalue())
