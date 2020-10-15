from lib import Enum
from xml.dom.minidom import parseString

class Commands(Enum.Enum):
	list_archives = 1
	open_archive = 2
	open_package = 3

class XMLProcessor:
	def __init__(self):
		pass
	
	def processXML(self,data):
		pass
