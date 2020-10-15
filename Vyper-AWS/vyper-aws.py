import os, sys
import urlparse
import random
import time
import urllib

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix.hash import lists

from vyperlogix.classes import SmartObject

from vyperlogix import oodb

from vyperlogix.url.tiny import bitly
from vyperlogix.socials.tweets import twitter_post_update

import logging

from vyperlogix.daemon.daemon import Log
from vyperlogix.daemon.daemon import CustomLog
from vyperlogix.logging import standardLogging

_root_ = os.path.dirname(__file__)
_data_path_ = os.path.join(_root_,'dbx')

_movie_indexes = [('DVD','Babylon 5'),('DVD','Star Trek'),('DVD','Action'),('DVD','Sex'),('DVD','Sci Fi')]
_gamer_indexes = [('VideoGames','XBox'),('VideoGames','PSP'),('VideoGames','PS2'),('VideoGames','PS3'),('VideoGames','Gameboy')]

# 'All'
_all_indexes = ['Apparel', 'Automotive', 'Baby', 'Beauty', 'Blended', 'Books', 'Classical', 'DVD', 'DigitalMusic', 'Electronics', 
		'GourmetFood', 'Grocery', 'HealthPersonalCare', 'HomeGarden', 'Industrial', 'Jewelry', 'KindleStore', 'Kitchen', 
		'MP3Downloads', 'Magazines', 'Marketplace', 'Merchants', 'Miscellaneous', 'Music', 'MusicTracks', 'MusicalInstruments', 
		'OfficeProducts', 'OutdoorLiving', 'PCHardware', 'PetSupplies', 'Photo', 'Shoes', 'SilverMerchants', 'Software', 
		'SportingGoods', 'Tools', 'Toys', 'UnboxVideo', 'VHS', 'Video', 'VideoGames', 'Watches', 'Wireless', 'WirelessAccessories']

d_twitter = lists.HashedLists2()
d_twitter['vyperlogix'] = 'peekab00'

d_bitly = lists.HashedLists2()
d_bitly['python'] = 'R_80abf6d71153a5b99652637f7b08a37d'

# 'http://astore.amazon.com/vyplogblo-20/detail/%s' % ('1430218436') # where 1430218436 is the ASIN.

# movietwitz/peekab00
# gamertwitz/peekab00

def _init_(logging,dbx_name,_indexes):
    import ecs
    ecs.setLicenseKey(_licensekey)
    
    logging.info('%s :: Performing Intialization.' % (_utils.timeStampLocalTime()))
    
    dbx = oodb.PickledFastHash2(dbx_name)
    dbx.open()
    try:
	for anIndex in _indexes:
	    index,keyword = anIndex
	    try:
		i = 0
		items = ecs.ItemSearch(keyword, SearchIndex=index, ResponseGroup='Small')
		logging.info('%s :: %s->%s.' % (_utils.timeStampLocalTime(),index,keyword))
		n = len(items)
		for anItem in items:
		    so = SmartObject.SmartObject2()
		    so.ASIN = anItem.ASIN
		    so.DetailPageURL = anItem.DetailPageURL
		    so.ProductGroup = anItem.ProductGroup
		    so.Title = anItem.Title
		    so.used = 0
		    dbx[so.ASIN] = rec = so.asPythonDict()
		    logging.info('%s :: %d of %d %s.' % (_utils.timeStampLocalTime(),i,n,rec))
		    i += 1
		logging.info('%s :: %d items.' % (_utils.timeStampLocalTime(),n))
	    except Exception, e:
		logging.error('%s :: %s.' % (_utils.timeStampLocalTime(),_utils.formattedException(details=e)))
	    pass
    except Exception, e:
	logging.error('%s :: %s.' % (_utils.timeStampLocalTime(),_utils.formattedException(details=e)))
    finally:
	dbx.flush()
	logging.error('%s :: There are %d items in %s.' % (_utils.timeStampLocalTime(),len(dbx),dbx_name))
	dbx.close()
	
