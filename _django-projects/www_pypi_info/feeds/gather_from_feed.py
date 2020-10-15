import datetime

from feeds import models as feed_models

from django.contrib.sitemaps import ping_google

from vyperlogix.misc import _utils
from vyperlogix.html import myOOHTML as oohtml

_rss_feed = 'http://pypi.python.org/pypi?%3Aaction=rss'

def rss_content(url):
    from vyperlogix.rss import reader

    try:
	rss = reader.read_feed(url)
    except:
	rss = '(News is Offline at this time...)'

    return rss

def handle_rss_content(rss):
    delta = datetime.timedelta(days=0, hours=7)
    for item in rss:
	_name = item.title
	_link = item.link
	_descr = item.description
	_dt = item.pubdate
	
	_version = _link.split('/')[-1]
	_name = _name.replace(' %s' % (_version),'')
	feeds = feed_models.PyPI.objects.filter(name=_name)
	if (feeds.count() == 0):
	    ts = _utils.getFromDateTimeStr(_dt,format=_utils.formatDjangoDateTimeStr()) - delta
	    now = _utils.timeStampLocalTime(tsecs=_utils.timeSecondsFromTimeStamp(ts),format=_utils.format_mySQL_DateTimeStr())
	    aFeed = feed_models.PyPI(name=_name,version=_version,link=_link,descr=_descr,timestamp=now)
	    aFeed.save()
	    print '(+) %s %s, %s, %s' % (aFeed.name,aFeed.version,aFeed.link,aFeed.timestamp)
	    ping_google()
	else:
	    aFeed = feeds[0]
	    ts = _utils.getFromDateTimeStr(_dt,format=_utils.formatDjangoDateTimeStr()) - delta
	    if (ts != aFeed.timestamp) or (_link != aFeed.link) or (_descr != aFeed.descr) or (_version != aFeed.version):
		aFeed.version = _version
		aFeed.link = _link
		aFeed.descr = _descr
		now = _utils.timeStampLocalTime(tsecs=_utils.timeSecondsFromTimeStamp(ts),format=_utils.format_mySQL_DateTimeStr())
		aFeed.timestamp = now
		aFeed.save()
		print '(*) %s %s, %s, %s' % (aFeed.name,aFeed.version,aFeed.link,aFeed.timestamp)
		ping_google()
    return rss

if (__name__ == '__main__'):
    print 'Reading the feed...',
    rss = rss_content(_rss_feed)
    print 'done!'
    
    print 'Adding data to database...'
    handle_rss_content(rss)
    print 'done!'
    
    pass
