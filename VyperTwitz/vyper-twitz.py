import os, sys
import urlparse
import random
import time
import urllib

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix.lists.ListWrapper import ListWrapper

from vyperlogix import oodb

from vyperlogix.misc import ReportTheList

from vyperlogix.sql.sqlalchemy import queries

from vyperlogix.classes.SmartObject import SmartObject2 as SmartObject

from vyperlogix.url.tiny import bitly

from vyperlogix.products import keys

import logging

from vyperlogix.daemon.daemon import Log
from vyperlogix.daemon.daemon import CustomLog
from vyperlogix.logging import standardLogging

from vyperlogix.misc import threadpool

from vyperlogix.analysis import ioTimeAnalysis

from vyperlogix.django import django_utils

_isTest = False
_isBitlyTest = False

#_secure_url = lambda login,apikey,url:'http://www.vyperlogix.com/twitter-special/?'+keys._encode('django=1&TWITTER_LINK='+keys._encode(bitly(login,apikey,url)))
#_bitly = lambda login,apikey,url:bitly(login,apikey,_secure_url(login,apikey,url)) if (not _isBitlyTest) else _secure_url(login,apikey,url)

_secure_url = 'http://www.vyperlogix.com'
_bitly = lambda login,apikey,url:bitly(login,apikey,_secure_url(login,apikey,url)) if (not _isBitlyTest) else _secure_url

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()

if (_cname in ['undefined3','id3859']):
    print 'TEST MODE...'
    from vyperlogix.socials.tweets import twitter_post_update_simulated as twitter_post_update
else:
    from vyperlogix.socials.tweets import twitter_post_update

import sqlalchemy_models
# prepositional phrase - begin with preposition end with a noun.

random.seed()

messages_1 = []
messages_2 = []
messages_3 = []

_root_ = os.path.dirname(__file__)
_data_path_ = os.path.join(_root_,'dbx')

amazon_licensekey = 'AKIAI52A6BTLWZHHDLCA'
amazon_trackingid = 'vyplogblo-20'

def get_smtp_server():
    from vyperlogix.mail.mailServer import GMailServer
    smtp = GMailServer(keys._decode('76797065726C6F67697840676D61696C2E636F6D'), keys._decode('7065656B61623030'))
    return smtp

def send_problem_email(email_address,problem_msg,subject):
    try:
	from vyperlogix.mail.message import Message
	msg = Message(email_address,'support@vyperlogix.com', problem_msg, subject=subject)
	smtp = get_smtp_server()
	smtp.sendEmail(msg)
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print 'ERROR :: %s' % (info_string)

    return msg_context

def rss_links(url):
    from vyperlogix.rss import reader

    try:
	links = reader.read_feed_links(url)
    except:
	links = []

    return links

def rss(url):
    from vyperlogix.rss import reader

    try:
	links = reader.read_feed(url)
    except:
	links = []

    return links

def sitemap_links(url):
    from vyperlogix.sitemap import reader

    try:
	links = reader.read_sitemap_links(url)
    except:
	links = []

    return links

def make_sense_of_url(url):
    toks = misc.reverseCopy([t for t in str(url).split('/') if (len(t) > 0)])
    parts = []
    combine_parts = lambda foo:' '.join([urllib.unquote_plus(s).replace('-',' ').replace('_',' ').capitalize() for s in misc.reverseCopy(foo)])
    for t in toks:
	if (t.isdigit()) or (len(t.split('.')) > 1):
	    return combine_parts(parts)
	parts.append(t)
    return combine_parts(parts)

