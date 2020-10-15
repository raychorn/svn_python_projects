# http://www.sqlalchemy.org/docs/05/ormtutorial.html
import sys

from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.classes.CooperativeClass import Cooperative

from vyperlogix.sql.sqlalchemy import SQLAgent

from sqlalchemy import types as sqltypes

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

import pypi_tables

####################################################################################################
## Notes: Eventually this module should become an object to allow for data to be cached for the
##        lifetime of the object - this reduces interactions with the database and speeds data access.
####################################################################################################

class Classifiers(SQLAgent.BaseObject):
    pass

class PackageClassifiers(SQLAgent.BaseObject):
    pass

class Packages(SQLAgent.BaseObject):
    #__model__ = pypi_tables.packages
    #cols = __model__.columns.keys()
    
    def __init__(self, *args, **kwargs):
        super(Packages, self).__init__(*args, **kwargs)

    def __getitem__(self, name):
        return getattr(self,name)
        
    def __setitem__(self,name,value):
        setattr(self,name,value)
        
import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()

conn_str = ''
if (_cname == 'undefined3'):
    conn_str = 'mysql://root:peekab00@sql2005:3307/pypi_packages'
elif (_cname in ['ubuntu4.web20082']):
    conn_str = 'mysql://root:peekab00@localhost:3306/pypi_packages'
else:
    print 'ERROR: Cannot figure-out what to do with the computer named "%s".' % (_cname)
    sys.exit(1)

try:
    agent = SQLAgent.SQLAgent(conn_str)
except SQLAgent.sqlalchemy.exc.OperationalError, details:
    print >>sys.stderr, _utils.formattedException(details=details)

def new_agent(connStr):
    try:
        agent = SQLAgent.SQLAgent(connStr)
    except SQLAgent.sqlalchemy.exc.OperationalError, details:
        print >>sys.stderr, _utils.formattedException(details=details)
    agent.add_mapper(Packages,pypi_tables.packages)
    agent.add_mapper(PackageClassifiers,pypi_tables.package_classifiers)
    agent.add_mapper(Classifiers,pypi_tables.classifiers)
    return agent

def get_packages(agent):
    pkgs = agent.session.query(Packages).order_by("name").all()
    return pkgs

def get_package_by_name(agent,name):
    pkgs = agent.session.query(Packages).filter("name='%s'" % (name)).order_by("name").all()
    return pkgs

def get_package_classifiers_by_pid(agent,pid):
    package_classifiers = agent.session.query(PackageClassifiers).filter("pid=%d" % (pid)).all()
    return package_classifiers

def put_package_classifier_for_cid_pid(cid,pid):
    agent = new_agent(conn_str)
    aPackageClassifier = PackageClassifiers(cid=cid,pid=pid)
    agent.beginTransaction()
    agent.add(aPackageClassifier)
    agent.commit()
    return agent.lastError

def get_package_classifiers_for_package_by_name(agent,name):
    pkgs = get_package_by_name(agent,name)
    pkg = pkgs[0] if (len(pkgs) > 0) else None
    if (pkg is not None):
        return get_package_classifiers_by_pid(agent,pkg.id)
    return []

def get_classifier_by_name(agent,classifier):
    classifiers = agent.session.query(Classifiers).filter("classifier='%s'" % (classifier)).order_by("classifier").all()
    return classifiers

def put_classifiers_for_package_by_name(agent,name,classifiers):
    pkgs = get_package_by_name(agent,name)
    pkg = pkgs[0] if (len(pkgs) > 0) else None
    if (pkg is not None):
        for classifier in classifiers:
            klassifiers = get_classifier_by_name(agent,classifier)
            for klassifier in klassifiers:
                last_error = put_package_classifier_for_cid_pid(cid=klassifier.id,pid=pkg.id)
                if (len(last_error) > 0):
                    return last_error
    return ''

def insert_new_classifier(classifier):
    agent = new_agent(conn_str)
    agent.beginTransaction()
    agent.add(classifier)
    agent.commit()
    agent.close()
    return agent.lastError

