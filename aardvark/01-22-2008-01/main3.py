import psyco
import sys
from os import path
import os
import time
import pyodbc
import gc
import datetime
import adodbapi

_isVerbose = False
_sequence_start = 0x0000000000000000
_sequence_end = 0xFFFFFFFFFFFFFFFF

_mssql_connection_string = 'DRIVER={SQL Server};SERVER=MURRE\DEV2005;DATABASE=aardvark_fresh;CommandTimeout=0;UID=sa;PWD=peekaboo'
_mssql_connection_string2 = 'DRIVER={SQL Server};SERVER=MURRE\DEV2005;DATABASE=surrogate_countrywide;CommandTimeout=0;UID=sa;PWD=peekaboo'

_colsep3 = chr(255)
_rowsep3 = "\n"

_ioTime = {}
_ioElapsedTime = 0

DSS_RUN_MODE_USE_INTERNAL_ID = 0
DSS_RUN_MODE_USE_BES_ID = 1

# DSS_RUN_MODE => 0 means do convert bes_computer_id into an internal computer id
# DSS_RUN_MODE => 1 means do not convert bes_computer_id into an internal computer id
#DSS_RUN_MODE = DSS_RUN_MODE_USE_BES_ID
DSS_RUN_MODE = DSS_RUN_MODE_USE_INTERNAL_ID

# these col_index_* constants specify mappings of column index from a query or field index from a csv file
COL_INDEX_COMPUTER_ID = 0
COL_INDEX_VALUE = 1
COL_INDEX_SEQUENCE = 2
COL_INDEX_PROPERTY_ID = 3
COL_INDEX_SITE_ID = 4

INT_COLS_LIST = [COL_INDEX_COMPUTER_ID,COL_INDEX_SEQUENCE,COL_INDEX_PROPERTY_ID,COL_INDEX_SITE_ID]

# these are constants from aardvark table 'property_types'
PROPERTY_TYPE_COMPUTER = 1
PROPERTY_TYPE_APP_TRACKING = 2
PROPERTY_TYPE_INSTALLED_APPS = 3

# output format of csv files this script will generate
OUTPUT_COL_SEP = "\t\t"
OUTPUT_ROW_SEP = "\n\n"

# csv files this script will generate
OUTPUT_FILE_PROPERTIES = "%s%setl_computer_properties.csv" % (os.getcwd(),os.sep)
OUTPUT_FILE_PACKAGES = "%s%setl_computers_packages.csv" % (os.getcwd(),os.sep)
OUTPUT_FILE_APP_TRACKING = "%s%setl_computer_app_tracking.csv" % (os.getcwd(),os.sep)
OUTPUT_FILE_CIDS_W_PROPERTIES = "%s%setl_computers_with_properties.csv" % (os.getcwd(),os.sep)
OUTPUT_FILE_CIDS_W_PACKAGES = "%s%setl_computers_with_packages.csv" % (os.getcwd(),os.sep)
OUTPUT_FILE_CIDS_W_APP_TRACKING = "%s%setl_computers_with_app_tracking.csv" % (os.getcwd(),os.sep)

OUTPUT_FILE_LIST = [OUTPUT_FILE_PROPERTIES,OUTPUT_FILE_PACKAGES,OUTPUT_FILE_APP_TRACKING,OUTPUT_FILE_CIDS_W_PROPERTIES,OUTPUT_FILE_CIDS_W_PACKAGES,OUTPUT_FILE_CIDS_W_APP_TRACKING]

# SQL Server XML bulk format files this script will use when bulk inserting the data
SQL_FORMAT_FILE_PROPERTIES = "%s%scomputer_properties_format.xml" % (os.getcwd(),os.sep)
SQL_FORMAT_FILE_PACKAGES = "%s%scomputers_packages_format.xml" % (os.getcwd(),os.sep)
SQL_FORMAT_FILE_APP_TRACKING = "%s%scomputer_app_tracking_format.xml" % (os.getcwd(),os.sep)
SQL_FORMAT_FILE_CIDS_W_PROPERTIES = "%s%scomputer_ids_format.xml" % (os.getcwd(),os.sep)
SQL_FORMAT_FILE_CIDS_W_PACKAGES = "%s%scomputer_ids_format.xml" % (os.getcwd(),os.sep)
SQL_FORMAT_FILE_CIDS_W_APP_TRACKING = "%s%scomputer_ids_format.xml" % (os.getcwd(),os.sep)

