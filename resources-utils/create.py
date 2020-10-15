import os, sys
import re

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

from vyperlogix.daemon.daemon import Log
from vyperlogix.daemon.daemon import EchoLog

from vyperlogix.hash import lists

from vyperlogix.misc import threadpool

import sys

from sqlalchemy.exc import OperationalError
from vyperlogix.sql.sqlalchemy.SQLAgent import BaseObject
from vyperlogix.sql.sqlalchemy.SQLAgent import SQLAgent
from vyperlogix.sql.sqlalchemy.SQLAgent import SQLAgentMultiSession

from sqlalchemy import types as sqltypes

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

from vyperlogix import oodb
dbx_name = lambda fpath,name:oodb.dbx_name(name,fpath)

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

from vyperlogix.classes.CooperativeClass import Cooperative

_log_path = os.path.join(os.path.dirname(sys.argv[0]),'logs')

_utils._makeDirs(_log_path)

_logFile = open(os.path.join(_log_path, '%s_%s.txt' % (os.path.basename(sys.argv[0]),_utils.timeStampLocalTime(format=_utils.formatSalesForceDateTimeStr()).replace(' ','_').replace(':','_'))),'w')
_log = EchoLog(_logFile)

class NodeFactory(Cooperative):
    def __init__(self):
	pass
	
    def make_node(self,_id=-1,_parent=-1,_name='',_creation_date=_utils.timeStampLocalTime(),_modification_date=_utils.timeStampLocalTime(),_is_active=False,_is_file=False,_is_url=False):
	return Node(id=_id,name=_name,parent=_parent,creation_date=default_date(_creation_date),modification_date=default_date(_modification_date),is_active=_is_active,is_file=_is_file,is_url=_is_url)

_is_running_local = True

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()
print >>_log, '_cname=%s' % (_cname)
if (_cname == 'web22.webfaction.com'):
    _is_running_local = False
    conn_str = 'mysql://raychorn_resourc:peekab00@localhost:3306/raychorn_resourc'
elif (_cname in ['undefined3','sql2005.halsmalltalker.com']):
    _is_running_local = False
    conn_str = 'mysql://root:peekab00@sql2005:3306/resources'
elif (_cname == 'misha-lap.ad.magma-da.com'):
    conn_str = 'mysql://root:peekaboo@localhost:3306/resources'
else:
    print >>_log, 'NOTHING TO DO !'
    sys.exit(1)
    
try:
    agent = SQLAgentMultiSession(conn_str,Node,node_table)
except OperationalError, details:
    print >>_log, _utils.formattedException(details=details)
    sys.exit(1)

_factory = NodeFactory()

top = r'%s:\@myFiles\@Python' % ('Z' if (_is_running_local) else 'M')

pattern = '@python'

_symbol_InternetShortcut = '[InternetShortcut]'

svnFilter = '[._]svn' 
rxSVN=re.compile(svnFilter)

py26Filter = '@Python_2.6a3' 
rxPy26=re.compile(py26Filter)

filter = lambda f:(f.lower().find(pattern) > -1)

def root_folders(_top,_filter=None):
    files = os.listdir(_top)
    return [os.sep.join([_top,f]) for f in files if (not callable(_filter)) or ((callable(_filter)) and _filter(f))]

def process_name(cls,d_url,_rr_,_name,isInternetShortcut=False):
    '''
    This function CANNOT be run in the background via any kind of threading mechanism because the state of the parent
    depends on the number of records in the database.
    '''
    import os, sys
    from vyperlogix.misc import _utils

    sess = agent.new_session()
    if (sess is None):
	print >>_log, '1. LAST_ERROR :: %s' % (agent.lastError)
	return
    agent.use_session(sess)
    if (agent.session is None):
	print >>_log, '2. LAST_ERROR :: %s' % (agent.lastError)
	return
    logger = Log(open(os.path.join(_log_path, '%s_%s_%s.txt' % (os.path.basename(sys.argv[0]),sess,_utils.timeStampLocalTime(format=_utils.formatSalesForceDateTimeStr()).replace(' ','_').replace(':','_'))),'w'))
    print >>logger, 'BEGIN: Session %s' % (sess)
    try:
	_is_file_ = os.path.isfile(_name)
	s_name = _name.replace(_rr_,'')
	print >>logger, '\t%s' % (s_name)
	nodes = s_name.split(os.sep)
	_parent = -1
	num_recs = agent.session.query(cls).count()
	for s in nodes[0:-1]:
	    if (len(s) == 0):
		continue
	    rec = agent.session.query(cls).filter("name=:name and parent=:parent").params(name=s, parent=_parent)
	    print >>logger, 'rec.count()=%s, name is "%s", parent is "%s".' % (rec.count(),s,_parent)
	    if (rec.count() == 0):
		_id = num_recs+1
		aNode = _factory.make_node(_id=_id,_parent=_parent,_name=s,_creation_date=None,_modification_date=None,_is_active=True,_is_file=False,_is_url=False)
		agent.add(aNode)
		agent.flush()
		print >>logger, '1. Commit. aNode is %s' % (str(aNode))
		_parent = _id
		num_recs += 1
	    else:
		aNode = rec.first()
		_parent = aNode.id
	recs = agent.all()
	_id = len(recs)+1
	if (not isInternetShortcut):
	    rec = agent.session.query(cls).filter("name=:name and parent=:parent").params(name=nodes[-1], parent=_parent)
	    print >>logger, 'rec.count()=%s, name is "%s", parent is "%s".' % (rec.count(),nodes[-1],_parent)
	    if (rec.count() == 0):
		aNode = _factory.make_node(_id=_id,_parent=_parent,_name=nodes[-1],_creation_date=None,_modification_date=None,_is_active=True,_is_file=_is_file_,_is_url=False)
		agent.add(aNode)
		agent.commit()
		print >>logger, '2. Commit.'
	else:
	    for k,v in d_url.iteritems():
		rec = agent.session.query(cls).filter("name=:name and parent=:parent").params(name=v, parent=_parent)
		print >>logger, 'rec.count()=%s, name is "%s", parent is "%s".' % (rec.count(),v,_parent)
		if (rec.count() == 0):
		    aNode = _factory.make_node(_id=_id,_parent=_parent,_name=v,_creation_date=None,_modification_date=None,_is_active=True,_is_file=False,_is_url=True)
		    agent.add(aNode)
		    agent.commit()
		    print >>logger, '3. Commit.'
    except Exception, details:
	from vyperlogix.misc import _utils
	info_string = _utils.formattedException(details=details)
	print >>logger, info_string
    finally:
	print >>logger, 'END!  Session %s' % (sess)
	agent.destroy_session(sess)
	logger.flush()
	logger.close()

