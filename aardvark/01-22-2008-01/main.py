import sys
from os import path
import pyodbc
import gc
import shelveSupport
import baseconvert 
import time
import re
from decorators import memoized

_isProfiling = False
_isVerbose = False
_isPsyco = False
_serverName = 'aracari'

#valid numbers are 1 or 2 where 1 is the separate method and 2 is the combined method... useful only for comparison...
_subMethod1 = 3

_psyco_subMethod = 'bind'

_pipelined_process_number = 2

_colsep = "\t\t"
_rowsep = "\n"

_colsep3 = chr(255)
_rowsep3 = "\n"

# TOP 100 
_SQL_STATEMENT = "SELECT qr.computerid, COALESCE(qr.resultstext, lqr.resultstext) as resultstext, cast(qr.sequence as bigint) as 'sequence', qr.id, qr.siteid FROM countrywide.dbo.questionresults as qr with (nolock) INNER JOIN countrywide.dbo.computers with (nolock) ON (computers.computerid = qr.computerid AND computers.isdeleted = 0) LEFT OUTER JOIN countrywide.dbo.longquestionresults as lqr with (nolock) on (qr.siteid = lqr.siteid AND qr.id = lqr.id AND qr.computerid = lqr.computerid) WHERE  qr.siteid = 1 AND qr.IsFailure = 0 AND qr.id IN (96514, 82118, 31, 17, 27, 18) AND qr.sequence > 0 AND qr.sequence <= convert(timestamp, master.dbo.fn_varbintohexstr(@@DBTS)) AND qr.resultscount < 700"

# these col_index_* constants specify mappings of column index from a query or field index from a csv file
COL_INDEX_COMPUTER_ID = 0
COL_INDEX_VALUE = 1
COL_INDEX_SEQUENCE = 2
COL_INDEX_PROPERTY_ID = 3
COL_INDEX_QUESTION_ID = 3
COL_INDEX_SITE_ID = 4

# output format of csv files this script will generate
OUTPUT_COL_SEP = "\t\t"
OUTPUT_ROW_SEP = "\n\n"

#_bufSize = 100000
#_bufSize = 1000000000
_bufSize = 10000

_ioBeginTime = []
_ioEndTime = []
_ioElapsedTime = 0

_handlers = {}
_property_dict = {}
_computer_map = {}
_package_map = {}
_computer_id_dict = {}

_mssql_connection_string = 'DRIVER={SQL Server};SERVER=MURRE\DEV2005;DATABASE=aardvark_fresh;CommandTimeout=0;UID=sa;PWD=peekaboo'
_mssql_surrogate_connection_string = 'DRIVER={SQL Server};SERVER=MURRE\DEV2005;DATABASE=surrogate_countrywide;CommandTimeout=0;UID=sa;PWD=peekaboo'

# csv files this script will generate
OUTPUT_FILE_PROPERTIES = "etl_computer_properties.csv"
OUTPUT_FILE_PACKAGES = "etl_computers_packages.csv"
OUTPUT_FILE_APP_TRACKING = "etl_computer_app_tracking.csv"
OUTPUT_FILE_CIDS_W_PACKAGES = "etl_computers_with_packages.csv"
OUTPUT_FILE_CIDS_W_APP_TRACKING = "etl_computers_with_app_tracking.csv"

OUTPUT_FILE_PROPERTIES_TEMP = OUTPUT_FILE_PROPERTIES.replace(".csv",".tmp")
OUTPUT_FILE_PACKAGES_TEMP = OUTPUT_FILE_PACKAGES.replace(".csv",".tmp")
OUTPUT_FILE_APP_TRACKING_TEMP = OUTPUT_FILE_APP_TRACKING.replace(".csv",".tmp")

RE_MULTIDATA_SEP = "\n"

def load_package_map():
	global _mssql_connection_string
	global _package_map
	global _isVerbose
	try:
		rowcount = 0
		_aardvark_dbh = pyodbc.connect(_mssql_connection_string)
		cursor = _aardvark_dbh.execute("select id, name from v_packages")
		for row in cursor:
			_package_map[row[1]] = row[0]
			rowcount += 1
		if (_isVerbose):
			print "_package_map = [%s], based on rowcount of %s" % (str(_package_map),str(rowcount))
		_aardvark_dbh.close()
	except Exception, details:
		print '(load_package_map) :: ERROR :: (%s)' % str(details)

def get_property_map():
	global _mssql_connection_string
	dict = {}
	_aardvark_dbh = pyodbc.connect(_mssql_connection_string)
	for row in _aardvark_dbh.execute("select id, datasource_identifier, name from properties where import = 1"):
		column_names = [ t[0] for t in row.cursor_description ]
		a = row.datasource_identifier.split(_rowsep)
		yml = {}
		for y in a:
			b = y.split(':')
			if (len(b) == 2):
				yml[b[0].strip()] = b[1].strip()
		dict[yml['analysis_id']] = row[0]
	_aardvark_dbh.close()
	return dict

def get_mapped_computer_id(bes_computer_id):
	global _mssql_connection_string
	global _computer_map
	_aardvark_dbh = pyodbc.connect(_mssql_connection_string)
	bes_computer_id = long(bes_computer_id)
	print "_computer_map.has_key(%s)=(%s)" % (bes_computer_id,_computer_map.has_key(bes_computer_id))
	if (_computer_map.has_key(bes_computer_id) == False):
		_sql = "insert into computers (datasource_identifier, datasource_id, last_seen) values (%s,1,current_timestamp)" % (str(bes_computer_id))
		_val = _aardvark_dbh.execute(_sql)
		if (_val):
			print '(%s) _sql=(%s)' % (_val,_sql)
			sth_insert_new_computer = _aardvark_dbh.execute("SELECT id FROM computers WHERE (datasource_identifier = %s) AND (datasource_id = 1)" % (str(bes_computer_id)))
			row = sth_insert_new_computer.fetchone()
			print "(get_mapped_computer_id) :: bes_computer_id=(%s), id=(%s)" % (str(bes_computer_id),str(row[0]))
			_computer_map[bes_computer_id] = row[0]
	_aardvark_dbh.close()
	return _computer_map[bes_computer_id]

