import os,sys
import logging
from vyperlogix.logging import standardLogging
from vyperlogix.misc import _utils
from vyperlogix.daemon import framework
import socket

from vyperlogix.mail import mailServer
from vyperlogix.mail import message

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class SpawnProgram(framework.PyDaemonFramework):
    def __init__(self):
        pass

    def spawn(self,fpath,tasklet_name='',freq=30):
        import time
        _name = _utils.funcName()
        _bool_tasklet_name = len(tasklet_name) > 0
        if (_bool_tasklet_name):
            self.tasklet_name = tasklet_name
            logging.warning("(%s) :: Spawning %s." % (_name,fpath))
            _beginTS = _utils.timeSeconds()
            if (os.path.exists(fpath)):
                root_details = os.path.dirname(fpath)
                fOut_details = open(os.sep.join([root_details,'%s.log' % (tasklet_name)]),'w')
                try:
                    _details = _utils.spawnProcessWithDetails(fpath,fOut=fOut_details)
                finally:
                    fOut_details.flush()
                    fOut_details.close()
                    _details = _utils.readFileFrom(fOut_details.name)
                if (len(_details) > 0):
                    logging.warning(_details)
                    mailServer = mailServer.AdhocServer('tide2.magma-da.com:8025')
                    msg = message.Message('salesforce-support@magma-da.com','rhorn@magma-da.com',_details,'pyMonit Tasklet Results for "%s".' % (tasklet_name))
                    mailServer.sendEmail(msg)
            else:
                logging.warning('(%s) :: This function requires the fpath argument to be something other than "%s".' % (_name,fpath))
            _elapsedTS = _utils.timeSeconds()-_beginTS
            self.record_results({'fpath':fpath,'seconds':_elapsedTS})
        elif (not _bool_tasklet_name):
            logging.error('(%s) :: This function requires the tasklet_name argument to be something other than "%s".' % (_name,tasklet_name))
        pass

