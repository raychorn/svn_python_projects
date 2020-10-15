import sys
import types
import logging
from vyperlogix import oodb
from vyperlogix.misc import _utils
from vyperlogix import misc
from vyperlogix.misc.threadpool import *
import traceback
from vyperlogix.hash import lists

__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

                   All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

_threadQ = ThreadQueue(1)

def dummy():
  pass

@threadify(_threadQ)
def execute_callback2(m):
  try:
    m.callback2(m.metadata)
  except:
    exc_info = sys.exc_info()
    info_string = '\n'.join(traceback.format_exception(*exc_info))
    logging.error(info_string)
  pass

class PyDaemonFramework:
  __dbx__ = None
  __tasklet_name__ = ''
  __callback__ = dummy
  __metadata__ = lists.HashedLists2()
  __callback2__ = dummy
  
  def _c_dbxName(self,name=''):
    if (len(name) > 0):
      toks = name.split('.')
      toks[0] += self.suffix
      return '.'.join(toks)
    else:
      return ''
  
  def dbxName(self):
    import os
    return os.sep.join([os.path.abspath('.'),'%s.dbx' % (self.tasklet_name)])

  def c_dbxName(self):
    return self._c_dbxName(self.dbxName())
  
  def record_results(self,results):
    if (results != None):
      _name = misc.funcName()
      _dbx = self.dbx
      ts = _utils.timeStamp()
      nk1 = len(_dbx.keys())
      _keys = _dbx.normalizedSortedKeys()
      if (len(_keys) > 0):
        try:
          _last_i = int(_keys[0].split(',')[0])
        except:
          _last_i = -1
      else:
        _last_i = 0
      if (_last_i > -1):
        _dbx['%d,%s' % (_last_i+1,ts)] = results
        nk2 = len(_dbx.keys())
        logging.info('(%s) :: There were %d key%s but now %d key%s in the file named %s.' % (_name,nk1,'s' if nk1 > 1 else '',nk2,'s' if nk2 > 1 else '',self.c_dbxName))
        for k in _keys[0:5]:
          logging.info('(%s) :: %s.' % (_name,k))
        _dbx.sync()
        _dbx.close()
    else:
      logging.warning('Unable to record the results due to there are no results to record because results are of type "%s".' % (type(results)))
  
  def process_loop(self):
    while (1):
      _beginTS = _utils.timeSeconds()
      try:
        self.callback(self)
      except:
        exc_info = sys.exc_info()
        info_string = '\n'.join(traceback.format_exception(*exc_info))
        logging.error(info_string)
        
      tasklet_name = self.metadata['_tasklet_name'] if (self.metadata.has_key('_tasklet_name')) else '*UNDEFINED*'
      freq = self.metadata['_run_frequency'] if (self.metadata.has_key('_run_frequency')) else -1
      if (freq > -1):
        _elapsedTS = _utils.timeSeconds()-_beginTS
        _secs = freq - _elapsedTS
        logging.info("(%s) :: That took %-4.2f second%s, sleeping for %-4.2f second%s." % (tasklet_name,_elapsedTS,'s' if _elapsedTS > 1 else '',_secs,'s' if _secs > 1 else ''))

        try:
          execute_callback2(self)
        except:
          exc_info = sys.exc_info()
          info_string = '\n'.join(traceback.format_exception(*exc_info))
          logging.error(info_string)

        if (_secs > 0):
          time.sleep(_secs)
      else:
        logging.warning('Unable to reschedule the tasklet "%s" due to a problem with the _run_frequency value which is "%s".' % (tasklet_name,freq))
    pass

  def get_suffix(self):
    return '_c'

  def get_dbx(self):
    self.__dbx__ = oodb.PickledHash(self.c_dbxName(),oodb.PickleMethods.useSafeSerializer)
    return self.__dbx__
  
  def set_dbx(self,handle):
    self.__dbx__ = handle

  def get_tasklet_name(self):
    return self.__tasklet_name__
  
  def set_tasklet_name(self,name):
    self.__tasklet_name__ = name
    
  def get_callback(self):
    return self.__callback__
  
  def set_callback(self,func):
    self.__callback__ = func if (callable(func)) else dummy
    
  def get_callback2(self):
    return self.__callback2__
  
  def set_callback2(self,func):
    self.__callback2__ = func if (callable(func)) else dummy

  def get_metadata(self):
    return self.__metadata__
  
  def set_metadata(self,data):
    self.__metadata__ = data if (isinstance(data,dict)) else lists.HashedLists2()
    
  suffix = property(get_suffix)
  dbx = property(get_dbx,set_dbx)
  tasklet_name = property(get_tasklet_name,set_tasklet_name)
  callback = property(get_callback,set_callback)
  callback2 = property(get_callback2,set_callback2)
  metadata = property(get_metadata,set_metadata)
