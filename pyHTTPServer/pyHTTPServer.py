# pyDaemon
#
# Features:
#    Monitor Specific IP:Port for specific feedback to determine system health and take specific error recovery steps.
#    Provide light-weight web interface to show system health and allow monitoring functions to be adjusted.

import os, sys
import re
os.environ['TZ'] = 'UTC'
import time
if hasattr(time, 'tzset'):
    time.tzset()
import datetime

import logging
import logging.handlers
import traceback
import tempfile

if (sys.platform.find('win') == -1):
    _eggName = 'VyperLogixLib_1.0_py25.zip'
    if (os.path.exists(_eggName)):
        sys.path.append(os.sep.join([os.path.abspath('.'),_eggName]))

from vyperlogix.html import oohtml

from vyperlogix.oodb import *
from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc.threadpool import *
from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint
from vyperlogix.logging import standardLogging
from vyperlogix.hash import lists
from vyperlogix.daemon import framework
from vyperlogix.misc import ObjectTypeName
from vyperlogix.daemon.daemon import Log
from vyperlogix.sockets import sniffer

d_sys_path_tracking = lists.HashedLists2()

root_path = '/'
login_url = '/login'
_serve_address = '0.0.0.0'
_port = 8080

_data_retention_policy = 60*60*24

_threadQ = ThreadQueue(10)

_HOSTNAME_symbol = 'HOSTNAME'
_COMPUTERNAME_symbol = 'COMPUTERNAME'

_isVerbose = False
_freq = -1
_daemon = False

_daemon_metadata = lists.HashedLists2()

_user_sessions = lists.HashedLists2()

def isURL(s):
    try:
        return (s.startswith('http://')) or (s.startswith('https://'))
    except:
        return False

def _URI(env):
    return env['SERVER_NAME']+':'+env['SERVER_PORT']

def httpURI(env):
    return 'http://'+_URI(env)

def html_anchor(url,target,label):
    return '<a href="%s" target="%s">%s</a>' % (url,target,label)

def html_table_tr_td(content):
    return '<tr><td>%s</td></tr>' % content

def htmnl_login_form():
    _content = ''
    _content += '<table width="100%">'

    _content += html_table_tr_td('You must enter your SalesForce Credentials before entering Admin Mode.')
    _content += html_table_tr_td('<form action="/login" method="post" name="login_form">')
    _content += html_table_tr_td('<b>Username:</b>&nbsp;<input type="Text" name="txtUsername" size="30" maxlength="255">')
    _content += html_table_tr_td('<b>Password:</b>&nbsp;<input type="Password" name="txtPassword" size="16" maxlength="30">&nbsp;&nbsp;<input type="Submit" name="submit">')
    _content += html_table_tr_td('</form>')
    _content += html_table_tr_td('<small>Only those who have been granted Admin Rights in SalesForce may use Admin Mode.</small>')

    _content += '</table>'
    return _content

def __content__(contents=''):
    h_html = oohtml.Html()
    h_html.text(oohtml.DOCTYPE_40_TRANSITIONAL)

    html_html = h_html.tag(oohtml.HTML)
    head_html = html_html.tag(oohtml.HEAD)
    head_html.tagOp(oohtml.META, http_equiv=oohtml.CONTENT_TYPE, content=oohtml.TEXT_HTML_CHARSET_ISO_8859_1)
    head_html.metas(
        (oohtml.AUTHOR, "Ray C Horn (raychorn@vyperlogix.com)"),
        (oohtml.KEYWORDS, "Sample WebServer"),
        (oohtml.DESCRIPTION, "Sample WebServer"),
        (oohtml.ROBOTS, oohtml.ALL))
    head_html.tagTITLE('Sample WebServer')

    body_html = html_html.tag(oohtml.BODY)
    idContent = body_html.tag(oohtml.DIV, id="content", style="background-color: #FFFF80")
    idContent.text(contents)

    return h_html.toHtml()