SQL_BULK_INSERT_BATCH_SIZE = 100000

RE_MULTIDATA_SEP = "\n"

property_map = {}
app_tracking_property_map = {}
installed_apps_property_map = {}

handlers = {}

computer_map = {}                   # hash of existing bes computer ids to aardvark computer ids where key is the bes computer id
package_map = {}                    # hash of catalog packages. key is name and value is id
computer_ids_with_properties = {}   # simple hash where key is a computer id. represents which computers we saw properties for
computer_ids_with_packages = {}     # simple hash where key is a computer id. represents which computers we saw installed app analysis
computer_ids_with_app_tracking = {} # simple hash where key is a computer id. represents which computers we saw app tracking analysis

FH_COMPUTER_PROPS = -1
FH_COMPUTER_PACKAGES = -1
FH_COMPUTER_APP_TRACKING = -1

def initIOTime(reason):
	global _ioTime
	if (_ioTime.has_key(reason) == False):
		_ioTime[reason] = [0.0]

def ioBeginTime(reason):
	global _ioTime
	initIOTime(reason)
	_ioTime[reason].append(time.time())

def ioEndTime(reason):
	global _ioTime
	initIOTime(reason)
	d = _ioTime[reason]
	d.append(time.time())
	diff = d.pop() - d.pop()
	d[0] += diff
	_ioTime[reason] = d

def ioTimeAnalysis():
	global _ioTime
	global _ioElapsedTime

	_ioElapsedTime = 0
	for k in _ioTime.keys():
		d = _ioTime[k]
		print '(ioTimeAnalysis) :: Category: "%s" = (%s)' % (k,d[0])
		_ioElapsedTime += d[0]
	return _ioElapsedTime

def parseSequenceNumber(sInput):
	match = re.search(r"^0x[0-9A-F]{16}$", sInput)
	if match:
		return match.group()
	return ''

def isValidConnectionStringTokens(toks):
	l = [s[0] for s in toks]
	return ( ('DRIVER' in l) and ('SERVER' in l) and ('DATABASE' in l) and ('UID' in l) and ('PWD' in l) )

def cropTimeSeen(timeSeen):
	try:
		weekDay = timeSeen.split(',')
		timeZone = weekDay[len(weekDay)-1].split('-')
		return '%s%s' % (timeZone[0].strip(),timeZone[1])
	except:
		pass
	return timeSeen

def makeTermsInts(term,list):
	if (term.isdigit()):
		list.append(int(term))
	return -1

def calcTimeDuration(sTimeSpec):
	try:
		list = sTimeSpec.strip().replace(",",":").replace(" ",":").split(":")
		_list = []
		[makeTermsInts(t,_list) for t in list]
		n = len(_list)
		if ( (n == 1) and (_list[0] <= 36500) ):
			return (_list[0] * 86400)
		elif (n == 3):
			return (_list[0] * 3600) + (_list[1] * 60) + _list[2]
		elif ( (n == 4) and (_list[0] <= 36500) ):
			return (_list[0] * 86400) + (_list[1] * 3600) + (_list[2] * 60) + _list[3]
	except:
		pass
	return 0

