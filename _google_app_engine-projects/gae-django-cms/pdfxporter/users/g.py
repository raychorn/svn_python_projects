import logging

from vyperlogix.misc import _utils
from vyperlogix.classes.SmartObject import SmartObject

symbol_Polymorphic = 'Polymorphic'
symbol_PDFXporter = 'PDFXporter'
symbol_Logos = 'Logos'
symbol_Flexstylus = 'Flexstylus'
symbol_ChartsDemo = 'Charts-Demo'
symbol_free4u = 'free-4u'
symbol_starbucks = 'starbucks'

air_id = ''
air_version = SmartObject()
air_version[symbol_Polymorphic] = '0.2.0.0'
air_version[symbol_PDFXporter] = '0.3.0.0'
air_version[symbol_Logos] = '0.1.1.0'
air_version[symbol_Flexstylus] = '0.1.0.0'
air_version[symbol_ChartsDemo] = '0.3.18'
air_version[symbol_free4u] = '1.0.0'   # this version number cannot be more than 3 digits

air_domain = SmartObject()
air_domain[symbol_Polymorphic] = 'polymorphical.appspot.com'
air_domain[symbol_PDFXporter] = 'pdfxporter.appspot.com'
air_domain[symbol_Logos] = 'vyperlogos.appspot.com'
air_domain[symbol_Flexstylus] = 'flexstylus.appspot.com'
air_domain[symbol_ChartsDemo] = 'charts-demo.appspot.com'
air_domain[symbol_free4u] = 'free-4u.appspot.com'

air_sender = {}
air_sender[symbol_Polymorphic] = 'raychorn@gmail.com'
air_sender[symbol_PDFXporter] = 'raychorn@gmail.com'
air_sender[symbol_Logos] = 'raychorn@gmail.com'
air_sender[symbol_Flexstylus] = 'vyperlogix@gmail.com'
air_sender[symbol_ChartsDemo] = 'vyperlogix@gmail.com'
air_sender[symbol_free4u] = 'vyperlogix@gmail.com'

air_site = {}
air_site[symbol_Polymorphic] = 'www.Polymorphical.com'
air_site[symbol_PDFXporter] = 'www.PDFXporter.com'
air_site[symbol_Logos] = 'Logos'
air_site[symbol_Flexstylus] = 'Flex Stylus'
air_site[symbol_ChartsDemo] = 'Charts Demo'
air_site[symbol_free4u] = 'Free-4U'

updater_domainName = 'downloads.vyperlogix.com'


__QUEUE_DAILY_COUNT__ = 2000
__QUEUE_DAYS_COUNT__ = 7
__QUEUE_MAX_COUNT__ = __QUEUE_DAILY_COUNT__ * __QUEUE_DAYS_COUNT__

#__EMAIL_POST_ADDRESS__ = 'http://www.near-by.info/php/send_gmail2.php'
__EMAIL_POST_ADDRESS__ = 'http://www.near-by.info/php/send_gmail3.php'

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
    #logging.warning('today().1 _today=%s' % (_today))
    _today = _utils.getFromDateTimeStr(_utils.getAsSimpleDateStr(_today,_utils.formatDate_MMDDYYYY_slashes()),_utils.formatDate_MMDDYYYY_slashes())
    #logging.warning('today().2 _today=%s' % (_today))
    return _today

def get_starbucks_data(u,_user,__air_id__,parms):
    import models
    from vyperlogix import misc
    if (__air_id__ == symbol_free4u) and (parms[-2] == symbol_starbucks):
        next_sunday = next_drawing()
        # Choose only the Starbucks for the current version and user
        # then Choose the Starbucks for the current version and build-in a threshold like 1000 per drawing.
        starbucks = [s for s in models.StarbucksCheckIn.all() if (s.version == air_version[__air_id__]) and (s.drawing) and (s.drawing.date == next_sunday)]
        u['starbucks'] = {}
        if (len(starbucks) > 0):
            u['starbucks']['is_registered'] = len([s for s in starbucks if (not _user.is_anonymous) and (s.user.id == _user.id)]) > 0
        u['starbucks']['count'] = len(starbucks)
        #drawing = models.StarbucksDrawing.objects.filter(next_drawing__gte=next_sunday)
        # Make sure the next_drawing depends on the number of Starbucks for the current version...
        drawings = [s for s in models.StarbucksDrawing.all() if s.date == next_sunday]
        if (len(drawings) == 0):
            drawing = models.StarbucksDrawing(date=next_sunday,prize=5.0)
            drawing.save()
            drawings = [s for s in models.StarbucksDrawing.all() if s.date == next_sunday]
        winners = []
        for drawing in drawings:
            u['starbucks']['next_drawing'] = _utils.getAsSimpleDateStr(drawing.date,_utils.formatDate_MMDDYYYY_slashes())
            u['starbucks']['next_prize'] = asCurrency(drawing.prize)
            for winner in models.StarbucksWinner.all():
                if (winner.drawing.date == drawing.date):
                    winners.append(winner)
        if (len(winners) > 0):
            u['starbucks']['winners'] = {}
            for winner in winners:
                u['starbucks']['winners'][winner.winner.user.name] = {}
                u['starbucks']['winners'][winner.winner.user.name]['date'] = winner.drawing.date
                u['starbucks']['winners'][winner.winner.user.name]['prize'] = winner.drawing.prize
                u['starbucks']['winners'][winner.winner.user.name]['timestamp'] = _utils.getAsSimpleDateStr(winner.timestamp, _utils.formatApacheDateTimeStr())
        logging.debug('%s :: %s' % (misc.funcName(),dict_to_json(u)))
    return u

