import os
import time
import psyco
import sys
import pyodbc
import logging
from vyperlogix import WinProcesses
from vyperlogix import threadpool
from threading import BoundedSemaphore
from vyperlogix import ioTimeAnalysis
import deleteAllFilesUnder
import adodbapi
import Queue
from vyperlogix import _utils

# Requirements:
# Multi-Data Sources via multi-threads, etc.

_isVerbose = False
_isThreaded = 100

_pool = threadpool.Pool(_isThreaded)
_db_pool = threadpool.Pool(10)

_data_queue = Queue.Queue()
_id_queue = Queue.Queue()

_Semaphore = BoundedSemaphore(value=1)

_resultsFolderName = 'bcp'

_memoryUsed = []

_lines = []

_colsep3 = '\t\t'
_rowsep3 = '\n\n'

_fileNum = 0

_rowCount = 0

_dbRunning = True

_memoryThreshold = 100000*1024

_rowThreshold = 25000

_mssql_connection_string = 'DRIVER={SQL Server};SERVER=MURRE\DEV2005;DATABASE=countrywide_2005;CommandTimeout=0;UID=sa;PWD=peekab00'
_mssql_connection_string3 = 'DRIVER={SQL Server};SERVER=MURRE\DEV2005;DATABASE=countrywide_2005;CommandTimeout=0;UID=sa;PWD=peekab00'
_mssql_connection_string3k = 'DRIVER={SQL Server};SERVER=katamari;DATABASE=countrywide_2005;CommandTimeout=0;UID=test;PWD=peekab00'

SQL_RECORD_SPEC = 'TOP %s ' % _rowThreshold
# 
SQL_STATEMENT = "SELECT TOP (1000) qr.computerid, COALESCE(qr.resultstext, lqr.resultstext) as resultstext, qr.sequence, qr.id as property_id, qr.siteid FROM questionresults as qr with (nolock) INNER JOIN computers with (nolock) ON (computers.computerid = qr.computerid AND computers.isdeleted = 0) LEFT OUTER JOIN longquestionresults as lqr with (nolock) on (qr.siteid = lqr.siteid AND qr.id = lqr.id AND qr.computerid = lqr.computerid) WHERE qr.siteid = 1 AND qr.IsFailure = 0 AND ((qr.siteid = 1 AND qr.id = 27)OR (qr.siteid = 1 AND qr.id = 96514)OR (qr.siteid = 1 AND qr.id = 18)OR (qr.siteid = 1 AND qr.id = 82118)OR (qr.siteid = 1 AND qr.id = 31)OR (qr.siteid = 1 AND qr.id = 17)) AND qr.resultscount < 700"

# BEGIN:  This statement returns a list of computer ID's...
SQL_STATEMENT_ID_LIST = "SELECT TOP (1000) qr.ComputerID FROM QUESTIONRESULTS AS qr WITH (nolock) INNER JOIN COMPUTERS WITH (nolock) ON COMPUTERS.ComputerID = qr.ComputerID AND COMPUTERS.IsDeleted = 0 WHERE (qr.SiteID = 1) AND (qr.IsFailure = 0) AND (qr.SiteID = 1) AND (qr.ID = 27) AND (qr.ResultsCount < 700) OR (qr.SiteID = 1) AND (qr.IsFailure = 0) AND (qr.SiteID = 1) AND (qr.ID = 96514) AND (qr.ResultsCount < 700) OR (qr.SiteID = 1) AND (qr.IsFailure = 0) AND (qr.SiteID = 1) AND (qr.ID = 18) AND (qr.ResultsCount < 700) OR (qr.SiteID = 1) AND (qr.IsFailure = 0) AND (qr.SiteID = 1) AND (qr.ID = 82118) AND (qr.ResultsCount < 700) OR (qr.SiteID = 1) AND (qr.IsFailure = 0) AND (qr.SiteID = 1) AND (qr.ID = 31) AND (qr.ResultsCount < 700) OR (qr.SiteID = 1) AND (qr.IsFailure = 0) AND (qr.SiteID = 1) AND (qr.ID = 17) AND (qr.ResultsCount < 700)"
# END!    This statement returns a list of computer ID's...