def get_property_map(property_type_id):
	global _mssql_connection_string
	_aardvark_dbh = pyodbc.connect(_mssql_connection_string)
	_sql = "select id, datasource_identifier, name from properties where property_type_id = %s" % str(property_type_id)
	dict = {}
	for row in _aardvark_dbh.execute(_sql):
		a = row.datasource_identifier.split(_rowsep3)
		yml = {}
		for y in a:
			b = y.split(':')
			if (len(b) == 2):
				yml[b[0].strip()] = b[1].strip()
		siteID = int(yml['site_id'])
		if (dict.has_key(siteID) == False):
			d = dict[siteID] = {}
		else:
			d = dict[siteID]
		d[int(yml['property_id'])] = row[0]
	_aardvark_dbh.close()
	return dict

def exec_and_commit_sql(_sql):
	global _mssql_connection_string
	try:
		_aardvark_dbh = pyodbc.connect(_mssql_connection_string)
		_cursor = _aardvark_dbh.cursor()
		_cursor.execute(_sql)
		_aardvark_dbh.commit()
		_aardvark_dbh.close()
	except Exception, details:
		print '(exec_and_commit_sql) :: Error "%s" _sql=(%s).' % (str(details),_sql)

def exec_and_fetch_sql(_sql):
	global _mssql_connection_string
	try:
		_aardvark_dbh = pyodbc.connect(_mssql_connection_string)
		_cursor = _aardvark_dbh.cursor()
		_cursor.execute(_sql)
		row = _cursor.fetchone()
		_aardvark_dbh.close()
		return row
	except Exception, details:
		print '(exec_and_fetch_sql) :: Error "%s" _sql=(%s).' % (str(details),_sql)
	return []

def get_mapped_computer_id(bes_computer_id):
	global computer_map
	global DSS_RUN_MODE
	global DSS_RUN_MODE_USE_BES_ID
	ioBeginTime('get_mapped_computer_id')
	if (computer_map.has_key(bes_computer_id) == False):
		if (DSS_RUN_MODE == DSS_RUN_MODE_USE_BES_ID):
			computer_map[bes_computer_id] = bes_computer_id
		else:
			sth_insert_new_computer = "insert into computers (datasource_identifier, datasource_id, last_seen) values (%s,1,current_timestamp)" % (bes_computer_id)
			exec_and_commit_sql(sth_insert_new_computer)
			row = exec_and_fetch_sql("SELECT IDENT_CURRENT ('computers') AS new_computer_id")
			computer_map[bes_computer_id] = row.new_computer_id
	ioEndTime('get_mapped_computer_id')
	return computer_map[bes_computer_id]

def handle_property(row):
	global FH_COMPUTER_PROPS
	global computer_ids_with_properties

	computer_id = get_mapped_computer_id(row[COL_INDEX_COMPUTER_ID])
	row[COL_INDEX_VALUE] = row[COL_INDEX_VALUE].strip()
	computer_ids_with_properties[computer_id] = 1
	try:
		propMapVal = None
		siteID = row[COL_INDEX_SITE_ID]
		if (property_map.has_key(siteID)):
			d = property_map[siteID]
			propMapVal = d[row[COL_INDEX_PROPERTY_ID]]
		ioBeginTime('handle_property')
		FH_COMPUTER_PROPS.writelines('%s%s%s%s%s%s%s' % (OUTPUT_COL_SEP,computer_id,OUTPUT_COL_SEP,propMapVal,OUTPUT_COL_SEP,row[COL_INDEX_VALUE],OUTPUT_ROW_SEP))
		ioEndTime('handle_property')
	except Exception, details:
		print '(handle_property).4 :: Error "%s" with FH_COMPUTER_PROPS (%s) (%s).' % (str(details),str(FH_COMPUTER_PROPS),FH_COMPUTER_PROPS.__class__)

def handle_installed_apps(row):
	global computer_ids_with_packages
	global package_map

	computer_id = get_mapped_computer_id(row[COL_INDEX_COMPUTER_ID])
	computer_ids_with_packages[computer_id] = 1
	for l in row[COL_INDEX_VALUE].split(RE_MULTIDATA_SEP):
		if (package_map.has_key(l)):
			ioBeginTime('handle_app_tracking')
			FH_COMPUTER_PACKAGES.writelines('%s%s%s%s' % (computer_id,OUTPUT_COL_SEP,package_map[l],OUTPUT_ROW_SEP))
			ioEndTime('handle_app_tracking')

