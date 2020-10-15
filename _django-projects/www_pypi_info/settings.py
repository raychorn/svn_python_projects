# Django settings for mysite project.
import os 

from vyperlogix.misc import _utils

ADMINS = (
    ('Admin', 'support@vyperlogix.com'),
)

MANAGERS = ADMINS

from vyperlogix.products import keys
from vyperlogix.django import django_utils

DATABASE_ENGINE = 'mysql'                                # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DEBUG = False

DATABASE_NAME1 = 'raychorn_joomla'                       # Or path to database file if using sqlite3.

if (django_utils._cname == 'web22.webfaction.com'):
    DATABASE_NAME = 'raychorn_vyper'                     # Or path to database file if using sqlite3.
    DATABASE_NAME2 = 'raychorn_frehost'                  # Or path to database file if using sqlite3.
    DATABASE_USER = 'raychorn_joomla'                    # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61623030') # Not used with sqlite3.
    DATABASE_HOST = 'localhost'                          # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'                               # Set to empty string for default. Not used with sqlite3.
elif (django_utils._cname in ['undefined3']):
    DATABASE_NAME = 'pypi'                               # Or path to database file if using sqlite3.
    DATABASE_NAME2 = 'freehosts'                         # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'                               # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61623030') # Not used with sqlite3.
    DATABASE_HOST = 'SQL2005'                            # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3307'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = True
elif (django_utils.is_Production or django_utils.is_Staging or (django_utils._cname in ['ubuntu4.web20082'])):
    DATABASE_NAME = 'pypi'                               # Or path to database file if using sqlite3.
    DATABASE_NAME2 = 'freehosts'                         # Or path to database file if using sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61623030') # Not used with sqlite3.
    DATABASE_HOST = 'localhost'                            # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3306'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = False if (django_utils.is_Production) else True
    TEMPLATE_DEBUG = DEBUG
elif (django_utils.is_Production or django_utils.is_Staging or (django_utils._cname in ['raychorn-ubuntu-desktop'])):
    DATABASE_NAME = 'pypi'                               # Or path to database file if using sqlite3.
    DATABASE_NAME2 = 'freehosts'                         # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'                               # Not used with sqlite3.
    DATABASE_PASSWORD = keys._decode('7065656B61623030') # Not used with sqlite3.
    DATABASE_HOST = 'web2008'                            # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '3307'                               # Set to empty string for default. Not used with sqlite3.
    DEBUG = False if (django_utils.is_Production) else True
else:
    print 'WARNING: %s' % (django_utils._cname)
TEMPLATE_DEBUG = DEBUG

#SMTP_SERVER = 'smtp.gmail.com'
#SMTP_PORT = 587
#SMTP_USERNAME = 'vyperlogix@gmail.com'
#SMTP_PASSWORD = keys._decode('7065656B61623030')

_SMTP_SERVER = 'sql2005:8025'

#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = 'vyperlogix@gmail.com'
#EMAIL_HOST_PASSWORD = keys._decode('7065656B61623030')
#EMAIL_PORT = 587

#from django.core.mail import EmailMessage
#email = EmailMessage('Subject', 'Body', t=['raychorn@hotmail.com'])
#email.save()

from vyperlogix.hash import lists
from vyperlogix.django import tabs

_navigation_menu_types = tabs._navigation_menu_types

_navigation_menu_type = _navigation_menu_types[0]

