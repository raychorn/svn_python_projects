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

from vyperlogix.oodb import *
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

def getMetadataForNamedDaemon(name):
   if (_daemon_metadata.has_key(name)):
      return _daemon_metadata[name]
   daemon_name = 'daemons.%s' % name
   if (_daemon_metadata.has_key(daemon_name)):
      return _daemon_metadata[daemon_name]
   return {}

def storeMetaDataInfoFor(d,n,v):
   d[n] = v
   return v

def indexDaemonMetadata(d):
   h = lists.HashedLists()
   for k,v in d.iteritems():
      for kk,vv in v.iteritems():
         h[kk] = vv
         try:
            h[vv] = v
         except:
            pass
   return h

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

def isMutable(n):
   return n not in ['_tasklet_name']

def authenticateUser(username,password):
   from authentication import SalesForceAuthentication

   sfAuth = SalesForceAuthentication.SalesForceAuthentication(username,password)
      
   return sfAuth

def dispatch(*args):
   import urllib
   from vyperlogix.html import oohtml
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

      try:
         pass
      except:
         exc_info = sys.exc_info()
         info_string = '\n'.join(traceback.format_exception(*exc_info))
         print info_string
      
      f_path = os.path.abspath('.')
      files = [n for n in os.listdir(f_path) if n.endswith('.dbx')]
      daemons = getNormalizedDaemonNamespaces()
      daemons_metadata_d = {}
      daemons_metadata = [storeMetaDataInfoFor(daemons_metadata_d,n,getMetadataForNamedDaemon(n)) for n in daemons]
      h_d = indexDaemonMetadata(daemons_metadata_d)
      n = len(files)

      _isAdmin = path.startswith('/admin')
      _isLogin = path.startswith('/login')
      _isLogout = path.startswith('/logout')

      p_toks = [t for t in path.split('/') if len(t) > 0]

      h_html = oohtml.Html()
      h_html.text(oohtml.DOCTYPE_40_TRANSITIONAL)
      
      html_html = h_html.tag(oohtml.HTML)
      head_html = html_html.tag(oohtml.HEAD)
      head_html.tagOp(oohtml.META, http_equiv=oohtml.CONTENT_TYPE, content=oohtml.TEXT_HTML_CHARSET_ISO_8859_1)
      head_html.metas(
              (oohtml.AUTHOR, "Ray C Horn (rhorn@magma-da.com)"),
              (oohtml.KEYWORDS, "CRON Replacement"),
              (oohtml.DESCRIPTION, "CRON Replacement"),
              (oohtml.ROBOTS, oohtml.ALL))
      head_html.tagTITLE('pyDaemon Status v1.1  (powered by Python on Rails v0.1)%s' % (' (ADMIN)' if (_isAdmin) else ''))
      
      _content = ''
      
      print '_isLogout=%s' % _isLogout
      print 'len(d_form)=%s' % len(d_form)
      
      _isRedirecting = False
      if (_isLogin):
         _username = d_form['txtUsername']
         _password = d_form['txtPassword']
         _sfAuth = authenticateUser(_username,_password)
         isUserAllowed = _sfAuth.isLoginSuccessful
         if (isUserAllowed):
            _sess = lists.HashedLists2()
            _sess['username'] = _username
            _sess['user'] = _sfAuth.userRecord
            _sess['timeStamp'] = _utils.timeStamp()
            _user_sessions[_user_signature] = _sess
            _url = '%s/admin' % httpURI(env)
            _content += '<script language="JavaScript" type="text/javascript">document.location.href = "%s";</script>' % _url
            _isRedirecting = True
      elif (_isLogout):
         del _user_sessions[_user_signature]
         _url = '%s/' % httpURI(env)
         _content += '<script language="JavaScript" type="text/javascript">document.location.href = "%s";</script>' % _url
         _isRedirecting = True
         pass
      
      if (not _isRedirecting):
         _is_user_session_active = _user_sessions.has_key(_user_signature)
         if (_isAdmin) and (not _is_user_session_active):
            _content += htmnl_login_form()
         elif (not _isAdmin) or ( (_isAdmin) and (_is_user_session_active) ):
            if (_is_user_session_active):
               _sess = _user_sessions[_user_signature]
               _user = _sess['user']
               _ts = _utils.getFromDateTimeStr(_sess['timeStamp'])
               _ts_local = _utils.localFromUTC(_ts)
               _content += '<p>Welcome back, %s (%s, <small>Click %s if you are not <i>%s</i></small>), You logged-in at %s</p>' % (_user['Name'],_sess['username'],html_anchor('/logout','_top','here'),_user['Name'],_ts_local)
            
            _content += '<p>There %s <b>%d</b> daemon%s at this time.</p>' % ('is' if n == 1 else 'are',n,'' if n == 1 else 's')
      
            _daemons = []
            for f in files:
               _daemons.append(f)
               _db_mask = '_c.'
               d_name = f.split(_db_mask)[0]
               d_meta = h_d[d_name][0] if h_d.has_key(d_name) else {}
               _isViewingData = False
               _isViewingMetaData = (path.find('/metadata') > -1)
               _isViewingSpecificMetaData = (_isViewingMetaData) and (path.find('/%s%s' % (d_name,_db_mask)) > -1)
      
               _anchor_viewStatus = html_anchor(httpURI(env)+'/%sview/database/%s' % (pathIfAdmin(path,_isAdmin),urllib.quote_plus(f)),'_top','View Daemon Named "%s".' % d_name)
               _label_viewMetaData = 'View Metadata'
               _anchor_viewMetaData = html_anchor(httpURI(env)+'/%sview/metadata/%s' % (pathIfAdmin(path,_isAdmin),urllib.quote_plus(f)),'_top',_label_viewMetaData)
               view_content = 'Viewing <b>Daemon Named "%s"</b>&nbsp;&nbsp;%s<br>' % (d_name,_anchor_viewMetaData if (not _isViewingSpecificMetaData) else _label_viewMetaData)
      
               if (len(p_toks) != 3) or (f != p_toks[-1] if (len(p_toks) == 3) else ''):
                  pass
               else:
                  _isViewingData = True
      
               anchor_content = '%s&nbsp;&nbsp;%s<br>' % (_anchor_viewStatus,_anchor_viewMetaData if (not _isViewingSpecificMetaData) else _label_viewMetaData)
      
               if (_isViewingMetaData):
                  _content += anchor_content
               elif (_isViewingData):
                  _content += view_content
               else:
                  _content += anchor_content
      
               if (_isViewingSpecificMetaData) and (_isViewingData):
                  try:
                     if (len(d_meta) > 0):
                        _content += '<table border="1" width="80%" align="center">'
                        _content += '<tr bgcolor="silver">'
                        _content += '<td colspan="2" align="center">'
                        _content += '<b>Tasklet Metadata</b>'
                        _content += '</td>'
                        _content += '</tr>'
                        _content += '<tr bgcolor="silver">'
                        _content += '<td>'
                        _content += '<b>Name</b>'
                        _content += '</td>'
                        _content += '<td>'
                        _content += '<b>Value</b>'
                        _content += '</td>'
                        _content += '</tr>'
                        i = 0
                        for k,v in d_meta.iteritems():
                           _content += '<tr bgcolor="%s">' % ('cyan' if (i%2)==0 else 'lime')
                           _content += '<td>'
                           _content += '%s' % (k) if (not _isAdmin) else html_anchor(httpURI(env)+'/%sedit/metadata/%s/' % (pathIfAdmin(path,_isAdmin),urllib.quote_plus(f)),'_top','%s.' % k) if (isMutable(k)) else '%s' % (k)
                           _content += '</td>'
                           _content += '<td>'
                           _content += '%s' % (v) if (not isURL(v)) else '<a href="%s" target="_blank">%s</a>' % (v,v)
                           _content += '</td>'
                           _content += '</tr>'
                           i += 1
                        _content += '</table>'
                        _content += '<hr>'
                  except:
                     exc_info = sys.exc_info()
                     info_string = '\n'.join(traceback.format_exception(*exc_info))
                     logging.error(info_string)
            pass
         
         if (path != '/') and (not _isAdmin):
            _content += '<a href="%s" target="_top">Home</a><br>' % (httpURI(env)+'/%s' % (pathIfAdmin(path,_isAdmin)))
         if (len(p_toks) == 3) and (p_toks[0] in ['view','%sview' % pathIfAdmin(path,_isAdmin)]) and ('database' == p_toks[1]) and (p_toks[-1] in files):
            _content += '<br><br>'
            dbx = PickledHash(os.sep.join([f_path,p_toks[-1]]),PickleMethods.useSafeSerializer)
            _not_ok_list = [k for k in dbx.keys() if dbx[k].has_key('resp') and ('OK' not in dbx[k]['resp'] or 200 not in dbx[k]['resp'])]
            d_keys = dbx.normalizedSortedKeys(NormalizedKeyOptions.via_dict)
            d_keys_num = len(d_keys)
            d_keys_max = 50
            d_keys_n = d_keys_max if d_keys_num > d_keys_max else d_keys_num
            _content += '<b>Displaying %d of %d items retaining the last %d seconds (%s) of data.</b><br>' % (d_keys_n,d_keys_num,_data_retention_policy,_utils.timeDeltaAsReadable(datetime.timedelta(seconds=_data_retention_policy)))
            # To-Do:
            #    (1). Use the OO HTML Lib to make this into a ListBox rather than a Select List
            #    (2). Allow users to page thru the list... one page at a time.
            _content += '<select name="hist" id="hist">'
            try:
               for k,v in [aKey for aKey in d_keys.iteritems()][0:d_keys_max]:
                  _v = v[0].strip() if isinstance(v,list) else v
                  _val = str(dbx[_v]) if dbx.has_key(_v) else 'ERROR'
                  _content += '<option value="%s">%s</option>' % (k.split(',')[0],'%s=%s' % (k,_val))
            except:
               exc_info = sys.exc_info()
               info_string = '\n'.join(traceback.format_exception(*exc_info))
               logging.error(info_string)
            _content += '</select>'
            if (len(_not_ok_list) > 0):
               _content += '<hr width="50%" color="red">'
               for k in _not_ok_list[0:10]:
                  _content += '<font color="red">%s=%s</font><br>' % (k,dbx[k])
               pass
            dbx.close()
      
      body_html = html_html.tag(oohtml.BODY)
      idContent = body_html.tag(oohtml.DIV, id="content", style="background-color: #FFFF80")
      idContent.text(_content)
      
      outfile.write(h_html.toHtml())
   else:
      logging.error('Unable to dispatch args=[%s] due to problem with the number of arguments passed in from the http-server.' % str(args))
   pass

