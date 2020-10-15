# http://www.sqlalchemy.org/docs/05/ormtutorial.html
import sys

from django.conf import settings

from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.sql.sqlalchemy import SQLAgent

from sqlalchemy import types as sqltypes

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

import data_tables

import djangoTables

####################################################################################################
## Notes: Eventually this module should become an object to allow for data to be cached for the
##        lifetime of the object - this reduces interactions with the database and speeds data access.
####################################################################################################

class GeotaggerSample1(SQLAgent.BaseObject):
    pass

class GPS_1M(SQLAgent.BaseObject):
    pass

class SampleHeatMapData(SQLAgent.BaseObject):
    pass


import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()

conn_geotaggerSample1 = 'mysql://%s:%s@%s:%s/geotagger_sample1' % ('root','peekab00','127.0.0.1',3306)
conn_gps1M = 'mysql://%s:%s@%s:%s/geotagger_sample1' % ('root','peekab00','127.0.0.1',3306)

conn_geotaggerTarget1 = 'mysql://%s:%s@%s:%s/django-heat-maps-prototype' % ('root','peekab00','127.0.0.1',3306)

try:
    agent_geotaggerSample1 = SQLAgent.SQLAgent(conn_geotaggerSample1,classObj=GeotaggerSample1,tableDef=data_tables.geotagger_sample1_table,non_primary=False)
except SQLAgent.sqlalchemy.exc.OperationalError, details:
    print >>sys.stderr, _utils.formattedException(details=details)

try:
    agent_gps1M = SQLAgent.SQLAgent(conn_gps1M,classObj=GPS_1M,tableDef=data_tables.gps1M_table,non_primary=False)
except SQLAgent.sqlalchemy.exc.OperationalError, details:
    print >>sys.stderr, _utils.formattedException(details=details)

try:
    agent_SampleHeatMapData = SQLAgent.SQLAgent(conn_geotaggerTarget1,classObj=SampleHeatMapData,tableDef=djangoTables.smithmicro_sampleheatmapdata,non_primary=False)
except SQLAgent.sqlalchemy.exc.OperationalError, details:
    print >>sys.stderr, _utils.formattedException(details=details)

def get_qry_by_parts(qry,callback=None,step_by=None):
    items = []
    try:
        num_items = qry.count()
        try:
            one_percent = int(num_items / (100 if (not step_by) else step_by))
        except:
            one_percent = int(num_items / 100)
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

def get_samples_by_interation(callback=None,step_by=1000):
    qry = agent_geotaggerSample1.session.query(DataSamples).filter("heat_lat=:value").params(value=49).order_by("heat_lat ASC")
    items = get_qry_by_parts(qry,callback=callback,step_by=step_by)
    return items

def get_samples_qry():
    #qry = agent_geotaggerSample1.session.query(GeotaggerSample1).filter("heat_lat=:value").params(value=49).order_by("heat_lat ASC")
    qry = agent_geotaggerSample1.session.query(GeotaggerSample1).filter_by(heat_lat=49, heat_lng=2) 
    return qry

def get_gps1M_qry():
    #qry = agent_geotaggerSample1.session.query(GPS_1M).filter("heat_lat=:value").params(value=49).order_by("heat_lat ASC")
    qry = agent_gps1M.session.query(GPS_1M) 
    return agent_gps1M.session,qry

