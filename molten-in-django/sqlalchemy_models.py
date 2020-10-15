# http://www.sqlalchemy.org/docs/05/ormtutorial.html
import sys

from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.enum import Enum

from vyperlogix.sql.sqlalchemy import SQLAgent

from sqlalchemy import types as sqltypes

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

import molten_tables

class AccessMethods(Enum.Enum):
    none = 2**0
    local = 2**1
    tunnel = 2**2

####################################################################################################
## Notes: Eventually this module should become an object to allow for data to be cached for the
##        lifetime of the object - this reduces interactions with the database and speeds data access.
####################################################################################################

class Viewing(SQLAgent.BaseObject):
    pass

class Cases(SQLAgent.BaseObject):
    pass

class Accounts(SQLAgent.BaseObject):
    pass

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()
if (_cname == 'undefined3'):
    conn_str = 'mysql://root:peekab00@sql2005:3306/molten_development'
elif (_cname in ['rhorn-lap.ad.magma-da.com']):
    conn_str = 'mysql://root:peekaboo@localhost:3306/molten_development'
elif (_cname in ['rhorn2-srv.ad.magma-da.com']):
    conn_str = 'mysql://root:peekab00@localhost:3306/molten_development'
elif (_cname in ['molten1.magma-da.com','molten2.magma-da.com','molten3.magma-da.com','tide.magma-da.com']):
    conn_str = 'mysql://molten2:2molten@localhost:3306/molten_production'
else:
    print 'ERROR: Cannot figure-out what to do with the computer named "%s".' % (_cname)
    sys.exit(1)

try:
    agent = SQLAgent.SQLAgent(conn_str)
except SQLAgent.sqlalchemy.exc.OperationalError, details:
    print >>sys.stderr, _utils.formattedException(details=details)

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

def viewing_items(callback=None):
    agent.add_mapper(Viewing,molten_tables.viewing)
    qry = agent.session.query(Viewing).order_by("viewable_type ASC") #.all()
    items = []
    num_items = qry.count()
    num_items_part = num_items / 100
    for i in xrange(num_items):
        item = SQLAgent.instance_as_SmartObject(qry[i])
        items.append(item)
        if (i > 0) and ((i % num_items_part) == 0):
            print '%d of %d.' % (i,num_items)
            if (callable(callback)):
                try:
                    callback(items)
                finally:
                    items = []
    if (len(items) > 0):
        if (callable(callback)):
            try:
                callback(items)
            finally:
                items = []
    return items

def get_accounts_for_toshiba():
    agent.add_mapper(Accounts,molten_tables.sfaccount)
    accounts = agent.session.query(Accounts).filter(Accounts.name.like('%Toshiba%')).all()
    return accounts
    
def get_cases_for_toshiba(account_id):
    from sqlalchemy import and_
    from sqlalchemy import or_
    
    agent.add_mapper(Cases,molten_tables.sfcase)
    items = agent.session.query(Cases).filter(Cases.account_id == account_id).filter(Cases.is_closed == None).all() # .filter(or_(Cases.is_deleted == None,Cases.is_deleted == 'False'))
    return items

def get_case_by_id(id,session=agent.session):
    agent.add_mapper(Cases,molten_tables.sfcase)
    items = session.query(Cases).filter(Cases.sf_id == id).all()
    return items