def main(status_callback=None,log=sys.stdout):
    _files = root_folders(top)
    i = 1
    n = len(_files)
    begin_ts = _utils.timeSeconds()
    try:
	_rr_ = os.path.dirname(top)
	for _r_ in _files:
	    files = os.listdir(_r_)
	    i2 = 1
	    n2 = len(files)
	    for f in files:
		_f = os.sep.join([_r_,f])
		for root, dirs, files in os.walk(_f):
		    if (not rxSVN.search(root)) and (not rxPy26.search(root)):
			_root = os.sep.join([s for s in root.replace(_rr_,'').split(os.sep) if (len(s) > 0)])
			if (len(_root) > 0) and (len(files) > 0):
			    n_pcent = (float(i) / float(n))
			    pcent = n_pcent * 100.0
			    pcent2 = (float(i2) / float(n2)) * 100.0
			    curr_ts = _utils.timeSeconds()
			    et_ts = curr_ts - begin_ts
			    x_et_ts = (float(et_ts) * 100.0) / pcent
			    s_et_ts = '%-10.2f'%x_et_ts
			    s_et_ts = s_et_ts.strip()
			    x_et_ts2 = (float(et_ts) * 100.0) / pcent2
			    s_et_ts2 = '%-10.2f'%x_et_ts2
			    s_et_ts2 = s_et_ts2.strip()
			    if (callable(status_callback)):
				try:
				    status_callback(pcent,pcent2)
				except Exception, details:
				    info_string = _utils.formattedException(details=details)
				    print >>log, info_string
				    print >>sys.stderr, info_string
			    info_string = 'BEGIN: (%2.0f%%)/(%2.0f%%) (%s/%s secs remain) "%s"' % (pcent,pcent2,s_et_ts,s_et_ts2,_root)
			    print >>log, info_string
			    print >>sys.stderr, info_string
			    d_parent = None
			    for name in files:
				isInternetShortcut = False
				_name = os.sep.join([_rr_,_root,name])
				_url = ''
				d_url = lists.HashedLists2()
				if (name.lower().endswith('.url')):
				    #assert os.path.exists(_name), 'Oops, something went wrong "%s" does not seem to exist however it should.' % (_name)
				    if (os.path.exists(_name)):
					fIn = open(_name, 'rb')
					try:
					    bytes = fIn.read()
					finally:
					    fIn.close()
					l_bytes = bytes.split('\r\n')
					if (l_bytes[0] == _symbol_InternetShortcut):
					    isInternetShortcut = True
					    toks = ''.join(l_bytes[1:]).split('=')
					    _url = ''.join(toks[1:])
					    d_url[name] = ''.join(toks[1:])
					    info_string = '%s' % (_url)
					    print >>log, info_string
					    print >>sys.stderr, info_string
				# build this as a nested series of dictionary objects where the parent is the key for the parent dict.
				# nodes with no contents are leaf nodes otherwise the key is the name of the node.
				process_name(Node,d_url,_rr_,_name,isInternetShortcut=isInternetShortcut)
			    info_string = 'END! (%2.0f%%)/(%2.0f%%) (%s/%s secs remain) "%s"' % (pcent,pcent2,s_et_ts,s_et_ts2,_root)
			    print >>log, info_string
			    print >>sys.stderr, info_string
			    print >>log, '='*80
			    print >>sys.stderr, '='*80
			    print >>log, '\n'
			    print >>sys.stderr, '\n'
			    
		i2 += 1
	    i += 1
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>_log, info_string
    info_string = 'DONE !!!'
    print >>log, info_string
    print >>sys.stderr, info_string

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)

    main(log=_log)
