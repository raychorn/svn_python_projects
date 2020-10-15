# Django settings for mysite project.

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.url import _urllib2
from vyperlogix.django import django_utils

import os

ADMINS = (
    ('Admin', 'support@vyperlogix.com'),
)

VERSION = '1.0'

MANAGERS = ADMINS

SUPER_USER = 'raychorn@gmail.com'

from vyperlogix.products import keys

IS_PRODUCTION_WEB_SERVER = False
IS_NOT_LOGGED_IN = True
IS_LOGGED_IN = not IS_NOT_LOGGED_IN

CACHE_TIMER = 60 * 15
IS_CACHING_CONTENT = True

DOMAIN_NAME = django_utils.socket.gethostname()
print '1.DOMAIN_NAME=%s' % (DOMAIN_NAME)
if (DOMAIN_NAME in ['HPDV7-6163us','DGLYJ7V1','raychorn-VirtualBox','HORNRA3']):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'djangocloud',
            'USER' : 'root',
            'PASSWORD' : keys._decode('7065656B61623030'),
            'HOST' : '127.0.0.1',
            'PORT' : '33307',
        }
    }
    IS_PRODUCTION_SERVER = False
    LOCALHOST = '127.0.0.1:8888'
    MONGODB_ENDPOINT = '127.0.0.1:27017'
    SLEEPY_MONGOOSE = '127.0.0.1:27080'
    MONGODB_SERVICE_NAME = 'MongoDB'
    CURRENT_SITE = 'DjangoCloud.VyperLogix.Com'
    CACHE_BACKEND = 'memcached://127.0.0.1:11211/?timeout=%s' % (CACHE_TIMER)
    FILESYSTEM_TOP = 'J:/##nginx-windows' if (_utils.isUsingWindows) else '/'    
    DEBUG = True
elif (DOMAIN_NAME in ['HORNRA3']):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'djangocloud',
            'USER' : 'raychorn',
            'USER' : 'root',
            'PASSWORD' : keys._decode('7065656B61623030'),
            'HOST' : '127.0.0.1',
            'PORT' : '23337',
        }
    }
    IS_PRODUCTION_SERVER = True
    IS_PRODUCTION_WEB_SERVER = True
    LOCALHOST = '127.0.0.1:8002'
    MONGODB_ENDPOINT = '127.0.0.1:27017'
    SLEEPY_MONGOOSE = '127.0.0.1:27080'
    MONGODB_SERVICE_NAME = None #'MongoDB'
    CURRENT_SITE = 'DjangoCloud.VyperLogix.Com'
    CACHE_BACKEND = 'memcached://memcached1.fs7l9z.cfg.use1.cache.amazonaws.com:11211/?timeout=%s' % (CACHE_TIMER)
    FILESYSTEM_TOP = '/'    
    DEBUG = False
else: # Production
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'djangocloud',
            'USER' : 'raychorn',
            'PASSWORD' : keys._decode('7065656B61623030'),
            'HOST' : 'mysqldb1.c6ridqtz1twa.us-east-1.rds.amazonaws.com',
            'PORT' : '3306',
        }
    }
    IS_PRODUCTION_SERVER = True
    IS_PRODUCTION_WEB_SERVER = (DOMAIN_NAME.find('ip-10-190-122-29') > -1) and (DOMAIN_NAME.find('ip-10-202-210-94') == -1)
    LOCALHOST = '127.0.0.1:8001'
    MONGODB_ENDPOINT = '127.0.0.1:27017'
    SLEEPY_MONGOOSE = '127.0.0.1:27080'
    MONGODB_SERVICE_NAME = None #'MongoDB'
    CURRENT_SITE = 'DjangoCloud.VyperLogix.Com'
    CACHE_BACKEND = 'memcached://memcached1.fs7l9z.cfg.use1.cache.amazonaws.com:11211/?timeout=%s' % (CACHE_TIMER)
    FILESYSTEM_TOP = '/'    
    DEBUG = False