def handle_property(rowref):
	global COL_INDEX_VALUE
	global COL_INDEX_COMPUTER_ID
	global _property_dict
	global COL_INDEX_QUESTION_ID
	global FH_COMPUTER_PROPS
	computer_id = get_mapped_computer_id(rowref[COL_INDEX_COMPUTER_ID])
	print "(handle_property) :: computer_id=(%s)" % str(computer_id)
	v = rowref[COL_INDEX_VALUE].strip()
	FH_COMPUTER_PROPS.writelines("%s%s%s%s%s%s%s" % (OUTPUT_COL_SEP,str(computer_id),OUTPUT_COL_SEP,_property_dict[rowref[COL_INDEX_QUESTION_ID]],OUTPUT_COL_SEP,rowref[COL_INDEX_VALUE],OUTPUT_ROW_SEP))

def handleRow(rowref):
	global _handlers
	global COL_INDEX_QUESTION_ID
	print "(handleRow) :: COL_INDEX_QUESTION_ID=(%s)" % str(COL_INDEX_QUESTION_ID)
	print "(handleRow) :: rowref=(%s)" % str(rowref)
	print "(handleRow) :: len(rowref)=(%s)" % str(len(rowref))
	print "(handleRow) :: rowref[COL_INDEX_QUESTION_ID]=(%s) (%s)" % (str(rowref[COL_INDEX_QUESTION_ID]),rowref[COL_INDEX_QUESTION_ID].__class__)
	try:
		print "(handleRow) :: _handlers[rowref[COL_INDEX_QUESTION_ID]]=(%s)" % str(_handlers[rowref[COL_INDEX_QUESTION_ID]])
		if (_handlers[rowref[COL_INDEX_QUESTION_ID]]):
			_handlers[rowref[COL_INDEX_QUESTION_ID]](rowref)
		else:
			print "I don't know how to parse questionID %s" % str(rowref[COL_INDEX_QUESTION_ID])
	except Exception, details:
		print '(handleRow) :: ERROR :: (%s)' % str(details)
		print "Malformed rowref: (%s)" % str(rowref)
		print "_handlers=(%s)" % str(_handlers)
	print ""

def handleFileProperties1(f):
	global _colsep
	global _rowsep
	global _handlers
	global COL_INDEX_QUESTION_ID
	global COL_INDEX_COMPUTER_ID
	_masterList = []
	list = -1
	for l in f:
		ar = l.split(_colsep)
		if (len(ar) > 0):
			if (ar[0] == _rowsep):
				if (len(list) > 5):
					print "Check the stack_trace for the data aggregation process in main()."
					break
				else:
					try:
						if (_handlers[list[COL_INDEX_QUESTION_ID]]):
							_masterList.append([list[COL_INDEX_QUESTION_ID],list[COL_INDEX_COMPUTER_ID]])
					except:
						pass
				list = -1
			else:
				if (list == -1):
					list = ar
				else:
					if (ar[0] == ''):
						list = list + ar[1:len(ar)]
					else:
						if ( (len(ar) == 1) and (ar[0].endswith('\n')) ):
							list[len(list)-1] += ar[0]
						else:
							list = list + ar
	return _masterList

def handleFileProperties2(fHandle):
	global _colsep
	global _rowsep
	_masterList = []
	lst = []
	try:
		lst = [l.split(_colsep) for l in fHandle]
	except Exception, details:
		print '(handleFileProperties2) :: ERROR :: (%s)' % str(details)
	print str(lst[0:1000])
	return _masterList

def getComputerId(_list,qID,compID):
	global _handlers
	try:
		if (_handlers[_list[qID]]):
			return [_list[qID],_list[compID]]
	except:
		pass
	return []
#+++
def _getComputerId(_list,qID,compID):
	global _computer_id_dict
	list = getComputerId(_list,qID,compID)
	if (len(list) == 2):
		_qID, _compID = list
		if (_computer_id_dict.has_key(_compID) == False):
			_computer_id_dict[_compID] = []
		_computer_id_dict[_compID].append(_qID)
	return str(list)[1:-1]

def appendComputerId(_mList,_list,qID,compID):
	global _handlers
	try:
		if (_handlers[_list[qID]]):
			_mList.append(getComputerId(_list,qID,compID))
	except:
		pass

def handleFileProperties3(f):
	global _colsep3
	global _rowsep3
	global _handlers
	global COL_INDEX_QUESTION_ID
	global COL_INDEX_COMPUTER_ID
	_masterList = []
	for l in f:
		appendComputerId(_masterList,l.split(_colsep3),COL_INDEX_QUESTION_ID,COL_INDEX_COMPUTER_ID)
	return _masterList

def handleFileProperties4(f):
	global _colsep3
	global _rowsep3
	global _handlers
	global COL_INDEX_QUESTION_ID
	global COL_INDEX_COMPUTER_ID
	_masterList = [getComputerId(l.split(_colsep3),COL_INDEX_QUESTION_ID,COL_INDEX_COMPUTER_ID) for l in f]
	return _masterList

def handle_installed_apps():
	print "handle_installed_apps() :: DO NOTHING !"

def handle_app_tracking():
	print "handle_app_tracking() :: DO NOTHING !"

def initMetadata():
	global _handlers
	global _property_dict
	_property_dict = get_property_map()
	print "_property_dict=(%s)" % str(_property_dict)
	for id in _property_dict:
		_handlers[id] = handle_property
	_handlers[get_analysis_id('ActionSite', 'Installed Applications - Windows')] = handle_installed_apps
	_handlers[get_analysis_id('ActionSite', 'All Application Usage Information')] = handle_app_tracking

