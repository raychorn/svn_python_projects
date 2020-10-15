import uuid

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.classes.SmartObject import PyroSmartObject as SmartObject2
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc.ObjectTypeName import __typeName as ObjectTypeName__typeName

from vyperlogix.classes.CooperativeClass import Cooperative

import sqlalchemy

assert (any([sqlalchemy.__version__.find(v) > -1 for v in ['0.5.3','0.5.8','0.5.4p2','0.7.1']])), '%s :: Oops, wrong version of SQLAlchemy, expected 0.5.3 or 0.5.4p2 but got "%s".' % (__file__,sqlalchemy.__version__)

from sqlalchemy import create_engine

from sqlalchemy.orm import mapper, relation, create_session, clear_mappers

from sqlalchemy.orm import sessionmaker

def instance_as_SmartObject(item):
    '''This function fails from time to time so fix it !'''
    from vyperlogix.classes.SmartObject import PyroSmartObject as SmartObject
    d = lists.HashedLists2(dict([(k,v) for k,v in item.__dict__.iteritems() if (not ObjectTypeName.type_is_class(v))]))
    return SmartObject(d)

class BaseObject(object):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
	    
    def __str__(self):
	info = []
	for k,v in self.__dict__.iteritems():
	    if (k != '_sa_instance_state'):
		info.append('%s --> %s' % (_utils.ascii_only(k),_utils.ascii_only(v)))
		ch = '\n' if (len(info) > 10) else ', '
	return '(%s) %s' % (ObjectTypeName__typeName(self),ch.join(info))

