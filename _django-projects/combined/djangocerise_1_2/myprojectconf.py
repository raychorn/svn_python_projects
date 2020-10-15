###########################################################################
# Configuration
#
import os, sys

from vyperlogix.misc import _utils

_root_ = os.path.dirname(__file__)

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()

isProduction = (_cname in ['ubuntu.localdomain','ubuntu2.gateway.2wire.net','ubuntu3.gateway.2wire.net'])

DJANGO_SETTINGS = 'combined%s.settings' % ('.django' if (not isProduction) else '')

#if (not isProduction):
    #print 'BEGIN: (***)'
    #for p in sys.path:
        #print '%s' % (p)
    #print 'END !'

# Django settings
DJANGO_SERVE_ADMIN = True # Serve admin files

# Server settings
IP_ADDRESS = '127.0.0.1'
PORT = 8888
SERVER_NAME = 'localhost'
SERVER_VERSION = 'VyperDjango'
SERVER_THREADS = 1 if (not isProduction) else 1000
# Change it to True if you want it to run as daemon, if you use a
# daemon.sh file you should also change it to True
RUN_AS_DAEMON = False
DAEMON_RUN_DIR = '/' # The daemon will change directory to this one
                     # this is needed to prevent unmounting your
                     # disk.

# Log settings
from vyperlogix.misc import _utils
LOGFILE = os.sep.join([_root_,'logs','webserver_%s.log' % (_utils.timeStampLocalTimeForFileName())])
_utils.makeDirs(LOGFILE)
LOGLEVEL = 'INFO' # if DEBUG is True, overwritten to DEBUG
DEBUG = True

# It must match with the path given in your daemon.sh file if you are
# using a daemon.sh file to control the server. 
PIDFILE = '/var/run/django/%s_{port}.pid' % (os.path.dirname(_root_).split(os.sep)[-1])

# Launch as root to dynamically chown
SERVER_USER = 'nobody'
SERVER_GROUP = 'nobody'

# Enable SSL, if enabled, the certificate and private key must 
# be provided.
SSL = False
SSL_CERTIFICATE = '/full/path/to/certificate'
SSL_PRIVATE_KEY = '/full/path/to/private_key'

#
###########################################################################
