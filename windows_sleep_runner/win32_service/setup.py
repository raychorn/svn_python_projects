import os, sys

from distutils.core import setup

import py2exe

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = "0.5.0"
        self.company_name = "No Company"
        self.copyright = "no copyright"
        self.name = "py2exe sample files"

_packages = [[f for f in sys.path if (f.endswith('@lib'))][0]]
_includes = ['win32api','win32file','win32con']
_excludes = []
_service=['windows_sleep_runner_service']

windows_sleep_runner_service = Target(
    description = ' '.join([str(n).capitalize() for n in _service[0].split('.')[0].split('_')]),
    modules = _service,
    cmdline_style='pywin32',
)

try:
    print >>sys.stderr, 'Building...\n\tservice is "%s"\n\tpackages is "%s"\n\tincludes is "%s"\n\texcludes is "%s".' % (_service,_packages,_includes,_excludes)
    setup(
            service=[windows_sleep_runner_service],
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
