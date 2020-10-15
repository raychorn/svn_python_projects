import sys
from os import path
import os
import time
import pyodbc
import gc
import datetime
import adodbapi

_isProfiling = False
_isVerbose = False
_isPsyco = False

_psyco_subMethod = 'bind'

_colsep3 = chr(255)
_rowsep3 = "\n"

COL_INDEX_COMPUTER_ID = 0
COL_INDEX_VALUE = 1
COL_INDEX_SEQUENCE = 2
COL_INDEX_PROPERTY_ID = 3
COL_INDEX_SITE_ID = 4

PROPERTY_TYPE_COMPUTER = 1
PROPERTY_TYPE_APP_TRACKING = 2
PROPERTY_TYPE_INSTALLED_APPS = 3

# csv files this script will generate
OUTPUT_FILE_PROPERTIES = "%s%setl_computer_properties.csv" % (os.getcwd(),os.sep)
OUTPUT_FILE_PACKAGES = "%s%setl_computers_packages.csv" % (os.getcwd(),os.sep)
OUTPUT_FILE_APP_TRACKING = "%s%setl_computer_app_tracking.csv" % (os.getcwd(),os.sep)
OUTPUT_FILE_CIDS_W_PROPERTIES = "%s%setl_computers_with_properties.csv" % (os.getcwd(),os.sep)
OUTPUT_FILE_CIDS_W_PACKAGES = "%s%setl_computers_with_packages.csv" % (os.getcwd(),os.sep)
OUTPUT_FILE_CIDS_W_APP_TRACKING = "%s%setl_computers_with_app_tracking.csv" % (os.getcwd(),os.sep)

OUTPUT_FILE_UNIQUE_COMPUTERS = "%s%setl_unique_computers.csv" % (os.getcwd(),os.sep)
SQL_FORMAT_FILE_UNIQUE_COMPUTERS = "%s%sunique_computers_format.xml" % (os.getcwd(),os.sep)

SQL_BULK_INSERT_BATCH_SIZE = 100000

# output format of csv files this script will generate
OUTPUT_COL_SEP = "\t\t"
OUTPUT_ROW_SEP = "\n\n"

OUTPUT_COL_SEP1 = "\t"
OUTPUT_ROW_SEP1 = "\n"

_ioBeginTime = []
_ioEndTime = []
_ioElapsedTime = 0

_record_id = 0

_mssql_connection_string = 'DRIVER={SQL Server};SERVER=MURRE\DEV2005;DATABASE=aardvark_fresh;CommandTimeout=0;UID=sa;PWD=peekaboo'

_handlers = {}
_computer_id_dict = {}
_property_map = {}
_app_tracking_property_map = {}
_installed_apps_property_map = {}

computers_dict = {}

_global_data = []

def get_property_map(dict,property_type_id):
	global _mssql_connection_string
	global _rowsep3
	_aardvark_dbh = pyodbc.connect(_mssql_connection_string)
	_sql = "select id, datasource_identifier, name from properties where property_type_id = %s" % str(property_type_id)
	for row in _aardvark_dbh.execute(_sql):
		a = row.datasource_identifier.split(_rowsep3)
		yml = {}
		for y in a:
			b = y.split(':')
			if (len(b) == 2):
				yml[b[0].strip()] = b[1].strip()
		if (dict.has_key(yml['site_id']) == False):
			dict[yml['site_id']] = {}
		dict[yml['site_id']][yml['property_id']] = row[0]
	_aardvark_dbh.close()
	return dict

def handle_property(rowref):
	global COL_INDEX_VALUE
	global COL_INDEX_COMPUTER_ID
	global _property_map
	global COL_INDEX_PROPERTY_ID
	global FH_COMPUTER_PROPS
	computer_id = get_mapped_computer_id(rowref[COL_INDEX_COMPUTER_ID])
	print "(handle_property) :: computer_id=(%s)" % str(computer_id)
	v = rowref[COL_INDEX_VALUE].strip()
	FH_COMPUTER_PROPS.writelines("%s%s%s%s%s%s%s" % (OUTPUT_COL_SEP,str(computer_id),OUTPUT_COL_SEP,_property_map[rowref[COL_INDEX_PROPERTY_ID]],OUTPUT_COL_SEP,rowref[COL_INDEX_VALUE],OUTPUT_ROW_SEP))

def initHandlers(h,map):
	for site in map:
		if (h.has_key(site) == False):
			h[site] = {}
		for property in map[site]:
			h[site][property] = handle_property

def initMetadata():
	global _handlers
	global _property_map
	global _app_tracking_property_map
	global _installed_apps_property_map
	global ROPERTY_TYPE_COMPUTER
	global PROPERTY_TYPE_APP_TRACKING
	global PROPERTY_TYPE_INSTALLED_APPS
	_property_map = get_property_map(_property_map,PROPERTY_TYPE_COMPUTER)
	_app_tracking_property_map = get_property_map(_app_tracking_property_map,PROPERTY_TYPE_APP_TRACKING)
	_installed_apps_property_map = get_property_map(_installed_apps_property_map,PROPERTY_TYPE_INSTALLED_APPS)
	print "_property_map=(%s)\n" % str(_property_map)
	print "_app_tracking_property_map=(%s)\n" % str(_app_tracking_property_map)
	print "_installed_apps_property_map=(%s)\n" % str(_installed_apps_property_map)
	initHandlers(_handlers,_property_map)
	initHandlers(_handlers,_app_tracking_property_map)
	initHandlers(_handlers,_installed_apps_property_map)
