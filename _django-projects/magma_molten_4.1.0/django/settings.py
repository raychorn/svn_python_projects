# Django settings for mysite project.
import os, sys

from vyperlogix.misc import _utils
DEBUG = _utils.isBeingDebugged
TEMPLATE_DEBUG = DEBUG

from vyperlogix.google.gae import gae_utils
_is_running_local = gae_utils.is_running_local()

__version__ = '4.1.0'
__title__ = 'Magma Design Automation Molten'

from vyperlogix.products import keys

from maglib.salesforce.cred import credentials

e_passphrase = keys._decode('4D61676D612044657369676E204175746F6D6174696F6E204D6F6C74656E')
__sf_account__ = credentials(e_passphrase)

VERSION = __version__

TITLE = __title__

IMAGES_URL = 'http://media.vyperlogix.com/magma/images/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

CACHE_MIDDLEWARE_SECONDS = 180
CACHE_MIDDLEWARE_KEY_PREFIX = 'MOLTEN_%s_1' % (__version__)
CACHE_BACKEND = 'db://django_cache'

USE_SALESFORCE_STAGING = False

MORE_NEW_SOLUTIONS = 'More new solutions ...'
MORE_NEW_SOLUTIONS_LINK = '/solutions/recent/'

# Count new solutions in last N days
NEW_SOLUTIONS_LAST_N_DAYS = 30 # if (not _utils.isBeingDebugged) else 90

# Maximum # of Recent cases and solutions to show in the sidebar
RECENT_LIMIT = 5

# Maximum characters in the solution name lenght when showing in a list
SOLUTION_NAME_LIMIT = 47

# Number of support cases to show on home page
RECENTLY_UPDATED_LIMIT = 5

# Maximum solutions to show per/section on the home page
SOLUTION_HOME_LIMIT = 5

# Number of popular solutions to show on home page and left side
MOST_POPULAR_LIMIT = 5

# Number of days to go back when determining popular solutions
MOST_POPULAR_LAST_N_DAYS = 30

# Limit the number of articles in the sidebar
ARTICLE_LIMIT = 5

# Length of the article body to display on the articles list page
ARTICLE_LIST_BODY_LENGTH = 400
ARTICLE_LIST_TITLE_LENGTH = 80

ADMINS = (
    ('Admin', 'support@vyperlogix.com'),
)

MANAGERS = ADMINS

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()

if (_cname == 'undefined3'):
    _password = keys._decode('7065656B61623030')
    DATABASE_ENGINE = 'mysql'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'django_molten'   # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'            # Not used with sqlite3.
    DATABASE_PASSWORD = _password     # Not used with sqlite3.
    DATABASE_HOST = 'sql2005'         # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'            # Set to empty string for default. Not used with sqlite3.

if (_cname == 'misha-lap.ad.magma-da.com'):
    _password = keys._decode('7065656B61626F6F')
    DATABASE_ENGINE = 'mysql'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'django_molten'   # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'            # Not used with sqlite3.
    DATABASE_PASSWORD = _password     # Not used with sqlite3.
    DATABASE_HOST = 'localhost'       # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'            # Set to empty string for default. Not used with sqlite3.

if (_cname == 'tide.magma-da.com'):
    _password = keys._decode('326D6F6C74656E')
    DATABASE_ENGINE = 'mysql'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'molten4'         # Or path to database file if using sqlite3.
    DATABASE_USER = 'molten2'         # Not used with sqlite3.
    DATABASE_PASSWORD = _password     # Not used with sqlite3.
    DATABASE_HOST = 'localhost'       # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'            # Set to empty string for default. Not used with sqlite3.

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
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'static')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

#from vyperlogix.misc import GenPasswd
#SECRET_KEY = GenPasswd.GenPasswd(length=128,chars=GenPasswd.string.printable)
SECRET_KEY = 'N?:2Eus&Sw,@O(6>3UyV.X2hL.2{f\x0cbzI\\ht+:kG,iw_T\tAiRe^yJkF}SSQ<S|6ANX!Ca4Ue#Uxjz\x0b&^\'"([\x0c,EbGLOl({bHh+r\nm-zn\\YF\\\x0cDM<e(J\rG{="i!G,;M$e'

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
#    'django.middleware.cache.CacheMiddleware',
)

ROOT_URLCONF = 'urls'

#if (_is_running_local):
    #ROOT_URLCONF = 'urls'
#else:
    #ROOT_URLCONF = 'magma_molten.urls'

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

if (_is_running_local):
    handler404 = 'views.default_404'
else:
    handler404 = 'magma_molten.views.default_404'