def handle_app_tracking(row):
	global computer_ids_with_app_tracking
	global OUTPUT_COL_SEP
	global OUTPUT_ROW_SEP

	computer_id = get_mapped_computer_id(row[COL_INDEX_COMPUTER_ID])
	computer_ids_with_app_tracking[computer_id] = 1
	for l in row[COL_INDEX_VALUE].split(RE_MULTIDATA_SEP):
		x = l.split(';')
		if (len(x) == 7):
			exe_name, first_seen, junk1, last_seen, junk2, total_duration, runs = x
			if ( (len(exe_name+runs) > 0) and (first_seen.find('1601') == -1) ):
				first_seen = cropTimeSeen(first_seen)
				last_seen = cropTimeSeen(last_seen)
				total_duration_in_seconds = calcTimeDuration(total_duration)
				if (total_duration_in_seconds > 0):
					ioBeginTime('handle_installed_apps')
					FH_COMPUTER_APP_TRACKING.writelines('%s%s%s%s%s%s%s%s%s%s%s%s' % (computer_id,OUTPUT_COL_SEP,exe_name,OUTPUT_COL_SEP,first_seen,OUTPUT_COL_SEP,last_seen,OUTPUT_COL_SEP,runs,OUTPUT_COL_SEP,total_duration_in_seconds,OUTPUT_ROW_SEP))
					ioEndTime('handle_installed_apps')

def initHandlersFromMap(map,func):
	global handlers
	for site_id in map.keys():
		for property_id in map[site_id].keys():
			if (handlers.has_key(site_id) == False):
				handlers[site_id] = {}
			d = handlers[site_id]
			d[property_id] = func
			handlers[site_id] = d

def initHandlers():
	global property_map
	global app_tracking_property_map
	global installed_apps_property_map
	global handlers
	handlers = {}
	initHandlersFromMap(property_map,handle_property)
	initHandlersFromMap(app_tracking_property_map,handle_app_tracking)
	initHandlersFromMap(installed_apps_property_map,handle_installed_apps)
	print '(initHandlers) :: handlers=(%s)' % str(handlers)

def initMetadata():
	global property_map
	global app_tracking_property_map
	global installed_apps_property_map
	property_map = get_property_map(PROPERTY_TYPE_COMPUTER)
	print '(initMetadata).1 :: property_map=(%s)' % property_map
	app_tracking_property_map = get_property_map(PROPERTY_TYPE_APP_TRACKING)
	if (len(app_tracking_property_map.keys()) == 0):
		print '(initMetadata).2a :: No mapping for BES Application Tracking Analysis\n'
	else:
		print '(initMetadata).2b :: app_tracking_property_map=(%s)' % app_tracking_property_map
	installed_apps_property_map = get_property_map(PROPERTY_TYPE_INSTALLED_APPS)
	if (len(installed_apps_property_map.keys()) == 0):
		print '(initMetadata).3a :: No mapping for BES Installed Applications Analysis\n'
	else:
		print '(initMetadata).3b :: installed_apps_property_map=(%s)' % installed_apps_property_map
	initHandlers()

def load_computer_map():
	global _mssql_connection_string
	global computer_map
	_aardvark_dbh = pyodbc.connect(_mssql_connection_string)
	_sql = "select datasource_identifier, max(id) as computer_id from computers group by datasource_identifier"
	for row in _aardvark_dbh.execute(_sql):
		computer_map[int(row[0])] = row[1]
	_aardvark_dbh.close()

