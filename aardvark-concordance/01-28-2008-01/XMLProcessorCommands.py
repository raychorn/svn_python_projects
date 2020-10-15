import os
import sys
from lib import PickledHash
import ConcordanceProcessor
import traceback
from lib import sortedDictionary
import urllib

import globalVars
# To-Do:
#

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
					
					if ( (not os.path.exists(globalVars.concordance_packages_db)) or (not os.path.exists(globalVars.concordance_packages_synonyms_db)) or (not os.path.exists(globalVars.concordance_packages_concordance_db)) ):
						if (os.path.exists(globalVars.concordance_packages_db)):
							os.remove(globalVars.concordance_packages_db)
						if (os.path.exists(globalVars.concordance_packages_synonyms_db)):
							os.remove(globalVars.concordance_packages_synonyms_db)
						if (os.path.exists(globalVars.concordance_packages_concordance_db)):
							os.remove(globalVars.concordance_packages_concordance_db)
							
						self.resetActivityProgressBoundary()
						# debugLevel = ConcordanceProcessor.DebugLevels(ConcordanceProcessor.DebugLevels.process)|ConcordanceProcessor.DebugLevels(ConcordanceProcessor.DebugLevels.tokens)
						debugLevel = ConcordanceProcessor.DebugLevels.no_debugging
						c = ConcordanceProcessor.Concordance(globalVars._packages_filename, activityCallback, debugLevel, globalVars.concordance_packages_db, globalVars.concordance_packages_synonyms_db, globalVars.concordance_packages_concordance_db)

						if (not isinstance(c.dataBase,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.concordance_packages_db)
							commitDataFor(c.dataBase,dbx)
							dbx.close()
						else:
							isSimulatingActivity = True
							signalEndOfProcessingStep(False)

						if (not isinstance(c.synonyms,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.concordance_packages_synonyms_db)
							commitDataFor(c.synonyms,dbx)
							dbx.close()
						else:
							isSimulatingActivity = True
							signalEndOfProcessingStep(False)

						if (not isinstance(c.concordance,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.concordance_packages_concordance_db)
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

					if ( (not os.path.exists(globalVars.concordance_publishers_db)) or (not os.path.exists(globalVars.concordance_publishers_synonyms_db)) or (not os.path.exists(globalVars.concordance_publishers_concordance_db)) ):
						if (os.path.exists(globalVars.concordance_publishers_db)):
							os.remove(globalVars.concordance_publishers_db)
						if (os.path.exists(globalVars.concordance_publishers_synonyms_db)):
							os.remove(globalVars.concordance_publishers_synonyms_db)
						if (os.path.exists(globalVars.concordance_publishers_concordance_db)):
							os.remove(globalVars.concordance_publishers_concordance_db)

						self.resetActivityProgressBoundary()
						c = ConcordanceProcessor.Concordance(globalVars._publishers_filename, activityCallback, ConcordanceProcessor.DebugLevels(ConcordanceProcessor.DebugLevels.no_debugging), globalVars.concordance_publishers_db, globalVars.concordance_publishers_synonyms_db, globalVars.concordance_publishers_concordance_db)
	
						if (not isinstance(c.dataBase,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.concordance_publishers_db)
							commitDataFor(c.dataBase,dbx)
							dbx.close()
						else:
							isSimulatingActivity = True
							signalEndOfProcessingStep(False)
						
						if (not isinstance(c.synonyms,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.concordance_publishers_synonyms_db)
							commitDataFor(c.synonyms,dbx)
							dbx.close()
						else:
							isSimulatingActivity = True
							signalEndOfProcessingStep(False)
	
						if (not isinstance(c.concordance,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.concordance_publishers_concordance_db)
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

					if ( (not os.path.exists(globalVars.concordance_unknown_packages_db)) or (not os.path.exists(globalVars.concordance_unknown_packages_synonyms_db)) or (not os.path.exists(globalVars.concordance_unknown_packages_concordance_db)) ):
						if (os.path.exists(globalVars.concordance_unknown_packages_db)):
							os.remove(globalVars.concordance_unknown_packages_db)
						if (os.path.exists(globalVars.concordance_unknown_packages_synonyms_db)):
							os.remove(globalVars.concordance_unknown_packages_synonyms_db)
						if (os.path.exists(globalVars.concordance_unknown_packages_concordance_db)):
							os.remove(globalVars.concordance_unknown_packages_concordance_db)

						self.resetActivityProgressBoundary()
						c = ConcordanceProcessor.Concordance(globalVars._unknown_packages_filename, activityCallback, ConcordanceProcessor.DebugLevels(ConcordanceProcessor.DebugLevels.no_debugging), globalVars.concordance_unknown_packages_db, globalVars.concordance_unknown_packages_synonyms_db, globalVars.concordance_unknown_packages_concordance_db)
	
						if (not isinstance(c.dataBase,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.concordance_unknown_packages_db)
							commitDataFor(c.dataBase,dbx)
							dbx.close()
						else:
							isSimulatingActivity = True
							signalEndOfProcessingStep(False)
						
						if (not isinstance(c.synonyms,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.concordance_unknown_packages_synonyms_db)
							commitDataFor(c.synonyms,dbx)
							dbx.close()
						else:
							isSimulatingActivity = True
							signalEndOfProcessingStep(False)
	
						if (not isinstance(c.concordance,PickledHash.PickledHash)):
							dbx = PickledHash.PickledHash(globalVars.concordance_unknown_packages_concordance_db)
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
			for f in globalVars.concordance_files:
				if (not os.path.exists(f)):
					isConcordanceComplete = False
					break
			_xml = self.processor.dataToXML(isConcordanceComplete,self.commandName)
			self.__retVal = (_xml,self.command)
			print '(exec_cmd).%s :: self.__retVal=(%s)' % (self.commands(self.command),self.__retVal)
			return
		elif (self.commands(self.command) == self.commands(self.commands.openConcordance)):
			print >>sys.stderr, 'OPEN CONCORDANCE, args=(%s)' % self.args
			if (os.path.exists(globalVars.concordance_unknown_packages_db)):
				items = []
				dbx = PickledHash.PickledHash(globalVars.concordance_unknown_packages_db)
				for k,v in dbx.iteritems():
					items.append(v)
					if (len(items) >= 20):
						break
				dbx.close()
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
			if (os.path.exists(globalVars.concordance_unknown_packages_db)):
				dbx = PickledHash.PickledHash(globalVars.concordance_unknown_packages_db)
				for k,v in dbx.iteritems():
					ndx[v[0]] = k
				dbx.close()
			recNo = ndx[pName]
			print >>sys.stderr, '\t recNo=(%s)' % recNo
			if (recNo != None):
				if (os.path.exists(globalVars.concordance_unknown_packages_concordance_db)):
					dbx = PickledHash.PickledHash(globalVars.concordance_unknown_packages_concordance_db)
					for k,v in dbx.iteritems():
						for item in v:
							if (not ndxUnknown.has_key(item)):
								ndxUnknown[item] = []
							ndxUnknown[item].append(k)
					dbx.close()
			cTokens = [t.replace('(','').replace(')','') for t in ndxUnknown[recNo]]
			print >>sys.stderr, '\t cTokens=(%s)' % cTokens
			if (len(cTokens) > 0):
				if (os.path.exists(globalVars.concordance_packages_concordance_db)):
					dbx = PickledHash.PickledHash(globalVars.concordance_packages_concordance_db)
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
				if (os.path.exists(globalVars.concordance_packages_db)):
					dbx = PickledHash.PickledHash(globalVars.concordance_packages_db)
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
	import psyco
	psyco.full()
	isDebugging = True

	#c = ConcordanceProcessor.Concordance(globalVars._packages_filename, None, ConcordanceProcessor.DebugLevels(ConcordanceProcessor.DebugLevels.no_debugging), globalVars.concordance_packages_db, globalVars.concordance_packages_synonyms_db, globalVars.concordance_packages_concordance_db)
	#c = ConcordanceProcessor.Concordance(globalVars._publishers_filename, None, ConcordanceProcessor.DebugLevels(ConcordanceProcessor.DebugLevels.no_debugging), globalVars.concordance_publishers_db, globalVars.concordance_publishers_synonyms_db, globalVars.concordance_publishers_concordance_db)
	#c = ConcordanceProcessor.Concordance(globalVars._unknown_packages_filename, None, ConcordanceProcessor.DebugLevels(ConcordanceProcessor.DebugLevels.no_debugging), globalVars.concordance_unknown_packages_db, globalVars.concordance_unknown_packages_synonyms_db, globalVars.concordance_unknown_packages_concordance_db)
	
	for f in globalVars.concordance_files:
		if (os.path.exists(f)):
			tName = '.'.join([f.split('.')[0],'txt'])
			fHand = open(tName,'w')
			dbx = PickledHash.PickledHash(f)
			print >>fHand, '(%s) :: (%s) :: dbx=(%s)' % (__name__,f,str(dbx))
			if (isDebugging):
				for k,v in dbx.iteritems():
					print >>fHand, '%s=(%s)' % (k,v)
			dbx.close()
			
			if (isDebugging):
				print >>fHand
				print >>fHand, '='*60
				print >>fHand

			fHand.flush()
			fHand.close()
	