def products(db_handle,logging):
    import ecs
    ecs.setLicenseKey(amazon_licensekey)

    db_handle.agentProducts.new_session()
    qryProductKeywords = sqlalchemy_models.get_product_keywords_query(db_handle.agentProducts)
    if (qryProductKeywords.count() > 0):
	for aProductKeyword in qryProductKeywords:
	    items = ecs.ItemSearch(aProductKeyword.ProductKeywords.keyword, SearchIndex=aProductKeyword.ProductIndexes.product, ResponseGroup='Small')
	    n = len(items)
	    logging.info('%s :: %s->%s has %s items.' % (_utils.timeStampLocalTime(),aProductKeyword.ProductIndexes.product,aProductKeyword.ProductKeywords.keyword,n))
	    try:
		for anItem in items:
		    db_handle.agentProducts.new_session()
		    aProduct = sqlalchemy_models.Products(indx=aProductKeyword.ProductIndexes.id,asin=anItem.ASIN,url=urllib.unquote_plus(anItem.DetailPageURL),group=anItem.ProductGroup,title=anItem.Title)
		    sqlalchemy_models.put(db_handle.agentProducts,aProduct,logging=logging)
		    if (len(db_handle.agentProducts.lastError) > 0):
			print >>sys.stderr, db_handle.agentProducts.lastError
	    except Exception, e:
		info_string = _utils.formattedException(details=e)
		print >>sys.stderr, info_string
    else:
	print >>sys.stderr, 'WARNING :: Cannot process the lack of products...'

def fetch_rss(anRSS,links):
    for aLink in rss(anRSS):
	links.append(aLink)

def feed_source_with_links(aSource,links,_msgs_):
    if (len(links) > 0):
	_choice_source_aSource = aSource
	now = _utils.today_localtime()
	now_ts = _utils.timeSecondsFromTimeStamp(now)
	last_ts = _utils.timeSecondsFromTimeStamp(_choice_source_aSource.Feeds.last_used) if (_choice_source_aSource.Feeds.last_used is not None) else now_ts
	diff_secs = max(now_ts,last_ts) - min(now_ts,last_ts)
	print 'DEBUG :: now is %s, _choice_source_aSource.Feeds.last_used is %s, diff_secs is %s, _choice_source_aSource.Feeds.frequency is %s' % (now,_choice_source_aSource.Feeds.last_used,diff_secs,_choice_source_aSource.Feeds.frequency)
	is_twitz = (diff_secs < _choice_source_aSource.Feeds.frequency) and (_choice_source_aSource.Feeds.last_used is not None)
	_links = misc.copy(links)
	ioTimeAnalysis.init_AnalysisDataPoint('while(is_twitz)')
	ioTimeAnalysis.begin_AnalysisDataPoint('while(is_twitz)')
	iLoopCount = 0
	while (not is_twitz) and (iLoopCount < 10):
	    choice = random.choice(links)
	    logging.info('%s :: Choice is "%s".' % (_utils.timeStampLocalTime(),str(choice)))
	    db_handle.agentUsedLinks.new_session()
	    qryUsedLink = sqlalchemy_models.get_used_link_query(db_handle.agentUsedLinks,choice.link,_choice_source_aSource.Sources.id)
	    if (qryUsedLink.count() == 0):
		logging.info('%s :: Choice link is "%s".' % (_utils.timeStampLocalTime(),choice.link))
		url = _bitly(aSource.Bitlys.api_login,aSource.Bitlys.api_key,choice.link)
		deferred = []
		rand_phrase_type = random.choice(_msgs_)
		qryPhrases = sqlalchemy_models.get_least_used_phrases_query(db_handle.agentPhrases,rand_phrase_type)
		aPhrasesWrapper = queries.QueryWrapper(qryPhrases)
		print 'DEBUG :: qryPhrases.count() is %s.' % (qryPhrases.count())
		try:
		    aPhrase = random.choice(aPhrasesWrapper)
		    rand_msg = aPhrase.phrase
		    i = aPhrase.phrase_type
		    if (i == 1):
			extra = ' %s' % (choice.description[0:136-(len(rand_msg)+len(url))])
			message = '%s%s' % (rand_msg,extra)
			if (len(message)+len(url) > 135):
			    message = message[0:135-len(url)]+'...'
			message += ' '+str(url)
			twitter_post_update(aSource.Feeds.username,aSource.Feeds.password,_utils.ascii_only(message))
		    else:
			sponsors = sqlalchemy_models.get_sponsor_query(db_handle.agentSponsors,i)
			if (sponsors.count() > 0):
			    aSponsor = sponsors[0]
			    last_ts = _utils.timeSecondsFromTimeStamp(aSponsor.last_used) if (aSponsor.last_used is not None) else now_ts
			    diff_secs = max(now_ts,last_ts) - min(now_ts,last_ts)
			    print 'DEBUG :: now is %s, aSponsor.last_used is %s, diff_secs is %s, aSponsor.freq_secs is %s' % (now,aSponsor.last_used,diff_secs,aSponsor.freq_secs)
			    if (aSponsor.last_used is None) or (diff_secs >= aSponsor.freq_secs): 
				url_sponsor = _bitly(aSource.Bitlys.api_login,aSource.Bitlys.api_key,aSponsor.url)
				message = '%s %s.' % (rand_msg,url_sponsor)
				deferred.append(message)
				aSponsor.last_used = now
				sqlalchemy_models.put(db_handle.agentSponsors,aSponsor,logging=logging)
		    aPhrase.last_used = now
		    sqlalchemy_models.put(db_handle.agentPhrases,aPhrase,logging=logging)
		    if (len(deferred) > 0):
			cnt = 0
			for twit in deferred:
			    cnt += len(twit)
			if (cnt < 140):
			    twitter_post_update(aSource.Feeds.username,aSource.Feeds.password,' '.join([_utils.ascii_only(m) for m in deferred]))
			else:
			    for m in deferred:
				twitter_post_update(aSource.Feeds.username,aSource.Feeds.password,_utils.ascii_only(m))
		    db_handle.agentUsedLinks.new_session()
		    aUsedLink = sqlalchemy_models.UsedLinks(link=choice.link,source=_choice_source_aSource.Sources.id)
		    sqlalchemy_models.put(db_handle.agentUsedLinks,aUsedLink,logging=logging)
		    is_twitz = True
		    print 'DEBUG :: UPDATE _choice_source_aSource.Feeds.last_used.'
		    _choice_source_aSource.Feeds.last_used = now
		    sqlalchemy_models.put(db_handle.agentSources,_choice_source_aSource,logging=logging)
		    break
		except IndexError, e:
		    is_twitz = True
		    print 'DEBUG :: is_twitz is %s due to an error.' % (is_twitz)
		    info_string = _utils.formattedException(details=e)
		    print >>sys.stderr, info_string
		    break
	    else:
		links = list(set(links) - set([choice]))
	    if (len(links) == 0):
		logging.info('%s :: Removing all the previously used links for %s.' % (_utils.timeStampLocalTime(),_choice_source_aSource.Sources.source))
		db_handle.agentUsedLinks.new_session()
		qryAllUsedLinks = sqlalchemy_models.get_used_links_query(db_handle.agentUsedLinks,_choice_source_aSource.Sources.id)
		if (qryAllUsedLinks.count() > 0):
		    for obj in qryAllUsedLinks:
			db_handle.agentUsedLinks.delete(obj)
		    db_handle.agentUsedLinks.flush()
		links = misc.copy(_links)
		iLoopCount += 1
	ioTimeAnalysis.end_AnalysisDataPoint('while(is_twitz)')

