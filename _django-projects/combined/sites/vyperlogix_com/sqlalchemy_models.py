# http://www.sqlalchemy.org/docs/05/ormtutorial.html
import sys

from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.sql.sqlalchemy import SQLAgent

from sqlalchemy import types as sqltypes

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

import freeemail_tables
import iso_tables

####################################################################################################
## Notes: Eventually this module should become an object to allow for data to be cached for the
##        lifetime of the object - this reduces interactions with the database and speeds data access.
####################################################################################################

class FreeEmailHost(SQLAgent.BaseObject):
    pass

class IsoCountries(SQLAgent.BaseObject):
    pass

class IsoStates(SQLAgent.BaseObject):
    pass

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()
conn_str2 = ''
if (_cname == 'undefined3'):
    pwd = keys._decode('7065656B61623030')
    conn_str = 'mysql://root:%s@sql2005:3306/freehosts' % (pwd)
    conn_str2 = 'mysql://root:%s@sql2005:3306/iso_data' % (pwd)
elif (_cname == 'web22.webfaction.com'):
    pwd = keys._decode('7065656B61623030')
    conn_str = 'mysql://raychorn_frehost:%s@localhost:3306/raychorn_frehost' % (pwd)
elif (_cname == 'misha-lap.ad.magma-da.com'):
    conn_str = 'mysql://root:peekaboo@localhost:3306/free_email_list'
elif (_cname in ['ubuntu.localdomain','ubuntu2.gateway.2wire.net']):
    pwd = keys._decode('7065656B61623030')
    conn_str = 'mysql://root:%s@sql2005.gateway.2wire.net:3306/freehosts' % (pwd)
    conn_str2 = 'mysql://root:%s@sql2005.gateway.2wire.net:3306/iso_data' % (pwd)

try:
    agent = SQLAgent.SQLAgent(conn_str,classObj=FreeEmailHost,tableDef=freeemail_tables.freeemailhost__c)
except SQLAgent.sqlalchemy.exc.OperationalError, details:
    print >>sys.stderr, _utils.formattedException(details=details)

try:
    agent_countries = SQLAgent.SQLAgent(conn_str2,classObj=IsoCountries,tableDef=iso_tables.country)
except SQLAgent.sqlalchemy.exc.OperationalError, details:
    print >>sys.stderr, _utils.formattedException(details=details)

try:
    agent_states = SQLAgent.SQLAgent(conn_str2,classObj=IsoStates,tableDef=iso_tables.states)
except SQLAgent.sqlalchemy.exc.OperationalError, details:
    print >>sys.stderr, _utils.formattedException(details=details)

def get_qry_by_parts(qry,callback=None):
    items = []
    try:
        num_items = qry.count()
        one_percent = (num_items / 100)
        if (one_percent < 200):
            one_percent = 200
        num_items_part = one_percent if (num_items > 10000) else num_items
        for i in xrange(num_items):
            item = SQLAgent.instance_as_SmartObject(qry[i])
            items.append(item)
            if (i > 0) and ((i % num_items_part) == 0):
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
    except Exception, details:
        print >>sys.stderr, _utils.formattedException(details=details)
    return items

def get_freehosts(callback=None):
    qry = agent.session.query(FreeEmailHost).filter("IsActive__c=:value").params(value=1).order_by("Domain__c ASC")
    items = get_qry_by_parts(qry,callback=callback)
    return items

def get_freehost_by_name(domain_name):
    qry = agent.session.query(FreeEmailHost).filter("IsActive__c=:value and Domain__c=:domain_name").params(value=1,domain_name=domain_name)
    items = get_qry_by_parts(qry)
    return items

def get_countries(callback=None):
    qry = agent_countries.session.query(IsoCountries).filter("iso3<>:value").params(value='USA').order_by("printable_name ASC")
    items = get_qry_by_parts(qry,callback=callback)
    qry2 = agent_countries.session.query(IsoCountries).filter("iso3=:value").params(value='USA').order_by("printable_name ASC")
    items2 = get_qry_by_parts(qry2,callback=callback)
    return items2+items

def get_states(callback=None):
    qry = agent_states.session.query(IsoStates).order_by("name ASC")
    items = get_qry_by_parts(qry,callback=callback)
    return items
