import socket
import subprocess

import logging

from django.conf import settings
from django.core.cache import cache

from vyperlogix.misc import _utils

from vyperlogix.django.middleware.ServiceMiddlewareFramework import DjangoServiceMiddleware

class CheckCacheServer(DjangoServiceMiddleware):
    """
    Request-phase cache middleware that checks to make sure the Cache server is running.
    Starting it if it is not

    Must be first in the middleware stack so it can check before anything else runs
    """
    def __init__(self):
        self.cache_backend = settings.CACHE_BACKEND
        logging.info('self.cache_backend=%s' % (self.cache_backend))
        self.cache_service_name = self.cache_backend.split('://')[0] if (_utils.isUsingWindows) else None
        logging.info('self.cache_service_name=%s' % (self.cache_service_name))
        self.servers = self.cache_backend[self.cache_backend.index('//')+2 : self.cache_backend.rindex('/')].split(';')
        logging.info('self.servers=%s' % (self.servers))

    def process_request(self, request):
        """
            This is run for every request, it checks to see if it can get a
            defined item out of the cache, if that fails it tries to set it
            Failing that it decides the server is probably crashed, but
            goes though and attempts to connect to the server. Failing a connection
            It will launch a new server.
        """
        if not self.cache_backend.startswith('memcached'):
            logging.warning('Cannot understand settings.CACHE_BACKEND of "%s" !' % (self.cache_backend))
            return None
            
        alive = cache.get("test-connection")
        logging.info('alive=%s' % (alive))
        if not alive and not cache.set("test-connection", 1, 604800):        
            try:
                memcached = settings.CACHE_SERVER_STRING
            except AttributeError:
                memcached = "memcached -l %s -p %d -c 10 -d"
            logging.info('memcached=%s' % (memcached))
                
            for server in self.servers:
                ip, port = server.split(':')
                logging.info('ip:port=%s:%s' % (ip, port))
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                try:
                    s.connect((ip, int(port)))
                except socket.error, e:
                    # not running, start it
                    def handle_non_windows_service_restart():
                        cmd = memcached % (ip, int(port))
                        logging.info('Not running in Windows issuing "%s".' % (cmd))
                        subprocess.Popen(cmd, shell=True)
                    
                    logging.warning('memcached is not running, start it !')
                    self.__restart_service__(self.cache_service_name,callback=handle_non_windows_service_restart)
                finally:
                    s.close()
        
        return None