def splitTimeDuration(sTimeSpec):
	try:
		days = sTimeSpec.split(",")
		if (len(days) > 1):
			numDays = days[0].split(" ")
			hours = days[1].split(":")
			return [int(numDays[0]),int(hours[0]),int(hours[1]),int(hours[2])]
		else:
			hours = sTimeSpec.split(":")
			if (hours == 1):
				numDays = days[0].split(" ")
				return [int(numDays[0]),0,0,0]
			else:
				return [0,int(hours[0]),int(hours[1]),int(hours[2])]
	except:
		pass
	return [0,0,0,0]

def grabTimeDurationToken1(_tok,_list):
	if (_tok[0].isdigit()):
		_list.append(_tok)

time_token_digits = ['0','1','2','3','4','5','6','7','8','9']
time_token_digits_dict = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}

def grabTimeDurationToken1(_tok,_list):
	global time_token_digits
	try:
		if (_tok[0] in time_token_digits):
			_list.append(_tok)
	except:
		pass

def grabTimeDurationToken2(_tok,_list):
	global time_token_digits_dict
	try:
		if (time_token_digits_dict[_tok[0]] != None):
			_list.append(_tok)
	except:
		pass

def calcTimeDuration(sTimeSpec):
	try:
		list = sTimeSpec.strip().replace(",",":").replace(" ",":").split(":")
		n = len(list)
		if (n == 2):
			return (int(list[0]) * 86400)
		elif (n == 3):
			return (int(list[0]) * 3600) + (int(list[1]) * 60) + int(list[2])
		elif (n == 6):
			return (int(list[0]) * 86400) + (int(list[3]) * 3600) + (int(list[4]) * 60) + int(list[5])
	except:
		pass
	return 0

def calcDays(list,i=0):
	return (list[i] * 86400)

def calcHHMMSS(list,i=0):
	return (list[i] * 3600) + (list[i+1] * 60) + list[i+2]

def calcDaysHHMMSS(list):
	return calcDays(list) + calcHHMMSS(list,3)

time_duration_matrix = {}
time_duration_matrix[2] = calcDays
time_duration_matrix[3] = calcHHMMSS
time_duration_matrix[6] = calcDaysHHMMSS

def _int(val):
	try:
		return int(val)
	except:
		pass
	return 0

def calcTimeDuration2(sTimeSpec):
	global time_duration_matrix
	try:
		list = [_int(t) for t in sTimeSpec.strip().replace(",",":").replace(" ",":").split(":")]
		return time_duration_matrix[len(list)](list)
	except:
		pass
	return 0

def cropTimeSeen(timeSeen):
	try:
		weekDay = timeSeen.split(',')
		timeZone = weekDay[len(weekDay)-1].split('-')
		return '%s%s' % (timeZone[0].strip(),timeZone[1])
	except:
		pass
	return timeSeen

def splitFields(w):
	isError = False
	try:
		fields = w.split(";")
	except Exception:
		isError = True
	if ( (isError) or (len(fields) < 7) ):
		return ['','','','','','','']
	return fields

def handleAppsList(l,w):
	# optimize this and all functions this calls... !
	exe_name, first_seen, junk1, last_seen, junk2, total_duration, runs = splitFields(w)      # 360.960s, 359.037s, 407.412s, 400.192s, 402.010s
	try:
		if ( (len(exe_name + runs) > 0) and (first_seen.find('1601') == -1) ):
			total_duration_in_seconds = calcTimeDuration(total_duration)
			try:
				l.append([exe_name,cropTimeSeen(first_seen),cropTimeSeen(last_seen),runs,total_duration_in_seconds])
			except:
				pass
	except Exception, details:
		print '(handleAppsList).2a :: ERROR :: (%s)' % (str(details))
		print '(handleAppsList).2b :: item=(%s)' % (str(item))
		print '(handleAppsList).2c :: w=(%s)' % (w)
		print '(handleAppsList).2d :: \nexe_name=(%s), \nfirst_seen=(%s), \njunk1=(%s), \nlast_seen=(%s), \njunk2=(%s), \ntotal_duration=(%s) [%s], \nruns=(%s)' % (str(exe_name), str(first_seen), str(junk1), str(last_seen), str(junk2), str(total_duration), str(total_duration_in_seconds), str(runs))
		print '=' * 60
		print '\n'

def handleAppsListToFile(f,w):
	# optimize this and all functions this calls... !
	exe_name, first_seen, junk1, last_seen, junk2, total_duration, runs = splitFields(w)      # 360.960s, 359.037s, 407.412s, 400.192s, 402.010s
	try:
		if ( (len(exe_name + runs) > 0) and (first_seen.find('1601') == -1) ):
			f.writelines(str([exe_name,cropTimeSeen(first_seen),cropTimeSeen(last_seen),runs,calcTimeDuration(total_duration)])[1:-1] + '\n')
	except Exception, details:
		print '(handleAppsListToFile).2a :: ERROR :: (%s)' % (str(details))
		print '(handleAppsListToFile).2b :: item=(%s)' % (str(item))
		print '(handleAppsListToFile).2c :: w=(%s)' % (w)
		print '(handleAppsListToFile).2d :: \nexe_name=(%s), \nfirst_seen=(%s), \njunk1=(%s), \nlast_seen=(%s), \njunk2=(%s), \ntotal_duration=(%s) [%s], \nruns=(%s)' % (str(exe_name), str(first_seen), str(junk1), str(last_seen), str(junk2), str(total_duration), str(total_duration_in_seconds), str(runs))
		print '=' * 60
		print '\n'

