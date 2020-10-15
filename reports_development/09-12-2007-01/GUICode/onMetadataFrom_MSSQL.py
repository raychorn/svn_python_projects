import logging
import time
import gettext
from vyperlogix import *
_ = gettext.gettext

def termination_callback(data):
  logger = logging.getLogger(__name__)
  if (len(data) == 3):
    handle = data[2]
    if (len(handle) == 2):
      engine = handle[0]
      conn = handle[1]
      try:
        logger.info('INFO - Closing the connection to the database engine.')
        conn.close()
      except Exception, details:
          logger.info(('ERROR - Cannot process termination_callback due to a problem with closing the connection (%s) !'), str(details))
    else:
      logger.info(_('ERROR -  Cannot process termination_callback due to a problem with the handle (%s)'), str(handle))
  else:
    logger.info(_('ERROR -  Cannot process termination_callback due to a problem with the data (%s)'), str(data))
  return

def process_callback(context,i,num):
  logger = logging.getLogger(__name__)
  logger.info('INFO - process_callback with (%s).' % str(context))
  try:
    context[1].set(0, num)
    context[1].tick()
    context[0].ack() # can be ommitted in this program
  except Exception, details:
    logger.info('ERROR - Cannot handle process_callback because (%s).' % str(details))
  
def process(connector, progress):
  logger = logging.getLogger(__name__)
  progress.set(0, 100)
  logger.info(_('connector.__class__=%s'), connector.__class__)
  logger.info(_('connector.data.__class__=%s'), connector.data.__class__)
  logger.info(_('connector.data=%s'), str(connector.data))
  myDSN = connector.data[0].get()
  myProjName = connector.data[1].get()
  logger.info(_('myDSN=%s'), myDSN)
  logger.info(_('myProjName=%s'), myProjName)
  dbConn = dbConnections.connections()
  dbConn.server_datebase_spec = myDSN
  handle = dbConn.dbConnection_MSSQL()
  logger.info(_('handle=%s'), str(handle))
  if (handle == None):
    logger.info(_('ERROR - Cannot proceed due to invalid dbConn handle.'))
    return
  connector.data.append(handle)
  connector.callback = termination_callback
  factory = MetadataFactory.metadataFactory(handle,(connector, progress))
  factory.callback = process_callback
  factory.process(True,myProjName)

if __name__ == '__main__':
  logging.basicConfig()
  logging.getLogger().setLevel(logging.INFO)
  class dummy:
    def ack(self):
      pass
    def set(self, a, b):
      pass
    def tick(self):
      pass
  process(dummy(), dummy())
