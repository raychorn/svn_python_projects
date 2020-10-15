# Django settings for mysite project.

from vyperlogix.django import django_utils

import os

ADMINS = (
    ('Admin', 'support@vyperlogix.com'),
)

MANAGERS = ADMINS

from vyperlogix.products import keys

DATABASE_ENGINE = 'mysql'                            # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.

_SQL2005_symbol = 'SQL2005'
_WEB20082_symbol = 'WEB20082'

DATABASE_SOURCE = _WEB20082_symbol

if (django_utils._cname in ['undefined3']):
    DATABASE_NAME = 'vyperlogix2'                         # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'                                # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61623030')  # Not used with sqlite3.
    if (DATABASE_SOURCE == _SQL2005_symbol):
        DATABASE_HOST = '127.0.0.1'                       # Set to empty string for localhost. Not used with sqlite3.
        DATABASE_PORT = '3307'                            # Set to empty string for default. Not used with sqlite3.
    elif (DATABASE_SOURCE == _WEB20082_symbol):
        DATABASE_HOST = '127.0.0.1'                       # Set to empty string for localhost. Not used with sqlite3.
        DATABASE_PORT = '3306'                            # Set to empty string for default. Not used with sqlite3.
    #DATABASE_HOST = 'SQL2005'                            # Set to empty string for localhost. Not used with sqlite3.
    #DATABASE_PORT = '3307'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
elif (django_utils.is_Production or django_utils.is_Staging or (django_utils._cname in ['ubuntu4.web20082'])):
    DATABASE_NAME = 'vyperlogix2'                        # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'                               # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61623030') # Not used with sqlite3.
    DATABASE_HOST = 'localhost'                          # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = False if (django_utils._cname in ['ubuntu4.web20082']) else True
    TEMPLATE_DEBUG = DEBUG
elif (django_utils.is_Production or django_utils.is_Staging or (django_utils._cname in ['raychorn-ubuntu-desktop'])):
    DATABASE_NAME = 'vyperlogix2'                        # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'                               # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61623030') # Not used with sqlite3.
    DATABASE_HOST = 'web2008'                            # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3307'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = False if (django_utils._cname in ['raychorn-ubuntu-desktop']) else True
    TEMPLATE_DEBUG = DEBUG
else:
    print 'WARNING: %s' % (django_utils._cname)
    
from vyperlogix.django import tabs
_navigation_menu_types = tabs._navigation_menu_types
_NAVIGATION_MENU_TYPE = 0
NAVIGATION_MENU_TYPE = _navigation_menu_types[_NAVIGATION_MENU_TYPE]
NAVIGATION_TYPE = 'auto'

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1  # dynamically set based on the requesting domain...

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

USE_MULTITHREADED_SERVER = True

SESSION_COOKIE_SECURE = False #(django_utils.isProduction(django_utils._cname) or django_utils.isStaging(django_utils._cname))

_ROOT_ = os.path.dirname(__file__)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(_ROOT_, 'static')

RIBBONS_ROOT = os.path.join(MEDIA_ROOT,os.sep.join(['images', 'ribbons']))

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = "?\\hjeLQXv'4xi2ZTTY<|\x0c(tP\nEHZXU[/(]W6h-J}IO\ns3\rMIx|\tsd0%hk`>WY6\tB[l\t}~CY%Q)cB*\x0bU@]8#~e,1&gjq\t!W\tW(\x0bK\x0c-7\x0bRi1&]ei>PWSTlRSf.&`4~363\x0b"

# BEGIN: Generate a new SECRET_KEY using the block of code...
#from vyperlogix.misc import GenPasswd
#SECRET_KEY = GenPasswd.GenPasswd(length=128,chars=GenPasswd.chars_printable)
# END!   Generate a new SECRET_KEY using the block of code...

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

# List of middleware classes to use.  Order is important; in the request phase,
# this middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    #'vyperlogix.django.middleware.VyperCMS.VyperOptimizeMiddleware',
)

IS_CACHING_CONTENT = (django_utils.isProduction(django_utils._cname) or django_utils.isStaging(django_utils._cname))
if (IS_CACHING_CONTENT):
    CACHE_TIMER = 60 * 15
    CACHE_BACKEND = 'memcached://127.0.0.1:11211/?timeout=%s' % (CACHE_TIMER)
    CACHE_MIDDLEWARE_SECONDS = CACHE_TIMER
    
    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
    MIDDLEWARE_CLASSES.insert(0,'django.middleware.cache.UpdateCacheMiddleware')
    MIDDLEWARE_CLASSES.append('django.middleware.cache.FetchFromCacheMiddleware')
    MIDDLEWARE_CLASSES = tuple(MIDDLEWARE_CLASSES)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.sitemaps',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'views',
    'content',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = django_utils.seek_installed_apps(_ROOT_,INSTALLED_APPS=INSTALLED_APPS)