def handleAppsList3(l,w):
	# optimize this and all functions this calls... !
	try:
		_list = w.split(";")
	except Exception, details:
		_list = []
	if ( (len(_list) < 7) or (len(_list[0]+_list[6]) == 0) ):                                 # 370.269s --psyco=bind
		return
	exe_name, first_seen, junk1, last_seen, junk2, total_duration, runs = _list
	try:
		if (first_seen.find('1601') == -1):
			first_seen = cropTimeSeen(first_seen)
			last_seen = cropTimeSeen(last_seen)
			total_duration_in_seconds = calcTimeDuration(total_duration)
			item = [exe_name,first_seen,last_seen,runs,total_duration_in_seconds]
			try:
				l.append(item)
			except:
				pass
	except Exception, details:
		print '(handleAppsList).2a :: ERROR :: (%s)' % (str(details))
		print '(handleAppsList).2b :: item=(%s)' % (str(item))
		print '(handleAppsList).2c :: w=(%s)' % (w)
		print '(handleAppsList).2d :: \nexe_name=(%s), \nfirst_seen=(%s), \njunk1=(%s), \nlast_seen=(%s), \njunk2=(%s), \ntotal_duration=(%s) [%s], \nruns=(%s)' % (str(exe_name), str(first_seen), str(junk1), str(last_seen), str(junk2), str(total_duration), str(total_duration_in_seconds), str(runs))
		print '=' * 60
		print '\n'

def handleAppsList2(l,w):                                                                         # fastest time is 424.541s --psyco=bind
	# optimize this and all functions this calls... !
	try:
		_cols = w.split(";")
	except Exception, details:
		_cols = ['','','','','','','']
		#exe_name, first_seen, junk1, last_seen, junk2, total_duration, runs = ('','','','','','','')
		#   0         1         2        3         4         5           6
	if (len(_cols) == 7):
		try:
			if ( (len(_cols[0]) > 0) and (len(_cols[6]) > 0) and (_cols[1].find('1601') == -1) ): # 383.673s --psyco=bind
			#if ( (len(_cols[0] + runs) > 0) and (_cols[1].find('1601') == -1) ):                 # 341.963s --psyco=bind
			#if ( ((_cols[0] + _cols[6]) != '') and (_cols[1].find('1601') == -1) ):              # 392.304s --psyco=bind
				_cols[1] = cropTimeSeen(_cols[1])
				_cols[3] = cropTimeSeen(_cols[3])
				total_duration_in_seconds = calcTimeDuration(_cols[5])
				try:
					l.append(_cols)
				except:
					pass
		except Exception, details:
			print '(handleAppsList).2a :: ERROR :: (%s)' % (str(details))
			print '(handleAppsList).2b :: _cols=(%s)' % (str(_cols))
			print '(handleAppsList).2c :: w=(%s)' % (w)
			print '(handleAppsList).2d :: \nexe_name=(%s), \nfirst_seen=(%s), \njunk1=(%s), \nlast_seen=(%s), \njunk2=(%s), \ntotal_duration=(%s) [%s], \nruns=(%s)' % (str(_cols[0]), str(_cols[1]), str(_cols[2]), str(_cols[3]), str(_cols[4]), str(_cols[5]), str(total_duration_in_seconds), str(_cols[6]))
			print '=' * 60
			print '\n'

def handleFilePropertiesInstalledApps1(f):
	global _colsep3
	global _rowsep3
	global _handlers
	global COL_INDEX_QUESTION_ID
	global COL_INDEX_COMPUTER_ID
	global COL_INDEX_VALUE
	global RE_MULTIDATA_SEP
	global _package_map
	_masterListPrime = []
	_masterList = []
	_list_packages = []
	_list_apps = []
	for l in f:
		try:
			row = l.split(_colsep3)
			if (len(row) > 1):
				appendComputerId(_masterList,row,COL_INDEX_QUESTION_ID,COL_INDEX_COMPUTER_ID)
				resultstext = row[COL_INDEX_VALUE].decode('string_escape')
				toks = resultstext.split(RE_MULTIDATA_SEP)
				for w in toks:
					if (_package_map.has_key(w)):
						_list_packages.append([resultstext,_package_map[w]])
					handleAppsList(_list_apps,w)
		except Exception, details:
			print '(handleFilePropertiesInstalledApps1) :: ERROR :: (%s) [%s]' % (str(details),str(row))
	_masterListPrime.append(_masterList)
	_masterListPrime.append(_list_packages)
	_masterListPrime.append(_list_apps)
	return _masterListPrime

def handleFilePropertiesInstalledApps2(f):
	global _colsep3
	global _rowsep3
	global _handlers
	global COL_INDEX_QUESTION_ID
	global COL_INDEX_COMPUTER_ID
	global COL_INDEX_VALUE
	global RE_MULTIDATA_SEP
	global _package_map
	global OUTPUT_FILE_PROPERTIES_TEMP
	global OUTPUT_FILE_PACKAGES_TEMP
	global OUTPUT_FILE_APP_TRACKING_TEMP
	global _computer_id_dict
	_masterListPrime = []
	FH_COMPUTER_PROPS_TEMP = open(OUTPUT_FILE_PROPERTIES_TEMP, "w")
	FH_COMPUTER_PACKAGES_TEMP = open(OUTPUT_FILE_PACKAGES_TEMP, "w")
	FH_COMPUTER_APP_TRACKING_TEMP = open(OUTPUT_FILE_APP_TRACKING_TEMP, "w")
	for l in f:
		try:
			row = l.split(_colsep3)
			if (len(row) > 1):
				_getComputerId(row,COL_INDEX_QUESTION_ID,COL_INDEX_COMPUTER_ID)
				resultstext = row[COL_INDEX_VALUE].decode('string_escape')
				toks = resultstext.split(RE_MULTIDATA_SEP)
				for w in toks:
					if (_package_map.has_key(w)):
						FH_COMPUTER_PACKAGES_TEMP.writelines('%s%s%s\n' % (resultstext.encode('string_escape'),_colsep3,_package_map[w]))
					handleAppsListToFile(FH_COMPUTER_APP_TRACKING_TEMP,w)
		except Exception, details:
			print '(handleFilePropertiesInstalledApps2) :: ERROR :: (%s) [%s]' % (str(details),str(row))
	for anItem in _computer_id_dict.iteritems():
		FH_COMPUTER_PROPS_TEMP.writelines('%s%s%s\n' % (str(anItem[0]),_colsep3,str(anItem[1])[1:-1]))
	FH_COMPUTER_PROPS_TEMP.close()
	FH_COMPUTER_PACKAGES_TEMP.close()
	FH_COMPUTER_APP_TRACKING_TEMP.close()
	return _masterListPrime
