# -*- coding: utf-8 -*-
from ragendja.settings_pre import *

from vyperlogix.django import django_utils

# Increase this when you update your media on the production site, so users
# don't have to refresh their cache. By setting this your MEDIA_URL
# automatically becomes /media/MEDIA_VERSION/
MEDIA_VERSION = 1

# By hosting media on a different domain we can get a speedup (more parallel
# browser connections).
#if on_production_server or not have_appserver:
#    MEDIA_URL = 'http://media.mydomain.com/media/%d/'

# Add base media (jquery can be easily added via INSTALLED_APPS)
COMBINE_MEDIA = {
    'combined-%(LANGUAGE_CODE)s.js': (
        # See documentation why site_data can be useful:
        # http://code.google.com/p/app-engine-patch/wiki/MediaGenerator
        '.site_data.js',
    ),
    'combined-%(LANGUAGE_DIR)s.css': (
        'global/look.css',
    ),
}

# Change your email settings
if on_production_server:
    DEFAULT_FROM_EMAIL = 'raychorn@gmail.com'   # this must be your Google Account Login (the same one you use when logging into your Google App Engine Account)
    SERVER_EMAIL = DEFAULT_FROM_EMAIL
    IS_PRODUCTION_SERVER = True
else:
    DEFAULT_FROM_EMAIL = 'raychorn@gmail.com'   # this must be your Google Account Login (the same one you use when logging into your Google App Engine Account)
    SERVER_EMAIL = DEFAULT_FROM_EMAIL
    IS_PRODUCTION_SERVER = False

# Make this unique, and don't share it with anybody.
SECRET_KEY = '{$(;As?%SRf]ruO#eTcsX(om(g4d#,NSO\'X~c8-o8<c>$G_ihO$b_l&(rZI|OHtFZ~{a+@q\\~4)e0pvsRl&k.d2glr]?/i41H\\,*5p)c\\[`MKugv9"ye3nM=r/sb+PJ<'

BANNER_DIR = os.path.join(os.path.dirname(__file__), 'media', 'images' , 'x')

# Your copyright text, e.g. "All contents Copyright 2007, Acme Inc."
COPYRIGHT = '(c). Ray C Horn, All Rights Reserved except where otherwise noted.'

# Defines the root URL of your site, e.g. http://domain.com/
SITE_ROOT = '/'

# Defines the root URL for the blog path, e.g. if you want the blog to live at http://domain.com/blog/, this variable would be set to '/blog/'. If you want the blog to live at a different subdomain than the rest of the site, you will need to set an absolute URL: 'http://blog.domain.com/'
BLOG_ROOT = '/'

# BEGIN:  Customize this for your needs...
ACCOUNT_ACTIVATION_DAYS = 30
ACCOUNT_FEEDBACK_DAYS = 30

DOMAIN_NAME = 'raychorn.com'
APPSPOT_NAME = 'raychorn.appspot.com'     # WARNING: Be sure to change this for your needs...

SUPER_USER = 'admin'
SUPER_PASSWORD = 'peekab00'               # WARNING: Be sure to change this for your needs...
SUPER_EMAIL = DEFAULT_FROM_EMAIL
SUPER_FIRSTNAME = 'Super'
SUPER_LASTNAME = 'User'

FACEBOOK_APP_ID = '122703234439995'
FACEBOOK_SPONSOR_ID = '136808046340241'
# END!    Customize this for your needs...

# BEGIN:  DO NOT CHANGE OR BAD EVIL THINGS WILL HAPPEN
APP_SESSION_KEY= '__xxx__'
# END!    DO NOT CHANGE OR BAD EVIL THINGS WILL HAPPEN

LOCALHOST = '127.0.0.1:8888'

#ENABLE_PROFILER = True
#ONLY_FORCED_PROFILE = True
#PROFILE_PERCENTAGE = 25
#SORT_PROFILE_RESULTS_BY = 'cumulative' # default is 'time'
# Profile only datastore calls
#PROFILE_PATTERN = 'ext.db..+\((?:get|get_by_key_name|fetch|count|put)\)'

# Enable I18N and set default language to 'en'
USE_I18N = True
LANGUAGE_CODE = 'en'

# Restrict supported languages (and JS media generation)
LANGUAGES = (
    ('en', 'English'),
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
)

MIDDLEWARE_CLASSES = (
    'google.appengine.ext.appstats.recording.AppStatsDjangoMiddleware',
    'ragendja.middleware.ErrorMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Django authentication
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Google authentication
    #'ragendja.auth.middleware.GoogleAuthenticationMiddleware',
    # Hybrid Django/Google authentication
    #'ragendja.auth.middleware.HybridAuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'ragendja.sites.dynamicsite.DynamicSiteIDMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

# Google authentication
#AUTH_USER_MODULE = 'ragendja.auth.google_models'
#AUTH_ADMIN_MODULE = 'ragendja.auth.google_admin'
# Hybrid Django/Google authentication
#AUTH_USER_MODULE = 'ragendja.auth.hybrid_models'

LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'
LOGIN_REDIRECT_URL = '/'

BASE_APPS = (
    # Add jquery support (app is in "common" folder). This automatically
    # adds jquery to your COMBINE_MEDIA['combined-%(LANGUAGE_CODE)s.js']
    # Note: the order of your INSTALLED_APPS specifies the order in which
    # your app-specific media files get combined, so jquery should normally
    # come first.
    #'jquery',
    # Add blueprint CSS (http://blueprintcss.org/)
    'blueprintcss',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.webdesign',
    'django.contrib.flatpages',
    'django.contrib.redirects',
    'django.contrib.sites',
    'django.contrib.markup',
    'appenginepatcher',
    'ragendja'
)

INSTALLED_APPS = tuple(list(BASE_APPS) + [
    'registration',
    'feedback',
    'facebook',
    'about',
    'images',
    'myapp',
    'blog'
])

_ROOT_ = os.path.dirname(__file__)

MORE_APPS = django_utils.seek_installed_apps(_ROOT_,INSTALLED_APPS=list(set(INSTALLED_APPS)-set(BASE_APPS)))

TEMPLATE_DIRS = tuple(set(list(TEMPLATE_DIRS) + [os.path.join(_ROOT_, a, 'templates') for a in MORE_APPS]))

# List apps which should be left out from app settings and urlsauto loading
IGNORE_APP_SETTINGS = IGNORE_APP_URLSAUTO = (
    # Example:
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'yetanotherapp',
)

# Remote access to production server (e.g., via manage.py shell --remote)
DATABASE_OPTIONS = {
    # Override remoteapi handler's path (default: '/remote_api').
    # This is a good idea, so you make it not too easy for hackers. ;)
    # Don't forget to also update your app.yaml!
    #'remote_url': '/remote-secret-url',

    # !!!Normally, the following settings should not be used!!!

    # Always use remoteapi (no need to add manage.py --remote option)
    #'use_remote': True,

    # Change appid for remote connection (by default it's the same as in
    # your app.yaml)
    #'remote_id': 'otherappid',

    # Change domain (default: <remoteid>.appspot.com)
    #'remote_host': 'bla.com',
}

from ragendja.settings_post import *
