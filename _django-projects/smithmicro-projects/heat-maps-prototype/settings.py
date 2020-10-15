# Django settings for mysite project.

from vyperlogix.django import django_utils

import os

ADMINS = (
    ('Admin', 'support@vyperlogix.com'),
)

MANAGERS = ADMINS

from vyperlogix.products import keys

DOMAIN_NAME = django_utils.socket.gethostname()

if (DOMAIN_NAME in ['D-MV-RHORN']):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'django-heat-maps-prototype',
            'USER' : 'root',
            'PASSWORD' : keys._decode('7065656B61623030'),
            'HOST' : '127.0.0.1',
            'PORT' : '3306',
        }
    }
    IS_PRODUCTION_SERVER = False
    LOCALHOST = '127.0.0.1'
    DEBUG = True
else: # Production
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'django-heat-maps-prototype',
            'USER' : 'root',
            'PASSWORD' : keys._decode('7065656B61623030'),
            'HOST' : '127.0.0.1',
            'PORT' : '3306',
        }
    }
    IS_PRODUCTION_SERVER = True
    LOCALHOST = '127.0.0.1:9999'
    DEBUG = False

TEMPLATE_DEBUG = DEBUG

SLEEPY_MONGOOSE = '127.0.0.1:27080'
MONGODBS = 'gps_1M'
MONGODB_COLLECTION = 'num_connections'

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1  # dynamically set based on the requesting domain...

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

USE_MULTITHREADED_SERVER = True

SESSION_COOKIE_SECURE = False

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

# BEGIN: Generate a new SECRET_KEY using the block of code...
#from vyperlogix.misc import GenPasswd
#SECRET_KEY = GenPasswd.GenPasswd(length=128,chars=GenPasswd.chars_printable)
SECRET_KEY = '_Sp%o2oz%6.K+HFq?_AckQVWq9PwaK"b|O3|v4Y~$8!C,Hp\'SC:J+(Qlm)x*$Ije[_*0s5j2?EF?A~72wJu;pptB_K*2z%32g!p@5px?anT<a+Rxx]eEAfwxe!`L#)fY'
# END!   Generate a new SECRET_KEY using the block of code...

# BEGIN:  DO NOT CHANGE OR BAD EVIL THINGS WILL HAPPEN
APP_SESSION_KEY= '__xxx__'
# END!    DO NOT CHANGE OR BAD EVIL THINGS WILL HAPPEN

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#    'django.template.loader.find_template',
#     'django.template.loaders.eggs.load_template_source',
)

# List of middleware classes to use.  Order is important; in the request phase,
# this middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',
)

IS_CACHING_CONTENT = not DEBUG
if (IS_CACHING_CONTENT):
    CACHE_TIMER = 60 * 15
    CACHE_BACKEND = 'memcached://127.0.0.1:11211/?timeout=%s' % (CACHE_TIMER)
    CACHE_MIDDLEWARE_SECONDS = CACHE_TIMER
    
    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
    MIDDLEWARE_CLASSES.insert(0,'django.middleware.cache.UpdateCacheMiddleware')
    MIDDLEWARE_CLASSES.append('django.middleware.cache.FetchFromCacheMiddleware')
    MIDDLEWARE_CLASSES = tuple(MIDDLEWARE_CLASSES)

from vyperlogix import misc
cb = lambda foo:foo.find('templates') > -1 if (misc.isString(foo)) else false
from vyperlogix.django.findDjangoTemplateDirsIn import findDjangoTemplateDirsIn
TEMPLATE_DIRS = []
for t in findDjangoTemplateDirsIn(os.path.dirname(__file__),[],callback = cb):
    TEMPLATE_DIRS.append(t)
TEMPLATE_DIRS = tuple(TEMPLATE_DIRS)

INSTALLED_APPS = (
    'django.contrib.sitemaps',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'views',
    'users',
    'smithmicro'
)

ROOT_URLCONF = 'urls'