#+++
def handleFileInstalledApps1(f):
	global _package_map
	_list = []
	for l in f:
		toks = l[COL_INDEX_VALUE].split(RE_MULTIDATA_SEP)
		for w in toks:
			if (_package_map.has_key(w)):
				_list.append([l[COL_INDEX_VALUE],_package_map[w]])
	return _list

def ioTime(t1,t2):
	global _ioElapsedTime
	et = t2 - t1
	_ioElapsedTime += et
	#print "et=(%s)" % str(et)

def ioTimeAnalysis():
	global _ioBeginTime
	global _ioEndTime
	global _ioElapsedTime
	_ioElapsedTime = 0
	[ioTime(_ioBeginTime[i],_ioEndTime[i]) for i in xrange(len(_ioEndTime))]
	return _ioElapsedTime

def main(fname):
	print "Using Method #1"
	global _handlers
	global _isVerbose
	global _isProfiling
	global _property_dict
	global COL_INDEX_QUESTION_ID
	global COL_INDEX_COMPUTER_ID
	global FH_COMPUTER_PROPS
	global FH_COMPUTER_PACKAGES
	global FH_COMPUTER_APP_TRACKING
	global _subMethod1
	global _ioBeginTime
	global _ioEndTime
	if (path.exists(fname)):
		_ioBeginTime.append(time.time())
		initMetadata()
		load_package_map()
		_ioEndTime.append(time.time())
		print "_handlers=(%s)" % str(_handlers)
		print "_subMethod1=(%s)" % (str(_subMethod1))
		try:
			FH_COMPUTER_PROPS = open(OUTPUT_FILE_PROPERTIES, "w")
			FH_COMPUTER_PACKAGES = open(OUTPUT_FILE_PACKAGES, "w")
			FH_COMPUTER_APP_TRACKING = open(OUTPUT_FILE_APP_TRACKING, "w")
			if (str(_subMethod1) == "1"):
				f = open(fname, "r")
				_list_Properties = handleFileProperties3(f)
				f.close()
				f = open(fname, "r")
				_list_InstalledApps = handleFileInstalledApps1(f)
				f.close()
			elif (str(_subMethod1) == "2"):
				f = open(fname, "r")
				_list_Master = handleFilePropertiesInstalledApps1(f)
				f.close()
			elif (str(_subMethod1) == "3"):
				f = open(fname, "r")
				_list_Master = handleFilePropertiesInstalledApps2(f)
				f.close()
			FH_COMPUTER_PROPS.close()
			FH_COMPUTER_PACKAGES.close()
			FH_COMPUTER_APP_TRACKING.close()
			print "Time spent doing I/O :: (%s), _ioBeginTime=(%s), _ioEndTime=(%s)" % (str(ioTimeAnalysis()),str(_ioBeginTime),str(_ioEndTime))
			if (str(_subMethod1) == "1"):
				print "len(_list_Properties)=(%s)" % str(len(_list_Properties))
				print "len(_list_InstalledApps)=(%s)" % str(len(_list_InstalledApps))
				if (_isVerbose):
					print "_list_Properties=(%s)" % str(_list_Properties)
					print "_list_InstalledApps=(%s)" % str(_list_InstalledApps)
			elif (str(_subMethod1) == "2"):
				print "len(_list_Master)=(%s)" % str(len(_list_Master))
				for item in _list_Master:
					print "len(item)=(%s)" % str(len(item))
				if (_isVerbose):
					#print "_list_Master=(%s)" % str(_list_Master)
					for item in _list_Master:
						print "item=(%s)" % str(item[0:1000])
		except Exception, details:
			print '(main) :: ERROR :: (%s)' % details
	else:
		print 'WARNING :: Missing file "%s" - cannot continue.' % fname

def main2(fname):
	print "Using Method #2"
	global _bufSize, _isVerbose
	if (path.exists(fname)):
		try:
			_lineCount = 0
			f = open(fname, "r")
			fname = '.'.join(fname.split('.')[:2])
			try:
				_count = 0
				lines = f.readlines(_bufSize)
				if (_isVerbose):
					print "(%s) Read %s lines" % (str(_count), str(len(lines)))
				while (lines):
					_count += 1
					if (_isVerbose):
						print "(%s) Read %s lines" % (str(_count), str(len(lines)))
					for l in lines:
						_lineCount += 1
					lines = f.readlines(_bufSize)
			except Exception, details:
				print 'Might be done Readling the file :: (%s)' % details
			f.close()
			print "_lineCount=(%s)" % str(_lineCount)
		except Exception, details:
			print 'ERROR :: (%s)' % details
	else:
		print 'WARNING :: Missing file "%s" - cannot continue.' % fname

def getBES_dbHandle():
	global _serverName
	return pyodbc.connect("DRIVER={SQL Server};SERVER=%s;DATABASE=countrywide;CommandTimeout=0;UID=sa;PWD=fooblah" % _serverName)

