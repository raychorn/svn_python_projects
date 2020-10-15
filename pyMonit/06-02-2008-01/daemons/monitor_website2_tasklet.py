#Tasklet

import os,sys
import logging
from vyperlogix.logging import standardLogging
from vyperlogix.misc import _utils
from vyperlogix.oodb import *
import traceback

from dlib import site_monitor

def dummy(args):
  pass

# BEGIN: METADATA
_run_on_computer = ['UNDEFINED3','MISHA-LAP','ubuntu','river.magma-da.com']
_tasklet_name = 'www_monitor2'
_run_frequency = 30
_is_verbose = False
_salesforce_url = 'https://cs1.salesforce.com/a1JS0000000000vMAA'
_url = 'https://tide.magma-da.com/contact/login_form'
_description = 'Monitor the URL "%s" for activity every %d seconds.' % (_url,_run_frequency)

_metadata = {}
_metadata['_run_on_computer'] = _run_on_computer
_metadata['_tasklet_name'] = _tasklet_name
_metadata['_run_frequency'] = _run_frequency
_metadata['_is_verbose'] = _is_verbose
_metadata['_salesforce_url'] = _salesforce_url
_metadata['_description'] = _description
_metadata['_url'] = _url
# END! METADATA

def process_tasklet(m):
  try:
    m.monitor(_url,_tasklet_name,_run_frequency)
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
  
  m = site_monitor.SiteMonitor()
  m.metadata = _metadata
  m.callback = process_tasklet
  m.callback2 = callback
  m.process_loop()

if (__name__ == '__main__'):
    print '(c). Copyright 1990-2014, Vyper Logix Corp., All Rights Reserved., Published under Creative Commons License (http://creativecommons.org/licenses/by-nc/3.0/) restricted to non-commercial educational use only., See also: http://www.VyperLogix.com and http://python2.near-by.info for details.'
