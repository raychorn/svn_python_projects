import os
import tornado.httpserver
import tornado.ioloop
import tornado.wsgi
import sys
import django.core.handlers.wsgi

_vyperlogix_library_ = '/usr/local/cargochief/vyperlogix_2_7_0.zip'
_is_ = os.path.exists(_vyperlogix_library_)
print '1._is_ (%s) =%s' % (_vyperlogix_library_,_is_)
if (_is_):
    l = [f for f in sys.path if (f.find('vyperlogix') > -1)]
    print '1.1. len(l)=%s' % (len(l))
    if (len(l) == 0):
       print '1.2. sys.path.insert(0, %s)' % (_vyperlogix_library_)
	sys.path.insert(0, _vyperlogix_library_)

from vyperlogix import misc
from vyperlogix.misc import _utils

print '2. _utils.isUsingWindows=%s' % (_utils.isUsingWindows)
if (not _utils.isUsingWindows):
    if (os.path.exists('/usr/local/cargochief/_Django-1.3_Multi-Threaded')):
	l = [f for f in sys.path if (f.find('_Django-1.3_Multi-Threaded') > -1)]
	if (len(l) == 0):
	    sys.path.insert(1, '/usr/local/cargochief/_Django-1.3_Multi-Threaded')
    
    if (os.path.exists('/usr/local/cargochief/cargochief')):
	l = [f for f in sys.path if (f.find('cargochief') > -1)]
	if (len(l) == 0):
	    sys.path.insert(1, '/usr/local/cargochief/cargochief')
    
    if (not os.path.exists('/var/log/cargochief')):
	try:
	    os.mkdir('/var/log/cargochief')
	except:
	    pass

_is_ = os.environ.has_key('DJANGO_SETTINGS_MODULE')
print '3._is_=%s' % (_is_)
if (not _is_):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    application = django.core.handlers.wsgi.WSGIHandler()
    container = tornado.wsgi.WSGIContainer(application)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(8001, "127.0.0.1")
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()