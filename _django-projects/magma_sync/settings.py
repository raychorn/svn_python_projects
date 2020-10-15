# Django settings for mysite project.

import os

ADMINS = (
    ('Admin', 'support@vyperlogix.com'),
)

MANAGERS = ADMINS

from vyperlogix.products import keys

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0]
if (_cname.lower() == 'web22.webfaction.com'):
    DATABASE_ENGINE = 'mysql'                            # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'raychorn_msync'                     # Or path to database file if using sqlite3.
    DATABASE_USER = 'raychorn_msync'                     # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61623030') # Not used with sqlite3.
    DATABASE_HOST = 'localhost'                          # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    
if (_cname.lower() == 'undefined3'):
    DATABASE_ENGINE = 'mysql'                            # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'vyperlogix'                         # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'                               # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61623030') # Not used with sqlite3.
    DATABASE_HOST = 'sql2005'                            # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    
if (_cname.lower() == 'rhorn.ad.magma-da.com'.lower()):
    DATABASE_ENGINE = 'mysql'                            # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'django_magmasync'                   # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'                               # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61626F6F') # Not used with sqlite3.
    DATABASE_HOST = 'localhost'                          # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    
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
SECRET_KEY = ':L3RM]n9;v(n$sMT+Yo0ohN02PF1x]Y}HkEEg?r8<78f9?>E]&d}W3BQB./m3"$~bR.".9=}fcqI=xstO/0FqCOPYLlFB)NR\\"K\\|Hcyg*{;frQyD>@r>us:pC6}q8sR'

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
    #'logger.LoggingMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace(os.sep,'/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'magmaSync.views'
)

ROOT_URLCONF = 'magmaSync.urls'
handler404 = 'magmaSync.views.default.handle_404'