def get_analysis_id(site_name, analysis_name):
	_sql = "SELECT t.id as analysis_id FROM textfields t INNER JOIN versions AS v ON (t.isfixlet = v.isfixlet AND t.id = v.id AND t.sitename = v.sitename AND t.version = v.latestversion) INNER JOIN properties AS p ON (p.isfixlet = t.isfixlet AND p.id = t.id AND p.sitename = t.sitename) WHERE p.contenttype = 5 AND t.isfixlet = 0 AND t.FieldName = 'Name' AND t.sitename = '%s' AND cast(t.FieldContents as varchar(1024)) = '%s'" % (site_name,analysis_name)
	try:
		dbh = getBES_dbHandle()
		if (dbh):
			cursor = dbh.execute(_sql)
			row = cursor.fetchone()
			if (_isVerbose):
				print "get_analysis_id() :: (%s) --> [%s]" % (_sql,str(row[0]))
			dbh.close()
			return row[0]
	except Exception, details:
		print '(get_analysis_id) :: ERROR :: (%s)' % details
	return -1

def output1(fname):
	global _SQL_STATEMENT
	print "Using Output Method"
	dbh = None
	try:
		shelf = shelveSupport.persistence(fname)
		dbh = getBES_dbHandle()
		cursor = dbh.execute(_SQL_STATEMENT)
		num = 0
		_list = []
		_cols = ''
		iRange = xrange(len(_cols))
		for row in cursor:
			_list = [row[j] for j in iRange]
			#for x in _list:
			#	print "x.__class__=(%s) [%s]" % (x.__class__,str(x))
			#print "_list=(%s)" % str(_list)
			shelf.shelveThis("row_%s" % str(num),_list)
			#print "row.__class__=(%s)" % row.__class__
			num += 1
		_cols = [ t[0] for t in row.cursor_description ]
		shelf.shelveThis("_cols",_cols)
		shelf.shelveThis('numRows',num)
	except Exception, details:
		print '(output) :: ERROR :: (%s)' % details
	if (dbh):
		dbh.close()

def cropString(str):
	return str[1:len(str)-1]

def output(fname):
	global _serverName
	global _SQL_STATEMENT
	print "Using Output Method"
	dbh = None
	_mssql_connection_string2 = "DRIVER={SQL Server};SERVER=%s;DATABASE=countrywide;CommandTimeout=0;UID=sa;PWD=fooblah" % _serverName
	try:
		outHandle = open('%s.txt' % fname, "w")
		dbh = pyodbc.connect(_mssql_connection_string2)
		cursor = dbh.execute(_SQL_STATEMENT)
		num = 0
		_list = []
		_cols = 'computerid,resultstext,sequence,id,siteid'.split(',')
		_cols = [c for c in _cols]
		outHandle.writelines('%s\n' % cropString(str(_cols)))
		print "_cols=(%s)" % str(_cols)
		iRange = xrange(len(_cols))
		for row in cursor:
			_list = [row[j] for j in iRange]
			_list[1] = _list[1].encode('string_escape')
			_list[2] = '0x%s' % baseconvert.baseconvert(_list[2],baseconvert.BASE10, baseconvert.BASE16).rjust(16,'0')
			#for x in _list:
			#	print "x.__class__=(%s) [%s]" % (x.__class__,str(x))
			#print "_list=(%s)" % str(_list)
			#print "%s\n\n" % cropString(str(_list))
			_text = ''
			for x in _list:
				_text += str(x) + chr(255)
			outHandle.writelines('%s\n' % _text)
			num += 1
	except Exception, details:
		print '(output) :: ERROR :: (%s)' % details
	if (dbh):
		dbh.close()
		outHandle.close()
		print "num Rows = (%s)" % str(num)

def reader(fname):
	shelf = shelveSupport.persistence(fname)
	if (shelf):
		_numRows = shelf.unShelveThis('numRows')
		print "_numRows=(%s) [%s]" % (str(_numRows),_numRows.__class__)
		_cols = shelf.unShelveThis("_cols")
		print "_cols=(%s)" % str(_cols)
		if ( (_numRows == None) or (len(_numRows) == 0) ):
			i = 0
			try:
				while (True):
					aRow = shelf.unShelveThis("row_%s" % str(i))
					if ( (aRow == None) or (len(aRow) == 0) ):
						break
					i += 1
			except Exception, details:
				print '(reader) :: ERROR :: (%s)' % details
			shelf.shelveThis('numRows',i)

def timeReFunc(subject):
	return re.findall(r"(?:([0-9]+) days, )?(-?[0-2][0-9]):([0-5][0-9]):([0-5][0-9])", subject)

def timeRe1():
	datum = "25 days, 11:12:13"
	cols = timeReFunc(datum)

def timeSplits2():
	datum = "25 days, 11:12:13"
	cols = splitTimeDuration(datum)

def timeRe1a():
	datum = "11:12:13"
	cols = timeReFunc(datum)

def timeSplits2a():
	datum = "11:12:13"
	cols = splitTimeDuration(datum)

def timeRe1b():
	datum = "25 days"
	cols = timeReFunc(datum)
	if (len(cols) == 0):
		cols = timeReFunc(datum + ' 00:00:00')

def timeSplits2b():
	datum = "25 days"
	cols = splitTimeDuration(datum)

def timeReVersusSplits():
	from timeit import Timer
	
	all_timers = []
	all_tests = [["timeRe1","timeSplits2"],["timeRe1a","timeSplits2a"],["timeRe1b","timeSplits2b"]]
	
	for aTest in all_tests:
		_timers = []
		for specific_test in aTest:
			t = Timer('%s()' % specific_test, "from __main__ import %s" % specific_test)
			v = (1000000 * t.timeit(number=100000)/100000)
			_timers.append(v)
		all_timers.append(_timers)

	i = 0
	for vector in all_timers:
		aTest = all_tests[i]
		print "(%s) :: %.2f usec/pass" % (aTest[0],vector[0])
		print "(%s) :: %.2f usec/pass" % (aTest[1],vector[1])

		diff = (float(vector[1] - vector[0]) / float(vector[0])) * 100.0
		verb = 'slower'
		if (diff < 0):
			verb = 'faster'
			diff = -diff
		print "%s is %.2f%% %s then %s\n" % (aTest[1],diff,verb,aTest[0])
		i += 1

