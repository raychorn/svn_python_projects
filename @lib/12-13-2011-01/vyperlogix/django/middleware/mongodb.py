import socket
import subprocess

import logging

from django.conf import settings
from django.core.cache import cache

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix import mongodb

from vyperlogix.django.middleware.ServiceMiddlewareFramework import DjangoServiceMiddleware

class CheckMongoDb(DjangoServiceMiddleware):
    """
    Request-phase cache middleware that checks to make sure the Cache server is running.
    Starting it if it is not

    Must be first in the middleware stack so it can check before anything else runs
    """
    def __init__(self):
        self.mongodb_test = settings.MONGODB_TEST
        self.mongodb_mongoose = settings.SLEEPY_MONGOOSE
        self.mongodb_service_name = settings.MONGODB_SERVICE_NAME
        try:
            self.response = mongodb.SleepyMongoose(self.mongodb_mongoose).__http_gets__(self.mongodb_test)
        except Exception, ex:
            self.response = None
            logging.warning(_utils.formattedException(details=ex))
        try:
            self.results = mongodb.SleepyMongoose(self.mongodb_mongoose).connect()
        except Exception, ex:
            self.results = None
            logging.warning(_utils.formattedException(details=ex))
        logging.info('self.mongodb_mongoose=%s, self.mongodb_service_name=%s' % (self.mongodb_mongoose,self.mongodb_service_name))

    def process_request(self, request):
        """
            This is run for every request, it checks to see if it can get a
            defined item out of the cache, if that fails it tries to set it
            Failing that it decides the server is probably crashed, but
            goes though and attempts to connect to the server. Failing a connection
            It will launch a new server.
        """
        if not misc.isDict(self.results) or (not self.results.has_key('ok')) or (self.results['ok'] < 1):
            # Later-on we will be wanting to make sure the Sleepy Mongoose is also running...
            logging.warning('mongod service is not running, start it !')
            self.__restart_service__(self.mongodb_service_name)
            return None
            
        return None