# +++
def getComputerId(_list,siteID,propID,compID):
	global _computer_id_dict
	global _handlers
	global _property_map
	list = []
	_siteID = _list[siteID]
	_propID = _list[propID]
	print '_siteID=(%s), _propID=(%s), _handlers[%s][%s]=(%s)' % (_siteID,_propID,_siteID,_propID,_handlers[_siteID][_propID])
	if (_handlers[_siteID][_propID]):
		_qID = [_propID,_property_map[siteID][_propID]]
		_compID = _list[compID]
		list = [_qID,_compID]
		print '_qID=(%s), list=(%s)' % (str(_qID),str(list))
		if (_computer_id_dict.has_key(_compID) == False):
			_computer_id_dict[_compID] = []
		_computer_id_dict[_compID].append(_qID)
	return list

def fetchAllComputers():
	global _mssql_connection_string
	dict = {}
	_aardvark_dbh = pyodbc.connect(_mssql_connection_string)
	_sql = "SELECT id, datasource_identifier, datasource_id, last_exe_scan, last_app_tracking, last_installed_app, last_seen FROM computers ORDER BY id"
	for row in _aardvark_dbh.execute(_sql):
		_datasource_identifier = row.datasource_identifier
		if (str(_datasource_identifier.__class__).find("'str'") == -1):
			_datasource_identifier = str(_datasource_identifier)
			if (str(_datasource_identifier).endswith("L")):
				_datasource_identifier = _datasource_identifier[0:-1]
		dict[_datasource_identifier] = [row.id, row.datasource_id, str(row.last_exe_scan).replace("None", ""), str(row.last_app_tracking).replace("None", ""), str(row.last_installed_app).replace("None", ""), str(row.last_seen).replace("None", "")]
	_aardvark_dbh.close()
	return dict

def splitRawData(l,sep):
	global _global_data
	global COL_INDEX_PROPERTY_ID
	global COL_INDEX_COMPUTER_ID
	global COL_INDEX_VALUE
	try:
		row = l.split(sep)
		if (len(row) > 1):
			# no need to append all the rows - only those we want to glean data from...
			#_global_data.append(row)
			getComputerId(row,COL_INDEX_SITE_ID,COL_INDEX_PROPERTY_ID,COL_INDEX_COMPUTER_ID)
	except:
		pass

def getComputerRecord(_list,k):
	global OUTPUT_COL_SEP1
	global _record_id
	_record_id += 1
	return '%s%s%s%s%s%s%s%s%s%s%s%s%s%s' % (str(_record_id),OUTPUT_COL_SEP1,k,OUTPUT_COL_SEP1,str(_list[1]),OUTPUT_COL_SEP1,str(_list[2]),OUTPUT_COL_SEP1,str(_list[3]),OUTPUT_COL_SEP1,str(_list[4]),OUTPUT_COL_SEP1,str(_list[5]),OUTPUT_COL_SEP1)

def handleFilePropertiesInstalledApps2(f):
	global OUTPUT_ROW_SEP1
	global _colsep3
	global _rowsep3
	global _handlers
	global _computer_id_dict
	global _global_data
	global OUTPUT_FILE_UNIQUE_COMPUTERS
	global _ioBeginTime
	global _ioEndTime
	global _record_id
	global computers_dict

	#gc.disable()
	for l in f:
		splitRawData(l,_colsep3)
	_ioBeginTime.append(time.time())
	computers_dict = fetchAllComputers()
	_ioEndTime.append(time.time())
	_today = datetime.datetime.now()
	print '_computer_id_dict=(%s)\n' % str(_computer_id_dict)
	for k in _computer_id_dict.iterkeys():
		if (computers_dict.has_key(k) == False):
			computers_dict[k] = [len(computers_dict) + 1, 1, "", "", "", _today]
		else:
			computers_dict[k][5] = _today # 62 update computers.last_seen
	
	_record_id = 0
	_ioBeginTime.append(time.time())
	fHand = open(OUTPUT_FILE_UNIQUE_COMPUTERS, "w")
	fHand.writelines(OUTPUT_ROW_SEP1.join([getComputerRecord(computers_dict[k],k) for k in computers_dict.iterkeys()]))
	fHand.close()
	insertUniqueComputers(OUTPUT_FILE_UNIQUE_COMPUTERS)
	_ioEndTime.append(time.time())
	print 'Processed %s unique hosts.\n' % str(_record_id)
	#gc.enable()
	return

def ioTime(t1,t2):
	global _ioElapsedTime
	_ioElapsedTime += (t2 - t1)