# BEGIN:  This statement is very inefficient...
SQL_STATEMENT_BY_ID = "SELECT qr.computerid, COALESCE(qr.resultstext, lqr.resultstext) as resultstext, qr.sequence, qr.id as property_id, qr.siteid FROM questionresults as qr with (nolock) INNER JOIN computers with (nolock) ON (computers.computerid = qr.computerid AND computers.isdeleted = 0) LEFT OUTER JOIN longquestionresults as lqr with (nolock) on (qr.siteid = lqr.siteid AND qr.id = lqr.id AND qr.computerid = lqr.computerid) WHERE qr.siteid = 1 AND qr.IsFailure = 0 AND ((qr.siteid = 1 AND qr.id = 27)OR (qr.siteid = 1 AND qr.id = 96514)OR (qr.siteid = 1 AND qr.id = 18)OR (qr.siteid = 1 AND qr.id = 82118)OR (qr.siteid = 1 AND qr.id = 31)OR (qr.siteid = 1 AND qr.id = 17)) AND (qr.resultscount < 700)" #  AND (qr.computerid = 1168457049)
# END!    This statement is very inefficient...

FMT_LIST = ['<?xml version="1.0"?>','<BCPFORMAT xmlns="http://schemas.microsoft.com/sqlserver/2004/bulkload/format" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">','<RECORD>','<FIELD ID="1" xsi:type="CharTerm" TERMINATOR="%s" MAX_LENGTH="10"/>','<FIELD ID="2" xsi:type="CharTerm" TERMINATOR="%s" COLLATION="SQL_Latin1_General_CP1_CI_AS"/>','<FIELD ID="3" xsi:type="CharTerm" TERMINATOR="%s" MAX_LENGTH="16"/>','<FIELD ID="4" xsi:type="CharTerm" TERMINATOR="%s" MAX_LENGTH="10"/>','<FIELD ID="5" xsi:type="CharTerm" TERMINATOR="%t" MAX_LENGTH="10"/>','</RECORD>','<ROW>','<COLUMN SOURCE="1" NAME="computerid" xsi:type="SQLBIGINT"/>','<COLUMN SOURCE="2" NAME="resultstext" xsi:type="SQLTEXT"/>','<COLUMN SOURCE="3" NAME="sequence" xsi:type="SQLBIGINT"/>','<COLUMN SOURCE="4" NAME="property_id" xsi:type="SQLINT"/>','<COLUMN SOURCE="5" NAME="siteid" xsi:type="SQLINT"/>','</ROW>','</BCPFORMAT>']

fmtFname = 'datafmt.xml'

def exec_and_fetch_sql(_cnnStr,_sql):
	try:
		_aardvark_dbh = pyodbc.connect(_cnnStr)
		_cursor = _aardvark_dbh.cursor()
		_cursor.execute(_sql)
		row = _cursor.fetchone()
		_aardvark_dbh.close()
		return row
	except Exception, details:
		print '(exec_and_fetch_sql) :: Error "%s" _cnnStr=(%s), _sql=(%s).' % (str(details),_cnnStr,_sql)
	return None

def exec_and_process_sql(_cnnStr,_sql,_callback):
	try:
		_aardvark_dbh = pyodbc.connect(_cnnStr)
		_cursor = _aardvark_dbh.cursor()
		ioBeginTime('exec_and_process_sql (execute)')
		rows = _cursor.execute(_sql)
		ioEndTime('exec_and_process_sql (execute)')
		ioBeginTime('exec_and_process_sql (_callback)')
		try:
			_callback(rows)
		except Exception, details:
			_info = '(exec_and_process_sql).1 :: Error "%s" _cnnStr=(%s), _sql=(%s).' % (str(details),_cnnStr,_sql)
			print _info
			logging.warning(_info)
		ioEndTime('exec_and_process_sql (_callback)')
		_aardvark_dbh.close()
	except Exception, details:
		_info = '(exec_and_process_sql).2 :: Error "%s" _cnnStr=(%s), _sql=(%s).' % (str(details),_cnnStr,_sql)
		print _info
		logging.warning(_info)

