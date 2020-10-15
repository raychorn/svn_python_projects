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
    
if __name__ == "__main__":
    _argv = [str(s).strip() for s in sys.argv]
    print 'sys.argv=%s' % (_argv)
    from vyperlogix import misc
    from vyperlogix.lists.ListWrapper import ListWrapper
    l = ListWrapper(_argv)
    i = l.findFirstContaining('--proxy=')
    if (i > -1):
        __proxy__ = _argv[i].split('=')[-1]
        proxy = __proxy__.split(':')
	try:
	    if (len(proxy) == 2):
		proxy[-1] = int(proxy[-1])
		if (misc.isInteger(proxy[-1])):
		    from vyperlogix.sockets.proxies.socks import socks
		    import socket
		    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy[0], int(proxy[-1]))
		    socket.socket = socks.socksocket
		    print 'proxy=%s' % (proxy)
		else:
		    print 'ERROR: Invalid proxy=%s, due to malformed port number.' % (proxy)
	    else:
		print 'ERROR: Invalid proxy=%s, due to missing ":" (--proxy=127.0.0.1:8080).' % (proxy)
	except Exception, ex:
	    info_string = _utils.formattedException(details=ex,depth=2,delims='\n\t')
	    print 'ERROR: Invalid proxy=%s, due to the following:\n%s.' % (proxy,info_string)
        del _argv[i]
    try:
        execute_manager(settings, argv=_argv)
    except Exception, ex:
        print 'ERROR: %s' % (_utils.formattedException(details=ex))
    
    

