import sqlalchemy
import pyodbc
from sqlalchemy import *
import _mysql
from sqlalchemy.orm import *
import UnObscurePhrase
import logging

class connections(object):
    def __init__(self):
        self._pwd = UnObscurePhrase.UnObscurePhrase('\xf3\xe9\xf3\xeb\xef\xc0\xb7\xb6\xb6\xb0\xa4\xe2\xef\xef') # to be passed from the client later on...
        self.server_datebase_spec = ''
        self.logger = logging.getLogger(__name__)

    def connectMSSQL(self):
        s = 'DRIVER={SQL Server};%s' % (self.server_datebase_spec)
        if (self.server_datebase_spec.find('UID=') == -1):
            s = '%s;UID=sa' % (s)
        if (self.server_datebase_spec.find('PWD=') == -1):
            s = '%s;PWD=%s' % (s,self._pwd)
        self.logger.info(('connectMSSQL=%s'), s)
        return pyodbc.connect(s)

    def dbConnection_MSSQL(self):
        self.logger.info(('dbConnection_MSSQL self.server_datebase_spec=%s'), self.server_datebase_spec)
        try:
            engine = create_engine('mssql://', creator=self.connectMSSQL)
            conn = engine.connect()
        except Exception, details:
            self.logger.info(('ERROR - Cannot make a Database connection ! (%s)'), str(details))
            engine = None
            conn = None
        return(engine,conn)

    def dbConnection_mySQL(self,dsn):
        self.logger.info(('dbConnection_MSSQL self.server_datebase_spec=%s'), self.server_datebase_spec)
        try:
            engine = create_engine(dsn)
            conn = engine.connect()
        except Exception, details:
            self.logger.info(('ERROR - Cannot make a Database connection ! (%s)'), str(details))
            engine = None
            conn = None
        return(engine,conn)
