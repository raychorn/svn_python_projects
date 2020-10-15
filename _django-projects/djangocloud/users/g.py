import logging

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.products import keys

symbol_svncloud = 'svncloud'

air_id = ''
air_version = SmartObject()
air_version[symbol_svncloud] = '0.1.0.0'

air_domain = SmartObject()
air_domain[symbol_svncloud] = None

__air_sender__ = {}
__air_sender__[symbol_svncloud] = 'vyperlogix@gmail.com'
air_sender = lambda key:__air_sender__.get(key,'djangocloud@vyperlogix.com') if (__air_sender__) else None

__air_site__ = {}
__air_site__[symbol_svncloud] = None
air_site = lambda key:__air_site__.get(key,'Django Cloud @ Vyper Logix Corp.') if (__air_site__) else None

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

def send_php_email(url,parms={},is_html=False,data={},error_symbol=None):
    import urllib,urllib2

    content = ''
    try:
	__data__ = data # don't worry this line works...
	data = {}
	logging.warning('send_php_email().1 --> parms=%s' % (parms))
	if (len(parms.keys()) > 0):
	    _expected_keys = ['to','subject','body','altbody']
	    for k,v in parms.iteritems():
		if (k == 'altbody'):
		    data[k] = (v.replace('\n','').replace('\r','').replace("\'",'') if (k in _expected_keys) else '')
		else:
		    data[k] = (v.replace("\'",'') if (k in _expected_keys) else '')
	else:
	    data = {'to':'raychorn@vyperlogix.com', 'subject':'This is a test...', 'body':'<p>This is <b>just</b> a test...</p>', 'altbody':'This is just a test...'}
	logging.warning('send_php_email().2 --> data=%s' % (data))
	data = urllib.urlencode(data)
    
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = {'User-Agent':user_agent}
    
	req = urllib2.Request(url, data, headers)
	response = urllib2.urlopen(req)
	content = response.read()
	logging.warning('send_php_email().3 --> content=%s' % (content))
    except Exception, e:
	toks = ListWrapper(str(e).split())
	f = toks.findFirstContaining(']')
	message = 'send_php_email().ERROR --> "%s".' % (str(e))
	message2 = 'send_php_email().ERROR --> "%s".' % (' '.join(toks[f+1:f+1+5]+'...') if (f > -1) else str(e))
	if (error_symbol):
	    if (misc.isDict(__data__)):
		__data__[error_symbol] = message2
	logging.warning(message)
    return content

def __queue_email__(email_from,email_to,email_subject,email_body,email_body_html,__air_id__,is_html=False,data={},error_symbol=None):
    from django.conf import settings
    send_php_email(settings.__EMAIL_POST_ADDRESS__,parms={'to':email_to, 'subject':email_subject, 'body':email_body, 'altbody':email_body_html},is_html=is_html,data=data,error_symbol=error_symbol)

def queue_email(email_from,email_to,email_subject,email_body,email_body_html,__air_id__,is_html=False,data={},error_symbol=None):
    ''' See also: settings.py for the following:
    EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
    MAILGUN_ACCESS_KEY = 'key-50npnx4bhglbohd-f60k00ottnzop6a8'
    MAILGUN_SERVER_NAME = 'vyperlogix.com'
    '''
    try:
	from django.core import mail
	connection = mail.get_connection()
	connection.open()
	email1 = mail.EmailMessage(email_subject, email_body, email_from, [email_to], connection=connection)
	email1.send()
	connection.close()
    except Exception, ex:
	__queue_email__(email_from,email_to,email_subject,email_body,email_body_html,__air_id__,is_html=True,data=data,error_symbol=error_symbol)
	if (error_symbol):
	    if (misc.isDict(data) and not data.has_key(error_symbol)):
		data[error_symbol] = _utils.formattedException(details=ex)