def exec_and_process_sql_no_cursor(_cnnStr,_sql,_callback):
	try:
		_aardvark_dbh = pyodbc.connect(_cnnStr)
		ioBeginTime('exec_and_process_sql_no_cursor (execute)')
		rows = _aardvark_dbh.execute(_sql)
		ioEndTime('exec_and_process_sql_no_cursor (execute)')
		ioBeginTime('exec_and_process_sql_no_cursor (_callback)')
		try:
			_callback(rows)
		except Exception, details:
			_info = '(exec_and_process_sql_no_cursor).1 :: Error "%s" _cnnStr=(%s), _sql=(%s).' % (str(details),_cnnStr,_sql)
			print _info
			logging.warning(_info)
		ioEndTime('exec_and_process_sql_no_cursor (_callback)')
		_aardvark_dbh.close()
	except Exception, details:
		_info = '(exec_and_process_sql_no_cursor).2 :: Error "%s" _cnnStr=(%s), _sql=(%s).' % (str(details),_cnnStr,_sql)
		print _info
		logging.warning(_info)

def exec_and_process_sql_ado(_cnnStr,_sql,_callback):
	try:
		_aardvark_dbh = adodbapi.connect(_cnnStr)
		_cursor = _aardvark_dbh.cursor()
		ioBeginTime('exec_and_process_sql_ado (execute)')
		rows = _cursor.execute(_sql)
		ioEndTime('exec_and_process_sql_ado (execute)')
		ioBeginTime('exec_and_process_sql_ado (_callback)')
		try:
			_callback(_cursor)
		except Exception, details:
			_info = '(exec_and_process_sql_ado).1 :: Error "%s" _cnnStr=(%s), _sql=(%s).' % (str(details),_cnnStr,_sql)
			print _info
			logging.warning(_info)
		ioEndTime('exec_and_process_sql_ado (_callback)')
		_aardvark_dbh.close()
	except Exception, details:
		_info = '(exec_and_process_sql_ado).2 :: Error "%s" _cnnStr=(%s), _sql=(%s).' % (str(details),_cnnStr,_sql)
		print _info
		logging.warning(_info)

def doBCP(cmd):
	global _ioBeginTime
	global _ioEndTime
	
	ioBeginTime('doBCP')
	os.system(cmd)
	ioEndTime('doBCP')
	
def writeBCP(fname,cmd):
	fHand = open(fname, "w")
	fHand.writelines(cmd)
	fHand.close()

def writeFmtFile(fname):
	fHand = open(fname, "w")
	for l in FMT_LIST:
		fHand.writelines('%s\n' % l.replace('%s',_colsep3.encode('string_escape')).replace('%t',_rowsep3.encode('string_escape')))
	fHand.close()

def prepareSQLStatement(sql,newColSpecFunc):
	keyword1 = 'SELECT '
	_f1 = sql.find(keyword1)
	if (_f1 > -1):
		_f1 += len(keyword1)
	keyword2 = ' FROM'
	_f2 = sql.find(keyword2)
	if ( (_f1 > -1) and (_f2 > -1) ):
		colsSpec = sql[_f1:_f2]
		try:
			sql = newColSpecFunc(sql,colsSpec,_f1,_f2)
		except:
			pass
		return sql
	return ''

def prepSQLStatementForCount(sql,colsSpec,_f1,_f2):
	try:
		toks = colsSpec.split(',')
		sql = sql.replace(colsSpec,'count(%s) as count' % toks[0])
	except:
		pass
	return sql

def prepareSQLStatementForCount(sql):
	return prepareSQLStatement(sql,prepSQLStatementForCount)

