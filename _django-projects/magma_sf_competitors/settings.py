# Django settings for mysite project.
import os

from vyperlogix.misc import _utils
DEBUG = _utils.isBeingDebugged
TEMPLATE_DEBUG = DEBUG

from vyperlogix.google.gae import gae_utils
_is_running_local = gae_utils.is_running_local()

__version__ = '1.0.0'

__title__ = 'Magma Design Automation Current Assets Customer List Maintenance System'

ADMINS = (
    ('Admin', 'support@vyperlogix.com'),
)

MANAGERS = ADMINS

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()

if (_cname == 'misha-lap.ad.magma-da.com'):
    DATABASE_ENGINE = 'mysql'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = 'competitors'     # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'            # Not used with sqlite3.
    DATABASE_PASSWORD = 'peekaboo'    # Not used with sqlite3.
    DATABASE_HOST = 'localhost'       # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'            # Set to empty string for default. Not used with sqlite3.
    MEMCACHE_ADDRESS = 'tide2.magma-da.com:11211'

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

# Make this unique, and don't share it with anybody.
#from vyperlogix.misc import GenPasswd
#SECRET_KEY = GenPasswd.GenPasswd(length=128,chars=GenPasswd.string.printable)

SECRET_KEY = 'xe~l^G,FDAKzee4Cs/1Ep86oU<<{X|9+%i=f,r\'b\'eVh&~</A_8W>D~!1"?/BG)x\' /G\x0c\'CdR(#g.ED4+:&XejZ#Ngj(#&4R/B"LVw?y3a*Y/\x0c#B@pNG5m$WKho~?@^5'

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

#ROOT_URLCONF = 'magma_sf_competitors.urls'
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

handler404 = 'views.default_404'

if (_is_running_local):
    is_memcachable = True
    try:
        import memcache
    except ImportError:
        is_memcachable = False
        
    if (is_memcachable):
        mc = memcache.Client([MEMCACHE_ADDRESS], debug=0)
        is_memcachable = all([s.connect() for s in mc.servers])

    is_in_memcache = False
    if (is_memcachable):
        mc.delete('STATIC_PATTERNS')
        is_in_memcache = mc.get('STATIC_PATTERNS') is not None

    if (is_memcachable) and (not is_in_memcache):
        from django.core.urlresolvers import RegexURLResolver

        import re
        _reFilter = '[._]svn|Thumbs.db' 
        rejecting_re = re.compile(_reFilter)
        fpath = os.path.join(os.path.dirname(__file__), 'static')
        files = os.listdir(fpath)
        _patterns = []
        for root, dirs, files in _utils.walk(fpath, rejecting_re=rejecting_re):
            for f in files:
                _patterns.append(RegexURLResolver(r'^%s%s' % (_utils.eat_leading_token_if_empty(MEDIA_URL),os.path.join(root.replace(fpath,''),f)), 'django.views.static.serve', {'document_root': MEDIA_ROOT}))
        mc.set('STATIC_PATTERNS',_patterns)
   