_navigation_tabs = []
_navigation_tabs.append(tuple(['/','Home','"Vyper Logix Corp specializes in building products and systems based entirely on the Python Language."']))
#_navigation_tabs.append(tuple(['http://www.vyperlogix.com/vyper_cloud_sdk/','Vyper-Cloud&trade; SDK','Vyper-Cloud&trade; SDK is a Software Development Kit for those who wish to build and deploy their own Cloud Computing Platforms.']))
_navigation_tabs.append(tuple(['http://www.vyperlogix.com/','Vyper Logix Corp.','Vyper Logix Corp., the 21st Century Python Company.']))
_navigation_tabs.append(tuple(['http://library.vyperlogix.com','VyperLogixLib-1.0-py2.5.egg&trade; Docs','100% Reusable Python Code Library.']))
_navigation_tabs.append(tuple(['/about/','About','For the time being, we specialize in providing services and solutions related to the Python&trade; Language. Our products, pyEggs&trade; and PDFxporter&trade; are excellent examples of what we are capable of. ']))
_navigation_tabs.append(tuple(['/login/','Login','Login or Register to use this site.']))
#_navigation_tabs.append(tuple(['/register/','Register','Register to use this site.']))
_navigation_tabs.append(tuple(['/logout/','Logout','Logout']))
_navigation_tabs.append(tuple(['/problems/','Problems ?','Report any Problems or Usability Issues you may be having with this site.']))
_navigation_tabs.append(tuple(['/administrator/','Administrator','Administration of the site from the Joomla perspective.']))
#_navigation_tabs.append(tuple(['/feeds/','Feeds','<a href="/feeds/rss/" target="_blank"><img src="/static/rss/rss-feed_16x16.gif"/><br/>Rss 2.0 Feed</a>']))
_navigation_tabs.append(tuple(['/downloads/','Downloads','Building a huge library of Python Downloads all in one place... For Members <u>Only</u> !']))
_navigation_tabs.append(tuple(['/pypi/','PyPI','The Official Python Package Index and the PYPI API along with the PYPI API Demo.']))
_navigation_tabs.append(tuple(['/feeds/rss-pypi/',"<img src='/static/rss/rss-feed_16x16.gif' />",'The Official Python Package Index RSS Feed']))

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

USE_MULTITHREADED_SERVER = True

CACHE_TIMER = 60 * 15
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

SESSION_COOKIE_SECURE = (django_utils.isProduction(django_utils._cname) or django_utils.isStaging(django_utils._cname))
SESSION_EXPIRE_AT_BROWSER_CLOSE = (django_utils.isProduction(django_utils._cname) or django_utils.isStaging(django_utils._cname))

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
ADMIN_MEDIA_PREFIX = '/admin-static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'hpe2|]@\'Sk4-(`2y)\x0b3XvmX]D<7pb ZLOXn;D~:5t[P\x0b*iy6&\n/b{\x0cwC#$nxJ25Y%(|C^RO\x0c?-rV$7_d.*wxa i*99d5xq\x0bF/wF3i$!HDq?Gl$L\x0c+.e+.3a\x0b,Iu\\{9$l3]!8yI0%qSmyD_ 2.|5a+lK*R/-N9+(>B$B<2s[AZ\x0c-97eolS`m\x0c[_ 2a]K8Mf;<Jy^Y3a\rDT=Q7yScx1Wj=|C@!w62UMrNadyS`*>pzn/0Ko^\x0bh|ubK\'Oo.P +M(NLIxL#oK3lN`-R@hlV\'miSwR?OjrA{NIwEF9\\ =!)\t=tzbFAh;5~hkX/;(\\DMy\ty2fBR,.WHEU\'0qSO!#z`0/0+\x0c_F?)4<*pE(\nv)M9[&MNeSEb3RSB4\r;[CXni\r)M.e!b&bW\ri%%>6.0\t:}4])s\'+gp)[&MJWBxa}"\x0b=w 2<;b"teY8y239yEyb$/P!q9\'q]}$yk.YUuClChd-_1edKeeKPu0Sa\tR3sYYdM0.\r\thNv^\nNl!c4/R\x0c"\x0b#&=N7,^r5dM.'

DISALLOW_FREEHOSTS = False

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
    #'vyperlogix.django.middleware.requireSSL.SSLRedirect',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.sitemaps',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'views',
    'feeds',
    'downloads'
)


