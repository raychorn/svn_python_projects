import pyodbc
import logging

def exec_and_process_sql(cnnStr,sql,callback,useCommit=True,useClose=True):
	try:
		_dbh = pyodbc.connect(cnnStr)
		_cursor = _dbh.cursor()
		rows = _cursor.execute(sql)
		if (str(callback.__class__).find("'function'") > -1):
			try:
				callback(rows)
			except Exception, details:
				_info = '(exec_and_process_sql).1 :: Error in callback "%s".\ncnnStr=(%s)\nsql=(%s).\n' % (str(details),cnnStr,sql)
				print _info
				logging.warning(_info)
		if (useCommit):
			_dbh.commit()
		if (useClose):
			_dbh.close()
	except Exception, details:
		_info = '(exec_and_process_sql).2 :: Error "%s" cnnStr=(%s), sql=(%s).' % (str(details),cnnStr,sql)
		print _info
		logging.warning(_info)
