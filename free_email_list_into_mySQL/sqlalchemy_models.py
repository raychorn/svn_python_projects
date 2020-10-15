# http://www.sqlalchemy.org/docs/05/ormtutorial.html
import sys

from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.sql.sqlalchemy import SQLAgent

from sqlalchemy import types as sqltypes

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

import free_email_tables

####################################################################################################
## Notes: Eventually this module should become an object to allow for data to be cached for the
##        lifetime of the object - this reduces interactions with the database and speeds data access.
####################################################################################################

class FreeEmailHost(SQLAgent.BaseObject):
    pass

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()
if (_cname == 'undefined3'):
    conn_str = 'mysql://root:peekab00@sql2005:3306/molten_development'
elif (_cname == 'misha-lap.ad.magma-da.com'):
    conn_str = 'mysql://root:peekaboo@localhost:3306/free_email_list'

try:
    agent = SQLAgent.SQLAgent(conn_str,classObj=FreeEmailHost,tableDef=free_email_tables.freeemailhost__c)
except SQLAgent.sqlalchemy.exc.OperationalError, details:
    print >>sys.stderr, _utils.formattedException(details=details)

def insert_item(domain_name):
    host = FreeEmailHost(Domain__c=domain_name,IsActive__c=1)
    agent.add(host)

def viewing_items(callback=None):
    qry = agent.session.query(FreeEmailHost).filter("IsActive__c=:value").params(value=1).order_by("Domain__c ASC")
    items = []
    num_items = qry.count()
    one_percent = (num_items / 100)
    if (one_percent < 200):
        one_percent = 200
    num_items_part = one_percent if (num_items > 10000) else num_items
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

