import os, sys
import traceback

from vyperlogix.misc import _utils
from vyperlogix.hash import lists

_metadata = lists.HashedLists2()

def getDaemons(prefix, fpath):
   import re
   from vyperlogix import misc
   _name = misc.funcName()
   s_regex = r".+%s\.((py)|(pyc)|(pyo))" % ('_tasklet')
   s_svn_regex = '[._]svn'
   _regex = re.compile(s_regex)
   svn_regex = re.compile(s_svn_regex)
   files = [f for f in os.listdir(os.path.abspath(fpath)) if _regex.search(f)]
   rejects = [f for f in os.listdir(os.path.abspath(fpath)) if (not _regex.search(f)) and (not svn_regex.search(f)) and (f.find('__init__.') == -1) and (f.find('dlib') == -1)]
   if (len(rejects) > 0):
      print >>sys.stderr, '(%s) :: Rejected daemon files are "%s" using (not "%s") and (not "%s").  PLS check the file names to ensure your daemons will be executed as planned.' % (_name,rejects,s_regex,s_svn_regex)
   return files

def getNormalizedDaemons(prefix, fpath):
   h = lists.HashedLists()

   fs = []
   dms = getDaemons(prefix, fpath)
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

def getNormalizedDaemonNamespaces(prefix, fpath):
   return [f.split('.')[0] for f in getNormalizedDaemons(prefix, fpath)]

def execDaemon(f, dpath=None, _logging=None):
   _import_error = False
   try:
      exec "import " + f
   except ImportError:
      _import_error = True
      exc_info = sys.exc_info()
      info_string = '\n'.join(traceback.format_exception(*exc_info))
      if (_logging):
         _logging.error(info_string)
      else:
         print >>sys.stderr, info_string

   info_string = '_import_error=%s' % _import_error
   if (_logging):
      _logging.warning(info_string)
   else:
      print >>sys.stderr, info_string

   if (not _import_error):
      _metadata[f] = lists.HashedLists2()
      try:
         v = '%s._metadata' % (f)
         vv = eval(v)
         print '%s=[%s]' % (v,vv)
         _metadata[f] = lists.HashedLists2(vv)
         v = '%s.data_hook("%s")' % (f,dpath if (sys.platform[:3] != 'win') else dpath.replace(os.sep,'/'))
         vv = eval(v)
         print '%s=[%s]' % (v,vv)
      except AttributeError:
         pass
      except ImportError:
         exc_info = sys.exc_info()
         info_string = '\n'.join(traceback.format_exception(*exc_info))
         if (_logging):
            _logging.error(info_string)
         else:
            print >>sys.stderr, info_string

def execDaemons(prefix, fpath, dpath=None, _logging=None):
   for f in getNormalizedDaemonNamespaces(prefix, fpath):
      execDaemon("%s.%s" % (prefix,f.split('.')[0]), dpath=dpath, _logging=_logging)