def prepSQLStatementForSequenceRange(sql,colsSpec,_f1,_f2):
	try:
		sql = sql.replace(colsSpec,'count(qr.computerid) as count, cast(min(qr.sequence) as bigint) as min_sequence, cast(max(qr.sequence) as bigint) as max_sequence')
	except:
		pass
	return sql

def prepareSQLStatementForSequenceRange(sql):
	return prepareSQLStatement(sql,prepSQLStatementForSequenceRange)

def prepSQLStatementForNumberOfRecords(sql,colsSpec,_f1,_f2):
	global SQL_RECORD_SPEC
	try:
		sql = sql[0:_f1] + SQL_RECORD_SPEC + sql[_f1:]
	except:
		pass
	return sql

def prepareSQLStatementForNumberOfRecords(sql):
	return prepareSQLStatement(sql,prepSQLStatementForNumberOfRecords)

def getRecordCount():
	global _mssql_connection_string3
	global SQL_STATEMENT
	_sql = prepareSQLStatementForCount(SQL_STATEMENT)
	ioBeginTime('getRecordCount')
	_row = exec_and_fetch_sql(_mssql_connection_string3,_sql)
	ioEndTime('getRecordCount')
	_count = -1
	if (_row != None):
		_count = _row[0]
	return _count

def getSequenceNumberRange():
	global _mssql_connection_string3
	global SQL_STATEMENT
	_sql = prepareSQLStatementForSequenceRange(SQL_STATEMENT)
	ioBeginTime('getSequenceNumberRange')
	_row = exec_and_fetch_sql(_mssql_connection_string3,_sql)
	ioEndTime('getSequenceNumberRange')
	_stats = {'min':-1, 'max': -1, 'count': -1, 'spread': -1}
	try:
		if (_row != None):
			_count = _row.max_sequence - _row.min_sequence
			_spread = _count / _row.count
			_stats = {'min':_row.min_sequence, 'max': _row.max_sequence, 'count': _row.count, 'spread': _spread}
			print '(getSequenceNumberRange) :: _stats=(%s)' % (_stats)
	except Exception, details:
		print '(getSequenceNumberRange) :: Error details "%s".' % str(details)
	return _stats

def main1(fname):
	global fmtFname
	global SQL_STATEMENT

	stats = getSequenceNumberRange()
	if ( (stats.has_key('min')) and (stats.has_key('max')) and (stats.has_key('count')) and (stats.has_key('spread')) ):
		_min = stats['min']
		_max = stats['max']
		_steps = stats['count'] / 100000
		_spreadStep = stats['spread'] * 100000
		print 'getSequenceNumberRange() :: (_min=%s,_max=%s,rowCount=%s,spread=%s,_steps=%s,_spreadStep=%s)\n' % (_min,_max,stats['count'],stats['spread'],_steps,_spreadStep)
		
		sqlList = []
		i_seq = _min
		for i in xrange(_steps):
			i_seq2 = i_seq + _spreadStep
			if (i == (_steps - 1)):
				i_seq2 = _max
			_sql = '%s and (cast(qr.sequence as bigint) >= %s) and (cast(qr.sequence as bigint) <= %s)\n' % (SQL_STATEMENT,i_seq,i_seq2)
			i_seq = i_seq2
			print '_sql=(%s)' % _sql
			sqlList.append(_sql)
	ioAnalysis = ioTimeAnalysis()
	print "Time spent doing I/O :: (%s)" % (str(ioAnalysis))

def readFile(fname):
	data = ''
	if (os.path.exists(fname)):
		ioBeginTime('readFile')
		fHand = open(fname,'rb')
		data = fHand.read()
		fHand.close()
		ioEndTime('readFile')
	return data

def determineNextUsableFileNumber(fname,bool=False):
	global _fileNum
	global _Semaphore
	toks = fname.split('.')
	toks[0] = toks[0] + str(_fileNum)
	_fname = _resultsFolderName + '.'.join(toks)
	print '(determineNextUsableFileNumber) :: _fname=(%s)' % _fname
	if (os.path.exists(_fname) == bool):
		_Semaphore.acquire()
		_fileNum += 1
		_Semaphore.release()
		return _fname
	return fname