IS_NOT_PRODUCTION_WEB_SERVER = not IS_PRODUCTION_WEB_SERVER
print '2.DEBUG=%s' % (DEBUG)
print '3.DATABASES=%s' % (DATABASES)
print '4.IS_PRODUCTION_SERVER=%s' % (IS_PRODUCTION_SERVER)
print '5.IS_PRODUCTION_WEB_SERVER=%s' % (IS_PRODUCTION_WEB_SERVER)
print '5a.IS_NOT_PRODUCTION_WEB_SERVER=%s' % (IS_NOT_PRODUCTION_WEB_SERVER)
TEMPLATE_DEBUG = DEBUG

IS_HTTPS_REQUIRED = False

MONGODBS = 'gps_1M'
MONGODB_COLLECTION = 'num_connections'

MONGODB_TEST = None
print '6.MONGODB_ENDPOINT=%s' % (MONGODB_ENDPOINT)
if (misc.isString(MONGODB_ENDPOINT)):
    MONGODB_TEST = 'http://%s/test' % (MONGODB_ENDPOINT)
    s = _urllib2.get(MONGODB_TEST)
    if (len(s) == 0):
        MONGODB_TEST = MONGODB_ENDPOINT= None
print '7.MONGODB_ENDPOINT=%s' % (MONGODB_ENDPOINT)

print '8.SLEEPY_MONGOOSE=%s' % (SLEEPY_MONGOOSE)
if (misc.isString(SLEEPY_MONGOOSE)):
    u = 'http://%s/' % (SLEEPY_MONGOOSE)
    s = _urllib2.get(u)
    if (len(s) == 0):
        SLEEPY_MONGOOSE = None
print '9.SLEEPY_MONGOOSE=%s' % (SLEEPY_MONGOOSE)

ACCOUNT_ACTIVATION_DAYS = 10

__EMAIL_POST_ADDRESS__ = 'http://www.near-by.info/php/send_gmail3.php'

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = 'key-50npnx4bhglbohd-f60k00ottnzop6a8'
MAILGUN_SERVER_NAME = 'vyperlogix.com'

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1  # dynamically set based on the requesting domain...

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

USE_MULTITHREADED_SERVER = True

SESSION_COOKIE_SECURE = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'static')
print '10.MEDIA_ROOT=%s' % (MEDIA_ROOT)

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-static/'

# BEGIN: Generate a new SECRET_KEY using the block of code...
#from vyperlogix.misc import GenPasswd
#SECRET_KEY = GenPasswd.GenPasswd(length=128,chars=GenPasswd.chars_printable)
SECRET_KEY = '_Sp%o2oz%6.K+HFq?_AckQVWq9PwaK"b|O3|v4Y~$8!C,Hp\'SC:J+(Qlm)x*$Ije[_*0s5j2?EF?A~72wJu;pptB_K*2z%32g!p@5px?anT<a+Rxx]eEAfwxe!`L#)fY'
# END!   Generate a new SECRET_KEY using the block of code...

# BEGIN:  DO NOT CHANGE OR BAD EVIL THINGS WILL HAPPEN
APP_SESSION_KEY= '__xxx__'
# END!    DO NOT CHANGE OR BAD EVIL THINGS WILL HAPPEN

