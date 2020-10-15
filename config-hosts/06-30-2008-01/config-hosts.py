import os, sys
from vyperlogix.sockets import pinger
from vyperlogix.misc import _utils
from vyperlogix.logging import standardLogging
import socket
import traceback

import logging

_hostname = 'C:/WINDOWS/system32/drivers/etc/hosts'

def setHostIfNotSetAlready(hostname,ip=''):
    if (os.path.exists(_hostname)):
        fIn = open(_hostname,'r')
        lines = [l.strip() for l in fIn.readlines()]
        _lines = ['\t'.join(t) for t in [l.split() for l in lines] if (len(t) > 0) and (t[-1] != hostname)]
        fIn.close()
        aLine = '%s\t%s' % (ip,hostname)
        fOut = open(_hostname,'w')
        fOut.writelines('\n'.join(_lines))
        if (len(ip) > 0):
            fOut.write('\n%s' % aLine)
            logging.info('Added "%s" to "%s".' % (aLine,_hostname))
        else:
            logging.info('Removed all references to "%s".' % (hostname))
        fOut.flush()
        fOut.close()

def removeHostIfSetAlready(hostname):
    try:
        setHostIfNotSetAlready(hostname) # removes the host because ip is not specified...
    except:
        exc_info = sys.exc_info()
        info_string = '\n'.join(traceback.format_exception(*exc_info))
        logging.error('(%s) hostname=%s, Reason: %s' % (_utils.funcName(),hostname,info_string))

if (__name__ == '__main__'):
    if (os.environ.has_key('cwd')):
        _cwd = os.environ['cwd']
    elif (len(sys.argv) > 0):
        _cwd = os.path.dirname(sys.argv[0])
    else:
        _cwd = ''
    
    print '_cwd=%s' % _cwd

    name = _utils.getProgramName()
    _log_path = _utils.safely_mkdir_logs(_cwd)
    logFileName = os.sep.join([_log_path,'%s.log' % (name)])
    
    _logging = logging.INFO
    
    standardLogging.standardLogging(logFileName,_level=_logging,isVerbose=True)
    
    logging.warning('Logging to "%s" using level of "%s:.' % (logFileName,standardLogging.explainLogging(_logging)))

    svn_dyn_o_saur_com = 'svn.dyn-o-saur.com'
    addr1 = '192.168.1.68'
    sql2005 = 'SQL2005'
    try:
        host1 = pinger.socket.gethostbyname(svn_dyn_o_saur_com)
    except socket.gaierror:
        host1 = ''
    try:
        host2 = pinger.socket.gethostbyname(sql2005)
    except socket.gaierror:
        host2 = ''
    logging.info('host1 is "%s", host2 is "%s".' % (host1,host2))
    if (len(host2) > 0) and (host1 != host2):
        logging.info('Setting the host to allow local access to %s.' % (svn_dyn_o_saur_com))
        setHostIfNotSetAlready(svn_dyn_o_saur_com,host2)
    else:
        removeHostIfSetAlready(svn_dyn_o_saur_com)
    