def reportTimeAnalysis(tag='(Main)'):
	ioAnalysis = ioTimeAnalysis()
	print "%s :: Time spent doing I/O :: (%s)" % (tag,str(ioAnalysis))

def main(fname,seqNbr=-1):
	global fmtFname
	global SQL_STATEMENT

	print '(main).0 :: fname=(%s)' % fname
	_fname = determineNextUsableFileNumber(fname)
	print '(main) :: _fname=(%s)' % _fname
	sql = prepareSQLStatementForNumberOfRecords(SQL_STATEMENT)
	if (seqNbr > -1):
		sql += ' and (cast(qr.sequence as bigint) > %s)' % seqNbr
	CMD = 'bcp "%s" queryout %s -f %s -a 65535 -Saracari -Usa -Pfooblah' % (sql,_fname,fmtFname)
	print CMD

	writeBCP('dobcp.cmd',CMD)
	if (seqNbr == -1):
		writeFmtFile(_resultsFolderName+fmtFname)
	doBCP(CMD)

	if (os.path.exists(_fname)):
		statInfo = os.stat(_fname)
		if (statInfo.st_size > 0):
			print '\n'
			ioBeginTime('parseFile')
			rows = [t.split(_colsep3) for t in readFile(_fname).split(_rowsep3)]
			ioEndTime('parseFile')
			sample = rows.pop()
			print '(main) :: len(sample)=(%s) [%s] (%s)\n' % (len(sample),sample,len(sample[0]))
			if ( (len(sample) > 0) and (len(sample[0]) > 0) ):
				rows.append(sample)
			for t in rows[len(rows)-5:]:
				print '(main) :: t=(%s)\n' % t
			sample = rows[len(rows)-1]
			try:
				sample_sequence = eval('0x' + sample[2])
			except:
				sample_sequence = -1
			print '(main) :: sequence=(%s) (%s) [%s]\n' % (sample_sequence,sample[2],sample)
			
			print '\n'
			
			rows = None
			main(fname,sample_sequence)
		else:
			reportTimeAnalysis('(main)')
	else:
		reportTimeAnalysis('(main)')

def main_test(fname):
	global _rowCount
	global _isVerbose
	_info = '(main_test).0 :: fname=(%s)' % fname
	print _info
	_fname = determineNextUsableFileNumber(fname,True)
	_info = '(main_test).1 :: os.path.exists(%s)=(%s)' % (_fname,os.path.exists(_fname))
	print _info
	logging.warning(_info)
	if (os.path.exists(_fname)):
		statInfo = os.stat(_fname)
		_info = '(main_test).2 :: statInfo.st_size=(%s)' % (statInfo.st_size)
		print _info
		logging.warning(_info)
		if (statInfo.st_size > 0):
			print '\n'
			ioBeginTime('parseFile (%s)' % _fname)
			rows = [t.split(_colsep3) for t in readFile(_fname).split(_rowsep3)]
			ioEndTime('parseFile (%s)' % _fname)
			_rowCount += len(rows)
			_info = '(main_test).3 :: _rowCount=(%s), len(rows)=(%s)' % (_rowCount,len(rows))
			print _info
			logging.warning(_info + '\n')
			if (_isVerbose):
				for t in rows[0:5]:
					print '(main_test).4 :: t=(%s)\n' % t
				for t in rows[len(rows)-5:]:
					print '(main_test).5 :: t=(%s)\n' % t
			rows = None
			main_test(fname)
		else:
			reportTimeAnalysis('(main_test, _rowCount=(%s))' % _rowCount)
	else:
		reportTimeAnalysis('(main_test, _rowCount=(%s))' % _rowCount)

def main_read(fname):
	global _rowCount
	global _isVerbose

	ioBeginTime('parseFile (%s)' % fname)
	rows = [t.split(_colsep3) for t in readFile(fname).split(_rowsep3)]
	ioEndTime('parseFile (%s)' % fname)

	_rowCount += len(rows)
	_info = '(main_read) :: _rowCount=(%s)' % (_rowCount)
	print _info
	logging.warning(_info + '\n')