class SQLAgent(Cooperative):
    def __init__(self,connection_string,classObj=None,tableDef=None,autoflush=True,autocommit=True,isMultiSession=False,non_primary=False):
        '''Usage: connection_string = "mysql://root:password-goes-here@server-name=goes-here:3306/database-name-goes-here"
        http://www.sqlalchemy.org/docs/05/ormtutorial.html
        '''
	self.__isMultiSession__ = isMultiSession
	self.__non_primary__ = non_primary
	self.__autoflush__ = autoflush
	self.__autocommit__ = autocommit
	self.__engine__ = create_engine(connection_string, pool_size=20, max_overflow=0)
        self.__classObj__ = classObj
        self.__tableDef__ = tableDef
	self.__agents = lists.HashedLists2()
	self.__mappers = []
        self.__mapper__ = mapper(self.__classObj__, self.__tableDef__, non_primary=non_primary) if (self.__classObj__ is not None) and (self.__tableDef__ is not None) else None
	if (self.__mapper__ is not None):
	    self.__mappers.append(self.__mapper__)
	self.__session__ = None
	if (not self.__isMultiSession__):
	    self.new_session()
        self.__lastError__ = ''
	
    def asSmartObjects(self,items):
	self.__lastError__ = ''
	recs = []
	try:
	    for item in items:
		d = {}
		try:
		    for key in item.keys():
			obj = item.__getattribute__(key)
			d[key] = instance_as_SmartObject(obj)
		    recs.append(SmartObject2(d))
		except AttributeError:
		    recs.append(instance_as_SmartObject(item))
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
	return recs
        
    def add_mapper(self,cls, tbl, properties={}, **kwargs):
	self.__lastError__ = ''
	try:
	    if (self.agents[cls] is None):
		_mapper = mapper(cls, tbl, properties=properties, **kwargs) if (cls is not None) and (tbl is not None) else None
		if (_mapper is not None):
		    self.__mappers.append(_mapper)
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
	    
    def new_session(self):
	Session = sessionmaker()
	Session.configure(bind=self.__engine__,autoflush=self.autoflush,autocommit=self.autocommit)
	self.__session__ = Session()
    
    def add(self,obj):
	self.__lastError__ = ''
        try:
            self.session.add(obj)
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
	    
    def update(self,obj):
	self.__lastError__ = ''
        try:
            self.session.update(obj)
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
	    
    def delete(self,obj):
	self.__lastError__ = ''
        try:
            self.session.delete(obj)
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
	    
    def commit(self):
	self.__lastError__ = ''
        try:
            self.session.commit()
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
    
    def beginTransaction(self):
	self.__lastError__ = ''
        try:
            self.session.begin()
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
    
    def flush(self):
	self.__lastError__ = ''
        try:
            self.session.flush()
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
    
    def close(self):
	self.__lastError__ = ''
        try:
            self.session.close()
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
    
    def all(self):
        '''Usage: l_records = agent.all()
        l = [r for r in l_records if (r.id == 1)]
        '''
	self.__lastError__ = ''
        try:
	    return self.session.query(self.classObj).all()
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
	return []
    
    def query(self,lamda_clause):
        '''lamda_clause can be a lamda or function that accepts one argument that is the classObj that was passed-in when this object was created.
        l = agent.query_all(lambda cls:cls.id == 1)
        l = agent.query(lambda cls:cls.id == 1).all()
        l = agent.session.query(Node).filter("id>=1").order_by("id").all()
        >>> agent.session.query(User).filter("id<:value and name=:name").params(value=224, name='fred').order_by(User.id).one()
        >>> session.query(User).from_statement("SELECT * FROM users where name=:name").params(name='ed').all()
        query.filter(User.name == 'ed')
        query.filter(User.name != 'ed')
        query.filter(User.name.like('%ed%'))
        query.filter(User.name.in_(['ed', 'wendy', 'jack']))
        filter(User.name == None)
        from sqlalchemy import and_
        filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))
        from sqlalchemy import or_
        filter(or_(User.name == 'ed', User.name == 'wendy'))
        query.filter(User.name.match('wendy'))
        query.first()
        sql>>> try:  
        ...     user = query.one() 
        ... except Exception, e: 
        ...     print e
        Multiple rows were found for one()
        
        sql>>> try:
        ...     user = query.filter(User.id == 99).one() 
        ... except Exception, e: 
        ...     print e
        No row was found for one()
        sql>>> for user in session.query(User).filter("id<224").order_by("id").all():
        ...     print user.name
        '''
	self.__lastError__ = ''
        try:
	    if (callable(lamda_clause)):
		return self.session.query(self.classObj).filter(lamda_clause(self.classObj))
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
        return []

    def query_all(self,lamda_clause):
        '''lamda_clause can be a lamda or function that accepts one argument that is the classObj that was passed-in when this object was created.
        l = agent.query_all(lambda cls:cls.id == 1)
        >>> agent.session.query(User).filter("id<:value and name=:name").params(value=224, name='fred').order_by(User.id).one()
        >>> session.query(User).from_statement("SELECT * FROM users where name=:name").params(name='ed').all()
        query.filter(User.name == 'ed')
        query.filter(User.name != 'ed')
        query.filter(User.name.like('%ed%'))
        query.filter(User.name.in_(['ed', 'wendy', 'jack']))
        filter(User.name == None)
        from sqlalchemy import and_
        filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))
        from sqlalchemy import or_
        filter(or_(User.name == 'ed', User.name == 'wendy'))
        query.filter(User.name.match('wendy'))
        query.first()
        sql>>> try:  
        ...     user = query.one() 
        ... except Exception, e: 
        ...     print e
        Multiple rows were found for one()
        
        sql>>> try:
        ...     user = query.filter(User.id == 99).one() 
        ... except Exception, e: 
        ...     print e
        No row was found for one()
        sql>>> for user in session.query(User).filter("id<224").order_by("id").all():
        ...     print user.name
        '''
	self.__lastError__ = ''
        try:
	    if (callable(lamda_clause)):
		return self.query(lamda_clause).all()
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
        return []

    def query_one(self,lamda_clause):
        '''lamda_clause can be a lamda or function that accepts one argument that is the classObj that was passed-in when this object was created.
        sql>>> try:  
        ...     user = query.one() 
        ... except Exception, e: 
        ...     print e
        Multiple rows were found for one()
        
        sql>>> try:
        ...     user = query.filter(User.id == 99).one() 
        ... except Exception, e: 
        ...     print e
        No row was found for one()
        '''
	self.__lastError__ = ''
        try:
	    if (callable(lamda_clause)):
		return self.query(lamda_clause).one()
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
        return None

    def query_first(self,lamda_clause):
        '''lamda_clause can be a lamda or function that accepts one argument that is the classObj that was passed-in when this object was created.
        query.first()
        '''
	self.__lastError__ = ''
        try:
	    if (callable(lamda_clause)):
		return self.query(lamda_clause).first()
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
        return None

    def autocommit():
	doc = "autocommit"
	def fget(self):
	    return self.__autocommit__
	def fset(self, autocommit):
	    self.__autocommit__ = autocommit
	return locals()
    autocommit = property(**autocommit())

    def autoflush():
	doc = "autoflush"
	def fget(self):
	    return self.__autoflush__
	def fset(self, autoflush):
	    self.__autoflush__ = autoflush
	return locals()
    autoflush = property(**autoflush())

    def isMultiSession():
        doc = "isMultiSession"
        def fget(self):
            return self.__isMultiSession__
        return locals()
    isMultiSession = property(**isMultiSession())

    def table_names():
        doc = "table_names"
        def fget(self):
            return self.engine.table_names()
        return locals()
    table_names = property(**table_names())

    def agents():
        doc = "agents"
        def fget(self):
            return self.__agents
        def fset(self, agents):
            self.__agents = agents
        return locals()
    agents = property(**agents())

    def engine():
        doc = "engine"
        def fget(self):
            return self.__engine__
        def fset(self, engine):
            self.__engine__ = engine
        return locals()
    engine = property(**engine())

    def mapper():
        doc = "mapper"
        def fget(self):
            return self.__mapper__
        def fset(self, mapper):
            self.__mapper__ = mapper
        return locals()
    mapper = property(**mapper())
    
    def mappers():
        doc = "mappers"
        def fget(self):
            return self.__mappers
        return locals()
    mappers = property(**mappers())
    
    def session():
        doc = "session"
        def fget(self):
            return self.__session__
        def fset(self, session):
	    if (self.__session__ is not None) and (self.__session__ != session):
		self.__session__.commit()
		self.__session__.close()
            self.__session__ = session
        return locals()
    session = property(**session())
    
    def classObj():
        doc = "classObj"
        def fget(self):
            return self.__classObj__
        def fset(self, classObj):
            self.__classObj__ = classObj
        return locals()
    classObj = property(**classObj())
    
    def tableDef():
        doc = "tableDef"
        def fget(self):
            return self.__tableDef__
        def fset(self, tableDef):
            self.__tableDef__ = tableDef
        return locals()
    tableDef = property(**tableDef())
    
    def lastError():
        doc = "lastError"
        def fget(self):
            return self.__lastError__
        return locals()
    lastError = property(**lastError())

    def last_error():
        doc = "last_error aka. lastError"
        def fget(self):
            return self.__lastError__
        return locals()
    last_error = property(**last_error())

