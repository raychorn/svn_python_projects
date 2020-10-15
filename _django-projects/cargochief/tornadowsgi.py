import os
__can__tornado__ = True
try:
    import tornado.httpserver
    import tornado.ioloop
    import tornado.wsgi
except ImportError:
    __can__tornado__ = False
import sys
import django.core.handlers.wsgi

def __find_library__():
    __fpath__ = '/usr/local/@@TEMPLATE@@/vyperlogix_2_7_0.zip'
    for root,dirs,files in os.walk('/usr/local/'):
        for f in files:
            if (str(f).endswith('.zip')) and (f.find('vyperlogix') > -1):
                __fpath__ = os.sep.join([root,f])
                return __fpath__
    for root,dirs,files in os.walk('j:/@Vyper Logix Corp/@Projects/python-projects/@lib/'):
	for f in files:
	    if (str(f).endswith('.zip')) and (f.find('vyperlogix') > -1):
		__fpath__ = os.sep.join([root,f])
		return __fpath__
    return None

try:
    from vyperlogix import misc
except ImportError:
    _vyperlogix_library_ = __find_library__()
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
    from vyperlogix.misc import Args
    from vyperlogix.misc import PrettyPrint

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
            '--verbose':'output more stuff.',
            '--debug':'debug some stuff.',
            '--port=?':'port number.',
            '--ip=?':'ip address.',
            }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = __args__.programName
    
	_isVerbose = __args__.get_var('isVerbose',Args._bool_,False)
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: _isVerbose=%s' % (_isVerbose)
	_isDebug = __args__.get_var('isDebug',Args._bool_,False)
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: _isDebug=%s' % (_isDebug)
	_isHelp = __args__.get_var('isHelp',Args._bool_,False)
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: _isHelp=%s' % (_isHelp)

	if (_isHelp):
	    ppArgs()
	    sys.exit()

	__port__ = __args__.get_var('port',Args._int_,8001)
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: __port__=%s' % (__port__)

	__ip__ = __args__.get_var('ip',Args._str_,'127.0.0.1')
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: __ip__=%s' % (__ip__)

	os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
	application = django.core.handlers.wsgi.WSGIHandler()
	if (__can__tornado__):
	    container = tornado.wsgi.WSGIContainer(application)
	    http_server = tornado.httpserver.HTTPServer(container)
	    http_server.listen(__port__, __ip__)
	    tornado.ioloop.IOLoop.instance().start()
	else:
	    print >> sys.stderr, 'WARNING: Missing tornado !!!'

if (__name__ == "__main__"):
    main()