def main(db_handle,logging,source=-1):
    normalize_phrase = lambda foo:foo[0:29]+('...' if (len(foo) > 29) else '')

    if (_isInit):
	qry = sqlalchemy_models.get_prepositions_query(db_handle.agentPrepositions)
	if (qry.count() > 0):
	    for obj in qry:
		db_handle.agentPrepositions.delete(obj)
	    db_handle.agentPrepositions.flush()
	db_handle.agentPhrases.new_session()
	words = list(set([t.strip() for t in _utils.readFileFrom(os.path.join(_root_,'prepositions.txt')).split('\n') if (len(t.strip()) > 0)]))
	for word in words:
	    aPreposition = sqlalchemy_models.Prepositions(preposition=word)
	    sqlalchemy_models.put(db_handle.agentPrepositions,aPreposition,logging=logging)
	if (len(messages_1) > 0) and (len(messages_2) > 0) and (len(messages_3) > 0):
	    qry = sqlalchemy_models.get_query(db_handle.agentPhrases,sqlalchemy_models.Phrases)
	    if (qry.count() > 0):
		for obj in qry:
		    db_handle.agentPhrases.delete(obj)
		db_handle.agentPhrases.flush()
	    db_handle.agentPhrases.new_session()
	    for phrase in messages_1:
		aPhrase = sqlalchemy_models.Phrases(phrase=normalize_phrase(phrase),phrase_type=1)
		sqlalchemy_models.put(db_handle.agentPhrases,aPhrase,logging=logging)
	    db_handle.agentPhrases.new_session()
	    for phrase in messages_2:
		aPhrase = sqlalchemy_models.Phrases(phrase=normalize_phrase(phrase),phrase_type=2)
		sqlalchemy_models.put(db_handle.agentPhrases,aPhrase,logging=logging)
	    db_handle.agentPhrases.new_session()
	    for phrase in messages_3:
		aPhrase = sqlalchemy_models.Phrases(phrase=normalize_phrase(phrase),phrase_type=3)
		sqlalchemy_models.put(db_handle.agentPhrases,aPhrase,logging=logging)
	pass
    ioTimeAnalysis.init_AnalysisDataPoint('get_phrases_query')
    _msgs_ = []
    ioTimeAnalysis.begin_AnalysisDataPoint('get_phrases_query')
    db_handle.agentPhrases.new_session()
    qryPhrases = sqlalchemy_models.get_phrases_query(db_handle.agentPhrases)
    if (qryPhrases.count() > 0):
	for aPhrase in qryPhrases:
	    _msgs_.append(aPhrase.phrase_type)
    ioTimeAnalysis.end_AnalysisDataPoint('get_phrases_query')
    d_feeds_aggregator = lists.HashedLists()
    ioTimeAnalysis.init_AnalysisDataPoint('get_sources_with_joins_query')
    ioTimeAnalysis.begin_AnalysisDataPoint('get_sources_with_joins_query')
    qrySources = sqlalchemy_models.get_sources_with_joins_query(db_handle.agentSources)
    if (source > -1):
	qrySources = qrySources.filter('sources.id=:source').params(source=source)
    for aSource in qrySources:
	if (aSource.Sources.source_type == 'rss'):
	    d_feeds_aggregator[aSource.Sources.feed] = aSource.Sources.source
    ioTimeAnalysis.end_AnalysisDataPoint('get_sources_with_joins_query')
    links = []
    is_links_completed = False
    i_links = 0
    for aSource in qrySources:
	if (not is_links_completed):
	    ioTimeAnalysis.init_AnalysisDataPoint('get_rss_links%d' % (i_links))
	    ioTimeAnalysis.begin_AnalysisDataPoint('get_rss_links%d' % (i_links))
	    if (aSource.Sources.source_type == 'rss'):
		for anRSS in d_feeds_aggregator[aSource.Sources.feed]:
		    fetch_rss(anRSS,links)
	    else:
		print >>sys.stderr, 'WARNING :: Cannot handle this source type "%s".' % (aSource.Sources.source_type)
	    print >>sys.stderr, 'INFO :: Waiting for RSS Links to finish before proceeding...'
	    is_links_completed = True
	    ioTimeAnalysis.end_AnalysisDataPoint('get_rss_links%d' % (i_links))
	    i_links += 1
	print 'DEBUG :: Feed is %s (%s), Source is %s, %s links.' % (aSource.Feeds.name,aSource.Sources.feed,aSource.Sources.source,len(links))
	feed_source_with_links(aSource,links,_msgs_)
    ioTimeAnalysis.ioTimeAnalysis.ioTimeAnalysisReport()

