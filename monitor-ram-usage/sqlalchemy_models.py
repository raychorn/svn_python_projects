# http://www.sqlalchemy.org/docs/05/ormtutorial.html
import sys

from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.enum import Enum

from vyperlogix.sql.sqlalchemy import SQLAgent

from sqlalchemy import types as sqltypes

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

import monitor_tables

####################################################################################################
## Notes: Eventually this module should become an object to allow for data to be cached for the
##        lifetime of the object - this reduces interactions with the database and speeds data access.
####################################################################################################

class PS_Aux(SQLAgent.BaseObject):
    pass

class Source(SQLAgent.BaseObject):
    pass

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()
if (_cname == 'undefined3'):
    conn_str = 'mysql://root:peekab00@sql2005:3306/monitor'
elif (_cname in ['rhorn-lap.ad.magma-da.com']):
    conn_str = 'mysql://root:peekaboo@localhost:3306/monitor'
elif (_cname in ['rhorn2-srv.ad.magma-da.com']):
    conn_str = 'mysql://root:peekab00@localhost:3306/monitor'
elif (_cname in ['molten1.magma-da.com','molten2.magma-da.com','molten3.magma-da.com','tide.magma-da.com']):
    conn_str = 'mysql://molten2:2molten@localhost:3306/monitor'
elif (_cname in ['tide2.magma-da.com']):
    conn_str = 'mysql://tide:tide123@mysqldb.magma-da.com:3313/monitor'
else:
    print 'ERROR: Cannot figure-out what to do with the computer named "%s".' % (_cname)
    sys.exit(1)

parse_port_from_conn_str = lambda s:s.split('://')[-1].split('/')[0].split(':')[-1]

def get_conn_str(port=None):
    c = conn_str
    if (port is not None):
        _port = parse_port_from_conn_str(c)
        port = parse_port_from_conn_str(str(port))
        c = c.replace(':%s' % (_port),':%s' % (port))
    return c

def new_agent(connStr):
    try:
        agent = SQLAgent.SQLAgent(connStr)
    except SQLAgent.sqlalchemy.exc.OperationalError, details:
        print >>sys.stderr, _utils.formattedException(details=details)
    return agent

