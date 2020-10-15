import os
from vyperlogix.oodb import Enum
from vyperlogix.oodb import EnumInstance

data_folder_symbol = 'data'

pathName = data_folder_symbol

class DataFileTypes(Enum):
	noPurpose = 0
	deposits = 1
	withdrawls = 2
	
def dataFiles():
	path = os.sep.join([os.path.abspath(os.curdir),pathName])
	return [f for f in os.listdir(path) if (not os.path.isdir(os.sep.join([path,f])))]

def dataFilesFor(purpose=DataFileTypes.noPurpose,year=2005):
	if (isinstance(purpose,EnumInstance)):
		year = str(year)
		tag = '_deposits' if purpose == DataFileTypes.deposits else '_withdrawls'
		return [f for f in dataFiles() if f.find(year) > -1 and f.find(tag) > -1]
	else:
		print '(%s).dataFilesFor() :: Invalid purpose type used, purpose cannot be of type "%s".' % (__name__, str(purpose.__class__))
		return []

def PathName(f):
	return os.sep.join([pathName,f])
