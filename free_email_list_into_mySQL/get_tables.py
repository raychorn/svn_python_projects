import os
import re

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

from vyperlogix.hash import lists

import sys

try:
    from cStringIO import StringIO as StringIO
except:
    from StringIO import StringIO as StringIO

from vyperlogix.sql.sqlalchemy import SQLAgent

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()
if (_cname == 'undefined3'):
    conn_str = 'mysql://root:peekab00@sql2005:3306/resources'
elif (_cname == 'misha-lap.ad.magma-da.com'):
    conn_str = 'mysql://root:peekaboo@localhost:3306/free_email_list'
    
try:
    agent = SQLAgent.SQLAgent(conn_str,None,None)
except SQLAgent.sqlalchemy.exc.OperationalError, details:
    print >>sys.stderr, _utils.formattedException(details=details)

_symbol_table_names = '[table-names]'
_symbol_file_name = '[file-name]'

_cmd = 'sqlautocode -t %s %s -o %s' % (_symbol_table_names,conn_str,_symbol_file_name)

if (__name__ == '__main__'):
    tables = [table for table in agent.table_names]
    s_cmd = _cmd.replace(_symbol_table_names,','.join(tables)).replace(_symbol_file_name,'free_email_tables.py')
    io_buf = StringIO()
    print >>io_buf, '@echo off'
    print >>io_buf, '\n'
    print >>io_buf, s_cmd
    _utils.writeFileFrom('gencode2.cmd',io_buf.getvalue())
    