def writeDataToFile(fname):
	global _rowCount
	global _lines
	global _fileNum
	_fname = determineNextUsableFileNumber(fname,False)
	_info = '(writeDataToFile.processRows).1 :: (_rowCount=%s), (_fileName=%s), (_fname=%s), _fileNum=(%s)' % (_rowCount,fname,_fname,_fileNum)
	print _info
	logging.warning(_info)
	ioBeginTime('writeDataToFile.processRows (%s)' % _fname)
	fHand = open(_fname,"w")
	fHand.writelines(_rowsep3.join(_lines[_fileNum-1]))
	fHand.close()
	ioEndTime('writeDataToFile.processRows (%s)' % _fname)
	_lines[_fileNum-1] = []

@threadpool.threadpool(_pool)
def writeDataToFileThreaded(fname):
	writeDataToFile(fname)

def appendDataToLines(fname,datum):
	global _memoryUsed
	global _fileNum
	_lines[_fileNum].append(_colsep3.join(datum))
	ioBeginTime('main_bcp.processRows (WinProcesses.getProcessMemoryUsageForHandle)')
	_memoryUsed[_fileNum] = win_proc.getProcessMemoryUsageForHandle(procHandle)
	ioEndTime('main_bcp.processRows (WinProcesses.getProcessMemoryUsageForHandle)')
	if (_memoryUsed[_fileNum] >= _memoryThreshold):
		writeDataToFile(fname)

@threadpool.threadpool(_pool)
def appendDataToLinesThreaded(fname,datum):
	t = _colsep3.join(datum)
	_lines[_fileNum].append(t)
	ioBeginTime('main_bcp.appendDataToLinesThreaded')
	_memoryUsed[_fileNum] += (len(t) + 2)
	ioEndTime('main_bcp.appendDataToLinesThreaded')
	if (_memoryUsed[_fileNum] >= _memoryThreshold):
		writeDataToFileThreaded(fname)

@threadpool.threadpool(_pool)
def dataQueueConsumer(q):
	_info = '(main_bcp.dataQueueConsumer).1 :: init !'
	print _info
	logging.warning(_info)
	try:
		while (_dbRunning):
			f = q.get()
			appendDataToLinesThreaded(_fileName,f)
			q.task_done()
	except Exception, details:
		_info = '(main_bcp.dataQueueConsumer).4 :: ERROR "%s" !' % (str(details))
		print _info
		logging.warning(_info)
	_info = '(main_bcp.dataQueueConsumer).3 :: abend !'
	print _info
	logging.warning(_info)

@threadpool.threadpool(_pool)
def processRowThreaded(row):
	global _rowCount
	try:
		_data_queue.put([str(row[0]),str(row[1]),str(row[2]),str(row[3])])
		_rowCount += 1
		if ((_rowCount % 100) == 0):
			_info = '(main_bcp.processRowThreaded).1 :: _rowCount=(%s), _data_queue.qsize()=(%s)' % (_rowCount,_data_queue.qsize())
			print _info
			logging.warning(_info)
	except:
		pass