def main(logging):
    normalize = lambda foo:foo[0] if (misc.isList(foo)) else foo
    explain_boolean = lambda foo:'True' if (foo) else 'False'
    _isInit_movies = _isInit_games = _isInit
    for username,password in d_twitter.iteritems():
	_utils._makeDirs(_data_path_)
	dbx_name_movies = oodb.dbx_name('amazon_%s_movies.dbx' % (username),_data_path_)
	dbx = oodb.PickledFastHash2(dbx_name_movies)
	dbx.open()
	try:
	    is_empty = len(dbx) == 0
	    items_not_used = [so for so in [SmartObject.SmartObject2(normalize(v)) for v in dbx.values()] if (so.used == 0)]
	    _isInit_movies = (is_empty) or (len(items_not_used) == 0) or (_isInit)
	except:
	    pass
	finally:
	    dbx.close()
	dbx_name_games = oodb.dbx_name('amazon_%s_games.dbx' % (username),_data_path_)
	dbx = oodb.PickledFastHash2(dbx_name_games)
	dbx.open()
	try:
	    is_empty = len(dbx) == 0
	    items_not_used = [so for so in [SmartObject.SmartObject2(normalize(v)) for v in dbx.values()] if (so.used == 0)]
	    _isInit_games = (is_empty) or (len(items_not_used) == 0) or (_isInit)
	except:
	    pass
	finally:
	    dbx.close()
    logging.info('%s :: _isInit_movies is %s because is_empty is %s and items_not_used is %d.' % (_utils.timeStampLocalTime(),_isInit_movies,explain_boolean(is_empty),len(items_not_used)))
    logging.info('%s :: _isInit_games is %s because is_empty is %s and items_not_used is %d.' % (_utils.timeStampLocalTime(),_isInit_games,explain_boolean(is_empty),len(items_not_used)))
    if (_isInit_movies):
	fname = oodb.getMungedFilenameFor(dbx_name_movies)
	if (os.path.exists(fname)):
	    logging.info('%s :: Removing %s.' % (_utils.timeStampLocalTime(),dbx_name_movies))
	    os.remove(fname)
	_init_(logging,dbx_name_movies,_movie_indexes)
    if (_isInit_games):
	fname = oodb.getMungedFilenameFor(dbx_name_games)
	if (os.path.exists(fname)):
	    logging.info('%s :: Removing %s.' % (_utils.timeStampLocalTime(),dbx_name_games))
	    os.remove(fname)
	_init_(logging,dbx_name_games,_gamer_indexes)
    
if (__name__ == '__main__'):
    from vyperlogix.misc import Args
    from vyperlogix.misc import PrettyPrint

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--init':'init the Amazon database.',
	    '--trackingid=?':'the tracking id for the amazon store.',
	    '--licensekey=?':'the license key for the AWS api.',
	    '--cwd=?':'the path the program runs from, defaults to the path the program runs from.',
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
	logging.warning(info_string)
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
	if _argsObj.booleans.has_key('isInit'):
	    _isInit = _argsObj.booleans['isInit']
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
    
    _trackingid = 'vyplogblo-20'
    try:
	_trackingid = eval(_argsObj.arguments['trackingid']) if _argsObj.arguments.has_key('trackingid') else _trackingid
    except:
	pass
    
    _licensekey = 'AKIAI52A6BTLWZHHDLCA'
    try:
	_licensekey = eval(_argsObj.arguments['licensekey']) if _argsObj.arguments.has_key('licensekey') else _licensekey
    except:
	pass
	
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
    fpath=_cwd
    _log_path = _utils.safely_mkdir_logs(fpath=fpath)
    _log_path = _utils.safely_mkdir(fpath=_log_path,dirname=_utils.timeStampLocalTimeForFileName(delimiters=('_'),format=_utils.formatDate_MMDDYYYY_dashes()))
    #_data_path = _utils.safely_mkdir(fpath=fpath,dirname='dbx')

    logFileName = os.sep.join([_log_path,'%s.log' % (name)])

    print '(%s) :: logFileName=%s' % (_utils.timeStampLocalTime(),logFileName)

    _stdOut = open(os.sep.join([_log_path,'stdout.txt']),'w')
    _stdErr = open(os.sep.join([_log_path,'stderr.txt']),'w')
    _stdLogging = open(logFileName,'w')

    if (not _utils.isBeingDebugged):
	sys.stdout = Log(_stdOut)
	sys.stderr = Log(_stdErr)
    _logLogging = CustomLog(_stdLogging)

    standardLogging.standardLogging(logFileName,_level=_logging,console_level=_console_logging,isVerbose=_isVerbose)

    _logLogging.logging = logging # echos the log back to the standard logging...
    logging = _logLogging # replace the default logging with our own custom logging...

    main(logging)
    