def time_calcTimeDuration():
	from timeit import Timer

	all_timers = []
	all_tests = [["calcTimeDuration"]]
	all_variations = ["25 days","25 days, 01:02:03","01:02:03"]
	#all_variations = ["01:02:03"]

	reps = 100000
	for aTest in all_tests:
		_timers = []
		for specific_test in aTest:
			if (len(all_variations) > 0):
				t = Timer('%s("%s")' % (specific_test,all_variations[0]), "from __main__ import %s" % specific_test)
				v = (reps * t.timeit(number=reps)/reps)
				_timers.append(v)

			if (len(all_variations) > 1):
				t = Timer('%s("%s")' % (specific_test,all_variations[1]), "from __main__ import %s" % specific_test)
				v = (reps * t.timeit(number=reps)/reps)
				_timers.append(v)

			if (len(all_variations) > 2):
				t = Timer('%s("%s")' % (specific_test,all_variations[2]), "from __main__ import %s" % specific_test)
				v = (reps * t.timeit(number=reps)/reps)
				_timers.append(v)
		all_timers.append(_timers)

	#print 'all_timers=[%s]' % str(all_timers)
	for vector in all_timers:
		i = 0
		_t = 0
		for t in vector:
			print "%.4f usec/pass for %s" % (t,all_variations[i])
			_t += t
			i += 1

	print "\n%.4f usec/pass (average)\n" % (_t/len(all_variations))
			
	for v in all_variations:
		val = calcTimeDuration(v)
		print "[%s] = (%s)" % (v,str(val))

def load_computer_map():
	global _computer_map
	global _isVerbose
	global _ioBeginTime
	global _ioEndTime
	global _mssql_connection_string
	try:
		rowcount = 0
		_ioBeginTime.append(time.time())
		_aardvark_dbh = pyodbc.connect(_mssql_connection_string)
		cursor = _aardvark_dbh.execute("select datasource_identifier, max(id) as computer_id from computers group by datasource_identifier")
		_ioEndTime.append(time.time())
		for row in cursor:
			_computer_map[row[0]] = row[1]
			rowcount += 1
		if (_isVerbose):
			print "load_computer_map() :: _computer_map = [%s], based on rowcount of %s\n\n" % (str(len(_computer_map.keys())),str(rowcount))
	except Exception, details:
		print '(load_computer_map) :: ERROR :: (%s)' % str(details)
	print "_computer_map=(%s)\n" % str(_computer_map)
	_aardvark_dbh.close()

def pipelineProcessHandleProps(f):
	global _ioBeginTime
	global _ioEndTime
	global _isVerbose
	lineCount = 0
	for l in f:
		_cols = l.strip().split(_colsep3)
		if (len(_cols) == 2):
			if (lineCount < 1000):
				_ioBeginTime.append(time.time())
				computer_id = get_mapped_computer_id(_cols[0])
				_ioEndTime.append(time.time())
				if (_isVerbose):
					print 'computer_id=(%s), [%s] [%s]\n' % (str(computer_id),str(_cols[0]),str(_cols[1]))
		lineCount += 1
	return lineCount

def pipelineProcess2():
	global OUTPUT_FILE_PROPERTIES_TEMP
	load_computer_map();
	FH_COMPUTER_PROPS_TEMP = open(OUTPUT_FILE_PROPERTIES_TEMP, "r")
	numLines = pipelineProcessHandleProps(FH_COMPUTER_PROPS_TEMP)
	FH_COMPUTER_PROPS_TEMP.close()
	et = ioTimeAnalysis()
	expectedTime = (et / 1000) * numLines
	print "Time spent doing I/O :: (%s) of (%s) for numLines=(%s)" % (str(et),str(expectedTime),str(numLines))

def save2db(fname):
	global _mssql_surrogate_connection_string
	print '(save2db) :: fname=(%s)' % fname
	_ioBeginTime.append(time.time())
	f = open(fname, "r")
	rowCnt = 0
	_aardvark_dbh = pyodbc.connect(_mssql_surrogate_connection_string)
	_sql = "TRUNCATE table bes_data;"
	_aardvark_dbh.execute(_sql)
	_aardvark_dbh.commit()
	for l in f:
		try:
			row = l.split(_colsep3)
			if (len(row) > 1):
				_sql = "INSERT INTO bes_data (COMPUTER_ID, VALUE, SEQUENCE, PROPERTY_ID, SITE_ID) VALUES (%s,'%s',%s,%s,%s);" % (int(row[0]),row[1].decode('string_escape').replace("'","''"),eval(row[2]),int(row[3]),int(row[4]))
				_aardvark_dbh.execute(_sql)
				rowCnt += 1
				if ((rowCnt % 10000) == 0):
					print "rowCnt=(%s)" % (rowCnt)
		except Exception, details:
			print '(save2db) :: ERROR :: (%s)' % (str(details))
	_aardvark_dbh.commit()
	_aardvark_dbh.close()
	f.close()
	_ioEndTime.append(time.time())
	et = ioTimeAnalysis()
	print "Time spent doing I/O :: (%s) for numLines=(%s)" % (str(et),str(rowCnt))