def dispatch(*args):
    import urllib
    from vyperlogix.http.httpServer import dictFromHeaders

    def pathIfAdmin(p,bool):
        return p.replace(p.replace('/admin',''),'')[1:] if (bool) else ''

    # In this model the callback handles the mapping of URL path to process and emits HTML as-needed to outfile.
    # The callback is free to use whatever Framework may be desired to render the HTML or XML.
    if (len(args) == 5):
        httpServer, path, headers, outfile, env = args
        logging.info('path=[%s]\theaders=[%s]\toutfile=[%s]\tenv=[%s]' % (path,','.join(headers),outfile,env))
        d_headers = dictFromHeaders(headers)
        _user_signature = ','.join([env['REMOTE_ADDR'],d_headers['User-Agent']])

        print '\n%s\nd_headers=\n%s\n%s\n' % ('='*80,'\n'.join(['%s=%s' % (k,v) for k,v in d_headers.iteritems()]),'='*80)
        print '\n%s\nenv=\n%s\n%s\n' % ('='*80,'\n'.join(['%s=%s' % (k,v) for k,v in env.iteritems()]),'='*80)

        d_form = env['FORM']
        print '\n%s\nd_form=\n%s\n%s\n' % ('='*80,'\n'.join(['%s=%s' % (k,v) for k,v in d_form.iteritems()]),'='*80)

        p_toks = [t for t in path.split('/') if len(t) > 0]

        if (_root is None):
            outfile.write(__content__())
        else:
            try:
                for k,v in _root.iteritems():
                    if (k == p_toks[0]):
                        if (os.path.exists(v)):
                            if (os.path.isdir(v)):
                                if (path.startswith('/')):
                                    path = path[1:]
                                fpath = path.replace('/',os.sep).replace(k,v)
                                #fpath = os.path.sep.join([fpath,_index])
                                if (os.path.exists(fpath)) and (os.path.isfile(fpath)):
                                    ext = os.path.splitext(fpath)[-1]
                                    if (ext in ['.html','.htm']):
                                        outfile.write(_utils.readBinaryFileFrom(fpath))
                                    else:
                                        try:
                                            ___globals___= {}
                                            c = execfile( fpath, ___globals___)                                        
                                            pass
                                        except:
                                            outfile.write(__content__('404 ERROR -- Undefined URL (%s)-->(%s)' % (path,fpath)))
                                else:
                                    outfile.write(__content__('404 ERROR -- Undefined URL (%s)-->(%s)' % (path,fpath)))
                            else:
                                pass
            except:
                if (_root.has_key(path)):
                    fpath = os.path.sep.join([_root[path],str(path).replace('/',os.sep)]) if (path != '/') else _root[path]
                    fpath = fpath+os.sep if (not fpath.endswith(os.sep)) else fpath
                    if (os.path.exists(fpath)) and (os.path.isdir(fpath)):
                        fpath = os.path.sep.join([fpath,_index])
                        if (os.path.exists(fpath)) and (os.path.isfile(fpath)):
                            outfile.write(_utils.readBinaryFileFrom(fpath))
                        else:
                            outfile.write(__content__('404 ERROR -- Undefined URL (%s)-->(%s)' % (path,fpath)))
            pass
    else:
        logging.error('Unable to dispatch args=[%s] due to problem with the number of arguments passed in from the http-server.' % str(args))
    pass

def main(cwd):
    ver = _utils.getFloatVersionNumber()
    print 'Python version check... "%s".' % ver
    if (ver >= 2.5):
        name = _utils.getProgramName()
        _log_path = safely_mkdir_logs(fpath=cwd)
        logFileName = os.sep.join([_log_path,'%s.log' % (name)])

        standardLogging.standardLogging(logFileName,_level=_logging)

        logging.info('Logging to "%s" using level of "%s:.' % (logFileName,standardLogging.explainLogging(_logging)))
        logging.info('Data Retention Policy is %d seconds.' % _data_retention_policy)

        rootLogger = logging.getLogger('')
        timedHandler = logging.handlers.TimedRotatingFileHandler(logFileName,when="H",interval=1,backupCount=24*5)
        rootLogger.addHandler(timedHandler)

        from vyperlogix.http import httpServer
        httpServer.HTTPServer(root_path,login_url,_serve_address,_port,logging,callback=dispatch)
    else:
        print >> sys.stderr, 'ERROR - Cannot continue unless Python 2.5.x is being used, the current version is "%s" and this is unacceptable.' % ver
    pass

@threadify(_threadQ)
def daemon_main():
    main()

def safely_mkdir_logs(fpath='.'):
    _log_path = os.path.abspath(os.sep.join([fpath,'logs']))
    if (not os.path.exists(_log_path)):
        os.mkdir(_log_path)
    return _log_path

