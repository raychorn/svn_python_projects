import sys

from vyperlogix import misc
from vyperlogix.misc import _utils

from sqlalchemy.exc import OperationalError
from vyperlogix.sql.sqlalchemy.SQLAgent import BaseObject
from vyperlogix.sql.sqlalchemy.SQLAgent import SQLAgent
from vyperlogix.sql.sqlalchemy.SQLAgent import SQLAgentMultiSession

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import types as sqltypes

metadata = MetaData()
node_table = Table('views_node', metadata,
                    Column('id', sqltypes.Integer, nullable=False, default=0, primary_key=True),
                    Column('name', sqltypes.String(128), nullable=False),
                    Column('parent', sqltypes.Integer, nullable=True),
                    Column('creation_date', sqltypes.DateTime, nullable=False),
                    Column('modification_date', sqltypes.DateTime, nullable=False),
                    Column('is_active', sqltypes.Boolean, nullable=False),
                    Column('is_url', sqltypes.Boolean, nullable=False),
                    Column('is_file', sqltypes.Boolean, nullable=False)
)

class Node(BaseObject):
    pass

default_date = lambda dt:dt if (dt is not None) else _utils.timeStampLocalTime()

def get_conn_str(logger=sys.stderr):
    import socket
    _cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()
    print >>logger, 'Computer Name is "%s".' % (_cname)
    if (_cname == 'web22.webfaction.com'):
        _is_running_local = False
        conn_str = 'mysql://raychorn_resourc:peekab00@localhost:3306/raychorn_resourc'
    elif (_cname in ['undefined3']):
        _is_running_local = False
        conn_str = 'mysql://root:peekab00@sql2005:3306/resources2'
    elif (_cname in ['sql2005.halsmalltalker.com']):
        _is_running_local = False
        conn_str = 'mysql://root:peekab00@sql2005:3306/resources'
    elif (_cname == 'misha-lap.ad.magma-da.com'):
        conn_str = 'mysql://root:peekaboo@localhost:3306/resources'
    else:
        print >>logger, '%s :: NOTHING TO DO !' % (misc.funcName())
        sys.exit(1)
    print >>logger, 'Connection String is "%s".' % (conn_str)
    return conn_str

def get_sql_agent(conn_str,logger=sys.stderr):
    try:
        agent = SQLAgentMultiSession(conn_str,Node,node_table)
    except OperationalError, details:
        print >>logger, _utils.formattedException(details=details)
        sys.exit(1)
    return agent