def save2db_bulk(fname):
	global _mssql_surrogate_connection_string
	print '(save2db_bulk) :: fname=(%s)' % fname
	_ioBeginTime.append(time.time())
	_aardvark_dbh = pyodbc.connect(_mssql_surrogate_connection_string)
	_sql = "TRUNCATE TABLE bes_data; BULK INSERT bes_data FROM 'Z:\python projects\aardvark\Bigtest.txt' WITH (DATAFILETYPE = 'char', FIELDTERMINATOR = '%s', ROWTERMINATOR = '\n');" % _colsep3
	_aardvark_dbh.execute(_sql)
	_aardvark_dbh.commit()
	_aardvark_dbh.close()
	_ioEndTime.append(time.time())
	et = ioTimeAnalysis()
	print "Time spent doing I/O :: (%s) for numLines=(%s)" % (str(et),str(rowCnt))
#+++
if ( (len(sys.argv) == 1) or (sys.argv[1] == '--help') ):
	print '--help                    ... displays this help text.'
	print '--verbose                 ... output more stuff.'
	print '--profile                 ... use profiler.'
	print '--psyco                   ... use psyco.'
	print '--psyco=full              ... use psyco using full method.'
	print '--psyco=log               ... use psyco using log method.'
	print '--psyco=bind              ... use psyco using bind method.'
	print '--input=input_file_name   ... name of input file.'
	print '--input2=input_file_name  ... name of input file.'
	print '--server=server_name      ... name of SQL Server instance (aracari).'
	print '--output=output_file_name ... name of output file.'
	print '--read=input_file_name    ... name of input file (from --output=).'
	print '--save2db=input_file_name ... save contents of name of input file (from --output=) to db.'
	print '--timeRe                  ... time the re versus split for timeDurations.'
	print '--time01                  ... time the calcTimeDuration.'
	print '--subMethod=1             ... specify the sub-method for the analysis being performed.'
	print '--process=2               ... specify the process (pipelined process number).'
else:
	_fileName = ''
	for i in xrange(len(sys.argv)):
		if ( (sys.argv[i].find('--input=') > -1) or (sys.argv[i].find('--input2=') > -1) or (sys.argv[i].find('--output=') > -1) or (sys.argv[i].find('--read=') > -1) or (sys.argv[i].find('--timeRe') > -1) or (sys.argv[i].find('--time01') > -1) or (sys.argv[i].find('--process') > -1) or (sys.argv[i].find('--save2db') > -1) ): 
			if ( (sys.argv[i].find('--timeRe') == -1) and (sys.argv[i].find('--time01') == -1) and (sys.argv[i].find('--process') == -1) ):
				toks = sys.argv[i].split('=')
				_fileName = toks[1]
			elif (sys.argv[i].find('--process') > -1):
				toks = sys.argv[i].split('=')
				_pipelined_process_number = toks[1]
			if (_isPsyco):
				import psyco
				if (_psyco_subMethod == 'full'):
					psyco.full()
				elif (_psyco_subMethod == 'log'):
					psyco.log()
					psyco.profile()
				elif (_psyco_subMethod == 'bind'):
					psyco.bind(main)
					psyco.bind(main2)
					psyco.bind(pipelineProcess2)
			if (_isProfiling):
				import cProfile
				if (sys.argv[i].find('--input=') > -1):
					cProfile.run("main('%s')" % _fileName.replace('\\', '\\\\'))
				elif (sys.argv[i].find('--input2=') > -1):
					cProfile.run("main2('%s')" % _fileName.replace('\\', '\\\\'))
				elif (sys.argv[i].find('--output=') > -1):
					cProfile.run("output('%s')" % _fileName.replace('\\', '\\\\'))
				elif (sys.argv[i].find('--read=') > -1):
					cProfile.run("reader('%s')" % _fileName.replace('\\', '\\\\'))
				elif (sys.argv[i].find('--timeRe') > -1):
					cProfile.run("timeReVersusSplits()")
				elif (sys.argv[i].find('--process') > -1):
					cProfile.run("pipelineProcess%s()" % str(_pipelined_process_number))
				elif (sys.argv[i].find('--time01') > -1):
					cProfile.run("time_calcTimeDuration()")
			else:
				if (sys.argv[i].find('--input=') > -1):
					main(_fileName)
				elif (sys.argv[i].find('--input2=') > -1):
					main2(_fileName)
				elif (sys.argv[i].find('--output=') > -1):
					output(_fileName)
				elif (sys.argv[i].find('--read=') > -1):
					reader(_fileName)
				elif (sys.argv[i].find('--timeRe') > -1):
					if (_isPsyco):
						psyco.bind(timeRe1)
						psyco.bind(timeSplits2)
						psyco.bind(timeRe1a)
						psyco.bind(timeSplits2a)
						psyco.bind(timeRe1b)
						psyco.bind(timeSplits2b)
					timeReVersusSplits()
				elif (sys.argv[i].find('--process') > -1):
					if (_pipelined_process_number == 2):
						pipelineProcess2()
				elif (sys.argv[i].find('--time01') > -1):
					if (_isPsyco):
						psyco.bind(time_calcTimeDuration)
					time_calcTimeDuration()
				elif (sys.argv[i].find('--save2db') > -1):
					save2db(_fileName)
		elif (sys.argv[i].find('--profile') > -1):
			_isProfiling = True
		elif ( (sys.argv[i].find('--psyco') > -1) or (sys.argv[i].find('--psyco=') > -1) ):
			_isPsyco = True
			if (sys.argv[i].find('--psyco=') > -1):
				toks = sys.argv[i].split('=')
				_psyco_subMethod = toks[1]
		elif (sys.argv[i].find('--verbose') > -1):
			_isVerbose = True
		elif (sys.argv[i].find('--server') > -1):
			toks = sys.argv[i].split('=')
			_serverName = toks[1]
		elif (sys.argv[i].find('--subMethod') > -1):
			toks = sys.argv[i].split('=')
			_subMethod1 = toks[1]
