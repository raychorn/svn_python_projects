import os, sys
import logging

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.daemon import utils as daemon_utils
from vyperlogix.logging import standardLogging
from vyperlogix.daemon.daemon import EchoLog as Log

_tasklet_prefix = 'tasklets'
_tasklet_path = os.path.abspath(_tasklet_prefix)

_data_path_prefix = os.sep.join(['www.VyperLogixCorp.com','pdf_exporter'])

_context_dbx_name = '__context__.dbx'

__copyright__ = """\
(c). Copyright 1990-2014, Vyper Logix Corp., All Rights Reserved.
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
__isRunning__ = True

services = {
    #'echo': echo,
    #'echo.echo': echo
}

# To-Do:
#

def redirect_stderr(log_path):
    try:
        ts = _utils.timeStamp()
        _fname = '%s_console_%s.log' % (_utils.getProgramName(),ts)
        if (sys.platform == 'win32'):
            _fname = _fname.replace(':','-')
        _fp = os.sep.join([_log_path,_fname])
        fh = open(_fp,'w+')
        print '(%s) :: Log file is "%s".' % (misc.funcName(),fh.name)
        sys.stderr = Log(fh)
    except:
        exc_info = sys.exc_info()
        info_string = '\n'.join(traceback.format_exception(*exc_info))
        logging.warning(info_string)
        logging.warning('(%s) :: Cannot redirect stderr...' % (misc.funcName()))
    pass

def callback(args):
    global __isRunning__
    for k,v in daemon_utils._metadata.iteritems():
	funcs = v['_functions']
	for _f_ in funcs:
	    _f_ = _f_ if (isinstance(_f_,list)) else [_f_]
	    for f in _f_:
		if (f.__name__ == 'shutdown'):
		    v_shutdown_command = v['shutdown_command']
		    v_shutdown_command = v_shutdown_command if (not isinstance(v_shutdown_command,list)) else v_shutdown_command[0]
		    if (v_shutdown_command == args):
			__isRunning__ = False # signal the closing of the server process at the request of the client...
			logging.warning('%s :: SHUTTING DOWN !' % (misc.funcName()))

def main(services):
    from pyamf.remoting.gateway.wsgi import WSGIGateway
    from wsgiref import simple_server
    
    while (__isRunning__):
	logging.info('%s :: __isRunning__=%s' % (misc.funcName(),__isRunning__))
	gw = WSGIGateway(services)
    
	httpd = simple_server.WSGIServer(
	    ('localhost', 8000),
	    simple_server.WSGIRequestHandler,
	)
    
	httpd.set_app(gw)
    
	try:
	    httpd.handle_request()
	except KeyboardInterrupt:
	    break

def exception_callback(sections):
    _msg = 'EXCEPTION Causing Abend.\n%s' % '\n'.join(sections)
    print >>sys.stdout, _msg
    print >>sys.stderr, _msg
    logging.error('(%s) :: %s' % (misc.funcName(),_msg))
    sys.stdout.close()
    sys.stderr.close()
    sys.exit(1)
    
if __name__ == '__main__':
    #from vyperlogix.decorators import PrivateMethod
    #pt2 = PrivateMethod.PrivateTest2()
    #pt2.test2()
    
    ver = _utils.getFloatVersionNumber()
    print 'Python version check... "%s".' % ver
    if (ver >= 2.5):
        from vyperlogix.misc import _psyco
        _psyco.importPsycoIfPossible(main)
        
	from vyperlogix.handlers.ExceptionHandler import *
	excp = ExceptionHandler()
	excp.callback = exception_callback

        name = _utils.getProgramName()
        _log_path = _utils.safely_mkdir_logs()
        _log_path = _utils.safely_mkdir(fpath=os.sep.join([_log_path,_utils.timeStampLocalTimeForFileName(delimiters=('_'))]),dirname='')
        logFileName = os.sep.join([_log_path,'%s.log' % (name)])

        _logging = logging.INFO
        standardLogging.standardLogging(logFileName,_level=_logging,console_level=logging.INFO,isVerbose=True)
        
        redirect_stderr(_log_path)
	
	_data_path = _utils.appDataFolder(prefix=_data_path_prefix)
	
        logging.info('Logging to "%s" using level of "%s:.' % (logFileName,standardLogging.explainLogging(_logging)))
        logging.info('Data in "%s".' % (_data_path))

	if (not os.path.exists(_data_path)):
	    logging.info('Making Dirs for data in "%s".' % (_data_path))
	    os.makedirs(_data_path)
	else:
	    logging.info('Dirs exist for data in "%s".' % (_data_path))

        _tasklets = daemon_utils.getNormalizedDaemonNamespaces(_tasklet_prefix,_tasklet_path)
        for t in _tasklets:
	    _data_path = _data_path if (_data_path != os.path.dirname(sys.argv[0])) else ''
            daemon_utils.execDaemons(_tasklet_prefix,_tasklet_path, dpath=_data_path, _logging=logging.getLogger(''))
            
        for k,v in daemon_utils._metadata.iteritems():
            tname = v['_tasklet_name'][0]
	    rname = tname.split('.')[-1].split('_')[0]
            funcs = v['_functions']
            for _f_ in funcs:
		_f_ = _f_ if (isinstance(_f_,list)) else [_f_]
		for f in _f_:
		    services['.'.join([rname,f.__name__])] = f
		    logging.info('Registered new Service "%s".' % (f.__name__))
	    cb_hook = v['callback_hook']
	    logging.info('cb_hook #1 "%s".' % (cb_hook))
	    if (isinstance(cb_hook,list)):
		cb_hook = cb_hook[0]
	    if (cb_hook):
		if (type(cb_hook) == types.FunctionType):
		    try:
			logging.info('setting cb_hook "%s".' % (cb_hook))
			cb_hook(callback)
		    except:
			exc_info = sys.exc_info()
			info_string = '\n'.join(traceback.format_exception(*exc_info))
			logging.warning(info_string)
        
        from vyperlogix.hash import lists
        
        lists.prettyPrint(services,title='services',fOut=sys.stdout)

        toks = __copyright__.split('\n')
        _msg = []
        for t in toks:
            t = t.strip()
            if (len(t) == 0):
                break
            else:
                _msg.append(t)
        print >>sys.stdout, '\n'.join(_msg)
        print >>sys.stderr, '\n'.join(_msg)
        
        main(services)

    else:
        print >> sys.stderr, 'ERROR - Cannot continue unless Python 2.5.x is being used, the current version is "%s" and this is unacceptable.' % ver

