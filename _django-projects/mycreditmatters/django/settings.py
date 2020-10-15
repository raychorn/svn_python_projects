# Django settings for mysite project.

import os

ADMINS = (
    ('Admin', 'support@vyperlogix.com'),
)

MANAGERS = ADMINS

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()
if (_cname == 'web22.webfaction.com'):
    DATABASE_ENGINE = 'mysql'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'raychorn_resourc' # Or path to database file if using sqlite3.
    DATABASE_USER = 'raychorn_resourc' # Not used with sqlite3.
    DATABASE_PASSWORD = 'peekab00'    # Not used with sqlite3.
    DATABASE_HOST = 'localhost'       # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'            # Set to empty string for default. Not used with sqlite3.
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG

if (_cname == 'undefined3'):
    DATABASE_ENGINE = 'mysql'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'mycreditmatters' # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'            # Not used with sqlite3.
    DATABASE_PASSWORD = 'peekab00'    # Not used with sqlite3.
    DATABASE_HOST = 'sql2005'         # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'            # Set to empty string for default. Not used with sqlite3.
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

if (_cname == 'misha-lap.ad.magma-da.com'):
    DATABASE_ENGINE = 'mysql'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'mycreditmatters' # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'            # Not used with sqlite3.
    DATABASE_PASSWORD = 'peekaboo'    # Not used with sqlite3.
    DATABASE_HOST = 'localhost'       # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'            # Set to empty string for default. Not used with sqlite3.
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

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'static').replace(os.sep,'/')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = 'http://media.vyperlogix.com/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'nnE*S1UY*k>2@gCvX,ocr`HrFNrPuH]fbaYeBC*#YrLc3,op+|Rls0sIND.N2bs|=r={zAnM7!#CX`"@Q{NvIq=V6QG4FiHF$l=w<?u{XF)0SM~-4+,@Q-+Pc5DxY6:\''

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

_title = 'MyCreditMatters, Your Resource for Credit Repair'

from vyperlogix.django import tabs
_navigation_menu_types = tabs._navigation_menu_types
_navigation_menu_type = _navigation_menu_types[2]

_navigation_tabs = []
_navigation_tabs.append(tuple(['/','Home','Let us improve your Credit Score !']))

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace(os.sep,'/'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
)

handler404 = 'views.default.handle_404'

