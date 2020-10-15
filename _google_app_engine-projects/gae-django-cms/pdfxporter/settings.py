# -*- coding: utf-8 -*-
from ragendja.settings_pre import *

# Increase this when you update your media on the production site, so users
# don't have to refresh their cache. By setting this your MEDIA_URL
# automatically becomes /media/MEDIA_VERSION/
MEDIA_VERSION = 1

QUEUE_EMAILS = True

from users.g import air_domain, symbol_free4u, symbol_Polymorphic, symbol_ChartsDemo, current_site

SITE_ID = air_domain[symbol_ChartsDemo]
CURRENT_SITE = SITE_ID

try:
    if (current_site == air_domain[symbol_free4u]):
        from free4u_settings import DOMAIN_NAME, APPSPOT_NAME, LOCALHOST, GMAIL_USER, GMAIL_PASSWORD, SUPER_USER, DEFAULT_FROM_EMAIL, IS_PRODUCTION_SERVER, SERVER_EMAIL, SECRET_KEY, GMAIL_HOST, GMAIL_PORT, SUB_DOMAIN_NAME
    elif (current_site == air_domain[symbol_Polymorphic]):
        from polymorphical_settings import DOMAIN_NAME, APPSPOT_NAME, LOCALHOST, GMAIL_USER, GMAIL_PASSWORD, SUPER_USER, DEFAULT_FROM_EMAIL, IS_PRODUCTION_SERVER, SERVER_EMAIL, SECRET_KEY, GMAIL_HOST, GMAIL_PORT, SUB_DOMAIN_NAME
    elif (current_site == air_domain[symbol_ChartsDemo]):
        from chartsdemo1_settings import DOMAIN_NAME, APPSPOT_NAME, LOCALHOST, GMAIL_USER, GMAIL_PASSWORD, SUPER_USER, DEFAULT_FROM_EMAIL, IS_PRODUCTION_SERVER, SERVER_EMAIL, SECRET_KEY, GMAIL_HOST, GMAIL_PORT, SUB_DOMAIN_NAME
    else:
        raise ImportError('Cannot import the proper settings file.')
except ImportError:
    DOMAIN_NAME = 'pdfxporter.appspot.com'
    APPSPOT_NAME = 'pdfxporter.appspot.com'     # WARNING: Be sure to change this for your needs...
    LOCALHOST = '127.0.0.1:9000'
    SUB_DOMAIN_NAME = DOMAIN_NAME.split('.')[0]
    
    GMAIL_USER = 'raychorn@gmail.com'
    GMAIL_PASSWORD = 'peekab00'
    
    SUPER_USER = GMAIL_USER
    
    if on_production_server:
        DEFAULT_FROM_EMAIL = GMAIL_USER              # this must be your Google Account Login (the same one you use when logging into your Google App Engine Account)
        SERVER_EMAIL = DEFAULT_FROM_EMAIL
        IS_PRODUCTION_SERVER = True
    else:
        DEFAULT_FROM_EMAIL = GMAIL_USER              # this must be your Google Account Login (the same one you use when logging into your Google App Engine Account)
        SERVER_EMAIL = DEFAULT_FROM_EMAIL
        IS_PRODUCTION_SERVER = False
        
    GMAIL_HOST = 'smtp.gmail.com'
    GMAIL_PORT = 587
    
    # Change your email settings
    if on_production_server:
        #DEFAULT_FROM_EMAIL = 'support@vyperlogix.com'
        SERVER_EMAIL = DEFAULT_FROM_EMAIL
    
    # Make this unique, and don't share it with anybody.
    SECRET_KEY = 'W*zN`>c?)^a,2FqwOc|pM$A5/X9"e|:vk]#kHY[$!Q%3@\\=~DtnX|h.2U-Iu#*7],_ft7g)C#`)o9b2js-KlEf.f4rEWgIOy}uBqY;<o-/\\hosUDoaB4VB_*N$G1!.}\''


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

# BEGIN:  DO NOT CHANGE OR BAD EVIL THINGS WILL HAPPEN
APP_SESSION_KEY= '__xxx__'
# END!    DO NOT CHANGE OR BAD EVIL THINGS WILL HAPPEN

BANNER_DIR = os.path.join(os.path.dirname(__file__), 'media', 'images' , 'x')

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

#SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
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

INSTALLED_APPS = (
    # Add jquery support (app is in "common" folder). This automatically
    # adds jquery to your COMBINE_MEDIA['combined-%(LANGUAGE_CODE)s.js']
    # Note: the order of your INSTALLED_APPS specifies the order in which
    # your app-specific media files get combined, so jquery should normally
    # come first.
    'jquery',
    # Add blueprint CSS (http://blueprintcss.org/)
    'blueprintcss',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.webdesign',
    'django.contrib.flatpages',
    'django.contrib.redirects',
    'django.contrib.sites',
    'appenginepatcher',
    'ragendja',
    'users',
    'images',
    'logos',
)

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
