import logging

from vyperlogix.misc import _utils

class DjangoServiceMiddleware(object):
    """
    Request-phase cache middleware that checks to make sure the Cache server is running.
    Starting it if it is not

    Must be first in the middleware stack so it can check before anything else runs
    """
    def __status_name__(self,status):
        from vyperlogix.services import _win32service
        if (status == _win32service.STOPPED):
            return 'STOPPED'
        elif (status == _win32service.STARTING):
            return 'STARTING'
        elif (status == _win32service.RUNNING):
            return 'RUNNING'
        elif (status == _win32service.STOPPING):
            return 'STOPPING'
        return None
    
    def __restart_service__(self,service_name,callback=None):
        try:
            logging.info('_utils.isUsingWindows=%s, service_name=%s' % (_utils.isUsingWindows,str(service_name)))
            if (_utils.isUsingWindows) and (service_name is not None):
                from vyperlogix.services import _win32service
                if (_win32service.has_service_containing(service_name)):
                    service_fpath = _win32service.win32serviceutil.LocateSpecificServiceExe(service_name)
                    status = _win32service.win32serviceutil.QueryServiceStatus(service_name)[1]
                    logging.info('service_fpath=%s, status=%s' % (service_fpath,self.__status_name__(status)))
                    if (status == _win32service.STOPPED):
                        logging.info('StartService "%s".' % (service_name))
                        _win32service.win32serviceutil.StartService(service_name)
                    elif (status == _win32service.RUNNING):
                        logging.info('RestartService "%s".' % (service_name))
                        _win32service.win32serviceutil.RestartService(service_name,waitSeconds=1)
            elif (callable(callback)):
                callback(service_name)
            else:
                logging.error('Not running in Windows or no callback was used so someone needs to write some code.')
        except Exception, ex:
            logging.warning(_utils.formattedException(details=ex))
    