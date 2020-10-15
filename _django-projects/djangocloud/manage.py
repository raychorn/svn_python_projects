#!/usr/bin/env python
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
    from vyperlogix.misc import _utils
    from vyperlogix.django.manager import DjangoManager
    from vyperlogix.django.manager import isUsingWindows
    if (not isUsingWindows):
	__app__ = 'djangocloud/djangocloud'
    else:
	__app__ = '_django-projects/djangocloud'
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
    
#from vyperlogix.misc import ReportTheList
#ReportTheList.reportTheList(sys.path,'sys.path',fOut=sys.stderr)

if __name__ == "__main__":
    from vyperlogix.misc import threadpool
    _Q_ = threadpool.ThreadQueue(10)

    @threadpool.threadify(_Q_)
    def check_for_superuser():
	import time
	from django.contrib.auth.models import User
	_begin = time.time()
	
	def _make_admin_user():
	    try:
		from users.g import make_admin_user
		make_admin_user()
	    except:
		pass
	
	while (1):
	    try:
		users = User.objects.all()
		if (users.count() == 0):
		    _make_admin_user()
		    logging.debug('%s.DEBUG.1: _make_admin_user() !!!' % (misc.funcName()))
		    break
		elif (not any([aUser.is_superuser for aUser in users])):
		    _make_admin_user()
		    logging.debug('%s.DEBUG.2: _make_admin_user() !!!' % (misc.funcName()))
		    break
	    except Exception, ex:
		info_string = _utils.formattedException(details=ex)
		logging.debug('%s.DEBUG.3: %s' % (misc.funcName(),info_string))
		break
	    _now = time.time()
	    if (_now - _begin > 60000):
		logging.debug('%s.DEBUG.4: TIME-Out !!!' % (misc.funcName()))
		break

    try:
        from django.contrib.sites.models import Site
        aSite = Site.objects.get_current()
    except:
        from views.initialize import __init__
        __init__()
    check_for_superuser()
    try:
        execute_manager(settings, argv=sys.argv)
    except:
        pass
    
    

