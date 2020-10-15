import os,sys
import logging
from vyperlogix.logging import standardLogging
from vyperlogix.misc import _utils
from vyperlogix.daemon import framework
import socket

class SiteMonitor(framework.PyDaemonFramework):
  def __init__(self):
    self._error_patterns_d = {'502':'<title>502 Proxy Error</title>'}

  def fetchFromURL(self,u):
    import httplib
    import urlparse
    _name = _utils.funcName()
    url_o = urlparse.urlparse(u)
    conn = httplib.HTTPConnection(url_o.hostname, url_o.port)
    try:
      conn.request("GET", "%s%s?%s" % (url_o.path, url_o.params, url_o.query))
    except socket.gaierror:
      logging.error("(%s) :: The url '%s' contains an unknown hostname" % (_name,u))
    except socket.error:
      logging.error("(%s) :: The url '%s' contains an host/port combo that did not respond" % (_name,u))
    
    resp = conn.getresponse()
    if (resp.status != 200):
      if (resp.status == 302):
        logging.info("(%s) :: The url '%s' returned %d and this is normal." % (_name,u,resp.status))
        _head = dict(resp.getheaders())
        if (_head.has_key('location')):
          _location = _head['location']
          if (_location != u):
            logging.info('(%s) :: Following redirection to "%s" from "%s".' % (_name,_location,u))
            self.fetchFromURL(_location)
      else:
        logging.error("(%s) :: The url '%s' did not return 200 but it did return %d" % (_name,u,resp.status))
    return (url_o,resp)

  def monitor(self,url,tasklet_name='',freq=30):
    import time
    _name = _utils.funcName()
    _bool_tasklet_name = len(tasklet_name) > 0
    if (_bool_tasklet_name):
      self.tasklet_name = tasklet_name
      logging.info("(%s) :: Checking %s for signs of life." % (_name,url))
      _beginTS = _utils.timeSeconds()
      url_o,resp = self.fetchFromURL(url)
      _elapsedTS = _utils.timeSeconds()-_beginTS
      s = resp.read()
      _status_code = '%d' % resp.status
      _pattern = ''
      if (self._error_patterns_d.has_key(_status_code)):
        _pattern = self._error_patterns_d[_status_code]
      _isClassified = False
      if (len(_pattern) > 0):
        _isClassified = s.find(_pattern) > -1
      self.record_results({'url_o':[n for n in url_o], 'resp':[resp.status,_pattern if _isClassified else s if resp.status != 200 else s if (resp.status == 302) or len(s) < 1024 else 'OK' if (resp.status != 302) else s],'seconds':_elapsedTS})
    elif (not _bool_tasklet_name):
      logging.error('(%s) :: This function requires the tasklet_name argument to be something other than "%s".' % (_name,tasklet_name))
    pass