def dispatch(row):
	global handlers
	try:
		siteID = str(row[COL_INDEX_SITE_ID])
		if (handlers.has_key(siteID)):
			d = handlers[siteID]
			propID = str(row[COL_INDEX_PROPERTY_ID])
			if (d.has_key(propID)):
				func = d[propID]
				try:
					if (func):
						for c in INT_COLS_LIST:
							row[c] = int(row[c])
						row[COL_INDEX_VALUE] = row[COL_INDEX_VALUE].decode('string_escape')
						func(row)
				except Exception, details:
					print '(dispatch).2 :: Error "%s" for (%s).' % (str(details),str(func))
	except Exception, details:
		print '(dispatch).1 :: Error "%s".' % str(details)

def write_processed_computers(fname, map):
	FH = open(fname, "w")
	for k in map.keys():
		FH.writelines('%s\n' % (k))
	FH.close()

def write_data():
	global OUTPUT_FILE_PROPERTIES
	global SQL_FORMAT_FILE_PROPERTIES
	global SQL_BULK_INSERT_BATCH_SIZE
	global OUTPUT_FILE_CIDS_W_PACKAGES
	global SQL_FORMAT_FILE_CIDS_W_PACKAGES
	global OUTPUT_FILE_PACKAGES
	global SQL_FORMAT_FILE_PACKAGES
	global OUTPUT_FILE_APP_TRACKING
	global SQL_FORMAT_FILE_APP_TRACKING
	
	sqlList = []

	sqlList.append({'10 delete properties': "delete from computer_properties with (tablock)	from openrowset(bulk '%s', formatfile='%s') as foo where computer_properties.computer_id = foo.computer_id and computer_properties.property_id = foo.property_id" % (OUTPUT_FILE_PROPERTIES,SQL_FORMAT_FILE_PROPERTIES)})
	sqlList.append({'20 insert properties': "bulk insert computer_properties from '%s' with (tablock, batchsize=%s, formatfile='%s')" % (OUTPUT_FILE_PROPERTIES,SQL_BULK_INSERT_BATCH_SIZE,SQL_FORMAT_FILE_PROPERTIES)})
	sqlList.append({'30 delete packages': "delete from computers_packages with (tablock) from openrowset (bulk '%s', formatfile='%s') as foo where computers_packages.computer_id = foo.computer_id" % (OUTPUT_FILE_CIDS_W_PACKAGES,SQL_FORMAT_FILE_CIDS_W_PACKAGES)})
	sqlList.append({'40 insert packages': "bulk insert computers_packages from '%s' with (tablock, batchsize=%s, formatfile='%s')" % (OUTPUT_FILE_PACKAGES,SQL_BULK_INSERT_BATCH_SIZE,SQL_FORMAT_FILE_PACKAGES)})
	sqlList.append({'51 truncate tmp_computer_app_tracking': "truncate table tmp_computer_app_tracking"})
	sqlList.append({'52 move away unmodified computer app tracking records to tmp_computer_app_tracking': "insert into tmp_computer_app_tracking select computer_app_tracking.* from computer_app_tracking left outer join openrowset(bulk '%s',formatfile='%s') as foo on (computer_app_tracking.computer_id = foo.computer_id) where foo.computer_id is null" % (OUTPUT_FILE_CIDS_W_APP_TRACKING,SQL_FORMAT_FILE_CIDS_W_APP_TRACKING)})
	sqlList.append({'53 truncate computer_app_tracking': "truncate table computer_app_tracking"})
	sqlList.append({'54 remove index on computer_app_tracking': "if exists (select 1 from sysindexes where id = object_id('computer_app_tracking') and name = 'index_1' and indid > 0 and indid < 255) drop index computer_app_tracking.index_1"})
	sqlList.append({'55 insert into computer_app_tracking from csv file': "insert into computer_app_tracking with (tablock) (computer_id, exe_name, first_used, last_used, total_runs, total_time) select computer_id, exe_name, dateadd(hh, first_used_tzoffset * -1, first_used_datetime), dateadd(hh, last_used_tzoffset * -1, last_used_datetime), total_runs, total_time from openrowset(bulk '%s',formatfile='%s') as foo" % (OUTPUT_FILE_APP_TRACKING,SQL_FORMAT_FILE_APP_TRACKING)})
	sqlList.append({'56 insert into computer_app_tracking from tmp_computer_app_tracking': "insert into computer_app_tracking with (tablock) (computer_id, exe_name, first_used, last_used, total_runs, total_time) select computer_id, exe_name, first_used, last_used, total_runs, total_time from tmp_computer_app_tracking"})
	sqlList.append({'57 add index to computer_app_tracking': "create index index_1 on computer_app_tracking (computer_id asc,exe_name asc)"})
	sqlList.append({'60 update computers.last_app_tracking': "update computers with (tablock) set last_app_tracking = current_timestamp from openrowset (bulk '%s',formatfile='%s') as computers_seen where computers.id = computers_seen.computer_id" % (OUTPUT_FILE_CIDS_W_APP_TRACKING,SQL_FORMAT_FILE_CIDS_W_APP_TRACKING)})
	sqlList.append({'61 update computers.last_installed_app': "update computers with (tablock) set last_installed_app = current_timestamp from openrowset (bulk '%s',	formatfile='%s') as computers_seen where computers.id = computers_seen.computer_id" % (OUTPUT_FILE_CIDS_W_PACKAGES,SQL_FORMAT_FILE_CIDS_W_PACKAGES)})
	sqlList.append({'62 update computers.last_seen': "update computers with (tablock) set last_seen = current_timestamp from openrowset (bulk '%s',formatfile='%s') as computers_seen where computers.id = computers_seen.computer_id" % (OUTPUT_FILE_CIDS_W_PROPERTIES,SQL_FORMAT_FILE_CIDS_W_PROPERTIES)})

	for map in sqlList:
		for k in map.keys():
			print '"%s"\n[%s]\n' % (k,map[k])
			#exec_and_commit_sql(map[k]);

