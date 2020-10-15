# Django settings for mysite project.

from vyperlogix.django import django_utils

import os

ADMINS = (
    ('Admin', 'support@vyperlogix.com'),
)

MANAGERS = ADMINS

from vyperlogix.products import keys

DATABASE_ENGINE = 'mysql'                            # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.

if (django_utils._cname == 'web22.webfaction.com'):
    DATABASE_NAME = 'raychorn_vyper'                     # Or path to database file if using sqlite3.
    DATABASE_USER = 'raychorn_vyper'                     # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61623030') # Not used with sqlite3.
    DATABASE_HOST = 'localhost'                          # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
elif (django_utils._cname in ['undefined3']):
    DATABASE_NAME = 'vyperlogix'                         # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'                               # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61623030') # Not used with sqlite3.
    DATABASE_HOST = 'sql2005'                            # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
elif (django_utils._cname in ['rhorn2-srv.ad.magma-da.com']):
    DATABASE_NAME = 'vyperlogix'                         # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'                               # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61623030') # Not used with sqlite3.
    DATABASE_HOST = 'localhost'                            # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
elif (django_utils._cname == 'Misha-Lap.ad.magma-da.com'.lower()):
    DATABASE_NAME = 'django_vyperlogix'                  # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'                               # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61626F6F') # Not used with sqlite3.
    DATABASE_HOST = 'localhost'                          # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
elif (django_utils.isProduction(django_utils._cname) or (django_utils._cname in ['raychorn-ubuntu-desktop'])):
    DATABASE_NAME = 'vyperlogix'                         # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'                               # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61623030') # Not used with sqlite3.
    DATABASE_HOST = 'sql2005.gateway.2wire.net'          # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
elif (django_utils._cname == 's15323947.onlinehome-server.com'):
    DATABASE_NAME = 'django_vyperlogix'                  # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'                               # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7369736B6F403736363024626F6F') # Not used with sqlite3.
    DATABASE_HOST = 'localhost'                          # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
else:
    print 'WARNING: %s' % (django_utils._cname)
    
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

SITE_ID = 1.0

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

USE_MULTITHREADED_SERVER = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'static').replace(os.sep,'/')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/'

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

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'views',
)

ROOT_URLCONF = 'urls'
handler404 = 'views.default.handle_404'