def processRows(rows):
	global _rowCount
	global _rowThreshold
	global _memoryThreshold
	global _fileName
	global _isThreaded
	global _lines
	global _fileNum
	global _memoryUsed
	global _dbRunning
	_info = '(main_bcp.processRows).0 :: (_rowCount=%s)' % (_rowCount)
	print _info
	logging.warning(_info)
	_lines = [[] for i in xrange(1000)]
	_memoryUsed = [0 for i in xrange(1000)]
	ioBeginTime('main_bcp.processRows (WinProcesses.init)')
	win_proc = WinProcesses()
	pid = win_proc.getProcessIdByName('python')
	procHandle = win_proc.openProcessForPID(pid)
	ioEndTime('main_bcp.processRows (WinProcesses.init)')
	if ( (str(rows.__class__).find('pyodbc.Cursor') > -1) or (str(rows.__class__).find('adodbapi.adodbapi.Cursor') > -1) ):
		dataQueueConsumer(_data_queue)
		try:
			r = rows.fetchone()
			while (r):
				processRowThreaded(r)
				r = rows.fetchone()
		except Exception, details:
			_info = '(main_bcp.processRows).0 :: Error "%s".' % (str(details))
			print _info
			logging.warning(_info)
	_info = '(main_bcp.processRows).2 :: _data_queue.join() !'
	print _info
	logging.warning(_info)
	_data_queue.join()
	_dbRunning = False
	_info = '(main_bcp.processRows).3 :: (_rowCount=%s)' % (_rowCount)
	print _info
	logging.warning(_info)
	if (len(_lines) > 0):
		writeDataToFileThreaded(_fileName)
	ioBeginTime('main_bcp.processRows (WinProcesses.closeProcessHandle)')
	win_proc.closeProcessHandle(procHandle)
	ioEndTime('main_bcp.processRows (WinProcesses.closeProcessHandle)')
	reportTimeAnalysis('(main_bcp.processRows)')

def processRows_no_cursor(rows):
	_info = '(processRows_no_cursor) :: rows.__class__=(%s)' % (str(rows.__class__))
	print _info
	logging.warning(_info)

def processByComputerID(rows):
	_info = '(main_bcp.processByComputerID).1 :: init'
	print _info
	logging.warning(_info)
	ioBeginTime('main_bcp.processByComputerID')
	if ( (str(rows.__class__).find('pyodbc.Cursor') > -1) or (str(rows.__class__).find('adodbapi.adodbapi.Cursor') > -1) ):
		#dataQueueConsumer(_data_queue)
		#processRowsThreaded(rows)
		try:
			while (_dbRunning):
				pass
				#processRowsThreaded(rows)
		except Exception, details:
			_info = '(main_bcp.processByComputerID).0 :: Error "%s".' % (str(details))
			print _info
			logging.warning(_info)
	_info = '(main_bcp.processByComputerID).2 :: _pool.join()!'
	print _info
	logging.warning(_info)
	_pool.join()
	_info = '(main_bcp.processByComputerID).3 :: _id_queue.join()!'
	print _info
	logging.warning(_info)
	_id_queue.join()
	ioEndTime('main_bcp.processByComputerID')

@threadpool.threadpool(_db_pool)
def queryByComputerID(id):
	sql = '%s AND (qr.computerid = %s)' % (SQL_STATEMENT_BY_ID,id)
	_info = '(%s) :: (main_bcp.queryByComputerID).1 :: sql=(%s)' % (sql)
	print _info
	logging.warning(_info)
	exec_and_process_sql(_mssql_connection_string3,sql,processByComputerID)

@threadpool.threadpool(_pool)
def handleComputerIDs(q):
	try:
		while (True):
			id = q.get()
			ioBeginTime('main_bcp.handleComputerIDs')
			_info = '(%s) :: (main_bcp.handleComputerIDs).1 :: id=(%s)' % (_id_queue.qsize(),id)
			print _info
			logging.warning(_info)
			queryByComputerID(id)
			q.task_done()
			ioEndTime('main_bcp.handleComputerIDs')
	except:
		pass

def processComputerIDs(rows):
	_info = '(main_bcp.processComputerIDs).1 :: init'
	print _info
	logging.warning(_info)
	ioBeginTime('main_bcp.processComputerIDs')
	if ( (str(rows.__class__).find('pyodbc.Cursor') > -1) or (str(rows.__class__).find('adodbapi.adodbapi.Cursor') > -1) ):
		handleComputerIDs(_id_queue)
		r = rows.fetchone()
		while (r):
			_id_queue.put(r[0])
			r = rows.fetchone()
	_info = '(main_bcp.processComputerIDs).2 :: _pool.join()!'
	print _info
	logging.warning(_info)
	_pool.join()
	_info = '(main_bcp.processComputerIDs).3 :: _id_queue.join()!'
	print _info
	logging.warning(_info)
	_id_queue.join()
	_info = '(main_bcp.processComputerIDs).4 :: _db_pool.join()!'
	print _info
	logging.warning(_info)
	_db_pool.join()
	ioEndTime('main_bcp.processComputerIDs')
	_info = '(main_bcp.processComputerIDs).5 :: _id_queue.qsize()=(%s)' % (_id_queue.qsize())
	print _info
	logging.warning(_info)
	reportTimeAnalysis('(main_bcp.processRows)')