def main(fname):
	global _mssql_connection_string2
	global FH_COMPUTER_PROPS
	global FH_COMPUTER_PACKAGES
	global FH_COMPUTER_APP_TRACKING
	global OUTPUT_FILE_CIDS_W_PROPERTIES
	global OUTPUT_FILE_CIDS_W_PACKAGES
	global OUTPUT_FILE_CIDS_W_APP_TRACKING
	global computer_ids_with_properties
	global computer_ids_with_packages
	global computer_ids_with_app_tracking

	ioBeginTime('TRUNCATE table computers')
	exec_and_commit_sql("TRUNCATE table computers")
	ioEndTime('TRUNCATE table computers')
	
	ioBeginTime('Remove OUTPUT_FILE_LIST')
	for f in OUTPUT_FILE_LIST:
		try:
			if (os.path.exists(f)):
				os.remove(f)
		except:
			pass
	ioEndTime('Remove OUTPUT_FILE_LIST')
	
	ioBeginTime('main()')

	FH_COMPUTER_PROPS = open(OUTPUT_FILE_PROPERTIES, "w")
	FH_COMPUTER_PACKAGES = open(OUTPUT_FILE_PACKAGES, "w")
	FH_COMPUTER_APP_TRACKING = open(OUTPUT_FILE_APP_TRACKING, "w")

	ioBeginTime('initMetadata')
	initMetadata()
	ioEndTime('initMetadata')

	ioBeginTime('load_computer_map')
	load_computer_map()
	ioEndTime('load_computer_map')
	
	print 'computer_map=(%s)' % str(computer_map)

	if (os.path.exists(fname)):
		fHand = open(fname, "r")
		i = 0
		for row in fHand:
			if (i > 0):
				_row = row.strip().split(_colsep3)
				dispatch(_row)
			i += 1
		fHand.close()
	else:
		dbh = pyodbc.connect(_mssql_connection_string2)
		_cursor = dbh.cursor()
		_sql = "SELECT TOP 100 COMPUTER_ID as computerid, VALUE as resultstext, SEQUENCE, PROPERTY_ID, SITE_ID FROM bes_data ORDER BY computerid"
		rows = _cursor.execute(_sql)
		for _row in rows:
			dispatch(_row)
		dbh.close()

	FH_COMPUTER_PROPS.close()
	FH_COMPUTER_PACKAGES.close()
	FH_COMPUTER_APP_TRACKING.close()

	ioBeginTime('write_processed_computers')
	write_processed_computers(OUTPUT_FILE_CIDS_W_PROPERTIES, computer_ids_with_properties)
	write_processed_computers(OUTPUT_FILE_CIDS_W_PACKAGES, computer_ids_with_packages)
	write_processed_computers(OUTPUT_FILE_CIDS_W_APP_TRACKING, computer_ids_with_app_tracking)
	ioEndTime('write_processed_computers')
	
	ioBeginTime('write_data')
	#write_data()
	ioEndTime('write_data')
	
	ioEndTime('main()')

	time_analysis = ioTimeAnalysis()
	try:
		print "Time spent doing I/O :: (%s) of (%s)" % (time_analysis[0],time_analysis[1])
	except:
		pass

