import sqlalchemy
import pyodbc
from vyperlogix import *
from sqlalchemy import *
import _mysql
from sqlalchemy.orm import *

_pwd = UnObscurePhrase.UnObscurePhrase('\xf3\xe9\xf3\xeb\xef\xc0\xb7\xb6\xb6\xb0\xa4\xe2\xef\xef')

def connectMSSQL1():
    return pyodbc.connect('DRIVER={SQL Server};SERVER=UNDEFINED2\SQLEXPRESS;DATABASE=reports_development;UID=sa;PWD=' + _pwd)

def connectMSSQL2():
    return pyodbc.connect('DRIVER={SQL Server};SERVER=MURRE\SQLEXPRESS;DATABASE=reports_development;UID=sa;PWD=' + _pwd)

_mssql_connection_string = ''
_mysql_connection_string = ''

def connectMSSQLDynamic():
    print 'connectMSSQLDynamic() :: _mssql_connection_string=(%s)' % _mssql_connection_string
    return pyodbc.connect(_mssql_connection_string)

def dbConnection_MSSQLDynamic():
    try:
        engine = create_engine('mssql://', creator=connectMSSQLDynamic)
        print 'engine=', engine
        conn = engine.connect()
        print 'conn=', conn
    except Exception, details:
        print 'ERROR in "dbConnection_MSSQLDynamic" due to (%s)' % str(details)
    return(engine,conn)

def dbConnection_mySQLDynamic(connect_string):
    try:
        engine = create_engine(connect_string)
        print 'engine=', engine
        conn = engine.connect()
        print 'conn=', conn
    except Exception, details:
        print 'ERROR in "dbConnection_mySQLDynamic" due to (%s)' % str(details)
    return(engine,conn)

def dbConnectionFromYML(ymlObject):
    global _mssql_connection_string
    global _mysql_connection_string
    _adapter = ymlObject.attrValueForName('adapter')
    if (_adapter.find('mssql') > -1):
        _dsn = ymlObject.attrValueForName('dsn')
        if (len(_dsn) > 0):
            _mssql_connection_string = 'DSN=%s' % (_dsn)
        else:
            _driver = ymlObject.attrValueForName('driver')
            _server = ymlObject.attrValueForName('server')
            _database = ymlObject.attrValueForName('database')
            _uid = ymlObject.attrValueForName('uid')
            _pwd = UnObscurePhrase.UnObscurePhrase(ymlObject.attrValueForName('pwd'))
            _mssql_connection_string = 'DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (_driver,_server,_database,_uid,_pwd)
        print '_mssql_connection_string=[%s]' % _mssql_connection_string
        return dbConnection_MSSQLDynamic()
    elif (_adapter.find('mysql') > -1):
        _database = ymlObject.attrValueForName('database')
        _username = ymlObject.attrValueForName('username')
        _password = ymlObject.attrValueForName('password')
        _host = ymlObject.attrValueForName('host')
        _mysql_connection_string = '%s://%s:%s@%s/%s' % (_adapter,_username,_password,_host,_database)
        print '_mysql_connection_string=[%s]' % _mysql_connection_string
        return dbConnection_mySQLDynamic(_mysql_connection_string)
    return None
    
def dbConnection_MSSQL():
    try:
        engine = create_engine('mssql://', creator=connectMSSQL1)
        print 'engine=', engine
        conn = engine.connect()
        print 'conn=', conn
    except Exception:
        engine = create_engine('mssql://', creator=connectMSSQL2)
        print 'engine=', engine
        conn = engine.connect()
        print 'conn=', conn
    return(engine,conn)

def dbConnection_mySQL():
    try:
        engine = create_engine('mysql://root:foobarbaz@192.168.105.67/reports_development')
        print 'engine=', engine
        conn = engine.connect()
        print 'conn=', conn
    except Exception:
        engine = create_engine('mysql://root:peekaboo@127.0.0.1/reports_development')
        print 'engine=', engine
        conn = engine.connect()
        print 'conn=', conn
    return(engine,conn)

def dbConnection_mySQL2():
    try:
        engine = create_engine('mysql://root:peekaboo@localhost/reports_development')
        print 'engine=', engine
        conn = engine.connect()
        print 'conn=', conn
        return(engine,conn)
    except Exception:
        print 'ERROR - Cannot create a connection !'
    return None
