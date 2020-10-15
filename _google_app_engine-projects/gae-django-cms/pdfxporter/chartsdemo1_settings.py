from ragendja.settings_pre import *

DOMAIN_NAME = 'chartsdemo1.appspot.com'
APPSPOT_NAME = 'chartsdemo1.appspot.com'     # WARNING: Be sure to change this for your needs...
LOCALHOST = '127.0.0.1:9000'
SUB_DOMAIN_NAME = DOMAIN_NAME.split('.')[0]

GMAIL_USER = 'vyperlogix@gmail.com'
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
    SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'W*zN`>c?)^a,2FqwOc|pM$A5/X9"e|:vk]#kHY[$!Q%3@\\=~DtnX|h.2U-Iu#*7],_ft7g)C#`)o9b2js-KlEf.f4rEWgIOy}uBqY;<o-/\\hosUDoaB4VB_*N$G1!.}\''

