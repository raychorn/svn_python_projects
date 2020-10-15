import dbhash
import bsddb

import random
import psyco

from vyperlogix import ioTimeAnalysis
from vyperlogix import threadpool

numRecs = 20000

_pool = threadpool.Pool(1000)

@threadpool.threadpool(_pool)
def writeToDb(_db,key,value):
	_db[key] = value

@threadpool.threadpool(_pool)
def readFromDb(_db,key):
	return db[key]

data_source = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
_payload_numBytes = (10*1024)

def getPayload(num):
	payload = ''
	tag = '__%s__' % num
	payload += tag + ''.join([data_source[random.randint(0,len(data_source)-1)] for i in xrange(_payload_numBytes-len(tag))])
	return payload

psyco.full()

#_actions = ['WRITE', 'READ', 'READ-RANDOM', 'BEGIN-KEYS', 'END-KEYS']
#_actions = ['WRITE', 'READ-RANDOM']
_actions = ['READ-RANDOM']

ioTimeAnalysis.initIOTime('READ')
ioTimeAnalysis.initIOTime('WRITE')
ioTimeAnalysis.initIOTime('READ-RANDOM')
ioTimeAnalysis.initIOTime('BEGIN-KEYS')
ioTimeAnalysis.initIOTime('END-KEYS')
try:
	db = dbhash.open('C:\\Documents and Settings\\ray_horn\\My Documents\\databases\\myDB.db', 'c')
	if (isinstance(db,bsddb._DBWithCursor)):
		try:
			_action = 'BEGIN-KEYS'
			if (_action in _actions):
				ioTimeAnalysis.ioBeginTime(_action)
				keys = db.keys()
				ioTimeAnalysis.ioEndTime(_action)
				print 'There are (%s) keys.' % (str(len(keys)))

			_action = 'WRITE'
			if (_action in _actions):
				ioTimeAnalysis.ioBeginTime(_action)
				for i in xrange(numRecs):
					datum = str(i)
					db[datum] = getPayload(i)
				db.sync()
				ioTimeAnalysis.ioEndTime(_action)

			j = 0
			_action = 'READ'
			if (_action in _actions):
				ioTimeAnalysis.ioBeginTime(_action)
				for i in xrange(len(db)):
					datum = db[str(i)]
					if (len(datum)):
						j += 1
				ioTimeAnalysis.ioEndTime(_action)

			_action = 'READ-RANDOM'
			if (_action in _actions):
				ioTimeAnalysis.ioBeginTime(_action)
				if (len(db) > 0):
					for i in xrange(numRecs):
						datum = db[str(random.randint(0,numRecs-1))]
				ioTimeAnalysis.ioEndTime(_action)

			_action = 'END-KEYS'
			if (_action in _actions):
				ioTimeAnalysis.ioBeginTime(_action)
				keys = db.keys()
				ioTimeAnalysis.ioEndTime(_action)
				print 'There are now (%s) keys.  Read (%s) data elements.' % (str(len(keys)),j)
		except Exception, details:
			print 'ERROR.1 due to "%s".' % str(details)
		db.close()
	else:
		print 'Unable to open the database.'
except Exception, details:
	print 'ERROR.2 due to "%s".' % str(details)

_pool.join()
ioTimeAnalysis.ioTimeAnalysisReport(numRecs)