class SQLAgentMultiSession(SQLAgent):
    def __init__(self,connection_string,classObj=None,tableDef=None,autoflush=False,autocommit=True):
	'''
	This SQLAgent handles multi-sessions to allow for multi-threaded usage.
	
	Usage: connection_string = "mysql://root:password-goes-here@server-name=goes-here:3306/database-name-goes-here"
	
	http://www.sqlalchemy.org/docs/05/ormtutorial.html
	'''
	self.__sessions__ = lists.HashedLists2()
	super(SQLAgentMultiSession, self).__init__(connection_string,classObj=classObj,tableDef=tableDef,autoflush=autoflush,autocommit=autocommit,isMultiSession=True)
    
    def new_session(self):
	'''
	Use self.use_session = to set the current session from a previously created session.
	'''
	self.__lastError__ = ''
        try:
	    Session = sessionmaker(bind=self.engine,autoflush=self.autoflush,autocommit=self.autocommit)
	    session_id = uuid.uuid4()
	    self.__sessions__[session_id] = Session()
	    return session_id
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
	return None
	    
    def use_session(self,session_id):
	'''
	Use self.new_session = to get a new session for use with use_session.
	'''
	self.__lastError__ = ''
        try:
	    sess = self.__sessions__[session_id]
	    if (sess is not None):
		self.session = sess
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
	    
    def destroy_session(self,session_id):
	self.__lastError__ = ''
        try:
            del self.__sessions__[session_id]
        except Exception, details:
	    from vyperlogix.misc import _utils
	    self.__lastError__ = _utils.formattedException(details=details)
    
