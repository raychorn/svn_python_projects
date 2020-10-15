import psyco
import pyodbc
import logging
import traceback

# Concordance
_columnNameOfInterest = ''

_rows = []

#_mssql_connection_string = 'DRIVER={SQL Server};SERVER=UNDEFINED2;DATABASE=aardvark_cw;CommandTimeout=0;UID=sa;PWD=peekaboo'
_mssql_connection_string = 'DRIVER={SQL Server};SERVER=MURRE\\DEV2005;DATABASE=aardvark_cw;CommandTimeout=0;UID=sa;PWD=peekaboo'

_unknown_packages_symbol = 'unknown_packages'
_packages_symbol = 'packages'
_publishers_symbol = 'publishers'

SQL_STATEMENTS = {}
SQL_STATEMENTS[_publishers_symbol] = "SELECT id, app_dictionary_id, name, dont_care FROM dbo.publishers"
SQL_STATEMENTS[_packages_symbol] = "SELECT id, app_dictionary_id, software_title_version_id, name, dont_care FROM dbo.packages"
SQL_STATEMENTS[_unknown_packages_symbol] = "SELECT id, name, instances FROM dbo.unknown_packages"

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
		print '_row=(%s)' % str(_row)
		_rows.append(_row[_columnNameOfInterest])
		if ((len(_rows) % 100) == 0):
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

def makeUnique(_items):
	unique = {}
	for item in _items:
		if (not unique.has_key(item)):
			unique[item] = item
	_items = unique.keys()
	_items.sort()
	return _items

def saveToFileNamed(_list, fname):
	_list = makeUnique(_list)
	fHand = open(fname, 'w')
	fHand.writelines(['%s\n' % n for n in _list])
	fHand.flush()
	fHand.close()

def main():
	global _rows
	global _columnNameOfInterest

	print '(main) :: BEGIN:'
	_rows = []
	_columnNameOfInterest = 'name'
	exec_and_process_sql(_mssql_connection_string,SQL_STATEMENTS[_unknown_packages_symbol],processRows)
	saveToFileNamed(_rows, '#%s.txt' % _unknown_packages_symbol)

	_rows = []
	_columnNameOfInterest = 'name'
	exec_and_process_sql(_mssql_connection_string,SQL_STATEMENTS[_packages_symbol],processRows)
	saveToFileNamed(_rows, '#%s.txt' % _packages_symbol)

	_rows = []
	_columnNameOfInterest = 'name'
	exec_and_process_sql(_mssql_connection_string,SQL_STATEMENTS[_publishers_symbol],processRows)
	saveToFileNamed(_rows, '#%s.txt' % _publishers_symbol)

	print '(main) :: END !'

if (__name__ == '__main__'):
	psyco.bind(main)
	main()
	