def ioTimeAnalysis():
	global _ioBeginTime
	global _ioEndTime
	global _ioElapsedTime
	_ioElapsedTime = 0
	[ioTime(_ioBeginTime[i],_ioEndTime[i]) for i in xrange(len(_ioEndTime))]
	return _ioElapsedTime

def main(fname):
	global _isVerbose
	global _isProfiling
	global FH_COMPUTER_PROPS
	global FH_COMPUTER_PACKAGES
	global FH_COMPUTER_APP_TRACKING
	global _ioBeginTime
	global _ioEndTime
	if (path.exists(fname)):
		_ioBeginTime.append(time.time())
		initMetadata()
		_ioEndTime.append(time.time())
		print "_handlers=(%s)\n" % str(_handlers)
		try:
			f = open(fname, "r")
			handleFilePropertiesInstalledApps2(f)
			f.close()
			print "Time spent doing I/O :: (%s), _ioBeginTime=(%s), _ioEndTime=(%s)" % (str(ioTimeAnalysis()),str(_ioBeginTime),str(_ioEndTime))
		except Exception, details:
			print '(main).1 :: ERROR :: (%s)' % details
	else:
		print '(main).1a :: WARNING :: Missing file "%s" - cannot continue.' % fname

def insertUniqueComputers(fname):
	global _mssql_connection_string
	global SQL_BULK_INSERT_BATCH_SIZE
	global SQL_FORMAT_FILE_UNIQUE_COMPUTERS

	if (1):
		try:
			_aardvark_dbh = pyodbc.connect(_mssql_connection_string)
			_cursor = _aardvark_dbh.cursor()
			_sql = "TRUNCATE TABLE computers; BULK INSERT computers FROM '%s' WITH (DATAFILETYPE = 'char', FIELDTERMINATOR = '\t', ROWTERMINATOR = '\n');" % fname
			print 'insertUniqueComputers().2 :: _sql=(%s)\n' % _sql
			_cursor.execute(_sql)
			_aardvark_dbh.commit()
			_aardvark_dbh.close()
		except Exception, details:
			print 'insertUniqueComputers() :: Error (%s)' % str(details)
		
	if (0):
		try:
			_aardvark_dbh = adodbapi.connect(_mssql_connection_string)
			_cursor = _aardvark_dbh.cursor()
			_sql = "TRUNCATE TABLE computers; BULK INSERT computers FROM '%s' WITH (DATAFILETYPE = 'char', FIELDTERMINATOR = '\t', ROWTERMINATOR = '\n');" % fname
			_cursor.execute(_sql)
			_aardvark_dbh.commit()
			_aardvark_dbh.close()
		except adodbapi.DatabaseError, inst:
			print 'Error (%s)' % str(inst)

def main2(fname):
	if (path.exists(fname)):
		if (fname.find(os.getcwd()) == -1):
			fname = '%s%s%s' % (os.getcwd(),os.sep,fname)
		print 'Main2() :: Running insertUniqueComputers() on (%s)' % (fname)
		insertUniqueComputers(fname)
	else:
		print 'WARNING :: Missing file "%s" - cannot continue.' % fname

if ( (len(sys.argv) == 1) or (sys.argv[1] == '--help') ):
	print '--help                    ... displays this help text.'
	print '--verbose                 ... output more stuff.'
	print '--profile                 ... use profiler.'
	print '--psyco                   ... use psyco.'
	print '--psyco=full              ... use psyco using full method.'
	print '--psyco=log               ... use psyco using log method.'
	print '--psyco=bind              ... use psyco using bind method.'
	print '--input=input_file_name   ... name of input file.'
	print '--input2=input_file_name  ... name of input file for phase 2 (the unique computer csv).'
else:
	_fileName = ''
	for i in xrange(len(sys.argv)):
		if ( (sys.argv[i].find('--input=') > -1) or (sys.argv[i].find('--input2=') > -1) ): 
			toks = sys.argv[i].split('=')
			_fileName = toks[1]
			if (_isPsyco):
				import psyco
				if (_psyco_subMethod == 'full'):
					psyco.full()
				elif (_psyco_subMethod == 'log'):
					psyco.log()
					psyco.profile()
				elif (_psyco_subMethod == 'bind'):
					psyco.bind(main)
			if (_isProfiling):
				import cProfile
				if (sys.argv[i].find('--input=') > -1):
					cProfile.run("main('%s')" % _fileName.replace('\\', '\\\\'))
				elif (sys.argv[i].find('--input2=') > -1):
					cProfile.run("main2('%s')" % _fileName.replace('\\', '\\\\'))
			else:
				if (sys.argv[i].find('--input=') > -1):
					main(_fileName)
				elif (sys.argv[i].find('--input2=') > -1):
					main2(_fileName)
		elif (sys.argv[i].find('--profile') > -1):
			_isProfiling = True
		elif ( (sys.argv[i].find('--psyco') > -1) or (sys.argv[i].find('--psyco=') > -1) ):
			_isPsyco = True
			if (sys.argv[i].find('--psyco=') > -1):
				toks = sys.argv[i].split('=')
				_psyco_subMethod = toks[1]
		elif (sys.argv[i].find('--verbose') > -1):
			_isVerbose = True