def getDaemons():
   import re
   _name = _utils.funcName()
   _regex = re.compile(r".+tasklet\.((py)|(pyc)|(pyo))")
   files = [f for f in os.listdir(os.path.abspath(_daemons)) if _regex.search(f)]
   rejects = [f for f in os.listdir(os.path.abspath(_daemons)) if not _regex.search(f) and (f.find('.svn') == -1) and (f.find('_svn') == -1) and (f.find('__init__.') == -1) and (f.find('dlib') == -1)]
   if (len(rejects) > 0):
      logging.warning('(%s) :: Rejected daemon files are "%s".  PLS check the file names to ensure your daemons will be executed as planned.' % (_name,rejects))
   return files

def getNormalizedDaemons():
   h = lists.HashedLists()

   fs = []
   dms = getDaemons()
   for f in dms:
      h[f.split('.')[0]] = f.split('.')[-1]
   for k,v in h.iteritems():
      x = [n for n in v if n == 'py']
      if (len(x) == 0):
         x = [n for n in v if n == 'pyc']
      if (len(x) == 0):
         x = [n for n in v if n == 'pyo']
      if (len(x) > 0):
         fs.append('.'.join([k,x[0]]))
   return fs

def getNormalizedDaemonNamespaces():
   return [f.split('.')[0] for f in getNormalizedDaemons()]

