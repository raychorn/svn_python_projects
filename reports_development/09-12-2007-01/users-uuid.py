import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
import _mssql
import inspect
import pyodbc
import uuid
import time
from datetime import tzinfo, timedelta, datetime
from meta import *
from vyperlogix import *
from dbConnections import *

def iterateOverList(aList):
    i = 0
    for x in aList:
        print '(', i, ')=', x
        i += 1

def performFunc():
    version = sqlalchemy.__version__
    print 'version=', version

    _metadata = MetaData()
    _sessions_table = sessions_table.init_sessions_table(_metadata)
    _users_table = users_table.init_users_table(_metadata)

    handle = dbConnection_MSSQL()
    
    engine = handle[0]
    conn = handle[1]

    s = 'SELECT users.id, users.session_id, users.name, users.email, users.hashed_password, users.username, users.remember_token_expires_at, users.remember_token, users.salt, sessions.id AS sid, sessions.uuid FROM users LEFT OUTER JOIN sessions ON users.session_id = sessions.id'

    result = engine.execute(s)

    print 'result=', result

    row = result.fetchone()
    keys = row.keys()
    print 'row.__class__=', row.__class__, 'keys.__class__=', keys.__class__, 'len(keys)=', len(keys)
    #iterateOverList(keys)
    while (row):
        if  row.has_key('uuid'):
            print 'row.__getitem__(id)', row.__getitem__('id'), ', row.__getitem__(uuid)', row.__getitem__('uuid')
        row = result.fetchone()

    users_mapper = mapper(UserObj.UserObj, _users_table)

    sessions_mapper = mapper(SessionObj.SessionObj, _sessions_table)

    Session = sessionmaker(autoflush=True, transactional=True)
    sess = Session(bind=conn)
    d2 = sess.query(UserObj.UserObj)
    print 'sess.__class__=', sess.__class__
    print 'd2=', d2

    query = sess.query(users_mapper)
    x = query.filter(UserObj.UserObj.session_id==None).all()
    #x = query.all()

    print 'query.__class__=', query.__class__

    print 'x.__class__=', x.__class__, len(x)

    for k in range(len(x)):
        _userObj = x[k]
        print '_userObj.__class__=', _userObj.__class__
        print '\n#', k, '=', _userObj
        _conn = engine.connect()
        _uuid = str(uuid.uuid4())
        print '_uuid=', _uuid
        result = _conn.execute(_sessions_table.insert(), uuid=_uuid, theDate=datetime.today())
        print 'result=', str(result)
        result.close()
        _conn.close()
        _conn = engine.connect()
        _sqlStatement = _sessions_table.select('sessions.uuid=' + """'""" + _uuid + """'""")
        print '_sqlStatement.__class__=', _sqlStatement.__class__, '_sqlStatement=', _sqlStatement
        result2 = _conn.execute(_sqlStatement)
        print 'result2=', str(result2)
        row = result2.fetchone()
        print 'row=', str(row)
        print 'row.id=', row.id
        result.close()
        _conn.close()
        _userObj.session_id = row.id
        sess.save(_userObj)

        sess.commit()

#import cProfile
#cProfile.run('performFunc()')

performFunc()