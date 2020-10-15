import os, sys
import logging

isUsingWindows = (sys.platform.lower().find('win') > -1) and (os.name.lower() == 'nt')

if (isUsingWindows):
    tops = [
        'J:/@Vyper Logix Corp/@Projects/python-projects/@lib/12-13-2011-01',
        'J:/@Vyper Logix Corp/@Projects/python-projects/_Django-1.3_Multi-Threaded',
        'J:/@Vyper Logix Corp/@Projects/python-projects/_django-projects'
    ]
else:
    tops = [
        '/usr/local',
        '/usr/local',
        '/usr/local'
    ]

try:
    from vyperlogix.django.manager import DjangoManager
    from vyperlogix.django.manager import isUsingWindows
    if (not isUsingWindows):
        __app__ = 'cargochief/cargochief'
    else:
        __app__ = '_django-projects/cargochief'
    m = DjangoManager(tops=tops,app=__app__)
except ImportError, ex:
    print 'WARNING: Cannot proceed because: %s' % (ex)
    os._exit(0)

from django.core.management import execute_manager

try:
    import settings # Assumed to be in the same directory.
except ImportError, details:
    info_string = _utils.formattedException(details=details)
    print >>sys.stderr, "Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__
    print >>sys.stderr, info_string
    sys.exit(1)
except Exception, details:
    info_string = _utils.formattedException(details=details)
    print >>sys.stderr, info_string
    sys.exit(1)
    
if __name__ == "__main__":
    _argv = [str(s).strip() for s in sys.argv]
    print 'sys.argv=%s' % (_argv)
    try:
        execute_manager(settings, argv=_argv)
    except Exception, ex:
        from vyperlogix.misc import _utils
        print 'ERROR: %s' % (_utils.formattedException(details=ex))
    
    

