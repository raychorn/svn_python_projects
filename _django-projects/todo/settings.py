# Django settings for mysite project.

from vyperlogix.django import django_utils

import os

ADMINS = (
    ('Admin', 'support@vyperlogix.com'),
)

MANAGERS = ADMINS

from vyperlogix.products import keys

DATABASE_ENGINE = 'mysql'                            # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.

_cname = ''
try:
    import socket
    _cname = socket.gethostbyaddr(socket.gethostbyname(socket.gethostname()))[0]
except ImportError:
    pass

if (_cname in ['UNDEFINED3']):
    DATABASE_NAME = 'todo'                               # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'                               # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61623030') # Not used with sqlite3.
    DATABASE_HOST = '127.0.0.1'                          # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
elif (_cname in ['id3859.unmeteredservers.com']):
    DATABASE_NAME = 'todo'                               # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'                               # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61623030') # Not used with sqlite3.
    DATABASE_HOST = '127.0.0.1'                          # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
else: # running in the Google App Engine
    print 'WARNING: %s' % (_cname)
    
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

CACHE_TIMER = 60 * 15
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

SESSION_COOKIE_SECURE = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'static')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'RZl&.^gA+w4o&u=JD`b\\>GqOUj{qa6QXR.[d4^]y\\%>CzHW(m_y:Zo91f?4a"nqcqOm64p,!wXl\\NNH\\(qU[a2,__\'$>4-Q|>G;;AHPIB:jm@vlaxXG_SX?hns;$(B@!'

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

