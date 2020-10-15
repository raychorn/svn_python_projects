import os
import sys
from lib.oodb import PickledHash
import traceback
from lib import sortedDictionary
import urllib

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

		if (self.commands(self.command) == self.commands(self.commands.createConcordance)):
			try:
				print >>sys.stderr, 'CREATE CONCORDANCE, args=(%s)' % self.args
				isError = True
				if (os.path.exists('ConcordanceProcessor.txt')):
					os.remove('ConcordanceProcessor.txt')
				try:
					stderr = open('ConcordanceProcessor.txt', 'w')
					_stderr = sys.stderr
					sys.stderr = stderr

					isSimulatingActivity = False
					
					if ( (not os.path.exists(globalVars.fileNames()['concordance_packages_db'])) or (not os.path.exists(globalVars.fileNames()['concordance_packages_synonyms_db'])) or (not os.path.exists(globalVars.fileNames()['concordance_packages_concordance_db'])) ):
						if (os.path.exists(globalVars.fileNames()['concordance_packages_db'])):
							os.remove(globalVars.fileNames()['concordance_packages_db'])
						if (os.path.exists(globalVars.fileNames()['concordance_packages_synonyms_db'])):
							os.remove(globalVars.fileNames()['concordance_packages_synonyms_db'])
						if (os.path.exists(globalVars.fileNames()['concordance_packages_concordance_db'])):
							os.remove(globalVars.fileNames()['concordance_packages_concordance_db'])
							
						self.resetActivityProgressBoundary()
						# debugLevel = ConcordanceProcessor.DebugLevels(ConcordanceProcessor.DebugLevels.process)|ConcordanceProcessor.DebugLevels(ConcordanceProcessor.DebugLevels.tokens)
						debugLevel = ConcordanceProcessor.DebugLevels.no_debugging
						c = ConcordanceProcessor.Concordance(globalVars._packages_filename, activityCallback, debugLevel, globalVars.fileNames()['concordance_packages_db'], globalVars.fileNames()['concordance_packages_synonyms_db'], globalVars.fileNames()['concordance_packages_concordance_db'])

						if (not isinstance(c.dataBase,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.fileNames()['concordance_packages_db'])
							commitDataFor(c.dataBase,dbx)
							dbx.close()
						else:
							isSimulatingActivity = True
							signalEndOfProcessingStep(False)

						if (not isinstance(c.synonyms,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.fileNames()['concordance_packages_synonyms_db'])
							commitDataFor(c.synonyms,dbx)
							dbx.close()
						else:
							isSimulatingActivity = True
							signalEndOfProcessingStep(False)

						if (not isinstance(c.concordance,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.fileNames()['concordance_packages_concordance_db'])
							commitDataFor(c.concordance,dbx)
							dbx.close()
						else:
							isSimulatingActivity = True
							signalEndOfProcessingStep(False)
							signalEndOfProcessingStep(False)
					else:
						isSimulatingActivity = True
						signalEndOfProcessingStep(False) # Required to allow the GUI to "think" it can go to the next step in the process
						signalEndOfProcessingStep(False) # Required to allow the GUI to "think" it can go to the next step in the process
						signalEndOfProcessingStep(False) # Required to allow the GUI to "think" it can go to the next step in the process

					if ( (not os.path.exists(globalVars.fileNames()['concordance_publishers_db'])) or (not os.path.exists(globalVars.fileNames()['concordance_publishers_synonyms_db'])) or (not os.path.exists(globalVars.fileNames()['concordance_publishers_concordance_db'])) ):
						if (os.path.exists(globalVars.fileNames()['concordance_publishers_db'])):
							os.remove(globalVars.fileNames()['concordance_publishers_db'])
						if (os.path.exists(globalVars.fileNames()['concordance_publishers_synonyms_db'])):
							os.remove(globalVars.fileNames()['concordance_publishers_synonyms_db'])
						if (os.path.exists(globalVars.fileNames()['concordance_publishers_concordance_db'])):
							os.remove(globalVars.fileNames()['concordance_publishers_concordance_db'])

						self.resetActivityProgressBoundary()
						c = ConcordanceProcessor.Concordance(globalVars._publishers_filename, activityCallback, ConcordanceProcessor.DebugLevels(ConcordanceProcessor.DebugLevels.no_debugging), globalVars.fileNames()['concordance_publishers_db'], globalVars.fileNames()['concordance_publishers_synonyms_db'], globalVars.fileNames()['concordance_publishers_concordance_db'])
	
						if (not isinstance(c.dataBase,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.fileNames()['concordance_publishers_db'])
							commitDataFor(c.dataBase,dbx)
							dbx.close()
						else:
							isSimulatingActivity = True
							signalEndOfProcessingStep(False)
						
						if (not isinstance(c.synonyms,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.fileNames()['concordance_publishers_synonyms_db'])
							commitDataFor(c.synonyms,dbx)
							dbx.close()
						else:
							isSimulatingActivity = True
							signalEndOfProcessingStep(False)
	
						if (not isinstance(c.concordance,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.fileNames()['concordance_publishers_concordance_db'])
							commitDataFor(c.concordance,dbx)
							dbx.close()
						else:
							isSimulatingActivity = True
							signalEndOfProcessingStep(False)
							signalEndOfProcessingStep(False)
					else:
						isSimulatingActivity = True
						signalEndOfProcessingStep(False) # Required to allow the GUI to "think" it can go to the next step in the process
						signalEndOfProcessingStep(False) # Required to allow the GUI to "think" it can go to the next step in the process
						signalEndOfProcessingStep(False) # Required to allow the GUI to "think" it can go to the next step in the process

					if ( (not os.path.exists(globalVars.fileNames()['concordance_unknown_packages_db'])) or (not os.path.exists(globalVars.fileNames()['concordance_unknown_packages_synonyms_db'])) or (not os.path.exists(globalVars.fileNames()['concordance_unknown_packages_concordance_db'])) ):
						if (os.path.exists(globalVars.fileNames()['concordance_unknown_packages_db'])):
							os.remove(globalVars.fileNames()['concordance_unknown_packages_db'])
						if (os.path.exists(globalVars.fileNames()['concordance_unknown_packages_synonyms_db'])):
							os.remove(globalVars.fileNames()['concordance_unknown_packages_synonyms_db'])
						if (os.path.exists(globalVars.fileNames()['concordance_unknown_packages_concordance_db'])):
							os.remove(globalVars.fileNames()['concordance_unknown_packages_concordance_db'])

						self.resetActivityProgressBoundary()
						c = ConcordanceProcessor.Concordance(globalVars._unknown_packages_filename, activityCallback, ConcordanceProcessor.DebugLevels(ConcordanceProcessor.DebugLevels.no_debugging), globalVars.fileNames()['concordance_unknown_packages_db'], globalVars.fileNames()['concordance_unknown_packages_synonyms_db'], globalVars.fileNames()['concordance_unknown_packages_concordance_db'])
	
						if (not isinstance(c.dataBase,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.fileNames()['concordance_unknown_packages_db'])
							commitDataFor(c.dataBase,dbx)
							dbx.close()
						else:
							isSimulatingActivity = True
							signalEndOfProcessingStep(False)
						
						if (not isinstance(c.synonyms,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.fileNames()['concordance_unknown_packages_synonyms_db'])
							commitDataFor(c.synonyms,dbx)
							dbx.close()
						else:
							isSimulatingActivity = True
							signalEndOfProcessingStep(False)
	
						if (not isinstance(c.concordance,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.fileNames()['concordance_unknown_packages_concordance_db'])
							commitDataFor(c.concordance,dbx)
							dbx.close()
						else:
							isSimulatingActivity = True
							#signalEndOfProcessingStep(False)
					else:
						isSimulatingActivity = True
						signalEndOfProcessingStep(False) # Required to allow the GUI to "think" it can go to the next step in the process
						signalEndOfProcessingStep(False) # Required to allow the GUI to "think" it can go to the next step in the process
						signalEndOfProcessingStep(False) # Required to allow the GUI to "think" it can go to the next step in the process

					if (isSimulatingActivity):
						signalEndOfProcessingStep(False)
						#signalEndOfProcessingStep(False)
						#signalEndOfProcessingStep(False)
						
					isError = False

					stderr.flush()
					stderr.close()
					sys.stderr = _stderr
					#assert len(_dataBase.keys()) == len(c.dataBase), _assertionMsg
				except Exception, details:
					_title = 'ERROR'
					errCode = '(%s).ERROR in CREATE CONCORDANCE due to "%s".' % (self.command,str(details))
					print >>sys.stderr, errCode
					_traceBack = traceback.format_exc()
					print >>sys.stderr, _traceBack
					self.__retVal = ('<error><title>%s</title><details>%s, %s</details></error>' % (_title,details,_traceBack),str(self.command))
					return
				_xml = self.processor.dataToXML(not isError,self.commandName)
				print '(exec_cmd).%s :: _xml=(%s)' % (self.commands(self.command),_xml)
			except Exception, details:
				_title = 'Programming Error'
				errCode = '(%s).ERROR in CREATE CONCORDANCE due to "%s".' % (self.command,str(details))
				print >>sys.stderr, errCode
				_traceBack = traceback.format_exc()
				print >>sys.stderr, _traceBack
				self.__retVal = ('<error><title>%s</title><details>%s, %s</details></error>' % (_title,details,_traceBack),str(self.command))
				return
			self.__retVal = (_xml,self.command)
			print '(exec_cmd).%s :: self.__retVal=(%s)' % (self.commands(self.command),self.__retVal)
			return
		elif (self.commands(self.command) == self.commands(self.commands.isConcordanceComplete)):
			print >>sys.stderr, 'IS CONCORDANCE COMPLETE, args=(%s)' % self.args
			isConcordanceComplete = True
			for f in globalVars.fileNames().values():
				print 'f.__class__=(%s)' % str(f.__class__)
				print 'f=(%s)' % str(f)
				if (isinstance(f,list)):
					for n in f:
						if (not os.path.exists(n)):
							isConcordanceComplete = False
							break
				else:
					if (not os.path.exists(f)):
						isConcordanceComplete = False
						break
			_xml = self.processor.dataToXML(isConcordanceComplete,self.commandName)
			self.__retVal = (_xml,self.command)
			print '(exec_cmd).%s :: self.__retVal=(%s)' % (self.commands(self.command),self.__retVal)
			return
		elif (self.commands(self.command) == self.commands(self.commands.openConcordance)):
			print >>sys.stderr, 'OPEN CONCORDANCE, args=(%s)' % self.args
			items = []
			if (globalVars.fileNames().has_key('concordance_unknown_packages_db')):
				if (os.path.exists(globalVars.fileNames()['concordance_unknown_packages_db'])):
					ndx = {}
					dbx = PickledHash.PickledHash(globalVars.fileNames()['concordance_unknown_packages_db'])
					for k,v in dbx.iteritems():
						for item in v:
							if (len(item) > 2):
								ch = str(item[0]).upper()
								if (ch[0] in _valid_chars):
									if (not ndx.has_key(ch)):
										ndx[ch] = 0
									ndx[ch] += 1
					isProcessing = True
					while (isProcessing):
						_markedForDeletion = []
						isProcessing = False
						for k,v in ndx.iteritems():
							if (v > 50):
								_threshold = len(k)+1
								_markedForDeletion.append(k)
								isProcessing = True
						for k in _markedForDeletion:
							del ndx[k]
							for k,v in dbx.iteritems():
								for item in v:
									if (len(item) > 2):
										ch = str(item[:_threshold]).upper()
										if (ch[0] in _valid_chars):
											if (not ndx.has_key(ch)):
												ndx[ch] = 0
											ndx[ch] += 1
					dbx.close()
					items = ndx.keys()
					items.sort()
			_xml = self.processor.listToXML(items)
			self.__retVal = (_xml,self.command)
			print '(exec_cmd).%s :: self.__retVal=(%s)' % (self.commands(self.command),self.__retVal)
			return
		elif (self.commands(self.command) == self.commands(self.commands.unknownPackages)):
			print >>sys.stderr, 'OPEN CONCORDANCE, args=(%s)' % self.args
			pName = urllib.unquote(self.args[0])
			items = []
			ndx = {}
			if (os.path.exists(globalVars.fileNames()['concordance_unknown_packages_db'])):
				dbx = PickledHash.PickledHash(globalVars.fileNames()['concordance_unknown_packages_db'])
				for k,v in dbx.iteritems():
					for item in v:
						if (len(item) > 2):
							ch = str(item[0]).upper()
							if (ch == pName):
								ndx[item] = 1
				dbx.close()
				items = ndx.keys()
				items.sort()
			_xml = self.processor.listToXML(items)
			self.__retVal = (_xml,self.command)
			print '(exec_cmd).%s :: self.__retVal=(%s)' % (self.commands(self.command),self.__retVal)
			return
		elif (self.commands(self.command) == self.commands(self.commands.getSuggestions)):
			print >>sys.stderr, 'GET SUGGESTIONS, args=(%s)' % self.args
			pName = urllib.unquote(self.args[0])
			print >>sys.stderr, '\t pName=(%s)' % pName
			ndx = {}
			ndxUnknown = {}
			cTokens = []
			suggestedItems = {}
			suggestedPackages = []
			if (os.path.exists(globalVars.fileNames()['concordance_unknown_packages_db'])):
				dbx = PickledHash.PickledHash(globalVars.fileNames()['concordance_unknown_packages_db'])
				for k,v in dbx.iteritems():
					ndx[v[0]] = k
				dbx.close()
			recNo = ndx[pName]
			print >>sys.stderr, '\t recNo=(%s) [%s]' % (recNo,str(recNo.__class__))
			if (recNo != None):
				if (os.path.exists(globalVars.fileNames()['concordance_unknown_packages_concordance_db'])):
					dbx = PickledHash.PickledHash(globalVars.fileNames()['concordance_unknown_packages_concordance_db'])
					for k,v in dbx.iteritems():
						for item in v:
							if (not ndxUnknown.has_key(item)):
								ndxUnknown[item] = []
							ndxUnknown[item].append(k)
					dbx.close()
			try:
				cTokens = [t.replace('(','').replace(')','') for t in ndxUnknown[recNo]]
			except Exception, details:
				_traceBack = traceback.format_exc()
				print >>sys.stderr, '\n ERROR due to "%s" (Might be caused by the way Concordance Parsing works - some names result in no usable Tokens).\n%s\n' % (str(details),_traceBack)
			print >>sys.stderr, '\t cTokens=(%s)' % cTokens
			if (len(cTokens) > 0):
				if (os.path.exists(globalVars.fileNames()['concordance_packages_concordance_db'])):
					dbx = PickledHash.PickledHash(globalVars.fileNames()['concordance_packages_concordance_db'])
					for t in cTokens:
						print >>sys.stderr, '\t t=(%s)' % t
						if (dbx.has_key(t)):
							items = dbx[t]
							print >>sys.stderr, '\t items=(%s)' % items
							for item in items:
								suggestedItems[item] = item
					dbx.close()
			if (len(suggestedItems) > 0):
				suggestedPackages = {}
				if (os.path.exists(globalVars.fileNames()['concordance_packages_db'])):
					dbx = PickledHash.PickledHash(globalVars.fileNames()['concordance_packages_db'])
					for item in suggestedItems.keys():
						for t in list(dbx[item]):
							suggestedPackages[t] = 1
					dbx.close()
					suggestedPackages = suggestedPackages.keys()
					suggestedPackages.sort()
			else:
				suggestedPackages = []
				suggestedPackages.append('NO SUGGESTIONS AVAILABLE.')
			_xml = self.processor.listToXML(suggestedPackages)
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
	from lib import _psyco
	_psyco.importPsycoIfPossible()
	isDebugging = True

	