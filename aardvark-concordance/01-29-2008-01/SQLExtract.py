import pyodbc
import logging
import traceback
from vyperlogix import decodeUnicode
from vyperlogix.aima import utils as aima_utils
from vyperlogix import utils
import types

#_columnNamesOfInterest = ['PublisherName', 'AppName']
_columnNamesOfInterest = []

_rows = []

__column_names = []

#_mssql_connection_string = 'DRIVER={SQL Server};SERVER=UNDEFINED2;DATABASE=ExpressDB;CommandTimeout=0;UID=sa;PWD=peekaboo'
_mssql_connection_string = 'DRIVER={SQL Server};SERVER=MURRE\\DEV2005;DATABASE=ExpressDB;CommandTimeout=0;UID=sa;PWD=peekaboo'

#_mssql_connection_string2 = 'DRIVER={SQL Server};SERVER=UNDEFINED2;DATABASE=aardvark_cw;CommandTimeout=0;UID=sa;PWD=peekaboo'
_mssql_connection_string2 = 'DRIVER={SQL Server};SERVER=MURRE\\DEV2005;DATABASE=aardvark_cw;CommandTimeout=0;UID=sa;PWD=peekaboo'

_publishers_apps_symbol = 'express_metrix_publishers_apps'
_publishers_arps_symbol = 'aardvark_publishers_arps'

SQL_STATEMENTS = {}
SQL_STATEMENTS[_publishers_apps_symbol] = [_mssql_connection_string,"SELECT kbmanufacturer.name as PublisherName, kbapps.name AS AppName FROM kbmanufacturer LEFT OUTER JOIN kbapps ON kbmanufacturer.manufacturerid = kbapps.manufacturerid ORDER BY AppName"]
SQL_STATEMENTS[_publishers_arps_symbol] = [_mssql_connection_string2,"SELECT publishers.name AS PublisherName, packages.name AS PackageName FROM publishers LEFT OUTER JOIN packages ON publishers.app_dictionary_id = packages.app_dictionary_id"]

def exec_and_fetch_sql(_cnnStr,_sql):
	try:
		_aardvark_dbh = pyodbc.connect(_cnnStr)
		_cursor = _aardvark_dbh.cursor()
		_cursor.execute(_sql)
		row = _cursor.fetchone()
		_aardvark_dbh.close()
		return row
	except Exception, details:
		_traceBack = traceback.format_exc()
		print '(exec_and_fetch_sql) :: Error "%s" _cnnStr=(%s), _sql=(%s).\n%s' % (str(details),_cnnStr,_sql,_traceBack)
	return None

def exec_and_process_sql(_cnnStr,_sql,_callback):
	try:
		print '(exec_and_process_sql) :: connect()'
		_aardvark_dbh = pyodbc.connect(_cnnStr)
		_cursor = _aardvark_dbh.cursor()
		print '(exec_and_process_sql) :: execute()'
		rows = _cursor.execute(_sql)
		try:
			_callback(rows)
		except Exception, details:
			_info = '(exec_and_process_sql).1 :: Error "%s" _cnnStr=(%s), _sql=(%s).' % (str(details),_cnnStr,_sql)
			print _info
			logging.warning(_info)
		_aardvark_dbh.close()
	except Exception, details:
		_traceBack = traceback.format_exc()
		_info = '(exec_and_process_sql).2 :: Error "%s" _cnnStr=(%s), _sql=(%s).\n%s' % (str(details),_cnnStr,_sql,_traceBack)
		print _info
		logging.warning(_info)

def exec_and_process_sql_no_cursor(_cnnStr,_sql,_callback):
	try:
		_aardvark_dbh = pyodbc.connect(_cnnStr)
		rows = _aardvark_dbh.execute(_sql)
		try:
			_callback(rows)
		except Exception, details:
			_info = '(exec_and_process_sql_no_cursor).1 :: Error "%s" _cnnStr=(%s), _sql=(%s).' % (str(details),_cnnStr,_sql)
			print _info
			logging.warning(_info)
		_aardvark_dbh.close()
	except Exception, details:
		_traceBack = traceback.format_exc()
		_info = '(exec_and_process_sql_no_cursor).2 :: Error "%s" _cnnStr=(%s), _sql=(%s).\n%s' % (str(details),_cnnStr,_sql,_traceBack)
		print _info
		logging.warning(_info)

def rowDictFromRowObj(row,cols):
	_row = {}
	i = 0
	for c in cols:
		_row[c[0]] = row[i]
		i += 1
	return _row

def processRow(row,cols):
	try:
		_row = rowDictFromRowObj(row,cols)
		#print '_row=(%s)' % str(_row)
		if (len(_columnNamesOfInterest) > 0):
			_rows.append('\t\t'.join([decodeUnicode.decodeUnicode(_row[colName]) for colName in _columnNamesOfInterest]))
		else:
			_rows.append('\t\t'.join([decodeUnicode.decodeUnicode(_row[t[0]]) if t[1] == types.UnicodeType else _row[t[0]] for t in cols]))
		if ((len(_rows) % 1000) == 0):
			_info = '(main.processRowThreaded).1 :: len(_rows)=(%s)' % (len(_rows))
			print _info
	except Exception, details:
		_traceBack = traceback.format_exc()
		_info = '(main.processRows).0 :: Error "%s".\n%s' % (str(details),_traceBack)
		print _info
		logging.warning(_info)

def processRows(rows):
	if (isinstance(rows,pyodbc.Cursor)):
		try:
			r = rows.fetchone()
			column_names = [ t[0] for t in r.cursor_description]
			if (len(__column_names) == 0):
				for n in column_names:
					__column_names.append('"%s"' % n)
			columns = [ t for t in r.cursor_description]
			print '(processRows) :: column_names=(%s)' % column_names
			print '(processRows) :: columns=(%s)' % columns
			while (r):
				processRow(r,columns)
				r = rows.fetchone()
		except Exception, details:
			_traceBack = traceback.format_exc()
			_info = '(main.processRows).0 :: Error "%s".\n' % (str(details),_traceBack)
			print _info
			logging.warning(_info)

def saveToFileNamed(records, fname):
	try:
		records = aima_utils.unique(records)
	except:
		try:
			records = utils.unique(records)
		except:
			pass
	records.sort()
	if (len(_columnNamesOfInterest) > 0):
		records.insert(0,'\t\t'.join(_columnNamesOfInterest))
	else:
		records.insert(0,'\t\t'.join(__column_names))
	fHand = open(fname, 'w')
	for n in records:
		fHand.write('%s\n' % n)
	fHand.flush()
	fHand.close()

def main():
	global _rows

	print '(main) :: BEGIN:'
	for k,v in SQL_STATEMENTS.iteritems():
		_rows = []
		print '_rows=(%s)' % str(_rows)
		exec_and_process_sql(v[0],v[1],processRows)
		saveToFileNamed(_rows, '#%s.txt' % k)

	print '(main) :: END !'

if (__name__ == '__main__'):
	import psyco
	psyco.full()
	main()
	