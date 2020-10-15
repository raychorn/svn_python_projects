from vyperlogix.misc import _utils

from vyperlogix.sql.sqlalchemy import SQLAgent

from sqlalchemy import types as sqltypes

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

metadata = MetaData()
node_table = Table('library_node', metadata,
                    Column('id', sqltypes.Integer, nullable=False, default=0, primary_key=True),
                    Column('name', sqltypes.String(128), nullable=False),
                    Column('parent', sqltypes.Integer, nullable=True),
                    Column('creation_date', sqltypes.DateTime, nullable=False),
                    Column('modification_date', sqltypes.DateTime, nullable=False),
                    Column('is_active', sqltypes.Boolean, nullable=False),
                    Column('is_url', sqltypes.Boolean, nullable=False),
                    Column('is_file', sqltypes.Boolean, nullable=False)
)

class Node(SQLAgent.BaseObject):
    pass

from vyperlogix.classes.CooperativeClass import Cooperative

class NodeFactory(Cooperative):
    def __init__(self):
	pass
	
    def make_node(self,_id=-1,_parent=-1,_name='',_creation_date=_utils.timeStampLocalTime(),_modification_date=_utils.timeStampLocalTime(),_is_active=False,_is_file=False,_is_url=False):
	return Node(id=_id,name=_name,parent=_parent,creation_date=default_date(_creation_date),modification_date=default_date(_modification_date),is_active=_is_active,is_file=_is_file,is_url=_is_url)

class LibraryAgent(SQLAgent.SQLAgent):
    def __init__(self,conn_str):
	super(LibraryAgent, self).__init__(conn_str,Node,node_table)
    
    def nodes(self,parent=None,order_by='parent'):
	order_by = order_by if (node_table.columns.keys()) else 'parent'
	_filter = "parent = %d" % (int(str(parent)) if (parent is not None) and (str(parent).isdigit()) else -1)
	qry = self.session.query(Node)
	if (len(_filter) > 0):
	    qry.filter(_filter)
	items = qry.order_by(order_by).all()
	return items

