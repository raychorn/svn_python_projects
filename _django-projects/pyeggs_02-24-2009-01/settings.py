# Django settings for mysite project.

import os, sys

ADMINS = (
    ('Admin', 'support@vyperlogix.com'),
)

MANAGERS = ADMINS

from vyperlogix.products import keys

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()
if (_cname == 'web22.webfaction.com'):
    DATABASE_ENGINE = 'mysql'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'raychorn_pyeggs' # Or path to database file if using sqlite3.
    DATABASE_USER = 'raychorn_pyeggs' # Not used with sqlite3.
    DATABASE_PASSWORD = 'peekab00'    # Not used with sqlite3.
    DATABASE_HOST = 'localhost'       # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'            # Set to empty string for default. Not used with sqlite3.
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
elif (_cname == 'undefined3'):
    DATABASE_ENGINE = 'mysql'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'pyeggs'          # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'            # Not used with sqlite3.
    DATABASE_PASSWORD = 'peekab00'    # Not used with sqlite3.
    DATABASE_HOST = 'sql2005'         # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'            # Set to empty string for default. Not used with sqlite3.
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
elif (_cname == 'misha-lap.ad.magma-da.com'):
    DATABASE_ENGINE = 'mysql'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'pyeggs'          # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'            # Not used with sqlite3.
    DATABASE_PASSWORD = 'peekaboo'    # Not used with sqlite3.
    DATABASE_HOST = 'localhost'       # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'            # Set to empty string for default. Not used with sqlite3.
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
elif (_cname == 'ubuntu.localdomain'):
    DATABASE_ENGINE = 'mysql'                            # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'pyeggs'                             # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'                               # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61623030') # Not used with sqlite3.
    DATABASE_HOST = 'sql2005.gateway.2wire.net'          # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
elif (_cname == 's15323947.onlinehome-server.com'):
    DATABASE_ENGINE = 'mysql'                            # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'django_pyeggs'                      # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'                               # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7369736B6F403736363024626F6F') # Not used with sqlite3.
    DATABASE_HOST = 'localhost'                          # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
else:
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

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = 'C:\\Apache228\\htdocs\\pyeggs\\media\\'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
# from vyperlogix.misc import GenPasswd
# print GenPasswd.GenPasswd(length=128)
SECRET_KEY = 'o7H5iYU3(C?8y[,-:y[Q|2ZU9Eb;k23iT`eK{S)zeaJ]Qbh7ndH[\\uoAh`qfx\\?$Y3;3H2Qh.mBYg&;8{p7NLt"%fs6S&{$_,W]-O&M=;`]GTraez]+Wykwn!\\I@peG3'

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
    os.path.join(os.path.dirname(__file__), 'templates').replace(os.sep,'/'),
)
    
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    '%sviews' % ('vyperlogix_site.' if (_cname.lower() == 'web22.webfaction.com') else 'vyperlogix_site.django.' if (_cname == 'undefined3') else ''),
)

if (_cname.lower() == 'web22.webfaction.com'):
    ROOT_URLCONF = 'pyeggs.urls'
    handler404 = 'pyeggs.views.default.handle_404'
elif (_cname.lower() == 'undefined3'):
    ROOT_URLCONF = 'pyeggs.django.urls'
    handler404 = 'pyeggs.django.views.default.handle_404'
elif (_cname == 'ubuntu.localdomain'):
    ROOT_URLCONF = 'urls'
    handler404 = 'views.default.handle_404'
else:
    ROOT_URLCONF = 'urls'
    handler404 = 'views.default.handle_404'