def main_bcp(fname):
	_info = '(main_bcp).1'
	print _info
	logging.warning(_info)
	# data source is the local computer
	exec_and_process_sql(_mssql_connection_string3,SQL_STATEMENT,processRows)
	# data source is the katamari server
	#exec_and_process_sql(_mssql_connection_string3k,SQL_STATEMENT,processRows)

	#exec_and_process_sql_no_cursor(_mssql_connection_string3,SQL_STATEMENT,processRows_no_cursor)
	#exec_and_process_sql_ado(_mssql_connection_string,SQL_STATEMENT,processRows_no_cursor)
	#exec_and_process_sql_ado(_mssql_connection_string,SQL_STATEMENT,processRows)
	#exec_and_process_sql(_mssql_connection_string3,SQL_STATEMENT_ID_LIST,processComputerIDs)

if (os.path.exists(_resultsFolderName) == True):
	deleteAllFilesUnder(_resultsFolderName)

if (os.path.exists(_resultsFolderName) == False):
	os.mkdir(_resultsFolderName)

if (_resultsFolderName.endswith(os.sep) == False):
	_resultsFolderName += os.sep

print '(c). Copyright 2007-2008, Ray C Horn (raychorn@hotmail.com) and Hierarchical Applications Limited, Inc., All Rights Reserved.\n'
if ( (len(sys.argv) == 1) or (sys.argv[1] == '--help') ):
	print '--help                      ... displays this help text.'
	print '--verbose                   ... output more stuff.'
	print '--threaded=(2 to ?)         ... specify the number of threads in the pool.'
	print '--output=output_file_name   ... name of output file, usually Bigtest.txt or something like this.'
	print '--test=input_file_name      ... name of input file, usually Bigtest.txt or something like this.'
	print '--input=input_file_name     ... name of input file, usually Bigtest.txt or something like this.'
	print '--bcp=output_file_name      ... name of output file, usually Bigtest.txt or something like this.'
else:
	_fileName = 'Bigtest.txt'
	for i in xrange(len(sys.argv)):
		bool = ( (sys.argv[i].find('--output=') > -1) or (sys.argv[i].find('--test=') > -1) or (sys.argv[i].find('--input=') > -1) or (sys.argv[i].find('--bcp=') > -1) )
		if (bool): 
			toks = sys.argv[i].split('=')
			_fileName = toks[1]
		elif (sys.argv[i].find('--verbose') > -1):
			_isVerbose = True
		elif (sys.argv[i].find('--threaded') > -1):
			toks = sys.argv[i].split('=')
			if (toks[1].isdigit()):
				_isThreaded = int(toks[1])
				_pool = Pool(_isThreaded)
	if (_utils.getVersionNumber() >= 251):
		if (sys.argv[i].find('--output=') > -1):
			psyco.bind(main)
			_fileNum = 0
			main(_fileName)
		elif (sys.argv[i].find('--test=') > -1):
			psyco.bind(main_test)
			_fileNum = 0
			_rowCount = 0
			main_test(_fileName)
		elif (sys.argv[i].find('--input=') > -1):
			psyco.bind(main_read)
			_rowCount = 0
			main_read(_fileName)
		elif (sys.argv[i].find('--bcp=') > -1):
			psyco.bind(main_bcp)
			_fileNum = 0
			_rowCount = 0
			main_bcp(_fileName)
	else:
		print 'Try using Python Version 2.5.1 or later rather than verison "%s".' % sys.version_info
