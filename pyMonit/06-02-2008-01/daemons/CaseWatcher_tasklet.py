#Tasklet

import os,sys
import logging
from vyperlogix.logging import standardLogging
from vyperlogix.misc import _utils
from vyperlogix.oodb import *
import traceback

from dlib import spawn_program

def dummy(args):
  pass

# BEGIN: METADATA
_run_on_computer = ['tide2.magma-da.com']
_tasklet_name = 'CaseWatcher'
_run_frequency = 600
_is_verbose = False
_fpath = '/root/@utils/pyDaemon/CaseWatcher.sh'
_description = 'Run %s every %d seconds.' % (_tasklet_name,_run_frequency)
_callback = dummy

_metadata = {}
_metadata['_run_on_computer'] = _run_on_computer
_metadata['_tasklet_name'] = _tasklet_name
_metadata['_run_frequency'] = _run_frequency
_metadata['_is_verbose'] = _is_verbose
_metadata['_fpath'] = _fpath
_metadata['_description'] = _description
# END! METADATA

def process_tasklet(m):
  try:
    m.spawn(_fpath,_tasklet_name,_run_frequency)
  except:
    exc_info = sys.exc_info()
    info_string = '\n'.join(traceback.format_exception(*exc_info))
    logging.error(info_string)

def tasklet(isVerbose,callback=dummy):
  global _is_verbose
  global _callback
  _is_verbose = isVerbose
  logFileName = os.sep.join([os.path.abspath('.'),'%s.log' % (_tasklet_name)])
  _name = _utils.funcName()
  print '(%s.%s) :: logFileName=[%s]' % (_tasklet_name,_name,logFileName)
  print '(%s.%s) :: _is_verbose=[%s]' % (_tasklet_name,_name,_is_verbose)
  
  standardLogging.standardLogging(logFileName)
  
  m = spawn_program.SpawnProgram()
  m.metadata = _metadata
  m.callback = process_tasklet
  m.callback2 = callback
  m.process_loop()

if (__name__ == '__main__'):
    print '(c). Copyright 1990-2014, Vyper Logix Corp., All Rights Reserved., Published under Creative Commons License (http://creativecommons.org/licenses/by-nc/3.0/) restricted to non-commercial educational use only., See also: http://www.VyperLogix.com and http://python2.near-by.info for details.'
    