def _callback(_metadata):
   _hostname = _utils.getComputerName().lower()
   if (isinstance(_metadata,dict)):
      _tasklet_name = _metadata['_tasklet_name'] if (_metadata.has_key('_tasklet_name')) else ''
      _run_frequency = _metadata['_run_frequency'] if (_metadata.has_key('_run_frequency')) else -1
      logging.warning('_tasklet_name=%s, _run_frequency=%s' % (_tasklet_name,_run_frequency))
      if ( (len(_tasklet_name) > 0) and (_run_frequency > 0) ):
         frame = framework.PyDaemonFramework()
         frame.tasklet_name = _tasklet_name
         c_dbxName = getMungedFilenameFor(frame.c_dbxName())
         logging.warning('c_dbxName=%s' % (c_dbxName))
         if (os.path.exists(c_dbxName)):
            dbx = frame.dbx
            _keys = dbx.normalizedSortedKeys()
            toks1 = _keys[0].split(',')
            t1 = _utils.getFromDateTimeStr(toks1[-1])
            toks2 = _keys[-1].split(',')
            t2 = _utils.getFromDateTimeStr(toks2[-1])
            t_diff = t1-t2
            t_diff_secs = _utils.timeDeltaAsSeconds(t_diff)
            t_policy = float(_data_retention_policy)
            if (t_diff_secs > t_policy):
               t1_secs = time.mktime(t1.timetuple())
               t1_secs_past = t1_secs - t_policy
               t1_past = _utils.getAsDateTimeStr(t1_secs_past)
               __keys = dbx.keys()
               m = [k for k in __keys if (time.mktime(_utils.getFromDateTimeStr(k.split(',')[-1]).timetuple()) < t1_secs_past)]
               for item in m:
                  del dbx[item]
               if (len(m) > 0):
                  logging.info('Deleted %d records per the current policy which is "%-10.2f".' % (len(m),t_policy))
                  dbx.sync()
               pass
            dbx.close()
         else:
            logging.warning('Cannot perform data retention policy for tasklet "%s" on "%s" due to inability to locate the database named "%s".' % (_tasklet_name,_hostname,c_dbxName))
      else:
         logging.warning('Cannot perform data retention policy for tasklet "%s" on "%s" due to inability to determine the run frequency.' % (_tasklet_name,_hostname))
   else:
      logging.warning('Cannot perform data retention policy for tasklet "%s" on "%s" due to bad metadata which is of type "%s" but should be type "%s".' % (_tasklet_name,_hostname,type(_metadata),dict))
      
