# Django settings for mysite project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Admin', 'support@vyperlogix.com'),
)

MANAGERS = ADMINS

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()
if (_cname == 'web22.webfaction.com'):
    DATABASE_ENGINE = 'mysql'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'raychorn_pyeggs' # Or path to database file if using sqlite3.
    DATABASE_USER = 'raychorn_pyeggs' # Not used with sqlite3.
    DATABASE_PASSWORD = 'peekab00'    # Not used with sqlite3.
    DATABASE_HOST = 'localhost'       # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'            # Set to empty string for default. Not used with sqlite3.

if (_cname == 'undefined3'):
    DATABASE_ENGINE = 'mysql'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'pyeggs'          # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'            # Not used with sqlite3.
    DATABASE_PASSWORD = 'peekab00'    # Not used with sqlite3.
    DATABASE_HOST = 'sql2005'         # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'            # Set to empty string for default. Not used with sqlite3.

if (_cname == 'misha-lap.ad.magma-da.com'):
    DATABASE_ENGINE = 'mysql'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'pyeggs'          # Or path to database file if using sqlite3.
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

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2a!kw0yn*tr(d9z+qj5wkad7_#_rs!53#u*j+5@9vt@geszx5z'

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

ROOT_URLCONF = 'pyeggs.urls'

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

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
TEMPLATE_DIRS = findTemplateDirsIn(os.sep.join([_root,'templates']),TEMPLATE_DIRS)
    
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
)

_dirs = [f for f in os.listdir(_root) if ((os.path.exists(os.sep.join([_root,f,'models.py']))) or (os.path.exists(os.sep.join([_root,f,'models.pyc']))) or (os.path.exists(os.sep.join([_root,f,'models.pyo']))))]
_base = ROOT_URLCONF.split('.')[0]
td = list(INSTALLED_APPS)
for dName in _dirs:
    td.insert(len(td),'.'.join([_base,dName]))
    TEMPLATE_DIRS = findTemplateDirsIn(os.sep.join([_root,os.sep.join([dName,'templates'])]),TEMPLATE_DIRS)
INSTALLED_APPS = tuple(td)

if (_base == __name__.split('.')[0]):
    print 'BEGIN: TEMPLATE_DIRS'
    for appName in list(TEMPLATE_DIRS):
        print '%s' % (appName)
    print 'END! TEMPLATE_DIRS'
    print '\n'

    print 'BEGIN: INSTALLED_APPS'
    for appName in list(INSTALLED_APPS):
        print '%s' % (appName)
    print 'END! INSTALLED_APPS'
    print '\n'

handler404 = 'pyeggs.views.default'