def redirect_stdouts(fpath='.'):
    try:
        _log_path = safely_mkdir_logs(fpath=fpath)
        if (isinstance(sys.stdout,Log)):
            sys.stdout.rotate()
            sys.stdout.prune(os.sep.join([_log_path,'*_console_*.log']),24*5)
        else:
            ts = _utils.timeStamp()
            _fname = '%s_console_%s.log' % (_utils.getProgramName(),ts)
            if (sys.platform == 'win32'):
                _fname = _fname.replace(':','-')
            _fp = os.sep.join([_log_path,_fname])
            fh = open(_fp,'w+')
            print '(%s) :: Log file is "%s".' % (misc.funcName(),fh.name)
            sys.stdout = sys.stderr = Log(fh)
    except:
        exc_info = sys.exc_info()
        info_string = '\n'.join(traceback.format_exception(*exc_info))
        logging.warning(info_string)
        logging.warning('(%s) :: Cannot redirect stderr and stdout...' % (misc.funcName()))
    pass

@threadify(_threadQ)
def console_log_rotation(fpath='.'):
    while (1):
        time.sleep(86400/24)
        redirect_stdouts(fpath=fpath)

if (__name__ == '__main__'):
    def ppArgs():
        pArgs = [(k,args[k]) for k in args.keys()]
        pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
        pPretty.pprint()

    _old_stdout = sys.stdout
    _old_stderr = sys.stderr

    args = {'--help':'displays this help text.',
            '--verbose':'output more stuff.',
            '--cwd=?':'the path the program runs from, defaults to the path the program runs from.',
            '--daemon=?':'1 or true or yes to make into a daemon (Linux or Unix only)',
            '--freq=?':'how often (seconds) should the plug-in be executed.',
            '--port=?':'TCP/IP port for the WWW Interface.',
            '--logging=?':'[logging.INFO,logging.WARNING,logging.ERROR,logging.DEBUG]',
            '--retention=?':'1.. :: any number of seconds greater than zero',
            '--root=?':'web root for this app.',
            '--index=?':'index page for this app.',
            }
    _argsObj = Args.Args(args)

    try:
        _isHelp = _argsObj.booleans['isHelp'] if _argsObj.booleans.has_key('isHelp') else False
    except:
        _isHelp = False

    try:
        _isVerbose = _argsObj.booleans['isVerbose'] if _argsObj.booleans.has_key('isVerbose') else False
    except:
        _isVerbose = False

    try:
        _freq = int(_argsObj.arguments['freq']) if _argsObj.arguments.has_key('freq') else False
    except:
        _freq = -1

    try:
        _logging = eval(_argsObj.arguments['logging']) if _argsObj.arguments.has_key('logging') else False
    except:
        _logging = -1

    __cwd__ = os.path.dirname(sys.argv[0])
    try:
        __cwd = _argsObj.arguments['cwd'] if _argsObj.arguments.has_key('cwd') else __cwd__
        if (len(__cwd) == 0) or (not os.path.exists(__cwd)):
            if (os.environ.has_key('cwd')):
                __cwd = os.environ['cwd']
        __cwd__ = __cwd
    except:
        pass
    _cwd = __cwd__

    _log_path = safely_mkdir_logs(fpath=_cwd)
    fh = open(os.sep.join([_log_path,'%s_init.log' % _utils.getProgramName()]),'w+')
    sys.stdout = sys.stderr = Log(fh)

    print >>sys.stderr, '_argsObj=(%s)' % str(_argsObj)
    print '(%s) :: Init Log file is "%s".' % (_utils.getProgramName(),fh.name)

    try:
        _default_data_retention_policy = _data_retention_policy
        _data_retention_policy = _argsObj.arguments['retention'].split()[0] if _argsObj.arguments.has_key('retention') else _data_retention_policy
        k = [aKey for aKey in args.keys() if (aKey.find('--retention=') > -1)]
        if (len(k) > 0):
            k = k[0]
        else:
            k = ''
        _data_retention_policy_guide = args[k] if args.has_key(k) else ''
        if (len(_data_retention_policy_guide) > 0):
            if (not isinstance(_data_retention_policy_guide,int)):
                _bounds = re.findall(r"\b\d+\b", _data_retention_policy_guide)
                try:
                    _lower_bound = int(_bounds[0])
                except:
                    _lower_bound = -1
                try:
                    _upper_bound = int(_bounds[-1]) if (len(_bounds) > 1) else -1
                except:
                    _upper_bound = -1
                if ( (_lower_bound > 0) and (_upper_bound == -1) ):
                    _data_retention_policy = _data_retention_policy if (_data_retention_policy >= _lower_bound) else _default_data_retention_policy
                elif ( (_lower_bound > 0) and (_upper_bound > -1) ):
                    _data_retention_policy = _data_retention_policy if (_data_retention_policy >= _lower_bound) and (_data_retention_policy <= _upper_bound) else _default_data_retention_policy
                else:
                    _data_retention_policy = _lower_bound
        if (not isinstance(_data_retention_policy,int)):
            _bounds = re.findall(r"\b\d+\b", str(_data_retention_policy))
            _data_retention_policy = _bounds[0]

        _data_retention_policy = int(_data_retention_policy)
    except:
        exc_info = sys.exc_info()
        info_string = '\n'.join(traceback.format_exception(*exc_info))
        print >>sys.stderr, info_string

    try:
        _daemon = _argsObj.arguments['isDaemon'] if _argsObj.arguments.has_key('isDaemon') else False
    except:
        _daemon = False

    try:
        _port = int(_argsObj.arguments['port']) if _argsObj.arguments.has_key('port') else False
    except:
        _port = 8080

    try:
        _root = _argsObj.arguments['root'] if _argsObj.arguments.has_key('root') else None
        import simplejson
        try:
            _root = simplejson.loads(_root)
        except:
            if (_root.startswith('{')) and (_root.endswith('}')):
                _root = _root.replace('{','').replace('}','')
                toks = _root.split(',')
                tups = [t.split('::') for t in toks]
                tuples = []
                for t in tups:
                    tuples.append([tt.replace("'",'').replace("'",'') for tt in t])
                tuples = tuple(tuples)
                _root = dict(tuples)
            else:
                if (not os.path.exists(_root)) or (not os.path.isdir(_root)):
                    print '_root (%s) is invalid because it either does not exist or it is not a directory path.' % (_root)
                    _root = None
    except:
        _root = None

    try:
        _index = _argsObj.arguments['index'] if _argsObj.arguments.has_key('index') else ''
        if (isinstance(_root,dict)):
            if (_index):
                _cnt = 0
                for k,v in _root.iteritems():
                    _v_ = v+os.sep if (not v.endswith(os.sep)) else v
                    if (os.path.exists(_v_)) and (os.path.isdir(_v_)):
                        fpath = os.path.sep.join([v,_index])
                        if (os.path.isfile(fpath)):
                            _cnt += 1
                if (_cnt == 0):
                    print '_index (%s) is invalid because it either does not exist or it is not a file name hanging off the _root (%s).' % (_index,_root)
                    _index = ''
        else:
            if (_root) and (_index) and (os.path.exists(_root)) and (not os.path.isdir(_root)):
                fpath = os.path.sep.join([_root,_index])
                if (not os.path.isfile(fpath)):
                    print '_index (%s) is invalid because it either does not exist or it is not a file name hanging off the _root (%s).' % (_index,_root)
                    _index = ''
    except:
        _index = ''

    print '_daemon=[%s]' % _daemon
    if (_daemon):
        try:
            from os import fork
        except ImportError:
            print 'WARNING :: Cannot act as daemon due to lack of support from the OS - are you sure you are running under some form of Linux/Unix ?'
            _daemon = False

    if (_isHelp):
        ppArgs()
    elif (_daemon):
        from vyperlogix.daemon import daemon
        print '1.0 daemon.createDaemon()'

        procParams = """
                 process ID = %s
                 parent process ID = %s
                 process group ID = %s
                 session ID = %s
                 user ID = %s
                 effective user ID = %s
                 real group ID = %s
                 effective group ID = %s
                 """ % (os.getpid(), os.getppid(), os.getpgrp(), os.getsid(0), os.getuid(), os.geteuid(), os.getgid(), os.getegid())
        print '2.0\n%s' % procParams
        _fname = os.path.abspath("createDaemon.log")
        print 'Writing daemon parms to "%s".' % _fname
        open(_fname, "w").write(procParams + "\n")
        daemon.Daemon(func=daemon_main,dirName=os.path.abspath('.'))
        print '3.0 daemon.createDaemon()'
    else:
        sys.stdout = _old_stdout
        sys.stderr = _old_stderr

        if (not sniffer.isListenerActive('0.0.0.0',_port)):
            print 'sys.argv=%s' % sys.argv
            print '_cwd=%s' % _cwd
            print '_port=%s' % _port
            print '_root=%s' % _root

            redirect_stdouts(_cwd)
            console_log_rotation(_cwd)
            main(_cwd)
        else:
            print >>sys.stdout, '%s is already running on this computer.  No need to do so again.' % _utils.getProgramName()
            sys.stdout.close()
    sys.exit(0)
    pass