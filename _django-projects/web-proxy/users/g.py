import logging

from vyperlogix.misc import _utils
from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.products import keys

symbol_svncloud = 'svncloud'

air_id = ''
air_version = SmartObject()
air_version[symbol_svncloud] = '0.1.0.0'

air_domain = SmartObject()
air_domain[symbol_svncloud] = None

air_sender = {}
air_sender[symbol_svncloud] = 'vyperlogix@gmail.com'

air_site = {}
air_site[symbol_svncloud] = None

updater_domainName = 'downloads.vyperlogix.com'

_admin_username = 'raychorn'
_admin_password = keys._decode('7065656B61623030')

def make_admin_user():
    from django.contrib.auth.models import User
    try:
	user = User.objects.get(username=_admin_username)
    except:
	user = None
    if not user or user.username != _admin_username or not (user.is_active and user.is_staff and user.is_superuser and user.check_password(_admin_password)):
        user = User(username=_admin_username, email='raychorn@gmail.com', first_name='Ray', last_name='Horn', is_active=True, is_staff=True, is_superuser=True)
        user.set_password(_admin_password)
        user.save()

def fetch_from_url(url):
    import urllib2
    response = urllib2.urlopen(url)
    html = response.read()
    return html

def current_site():
    from django.conf import settings
    from vyperlogix import misc
    _current_site = settings.CURRENT_SITE
    logging.debug('%s.1 --> _current_site=%s' % (misc.funcName(),_current_site))
    return _current_site

def normalizeAmount(value):
    from vyperlogix.money import floatValue
    v = '%10.2f' % floatValue.floatAsDollars(value)
    return v.strip()

def asCurrency(dollars):
    from django.contrib.humanize.templatetags.humanize import intcomma
    dollars = float(dollars)
    return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])

def next_sunday():
    from datetime import datetime,timedelta
    today = datetime.today()
    today = _utils.getFromDateTimeStr(_utils.getAsSimpleDateStr(today,_utils.formatDate_MMDDYYYY_slashes()),_utils.formatDate_MMDDYYYY_slashes()) + timedelta(days = 1)
    _next_sunday = today + timedelta(days = 6 - today.weekday()) # next sunday is the next drawing...
    return _next_sunday

def next_drawing():
    return next_sunday()

def today():
    from datetime import datetime,timedelta
    _today = datetime.today()
    _today = _utils.getFromDateTimeStr(_utils.getAsSimpleDateStr(_today,_utils.formatDate_MMDDYYYY_slashes()),_utils.formatDate_MMDDYYYY_slashes())
    return _today

def xml_to_python(xml):
    from xml.dom import minidom
    dom = minidom.parseString(xml)
    return dom

def xml_to_json(xml):
    from xml.dom import minidom
    from django.utils import simplejson
    dom = minidom.parseString(xml)
    return simplejson.load(dom)

def json_to_python(json):
    d = {}
    try:
        from django.utils import simplejson
        d = simplejson.loads(json)
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        json = {'__error__':info_string}
    return d

def dict_to_json(dct):
    json = ''
    try:
        from django.utils import simplejson
        json = simplejson.dumps(dct)
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        json = {'__error__':info_string}
    return json

def xml2json(xml,callback=None,callbackB4=None,callbackNodeName=None):
    from vyperlogix.xml import XML2JSon

    json = ''

    def handle_data(name,data):
        try:
            if (callable(callback)):
                try:
                    callback(name,data)
                except:
                    pass
            #print name,data
        except Exception, details:
            from vyperlogix.misc import _utils
            info_string = _utils.formattedException(details=details)
            #print info_string

    po = XML2JSon.XMLConversionProxy(XML2JSon.XML2JSon())
    po.proxy.callback = handle_data
    json = po.process(xml)

    return json
