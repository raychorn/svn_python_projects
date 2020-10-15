# Django settings for mysite project.

from vyperlogix.misc import _utils
DEBUG = _utils.isBeingDebugged
TEMPLATE_DEBUG = DEBUG

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

if (_cname == 'undefined3'):
    DATABASE_ENGINE = 'mysql'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'resources'          # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'            # Not used with sqlite3.
    DATABASE_PASSWORD = 'peekab00'    # Not used with sqlite3.
    DATABASE_HOST = 'sql2005'         # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'            # Set to empty string for default. Not used with sqlite3.

if (_cname == 'misha-lap.ad.magma-da.com'):
    DATABASE_ENGINE = 'mysql'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'resources'          # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'            # Not used with sqlite3.
    DATABASE_PASSWORD = 'peekaboo'    # Not used with sqlite3.
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
MEDIA_ROOT = 'C:\\Apache228\\htdocs\\pyeggs\\media\\'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

from vyperlogix.misc import GenPasswd

# Make this unique, and don't share it with anybody.
_SECRET_KEY = '2a!kw0yn*tr(d9z+qj5wkad7_#_rs!53#u*j+5@9vt@geszx5z'
SECRET_KEY = GenPasswd.GenPasswd(length=len(_SECRET_KEY),chars=GenPasswd.string.printable)

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
)

ROOT_URLCONF = 'resources.urls'

def findTemplateDirsIn(fname,target):
    import re
    from vyperlogix.misc import collectFromPath
    __reFilter = '[._]svn' 
    rejecting_re = re.compile(__reFilter)
    _template_paths = collectFromPath.collectDirsFromPath(fname,rejecting_re=rejecting_re)
    td = list(target)
    for dirName in _template_paths.keys():
        td.insert(len(td),dirName)
    return tuple(td)

import os
_root = os.path.dirname(__file__)
_template_path = os.sep.join([_root,'templates'])

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

if (os.path.exists(_template_path)):
    td = list(TEMPLATE_DIRS)
    td.insert(0,_template_path)
    TEMPLATE_DIRS = tuple(td)
else:
    print 'Cannot find "%s".' % (_template_path)
    
print 'TEMPLATE_DIRS=%s' % (str(TEMPLATE_DIRS))
    
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'resources.library',
)

handler404 = 'resources.views.default'

