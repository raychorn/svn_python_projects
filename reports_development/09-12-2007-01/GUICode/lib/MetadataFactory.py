import sqlalchemy
from sqlalchemy import *
import dbConnections
import pyodbc
import _mssql
import os
import re
import logging

def dummy():
	return

class metadataFactory(object):
		def __init__(self,handle,context):
			self.logger = logging.getLogger(__name__)
			self.callback = dummy
			self.handle = handle
			self.context = context
			self.isMySQL = False
			self.isMSSQL = False
			self.isError = False
			try:
				if ( (handle == None) or (len(handle) != 2) ):
					self.logger.info('ERROR - Cannot proceed due to invalid dbConn handle.')
					return
			except Exception, details:
				self.isError = True
				self.logger.info(('ERROR - Cannot proceed due to invalid dbConn handle because (%s)'), str(details))
			if (self.isError == False):
				self.engine = handle[0]
				self.conn = handle[1]
				self.logger.info('engine=%s' % str(self.engine))
				self.logger.info('conn=%s' % str(self.conn))
				self.isMySQL = (str(self.engine).find('mysql://') > -1)
				self.isMSSQL = (str(self.engine).find('mssql://') > -1)
				if ( (self.engine == None) or (self.conn == None) ):
					self.logger.info('ERROR - Cannot proceed due to invalid engine and conn values.')
					return

		def isEngineMySQL(self):
			return (str(self.engine).find('mysql://') > -1)
			
		def isEngineMSSQL(self):
			return (str(self.engine).find('mssql://') > -1)

		def print_row_from(self,aList):
			self.logger.info(('aList.__class__=%s'), aList.__class__)
			self.logger.info(('aList=%s'), str(aList))

		def filterNumFrom(self,str):
			match = re.search(r"varchar\(([\d0-9]{1,3})\)", str, re.IGNORECASE | re.MULTILINE)
			if match:
					result = match.groups()[0]
			else:
					result = ""
			return(result)
				
		def mySQLFieldSpecFor(self,type):
			mType = ''
			if ( (type.find('bigint') > -1) | (type.find('smallint') > -1) | (type.find('tinyint') > -1) | (type.find('mediumint') > -1) | (type.find('int(') > -1) ):
				mType = 'Integer'
			else:
				if ( (type.find('timestamp') > -1) | (type.find('date') > -1) ):
					mType = 'DateTime'
				else:
					if (type.find('varchar') > -1):
						mType = 'String(%s)' % self.filterNumFrom(type)
					else:
						if (type.find('text') > -1):
							mType = 'Text'
						else:
							if ( (type.find('float') > -1) | (type.find('double') > -1) ):
								mType = 'Float'
			return mType

		def nullableSpecFor(self,type):
			mType = 'True'
			if (type == 'NO'):
				mType = 'False'
			return mType

		def autoIncrementSpecFor(self,type):
			mType = ''
			if (type == 'auto_increment'):
				mType = ', autoincrement=True'
			return mType

		def emitComma(self,bool):
			mType = ''
			if (bool == True):
				mType = ','
			return mType

		def generate_metadata_from(self,aList,tableName):
			content = ''
			content += 'from sqlalchemy import *\n'
			content += 'from sqlalchemy.orm import *\n'
			content += '\n'
			content += 'def init_%s_table(metadata):\n' % tableName
			content += '\t%s_table = Table(\'%s\', metadata,\n' % (tableName, tableName)
			isFirst = True
			num = len(aList)
			i = 1
			for s in aList:
				self.logger.info(('s=%s'), s)
				field = s.items()
				self.logger.info(('field.__class__=%s'), field.__class__)
				self.logger.info('(%s) field=%s' % (str(len(field)),str(field)))
				if (self.isEngineMSSQL()):
					fieldName = field[0][1]
					fieldDefault = field[1][1]
					fieldNull = field[2][1]
					fieldType = field[3][1]
					fieldKey = field[4][1]
					fieldExtra = field[5][1]
					content += '\t\tColumn(\'%s\', %s, nullable=%s%s)%s\n' % (fieldName, self.mySQLFieldSpecFor(fieldType), self.nullableSpecFor(fieldNull), self.autoIncrementSpecFor(fieldExtra), self.emitComma(isFirst))
				elif (self.isEngineMySQL()):
					fieldName = field[0][1]
					fieldType = field[1][1]
					fieldNull = field[2][1]
					fieldKey = field[3][1]
					fieldDefault = field[4][1]
					fieldExtra = field[5][1]
					content += '\t\tColumn(\'%s\', %s, nullable=%s%s)%s\n' % (fieldName, self.mySQLFieldSpecFor(fieldType), self.nullableSpecFor(fieldNull), self.autoIncrementSpecFor(fieldExtra), self.emitComma(isFirst))
				i += 1
				isFirst = (i < num)
			content += '\t\t)\n'
			content += '\treturn %s_table\n' % tableName
			return(content)

		def camelCase(self,str):
			s = ''
			x = str.split('_')
			for t in x:
				s += t.capitalize()
			return s

		def repeatSpecFor(self,aList,str):
			s = ''
			i = 1
			num = len(aList)
			isFirst = True
			for t in aList:
				s += str + self.emitComma(isFirst)
				i += 1
				isFirst = (i < num)
			return s

		def repeatedTemplateFor(self,aList,str):
			s = ''
			i = 1
			num = len(aList)
			isFirst = True
			for t in aList:
				field = t.items()
				fieldName = field[0][1]
				s += str + fieldName + self.emitComma(isFirst)
				i += 1
				isFirst = (i < num)
			return s

		def generate_objSpec_from(self,aList,tableName):
			content = ''
			content += 'class %sObj(object):\n' % self.camelCase(tableName)
			content += '\tdef __init__(self,'
			isFirst = True
			num = len(aList)
			i = 1
			for s in aList:
				field = s.items()
				fieldName = field[0][1]
				content += '%s%s' % (fieldName, self.emitComma(isFirst))
				i += 1
				isFirst = (i < num)
			content += '):\n'
			for s in aList:
				field = s.items()
				fieldName = field[0][1]
				content += '\t\tself.%s = %s\n' % (fieldName, fieldName)
			content += '\n'
			content += 'def __repr__(self):\n'
			content += '\treturn "<%s(%s)>" %% (%s)\n' % (self.camelCase(tableName), self.repeatSpecFor(aList, '%r'), self.repeatedTemplateFor(aList, 'self.'))
			return(content)

		def _writeFileFrom(self,fname,content):
			f = open(fname, 'w+')
			try:
				f.writelines(content)
			finally:
				f.close()

		def writeFileFrom(self,fname,content):
			self._writeFileFrom(fname, content)
			toks = fname.split('/')
			files = os.listdir(toks[0])
			initFname = '__init__.py'
			try:
				files.remove(initFname)
			finally:
				pass
			firstTime = True
			num = len(files)
			i = 1
			content = '__all__ = ["sessions_table", "UserObj", "users_table", "SessionObj"'
			for fn in files:
				content += '"%s"%s' % (fn, self.emitComma(firstTime))
				firstTime = (i < num)
				i += 1
			content += ']\n'
			self._writeFileFrom(initFname, content)
				
		def make_metadata_for(self,aList,projName):
			fpath = 'meta/' + projName
			files = os.listdir(fpath)
			
			self.logger.info('============================================================\n')
			iCnt = 1
			num = len(aList)
			for s in aList:
				try:
					self.logger.info('INFO - Issuing callback for termination clean-up.')
					self.callback(self.context,iCnt,num)
				except Exception, details:
					self.logger.info('WARNING - Cannot issue callback upon thread termination. (%s) (%s)' % (str(details), str(self.callback)))
	
				table_fname = s + '_table.py'
				obj_fname = self.camelCase(s) + 'Obj.py'
				try:
					i = files.index(table_fname)
				except Exception:
					i = -1
				try:
					j = files.index(obj_fname)
				except Exception:
					j = -1
				if ( (i == -1) | (j == -1) ):
					table_fname = fpath + '/' + table_fname
					obj_fname = fpath + '/' + obj_fname
					try:
						dbConn = dbConnections.connections()
						if (self.isEngineMySQL()):
							pass
						elif (self.isEngineMSSQL()):
							pass
						connection = self.engine.connect()
						sqlStatement = self.showFieldsSQLStatement(s)
						result = connection.execute(sqlStatement)
						self.logger.info('sqlStatement=%s' % sqlStatement)
						cols = result.fetchall()
						self.print_row_from(cols)
						self.logger.info('+++==============================\n')
						mCode = self.generate_metadata_from(cols, s)
						print mCode
						self.writeFileFrom(table_fname, mCode)
						oCode = self.generate_objSpec_from(cols, s)
						print oCode
						self.writeFileFrom(obj_fname, oCode)
						connection.close()
					except Exception, details:
						self.logger.info('ERROR - Skipping "%s"... Reason: %s' % (s,str(details)))
					self.logger.info('============================================================\n')
				iCnt += 1

		def showTablesSQLStatement(self):
			if (self.isMySQL):
				return 'SHOW Tables'
			elif (self.isMSSQL):
				return "select [NAME] from dbo.sysobjects where type = 'U' ORDER BY [NAME]"

		def showFieldsSQLStatement(self,tableName):
			if (self.isMySQL):
				return 'DESCRIBE %s' % tableName
			elif (self.isMSSQL):
				return "EXEC sp_columns @table_name = N'%s', @table_owner = N'dbo'" % tableName

		def process(self,isVerbose,projName):
			if (self.isError == False):
				isVerbose = (isVerbose == True) if isVerbose else False
				version = sqlalchemy.__version__
				if (isVerbose):
					self.logger.info('projName=%s' % projName)
					self.logger.info('version=%s' % version)

				tables = self.engine.table_names()

				if (isVerbose):
					self.logger.info('tables.__class__=%s, tables=%s' % (str(tables.__class__),str(tables)))
				
				if (len(tables) > 0):
					iCount = 0
					items = []
					for name in tables:
						canShow = True
						s = ''
						if (name.find('utt_') > -1):
								canShow = False
						s += name
						if (canShow):
							items.append(s)
							if (isVerbose):
								print '# %r :: %s' % (iCount, s)
							iCount += 1
					
					if (isVerbose):
						self.logger.info('items=%s' % str(items))

					self.make_metadata_for(items,projName)
	
					self.logger.info('Done!')
				else:
					self.logger.info('WARNING - No Data returned for SQL Statement (%s)' % sqlStatement)
				self.conn.close()