if (__name__ == '__main__'):
    from vyperlogix.misc import Args
    from vyperlogix.misc import PrettyPrint

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--init':'initialize the database.',
	    '--products':'initialize the products database.',
	    '--test':'test the system.',
	    '--bitlytest':'test the bitly system.',
	    '--test=?':'test the system for a number of seconds.',
	    '--dbuser=?':'database username.',
	    '--dbpwd=?':'database password.',
	    '--dbhost=?':'database host.',
	    '--dbport=?':'database port.',
	    '--dbname=?':'database name.',
	    '--source=?':'source id or the id of a source.',
	    '--sources':'this option causes each of the sources in the database to be fired off in the background.',
	    '--cwd=?':'the path the program runs from, defaults to the path the program runs from.',
	    '--interval=?':'number of seconds between updates.',
	    '--logging=?':'[logging.INFO,logging.WARNING,logging.ERROR,logging.DEBUG]',
	    '--console_logging=?':'[logging.INFO,logging.WARNING,logging.ERROR,logging.DEBUG]'}
    _argsObj = Args.Args(args)

    _progName = _argsObj.programName
    _isVerbose = True
    try:
	if _argsObj.booleans.has_key('isVerbose'):
	    _isVerbose = _argsObj.booleans['isVerbose']
    except Exception, e:
	info_string = _utils.formattedException(details=e)
	print >>sys.stderr, info_string
	_isVerbose = False
	
    _isHelp = False
    try:
	if _argsObj.booleans.has_key('isHelp'):
	    _isHelp = _argsObj.booleans['isHelp']
    except:
	pass
    
    if (_isHelp):
	ppArgs()

    _isInit = False
    try:
	_isInit = _argsObj.booleans['isInit'] if _argsObj.booleans.has_key('isInit') else False
    except:
	pass

    _isProducts = False
    try:
	_isProducts = _argsObj.booleans['isProducts'] if _argsObj.booleans.has_key('isProducts') else False
    except:
	pass

    _isTest = False
    try:
	_isTest = _argsObj.booleans['isTest'] if _argsObj.booleans.has_key('isTest') else False
    except:
	pass
    
    _isBitlyTest = False
    try:
	_isBitlyTest = _argsObj.booleans['isBitlytest'] if _argsObj.booleans.has_key('isBitlytest') else False
    except:
	pass
    
    _testInterval = 0
    try:
	_testInterval = _argsObj.arguments['test'] if _argsObj.arguments.has_key('test') else _testInterval
	_testInterval = int(_testInterval)
	_isTest = (_testInterval > 0) | _isTest
    except:
	pass
    
    __cwd__ = os.path.dirname(sys.argv[0])
    try:
	__cwd = _argsObj.arguments['cwd'] if _argsObj.arguments.has_key('cwd') else __cwd__
	if (len(__cwd) == 0) or (not os.path.exists(__cwd)):
	    if (os.environ.has_key('cwd')):
		__cwd = os.environ['cwd']
	__cwd__ = __cwd
    except:
	pass
    _cwd = __cwd__
    
    _interval = 60*9
    try:
	_interval = _argsObj.arguments['interval'] if _argsObj.arguments.has_key('interval') else _interval
	_interval = int(_interval)
    except:
	pass
    
    _dbuser = ''
    try:
	_dbuser = _argsObj.arguments['dbuser'] if _argsObj.arguments.has_key('dbuser') else ''
    except:
	pass
    
    _dbpwd = ''
    try:
	_dbpwd = _argsObj.arguments['dbpwd'] if _argsObj.arguments.has_key('dbpwd') else ''
    except:
	pass
    
    _dbhost = ''
    try:
	_dbhost = _argsObj.arguments['dbhost'] if _argsObj.arguments.has_key('dbhost') else ''
    except:
	pass
    
    _dbport = ''
    try:
	_dbport = _argsObj.arguments['dbport'] if _argsObj.arguments.has_key('dbport') else ''
    except:
	pass
    
    _dbname = ''
    try:
	_dbname = _argsObj.arguments['dbname'] if _argsObj.arguments.has_key('dbname') else ''
    except:
	pass
    
    _source = -1
    try:
	_source = _argsObj.arguments['source'] if _argsObj.arguments.has_key('source') else -1
	_source = django_utils._int(_source)
    except:
	pass
    
    _isSources = False
    try:
	_isSources = _argsObj.booleans['isSources'] if _argsObj.booleans.has_key('isSources') else False
    except:
	pass
    
    db_handle = SmartObject()
    db_handle.username = _dbuser
    db_handle.password = _dbpwd
    db_handle.hostname = _dbhost
    db_handle.port = _dbport
    db_handle.database = _dbname
    db_handle.conn_str = 'mysql://%s:%s@%s:%s/%s' % (db_handle.username,db_handle.password,db_handle.hostname,db_handle.port,db_handle.database)
    db_handle.agentPrepositions = sqlalchemy_models.agentPrepositions(db_handle)
    db_handle.agentPhrases = sqlalchemy_models.agentPhrases(db_handle)
    db_handle.agentUsedLinks = sqlalchemy_models.agentUsedLinks(db_handle)
    db_handle.agentSources = sqlalchemy_models.agentSources(db_handle)
    db_handle.agentProducts = sqlalchemy_models.agentProducts(db_handle)
    db_handle.agentSponsors = sqlalchemy_models.agentSponsors(db_handle)
    
    print db_handle.conn_str
    
    _logging = logging.WARNING
    try:
	_logging = eval(_argsObj.arguments['logging']) if _argsObj.arguments.has_key('logging') else False
    except:
	_logging = logging.WARNING
	
    _console_logging = logging.WARNING
    try:
	_console_logging = eval(_argsObj.arguments['console_logging']) if _argsObj.arguments.has_key('console_logging') else False
    except:
	_console_logging = logging.WARNING

    name = _utils.getProgramName()
    fpath = _cwd
    _log_path = _utils.safely_mkdir_logs(fpath=fpath)
    _log_path = _utils.safely_mkdir(fpath=_log_path,dirname=_utils.timeStampLocalTimeForFileName(delimiters=('_','-'),format=_utils.formatSalesForceTimeStr()))

    logFileName = os.sep.join([_log_path,'%s_%s.log' % (name,_source)])

    print '(%s) :: logFileName=%s' % (_utils.timeStampLocalTime(),logFileName)

    _stdOut = open(os.sep.join([_log_path,'stdout.txt']),'a')
    _stdErr = open(os.sep.join([_log_path,'stderr.txt']),'a')
    _stdLogging = open(logFileName,'a')

    if (not _utils.isBeingDebugged):
	sys.stdout = Log(_stdOut)
	sys.stderr = Log(_stdErr)
    _logLogging = CustomLog(_stdLogging)

    standardLogging.standardLogging(logFileName,_level=_logging,console_level=_console_logging,isVerbose=_isVerbose)

    _logLogging.logging = logging # echos the log back to the standard logging...
    logging = _logLogging # replace the default logging with our own custom logging...
    
    # when _isSources is True then issue the same command line for each source but replace --sources with --source=1 where "1" is the source id.
    if (not _isInit) and (not _isTest) and (not _isProducts):
	i = random.randint(0,_interval)
	#logging.info('%s :: Waiting... %d seconds.' % (_utils.timeStampLocalTime(),i))
	#time.sleep(i)
    elif (not _isInit) and (_isTest) and (_testInterval > 0) and (not _isProducts):
	logging.info('%s :: testing... for %d seconds.' % (_utils.timeStampLocalTime(),_testInterval))
	begin_ts = _utils.timeSecondsFromTimeStamp(_utils.today_localtime())
	while ((_utils.timeSecondsFromTimeStamp(_utils.today_localtime()) - begin_ts) < _testInterval):
	    if (_isSources):
		from vyperlogix.process import Popen
		l_sys_argv = ListWrapper(sys.argv)
		qrySources = sqlalchemy_models.get_sources_with_joins_query(db_handle.agentSources)
		for aSource in qrySources:
		    _id = aSource.Sources.id
		    i = l_sys_argv.findFirstMatching('--sources')
		    if (i > -1):
			l_sys_argv[i] = '--source=%s' % (i)
			ioBuf = _utils.stringIO()
			cmd = 'python %s' % (' '.join(l_sys_argv))
			print >>sys.stdout, 'INFO :: %s' % (cmd)
			shell = Popen.Shell([cmd],isExit=True,isWait=False,isVerbose=True,fOut=ioBuf)
	    else:
		main(db_handle,logging,source=_source)
	logging.info('%s :: exiting...' % (_utils.timeStampLocalTime()))
	sys.exit(1)
    elif (_isProducts):
	products(db_handle,logging)
    if (not _isProducts):
	main(db_handle,logging,source=_source)
    print >>sys.stderr, 'DONE !'