@threadify(_threadQ)
def execDaemon(f, _logging, _hostname):
   _import_error = False
   try:
      exec "import " + f
   except ImportError:
      _import_error = True
      exc_info = sys.exc_info()
      info_string = '\n'.join(traceback.format_exception(*exc_info))
      _logging.error(info_string)

   s_ts_lt = _utils.timeStampLocalTime()
   ts_lt = _utils.getFromDateTimeStr(s_ts_lt)
   s_ts = _utils.timeStamp()
   ts = _utils.getFromDateTimeStr(s_ts)
   ts_diff = ts - ts_lt
   _logging.warning('(%s) at %s/%s/%s/%s :: _import_error=%s' % (_utils.funcName(),s_ts_lt,s_ts,ts_diff,_utils.utcDelta(),_import_error))

   if (not _import_error):
      _daemon_metadata[f] = {}
      try:
         v = '%s._metadata' % (f)
         vv = eval(v)
         print '%s=[%s]' % (v,vv)
         _daemon_metadata[f] = vv
      except ImportError:
         exc_info = sys.exc_info()
         info_string = '\n'.join(traceback.format_exception(*exc_info))
         _logging.error(info_string)

      compNames = _daemon_metadata[f]['_run_on_computer'] if (_daemon_metadata[f].has_key('_run_on_computer')) else []

      _logging.warning('compNames=%s' % compNames)

      if (len(compNames) > 0):
         compNames = [str(n).lower() for n in _utils.listify(compNames)]
         _ishostName_good_to_go = False
         _logging.warning('_hostname=%s' % _hostname)
         if (isinstance(_hostname,list)):
            _ishostName_good_to_go = any([(h in compNames) for h in _hostname])
         else:
            _ishostName_good_to_go = (_hostname in compNames)

         _logging.warning('_ishostName_good_to_go=%s' % _ishostName_good_to_go)
         if (_ishostName_good_to_go):
            x = '%s.tasklet(%s,_callback)' % (f,_isVerbose)
            try:
               exec x
            except:
               exc_info = sys.exc_info()
               info_string = '\n'.join(traceback.format_exception(*exc_info))
               _logging.error(info_string)
      else:
         _logging.error('Cannot run tasklet "%s" on "%s" due to hostname mismatch.' % (f,_hostname))
   else:
      _logging.error('Unable to import the "%s" daemon tasklet.' % f)

   pass