def get_email_count_for_today():
    import models
    _count = 0
    _today = next_sunday() if (__QUEUE_DAYS_COUNT__ == 7) else today()
    counts = [s for s in models.EMailStats.all() if s.date == _today]
    if (len(counts) > 0):
	aCount = counts[0]
	_count = aCount.count
    return _count

def send_php_email(url,parms={},is_html=False):
    import urllib,urllib2

    content = ''
    try:
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
	#info_string = _utils.formattedException(details=e)
	logging.warning('send_php_email().ERROR --> info_string=%s' % (str(e)))
    return content

def queue_email(email_from,email_to,email_subject,email_body,email_body_html,__air_id__,__sub_domain__,is_html=False):
    import uuid
    import models
    from django.conf import settings
    from google.appengine.api.taskqueue import TransientError, taskqueue, TaskRetryOptions
    results = ''
    info_string = ''
    if (settings.IS_PRODUCTION_SERVER):
	_count = get_email_count_for_today()
        logging.warning('%s.INFO.1 --> _count=%s' % (__name__,_count))
	if (_count < __QUEUE_MAX_COUNT__):
	    _uuid = str(uuid.uuid4())
	    email = models.EMailQueue(uuid=_uuid,email_from=email_from,email_to=email_to,email_subject=email_subject)
	    email.email_body = email_body
	    email.email_altbody = email_body_html
	    email.save()
	    emails = [s for s in models.EMailQueue.all() if s.uuid == _uuid]
	    info_string = '%s.1 --> len(emails)=%s' % (__name__,len(emails))
	    results += info_string + '\n\n'
	    logging.debug(info_string)
	    if (len(emails) > 0):
		email_queue = taskqueue.Queue(name='emails')
		url = '/_ah/queue/emailhandler/%s/%s/%s/' % (emails[0].id,__sub_domain__,__air_id__)
		info_string = '%s.2 --> url=%s' % (__name__,url)
		results += info_string + '\n\n'
		logging.debug(info_string)
		next_task = taskqueue.Task(url=url)
		try:
		    email_queue.add(next_task)
		except TransientError:
		    pass # There was a transient error while accessing the queue. Please try again later.
	else:
	    logging.warning('%s.INFO.2 --> _count=%s' % (__name__,_count))
	    email_queue = taskqueue.Queue(name='phpemail')
	    url = '/_ah/queue/phpemailhandler/'
	    next_task = taskqueue.Task(url=url,params={'url':__EMAIL_POST_ADDRESS__, 'to':email_to, 'subject':email_subject, 'body':email_body, 'altbody':email_body_html},retry_options=TaskRetryOptions(min_backoff_seconds=10,max_backoff_seconds=30,task_retry_limit=65535,task_age_limit=30))
	    try:
		email_queue.add(next_task)
	    except TransientError:
		pass # There was a transient error while accessing the queue. Please try again later.
    else:
        logging.info('%s.INFO --> from=%s, to=%s, subject=%s, message=%s' % (__name__,email_from,email_to,email_subject,email_body))
	send_php_email(__EMAIL_POST_ADDRESS__,parms={'to':email_to, 'subject':email_subject, 'body':email_body, 'altbody':email_body_html},is_html=is_html)
    return results

def current_air_sender(_air_id=''):
    #logging.log(logging.INFO,'_air_id="%s"' % (_air_id))
    return air_sender[_air_id] if (air_sender.has_key(_air_id)) else 'UNKNOWN'

def current_air_site(_air_id=''):
    #logging.log(logging.INFO,'_air_id="%s"' % (_air_id))
    return air_site[_air_id] if (air_site.has_key(_air_id)) else 'UNKNOWN'

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