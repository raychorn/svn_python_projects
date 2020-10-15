# -*- coding: utf-8 -*-
import os
from ragendja.settings_pre import *

# Increase this when you update your media on the production site, so users
# don't have to refresh their cache. By setting this your MEDIA_URL
# automatically becomes /media/MEDIA_VERSION/
MEDIA_VERSION = 1

# Make this unique, and don't share it with anybody.
SECRET_KEY = '{$(;As?%SRf]ruO#eTcsX(om(g4d#,NSO\'X~c8-o8<c>$G_ihO$b_l&(rZI|OHtFZ~{a+@q\\~4)e0pvsRl&k.d2glr]?/i41H\\,*5p)c\\[`MKugv9"ye3nM=r/sb+PJ<'

#ENABLE_PROFILER = True
#ONLY_FORCED_PROFILE = True
#PROFILE_PERCENTAGE = 25
#SORT_PROFILE_RESULTS_BY = 'cumulative' # default is 'time'
#PROFILE_PATTERN = 'ext.db..+\((?:get|get_by_key_name|fetch|count|put)\)'

# Enable I18N and set default language to 'en'
USE_I18N = False #False(en)/True(cn)
LANGUAGE_CODE = 'en'

#Restrict supported languages (and JS media generation)
#LANGUAGES = (
#    ('en', 'English'),
#    ('zh_CN', '简体中文'),
#)

#must be admin email of your GAE . 'yourgmail@gmail.com'
DEFAULT_FROM_EMAIL = 'raychorn@gmail.com'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
)

MIDDLEWARE_CLASSES = (
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

GLOBALTAGS = (
    'ragendja.templatetags.ragendjatags',
    'django.templatetags.i18n',
)

TEMPLATE_DIRS = [
    #os.path.join(os.path.dirname(__file__), './themes/default/templates').replace('\\','/'),
    #os.path.join(os.path.dirname(__file__), './themes').replace('\\','/'),
    #'./themes/default/templates',    
    #os.path.join(os.path.dirname(__file__), 'themes/bloger/templates').replace('\\','/')
]
#'''
themes = os.listdir(os.path.join(os.path.dirname(__file__), 'themes'))
for theme in themes:
    TEMPLATE_DIRS.append(os.path.join(os.path.dirname(__file__), 'themes/%s/templates'%theme).replace('\\','/'))
#'''
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'
LOGIN_REDIRECT_URL = '/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.webdesign',
    #'django.contrib.flatpages',
    'django.contrib.redirects',
    'django.contrib.sites',
    'appenginepatcher',
    #'myapp',
    'cms',
)

from ragendja.settings_post import *