if (not DEBUG):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level':'INFO',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': 'logs/default.log' if (_utils.isUsingWindows) else '/var/log/djangocloud/default.log',
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
                'formatter':'standard',
            },  
            'request_handler': {
                    'level':'INFO',
                    'class':'logging.handlers.RotatingFileHandler',
                    'filename': 'logs/django_request.log' if (_utils.isUsingWindows) else '/var/log/djangocloud/django_request.log',
                    'maxBytes': 1024*1024*5, # 5 MB
                    'backupCount': 5,
                    'formatter':'standard',
            },
        },
        'loggers': {
    
            '': {
                'handlers': ['default'],
                'level': 'DEBUG',
                'propagate': True
            },
            'django.request': { # Stop SQL debug from logging to main logger
                'handlers': ['request_handler'],
                'level': 'DEBUG',
                'propagate': False
            },
        }
    }
    print '11.LOGGING=%s' % (LOGGING)
    print '12.LOGGING["handlers"]["default"]["filename"]=%s' % (LOGGING["handlers"]["default"]["filename"])
    print '13.LOGGING["handlers"]["request_handler"]["filename"]=%s' % (LOGGING["handlers"]["request_handler"]["filename"])

    default_filepath = os.path.dirname(LOGGING["handlers"]["default"]["filename"])
    print '14.default_filepath=%s --> (%s)' % (default_filepath,os.path.exists(default_filepath))
    if (not os.path.exists(default_filepath)):
        _utils.makeDirs(default_filepath)
        print '14a.default_filepath=%s --> (%s)' % (default_filepath,os.path.exists(default_filepath))
        if (not os.path.exists(default_filepath)):
            os.mkdir(default_filepath)
        assert os.path.exists(default_filepath) == True, '14. Oops, there is something wrong with your assumption #7a1.'
    
    request_filepath = os.path.dirname(LOGGING["handlers"]["request_handler"]["filename"])
    print '15.request_filepath=%s --> (%s)' % (request_filepath,os.path.exists(request_filepath))
    if (not os.path.exists(request_filepath)):
        _utils.makeDirs(request_filepath)
        print '15a.request_filepath=%s --> (%s)' % (request_filepath,os.path.exists(request_filepath))
        if (not os.path.exists(request_filepath)):
            os.mkdir(request_filepath)
        assert os.path.exists(request_filepath) == True, '15. Oops, there is something wrong with your assumption #7b1.'
else:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format':
        '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(asctime)s  %(module)s %(message)s'
            },
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': True,
            },
            'app': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }    

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#    'django.template.loader.find_template',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.contrib.messages.context_processors.messages")

# List of middleware classes to use.  Order is important; in the request phase,
# this middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    #'vyperlogix.django.middleware.mongodb.CheckMongoDb',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',
)

from django.contrib.messages import constants as message_constants
MESSAGE_LEVEL = message_constants.DEBUG if (TEMPLATE_DEBUG) else message_constants.ERROR

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

if (IS_CACHING_CONTENT):
    CACHE_MIDDLEWARE_SECONDS = CACHE_TIMER
    
    #CACHE_SERVER_STRING = "memcached -l %s -p %d -c 10 -d"  # used only by non-Windows installations where memcached is present locally...
    
    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
    MIDDLEWARE_CLASSES.insert(0,'vyperlogix.django.middleware.memcached.CheckCacheServer')
    MIDDLEWARE_CLASSES.insert(1,'django.middleware.cache.UpdateCacheMiddleware')
    MIDDLEWARE_CLASSES.insert(2,'django.middleware.cache.FetchFromCacheMiddleware')
    MIDDLEWARE_CLASSES = tuple(MIDDLEWARE_CLASSES)

from vyperlogix import misc
cb = lambda foo:foo.find('templates') > -1 if (misc.isString(foo)) else false
from vyperlogix.django.findDjangoTemplateDirsIn import findDjangoTemplateDirsIn
TEMPLATE_DIRS = []
for t in findDjangoTemplateDirsIn(os.path.dirname(__file__),[],callback = cb):
    TEMPLATE_DIRS.append(t)
TEMPLATE_DIRS = tuple(TEMPLATE_DIRS)

INSTALLED_APPS = (
    'django.contrib.sitemaps',
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'views',
    'users',
)

if (TEMPLATE_DEBUG):
    INSTALLED_APPS = list(INSTALLED_APPS)
    INSTALLED_APPS.append('django.contrib.admin')
    INSTALLED_APPS = tuple(INSTALLED_APPS)

ROOT_URLCONF = 'urls'