def execDaemons(_logging):
   import socket
   _hostname = [socket.gethostname().lower(),socket.gethostbyname_ex(socket.gethostname())[0].lower()]

   print '(%s) :: BEGIN:' % (_utils.funcName())
   for f in getNormalizedDaemons():
      dname = "%s.%s" % (os.path.basename(_daemons),f.split('.')[0])
      print '(%s) :: dname=%s' % (_utils.funcName(),dname)
      execDaemon(dname,_logging,_hostname)
   print '(%s) :: END!' % (_utils.funcName())

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

      execDaemons(logging)

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
         print '(%s) :: Log file is "%s".' % (_utils.funcName(),fh.name)
         sys.stdout = sys.stderr = Log(fh)
   except:
      exc_info = sys.exc_info()
      info_string = '\n'.join(traceback.format_exception(*exc_info))
      logging.warning(info_string)
      logging.warning('(%s) :: Cannot redirect stderr and stdout...' % (_utils.funcName()))
   pass

def get_sys_path_tracking():
   from vyperlogix.misc import processAllFilesUnder
   
   d = lists.HashedLists2()

   def _callback(root,dirs,files,tag):
      for f in files:
         if (f.split('.')[-1] in ['py','pyc','pyo']):
            _fname = os.sep.join([root,f])
            if (os.path.exists(_fname)):
               d[_fname] = os.stat(_fname)
   
   for f in sys.path:
      if (os.path.exists(f)):
         d[f] = os.stat(f)
   return d

@threadify(_threadQ)
def console_log_rotation(fpath='.'):
   while (1):
      time.sleep(86400/24)
      redirect_stdouts(fpath=fpath)
   
@threadify(_threadQ)
def check_sys_path_tracking():
   while (1):
      time.sleep(5*60)
      d = get_sys_path_tracking()
      for k,v in d.iteritems():
         secs = d_sys_path_tracking[k]
         if (secs) and (v):
            if (secs.st_mtime != v.st_mtime):
               print '(%s) :: Detected the file "%s" has changed. Stopping %s and waiting for auto-restart.' % (_utils.funcName(),k,_utils.getProgramName())
               sys.exit(0)
               pass
            pass
         pass
   
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
           '--daemons=?':'path to daemons folder',
           '--freq=?':'how often (seconds) should the plug-in be executed.',
           '--port=?':'TCP/IP port for the WWW Interface.',
           '--logging=?':'[logging.INFO,logging.WARNING,logging.ERROR,logging.DEBUG]',
           '--retention=?':'1.. :: any number of seconds greater than zero'
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
   
   _daemons = _cwd
   try:
      __daemons = _argsObj.arguments['daemons'] if _argsObj.arguments.has_key('daemons') else _cwd
      if (len(__daemons) == 0) or (not os.path.exists(__daemons)):
	 __daemons = _cwd
      __daemons__ = __daemons
   except:
      pass
   _daemons = __daemons__
   
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
	 print '_daemons=%s' % _daemons
	    
         redirect_stdouts(_cwd)
         d_sys_path_tracking = get_sys_path_tracking()
         console_log_rotation(_cwd)
         #check_sys_path_tracking()
         main(_cwd)
      else:
         print >>sys.stdout, '%s is already running on this computer.  No need to do so again.' % _utils.getProgramName()
         sys.stdout.close()
   sys.exit(0)
   pass
