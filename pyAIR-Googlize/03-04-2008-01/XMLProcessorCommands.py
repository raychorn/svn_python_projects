import os
import sys
from vyperlogix.oodb import PickledHash
import traceback
from vyperlogix import sortedDictionary
import urllib
import ListToXMLOptions

_valid_chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']

class XMLProcessorCommands():
	def __init__(self, cmd, args, processor, commands, commandName):
		self.__cmd = cmd
		self.__processor = processor
		self.__commands = commands
		self.__args = args
		self.__retVal = None
		self.__commandName = commandName
		self.__progressBoundary = -1
		self.exec_cmd()
		
	def __repr__(self):
		return '%s :: command=(%s), commandName=(%s), args=(%s)' % (str(self.__class__),self.command,self.commandName,self.args)

	def get_commandName(self):
		return self.__commandName

	def get_retVal(self):
		return self.__retVal

	def get_args(self):
		return self.__args

	def get_commands(self):
		return self.__commands

	def get_processor(self):
		return self.__processor

	def get_cmd(self):
		return self.__cmd
	
	def resetActivityProgressBoundary(self):
		self.__progressBoundary = -1
	
	def exec_cmd(self):
		def activityCallback(args):
			count = args
			num = self.__progressBoundary if self.__progressBoundary > 0 else 100
			if ( (self.__progressBoundary < 0) or ((count % num) == 0) ):
				_xml = self.processor.dataToXML(count,'concordanceProgress')
				self.processor.connHandle.server.__send__(self.processor.connHandle,_xml)
				if (self.__progressBoundary < 0):
					self.__progressBoundary = count / 40 # 2.5 percent per tick
		
		def signalEndOfProcessingStep(bool):
			_xml = self.processor.dataToXML(bool,self.commandName)
			#print '(signalEndOfProcessingStep) :: (%s)' % _xml
			self.processor.connHandle.server.__send__(self.processor.connHandle,_xml)
		
		def commitDataFor(dDict, db):
			signalEndOfProcessingStep(False)

			self.resetActivityProgressBoundary()
			activityCallback(len(dDict.keys()))
			i = 1
			for k,v in dDict.iteritems():
				db[k] = v
				if ((i % self.__progressBoundary) == 0):
					activityCallback(i)
				i += 1

			print '(exec_cmd).%s :: dbx=(%s)' % (self.commands(self.command),db)
			print >>sys.stderr, '%s items in the database.' % (len(db))

		print 'self.command=(%s) (%s)' % (self.command,self.commands(self.command))
		if (self.commands(self.command) == self.commands(self.commands.execute_code)):
			try:
				foo = ''
				print >>sys.stderr, 'EXECUTE CODE, args=(%s)' % self.args
				isError = False
				try:
					foo = eval(self.args[0])
				except Exception, details:
					isError = True
					foo = str(details)

				print 'foo=(%s)' % foo
				_xml = '<response>' + self.processor.dataToXML(foo,self.commandName) + '</response>'
				print '(exec_cmd).%s :: _xml=(%s)' % (self.commands(self.command),_xml)
			except Exception, details:
				_title = 'Programming Error'
				errCode = '(%s).ERROR in EXECUTE CODE due to "%s".' % (self.command,str(details))
				print >>sys.stderr, errCode
				_traceBack = traceback.format_exc()
				print >>sys.stderr, _traceBack
				self.__retVal = ('<error><title>%s</title><details>%s, %s</details></error>' % (_title,details,_traceBack),str(self.command))
				return
			self.__retVal = (_xml,self.command)
			print '(exec_cmd).%s :: self.__retVal=(%s)' % (self.commands(self.command),self.__retVal)
			return
		else:
			_cmd = str(self.command)
			self.__retVal = (_cmd,_cmd)
			return
	
	processor = property(get_processor)
	command = property(get_cmd)
	commands = property(get_commands)
	args = property(get_args)
	retVal = property(get_retVal)
	commandName = property(get_commandName)

if (__name__ == '__main__'):
	import pprint
	from vyperlogix import _psyco
	_psyco.importPsycoIfPossible()
	isDebugging = True

	