def reportRunMode():
	if (DSS_RUN_MODE == DSS_RUN_MODE_USE_INTERNAL_ID):
		print 'DSS_RUN_MODE = DSS_RUN_MODE_USE_INTERNAL_ID\n'
	elif (DSS_RUN_MODE == DSS_RUN_MODE_USE_BES_ID):
		print 'DSS_RUN_MODE = DSS_RUN_MODE_USE_BES_ID\n'
	else:
		print 'Unknown DSS_RUN_MODE = (%s)' % DSS_RUN_MODE

if ( (len(sys.argv) == 1) or (sys.argv[1] == '--help') ):
	print '--help                      ... displays this help text.'
	print '--verbose                   ... output more stuff.'
	print '--sequence_start=hex_value  ... sequence identifier, typically 16 hex digits. (Used only when input is SQL2005 db.)'
	print '--sequence_end=hex_value    ... sequence identifier, typically 16 hex digits. (Used only when input is SQL2005 db.)'
	print '--input=input_file_name     ... name of input file or specifies the connection string.'
else:
	_fileName = ''
	for i in xrange(len(sys.argv)):
		if ( (sys.argv[i].find('--sequence_start=') > -1) or (sys.argv[i].find('--sequence_end=') > -1) or (sys.argv[i].find('--input=') > -1) ): 
			toks = sys.argv[i].split('=')
			if (sys.argv[i].find('--sequence_start=') > -1):
				_sequence_start = parseSequenceNumber(toks[1])
				if (len(_sequence_start) == 0):
					print 'Missing or invalid sequence number given for sequence_start.'
			elif (sys.argv[i].find('--sequence_end=') > -1):
				_sequence_end = parseSequenceNumber(toks[1])
				if (len(_sequence_end) == 0):
					print 'Missing or invalid sequence number given for _sequence_end.'
			elif (sys.argv[i].find('--input=') > -1):
				_fileName = toks[1]
				psyco.bind(main)
				if (os.path.exists(_fileName)):
					main(_fileName)
				else:
					reportRunMode()
					try:
						_cnnString = sys.argv[i][sys.argv[i].find("=")+1:len(sys.argv[i])]
						_cnnToks = [t.split('=') for t in _cnnString.split(';')]
						#print 'len(_cnnToks)=(%s), len(_cnnToks[0])=(%s)' % (str(len(_cnnToks)),str(len(_cnnToks[0])))
						if (isValidConnectionStringTokens(_cnnToks)):
							dbh = pyodbc.connect(_cnnString)
							dbh.close()
							_mssql_connection_string = _cnnString
							main('')
						elif ( (len(_cnnToks) == 1) and (len(_cnnToks[0]) == 1) ):
							main('')
						else:
							print 'Missing or invalid connection string given, make sure to use "" chars to delimit the connection string.'
					except Exception, details:
						print details
						print 'Assuming (%s) is a file name.' % _fileName
						main(_fileName)
		elif (sys.argv[i].find('--verbose') > -1):
			_isVerbose = True
