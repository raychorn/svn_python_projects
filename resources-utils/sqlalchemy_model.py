# http://www.sqlalchemy.org/docs/05/ormtutorial.html
import sys

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
                    Column('is_file', sqltypes.Boolean, nullable=False)
)

class Node(SQLAgent.BaseObject):
    pass

# To-Do: Migrate the code above into an object in the lib.

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()
if (_cname == 'web22.webfaction.com'):
    conn_str = 'mysql://raychorn_resourc:peekab00@localhost:3306/raychorn_resourc'
elif (_cname == 'undefined3'):
    conn_str = 'mysql://root:peekab00@sql2005:3306/resources'
elif (_cname == 'misha-lap.ad.magma-da.com'):
    conn_str = 'mysql://root:peekaboo@localhost:3306/resources'
    
try:
    agent = SQLAgent.SQLAgent(conn_str,Node,node_table)
except SQLAgent.sqlalchemy.exc.OperationalError, details:
    from vyperlogix.misc import _utils
    print >>sys.stderr, _utils.formattedException(details=details)

for i in xrange(0,101):
    l = agent.session.query(Node).filter("id>=1").order_by("id").all()
    
    _id = 1 if (len(l) == 0) else l[-1].id+1
    
    aNode = Node(id=_id,name='name%d' % (_id),parent=None,creation_date=_utils.timeStampLocalTime(),modification_date=_utils.timeStampLocalTime(),is_active=True,is_file=False)
    agent.add(aNode)
    agent.commit()

pass