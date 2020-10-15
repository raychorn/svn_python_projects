import sqlalchemy
from sqlalchemy import *
from dbConnections import *
import pyodbc
from vyperlogix import *
import _mssql
import os
import re
import sys

def print_row_from(aList):
	print 'aList.__class__=', aList.__class__
	print 'aList=', aList

def filterNumFrom(str):
	match = re.search(r"varchar\(([\d0-9]{1,3})\)", str, re.IGNORECASE | re.MULTILINE)
	if match:
		result = match.groups()[0]
	else:
		result = ""
	return(result)
	
def fieldSpecFor(type,size):
	mType = ''
	if ( (type.find('bigint') > -1) | (type.find('smallint') > -1) | (type.find('tinyint') > -1) | (type.find('mediumint') > -1) | (type.find('int(') > -1) ):
		mType = 'Integer'
	else:
		if ( (type.find('timestamp') > -1) | (type.find('date') > -1) ):
			mType = 'DateTime'
		else:
			if ( (type.find('varchar') > -1) or (type.find('nvarchar') > -1) ):
				mType = 'String(%s)' % str(size)
			else:
				if (type.find('text') > -1):
					mType = 'Text'
				else:
					if ( (type.find('float') > -1) | (type.find('double') > -1) ):
						mType = 'Float'
	return mType

def nullableSpecFor(type):
	mType = 'True'
	if (type == 'NO'):
		mType = 'False'
	return mType

def autoIncrementSpecFor(type):
	mType = ''
	if (type == 'auto_increment'):
		mType = ', autoincrement=True'
	return mType

def emitComma(bool):
	mType = ''
	if (bool == True):
		mType = ','
	return mType

def generate_metadata_from(aList, col_names, tableName):
	content = ''
	content += 'from sqlalchemy import *\n'
	content += 'from sqlalchemy.orm import *\n'
	content += '\n'
	content += 'def init_%s_table(metadata):\n' % tableName
	content += '\t%s_table = Table(\'%s\', metadata,\n' % (tableName, tableName)
	isFirst = True
	num = len(aList)
	i = 1
	for row in aList:
		fieldName = row[col_names.index('column_name')]
		fieldType = row[col_names.index('type_name')].lower()
		fieldSize = row[col_names.index('column_size')]
		fieldNull = row[col_names.index('is_nullable')]
		fieldDefault = row[col_names.index('column_def')]
		fieldExtra = ''
		content += '\t\tColumn(\'%s\', %s, nullable=%s%s)%s\n' % (fieldName, fieldSpecFor(fieldType,fieldSize), nullableSpecFor(fieldNull), autoIncrementSpecFor(fieldExtra), emitComma(isFirst))
		i += 1
		isFirst = (i < num)
	content += '\t\t)\n'
	content += '\treturn %s_table\n' % tableName
	return(content)

def camelCase(str):
	s = ''
	x = str.split('_')
	for t in x:
		s += t.capitalize()
	return s

def repeatSpecFor(aList, str):
	s = ''
	i = 1
	num = len(aList)
	isFirst = True
	for t in aList:
		s += str + emitComma(isFirst)
		i += 1
		isFirst = (i < num)
	return s

def repeatedTemplateFor(aList, col_names, str):
	s = ''
	i = 1
	num = len(aList)
	isFirst = True
	for row in aList:
		fieldName = row[col_names.index('column_name')]
		s += str + fieldName + emitComma(isFirst)
		i += 1
		isFirst = (i < num)
	return s

def generate_objSpec_from(aList, col_names, tableName):
	content = ''
	content += 'class %sObj(object):\n' % camelCase(tableName)
	content += '\tdef __init__(self,'
	isFirst = True
	num = len(aList)
	i = 1
	for row in aList:
		fieldName = row[col_names.index('column_name')]
		content += '%s%s' % (fieldName, emitComma(isFirst))
		i += 1
		isFirst = (i < num)
	content += '):\n'
	for row in aList:
		fieldName = row[col_names.index('column_name')]
		content += '\t\tself.%s = %s\n' % (fieldName, fieldName)
	content += '\n'
	content += 'def __repr__(self):\n'
	content += '\treturn "<%s(%s)>" %% (%s)\n' % (camelCase(tableName), repeatSpecFor(aList, '%r'), repeatedTemplateFor(aList, col_names, 'self.'))
	return(content)

def _writeFileFrom(fname, content):
	f = open(fname, 'w+')
	try:
		f.writelines(content)
	finally:
		f.close()

def writeFileFrom(fname, content):
	_writeFileFrom(fname, content)
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
		content += '"%s"%s' % (fn, emitComma(firstTime))
		firstTime = (i < num)
		i += 1
	content += ']\n'
	_writeFileFrom(initFname, content)
	
def showFieldsSQLStatement(engine,tableName):
	isMySQL = (str(engine).find('mysql://') > -1)
	isMSSQL = (str(engine).find('mssql://') > -1)
	if (isMySQL):
		return 'DESCRIBE %s' % tableName
	elif (isMSSQL):
		return "EXEC sp_columns @table_name = N'%s', @table_owner = N'dbo'" % tableName

def generate_initPY_from(files):
	content = '__all__ = ['
	i = 1
	n = len(files)
	for f in files:
		content += '"%s"%s' % (f,emitComma(i < n))
		i += 1
	content += ']\n'
	return content
	
def appendFileNameTo(files,fname):
	toks = fname.split('/')
	toks = toks[len(toks) - 1].split('.')
	files.append(toks[0])

def isRailsTargetValid(fpath):
	configFpath = fpath + '/config'
	try:
		configFiles = os.listdir(configFpath)
	except Exception, details:
		print 'ERROR - Missing config folder for Rails App due to (%s) !' % str(details)
		return False
	
	database_yml = 'database.yml'
	i = configFiles.index(database_yml)
	if (i > -1):
		y = readYML.ymlReader(configFpath + '/' + database_yml)
		y.read()
		yObj = y.objectsNamed('development')
		#print 'len(yObj)=(%s)' % str(len(yObj))
		if (len(yObj) == 1):
			pass
			#for y in yObj:
				#print 'y=(%s)' % str(y)
			#print '%s\n' % (('=' * 10) * 3)
	else:
		print 'WARNING - Missing database.yml for Rails App due !'
		return False
	return True

def railsModelNameFrom(fname):
	if (fname.endswith('hes')):
		return fname[0:len(fname)-2]
	if (fname.endswith('s')):
		fname = fname[0:len(fname)-1]
	if (fname.endswith('ie')):
		fname = fname[0:len(fname)-2] + 'y'
	return fname

def makeRailsObjectNameValid(name):
	return name[0].upper() + name[1:len(name)]
	
def generate_RailsModel_from(rName):
	return 'class %s < ActiveRecord::Base\nend' % makeRailsObjectNameValid(rName)

def camelCaseToRailsTableName(aName):
	_name = ""
	isDebugging = False
	isFirstLetter = True
	if (isDebugging):
		print 'camelCaseToRailsTableName() :: aName=%s' % (aName)
	for ch in aName:
		if (isDebugging):
			print 'camelCaseToRailsTableName() :: ch=%s' % (ch)
		if (ch.isupper()):
			if (isDebugging):
				print 'camelCaseToRailsTableName() :: isFirstLetter=%s' % (str(isFirstLetter))
			if (isFirstLetter):
				_name += "_"
				isFirstLetter = False
			_name += ch.lower()
		elif (ch == '_'):
			if (isFirstLetter):
				_name += ch
				isFirstLetter = False
		else:
			_name += ch
		if (isDebugging):
			print 'camelCaseToRailsTableName() :: _name=%s\n' % (_name)
	_begin = 0
	_end = len(_name)
	if (_name.startswith('_')):
		_begin += 1
	if (_name.endswith('_')):
		_end -= 1
	_name = _name[_begin:_end]
	i = _name.find('s')
	if (isDebugging):
		print 'camelCaseToRailsTableName() :: i=%s, len=%s' % (str(i),str(len(_name)))
	if ( (i > -1) and ((i+1) == len(_name)) ):
		if (isDebugging):
			print 'camelCaseToRailsTableName() :: _name[i-1]=%s' % (_name[i-1])
		if (_name[i-1] == 'y'):
			_name = _name[0:i-1] + 'ie' + _name[i:len(_name)]
		elif (_name[i-1] == 'h'):
			_name = _name[0:i] + 'e' + _name[i:len(_name)]
	if (isDebugging):
		print 'camelCaseToRailsTableName() :: _name=%s\n' % (_name)
	return _name

def writeTestCodeBegins():
	return 'num_errors = 0\n'

def writeTestCodeEnds():
	return "puts 'num_errors=' + num_errors.to_s\n"

def writeTestCodeFor(name,step=1):
	content = "puts '#BEGIN: %s'\n" % name
	if (step == 1):
		content += 'begin\n'
		content += '\trequire \'%s\'\n' % name
		content += 'rescue\n'
		content += "\tputs 'Unable to load (%s)\n'\n" % name
		content += '\tnum_errors += 1\n'
		content += 'end\n\n'
	else:
		content += 'begin\n'
		content += '\t%s.find(:first)\n' % name
		content += 'rescue\n'
		content += '\tnum_errors += 1\n'
		content += "\tputs 'Unable to query (%s)\n'\n" % name
		content += 'end\n'
		content += "puts '#END! %s\n'\n" % name
	content += '\n'
	return content

def expectedRailsTableName(name):
	toks = name.split('_')
	isDebugging = False
	if (isDebugging):
		print 'expectedRailsTableName() :: [%s] (%s) [%s]' % (name,str(len(toks)),str(toks))
	while (len(toks) > 2):
		x = toks.pop()
		if (isDebugging):
			print 'expectedRailsTableName() :: (%s) [%s]' % (x,str(toks))
		toks[len(toks)-1] += x
		if (isDebugging):
			print 'expectedRailsTableName() :: (%s) [%s]\n' % (str(len(toks)),str(toks))
	try:
		x = toks[0] + '_' + toks[1]
		if (isDebugging):
			print 'expectedRailsTableName() :: [%s]\n\n' % (x)
		return x
	except Exception:
		return toks[0]

def make_metadata_for(isVerbose,handle,aList,projName,target,targetPath):
	if (isVerbose):
		print 'BEGIN: make_metadata_for()'
	if (len(handle) != 2):
		print 'ERROR - Cannot proceed in "make_metadata_for" !'
		return
	engine = handle[0]
	conn = handle[1]
	cursor = conn.connection.cursor()

	isRails = (target == 'Rails')
	isSQLAlchemy = (target == 'SQLAlchemy')
	if (isVerbose):
		print 'isRails=%s, isSQLAlchemy=%s' % (str(isRails),str(isSQLAlchemy))
	
	if (isSQLAlchemy):
		fpath = 'meta/' + projName
		try:
			files = os.listdir(fpath)
		except Exception, details:
			os.makedirs(fpath)
			files = os.listdir(fpath)
	elif (isRails):
		fpath = targetPath + '/app/models/'
	
	_isRailsTargetValid = isRailsTargetValid(targetPath)
	if ( (isRails) and (_isRailsTargetValid == False) ):
		print 'WARNING - Invalid Rails Target - Make sure your database.yml file is configured correctly !'
		return
	
	print '%s\n' % (('=' * 10) * 5)
	files = []
	sqlCode = ''
	isAnyRailsProblems = False
	if ( (isRails) and (_isRailsTargetValid) ):
		for s in aList:
			c_names = camelCaseToRailsTableName(s)
			if (c_names.endswith('s')):
				c_name = c_names[0:len(c_names)-1]
				if (c_name.endswith('he')):
					c_name = c_name[0:len(c_name)-1]
			bool = s.endswith('s')
			s_name = expectedRailsTableName(s)
			if ( (bool == False) or (s != c_names) ):
				isAnyRailsProblems = True
				print '+++ bool=(%s), c_names=(%s), c_name=(%s), s=(%s), s_name=(%s)\n' % (bool,c_names,c_name,s,s_name)
				print '\nWARNING - Table with name of "%s" needs an "s" at the end of the name and the name cannot be composed of mixed case (aka. Camel Case) but rather using this pattern (%s) (%s) - this is a Rails Standard.\n' % (s,c_names,s_name)
				sqlCode += "EXEC sp_rename 'dbo.%s', '%s';\n" % (s,c_names)
		if (isAnyRailsProblems):
			print '\nWARNING - Too many Rails exceptions - cannot continue processing.'
			if (len(sqlCode) > 0):
				print '\nINFO - SQL Code has been dumped into the target folder to correct the Table Naming Problems.'
				sql_fname = fpath + '/sqlCode.sql'
				writeFileFrom(sql_fname, sqlCode)
			return -1
	tCode = writeTestCodeBegins()
	tCode2 = ''
	for s in aList:
		if (isSQLAlchemy):
			table_fname = s + '_table.py'
			obj_fname = camelCase(s) + 'Obj.py'
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
					rows = cursor.columns(table=s).fetchall()
					col_names = [ t[0] for t in rows[0].cursor_description ]
					if (isVerbose):
						for row in rows:
							for n in col_names:
								print '%s=(%s)' % (n,str(row[col_names.index(n)]))
							print '%s\n' % (('=' * 10) * 3)
					mCode = generate_metadata_from(rows, col_names, s)
					if (isVerbose):
						print mCode
					writeFileFrom(table_fname, mCode)
					appendFileNameTo(files,table_fname)
					oCode = generate_objSpec_from(rows, col_names, s)
					if (isVerbose):
						print oCode
					writeFileFrom(obj_fname, oCode)
					appendFileNameTo(files,obj_fname)
				except Exception, details:
					print 'ERROR - Skipping "%s" due to (%s)...' % (s, str(details))
				print '%s\n' % (('=' * 10) * 6)
		elif ( (isRails) and (_isRailsTargetValid) ):
			_slash = ''
			if (fpath.endswith('/') == False):
				_slash += '/'
			_railsName = railsModelNameFrom(camelCase(s))
			model_fname = '%s%s%s.rb' % (fpath,_slash,_railsName)
			if (isVerbose):
				print 'model_fname=(%s)' % model_fname
			rCode = generate_RailsModel_from(_railsName)
			if (isVerbose):
				print rCode
			writeFileFrom(model_fname, rCode)
			if (isVerbose):
				print '%s\n' % (('=' * 10) * 6)
			tCode += writeTestCodeFor(_railsName,1)
			tCode2 += writeTestCodeFor(_railsName,2)
	#print 'files=(%s)' % str(files)
	if ( (isSQLAlchemy) and (len(files) > 0) ):
		init_fname = fpath + '/__init__.py'
		iCode = generate_initPY_from(files)
		if (isVerbose):
			print iCode
		writeFileFrom(init_fname, iCode)
	if (isVerbose):
		print '%s\n' % (('=' * 10) * 8)
	if ( (isRails) and (_isRailsTargetValid) ):
		tCode2 += writeTestCodeEnds()
		test_fname = fpath + '/test.rb'
		writeFileFrom(test_fname, tCode + tCode2)
	if (isVerbose):
		print 'END! make_metadata_for()'
	
def run(isVerbose, projName, ymlObject, target, _targetPath):
	isVerbose = (isVerbose == True) if isVerbose else False
	version = sqlalchemy.__version__
	if (isVerbose):
		print 'BEGIN: run()'
		print 'projName=%s' % projName
		print 'version=%s' % version
		print 'target=%s' % target
		print 'targetPath=%s' % _targetPath

	handle = dbConnectionFromYML(ymlObject)
	if handle == None:
		print 'WARNING -- Unable to make a handle for the database.  Processing halts.'
		return
	
	engine = handle[0]
	conn = handle[1]

	tables = engine.table_names()

	items = []
	iCount = 0
	for t in tables:
		canShow = True
		if (t.find('utt_') > -1):
			canShow = False
		if (canShow):
			items.append(t)
			if (isVerbose):
				print '# %r :: (%s)' % (iCount, t)
				iCount += 1
		
	print 'items=(%s)' % str(items)
	make_metadata_for(isVerbose,handle,items,projName,target,_targetPath)

	if (isVerbose):
		print 'END! run()'
	#conn.close()

def splitToksFrom(str,delim):
	return 	str.split(delim)

print 'sys.argv.__class__=%s' % sys.argv.__class__
print 'sys.argv=%s' % str(sys.argv)
if ( (len(sys.argv) == 1) or (sys.argv[1] == '--help') ):
	print '--help ... displays this help text'
	print '--yml=path to database.yml file'
	print '--pwd=plain-text password to obscure'
elif (sys.argv[1].find('--pwd=') > -1):
	toks = splitToksFrom(sys.argv[1],'=')
	if (len(toks) == 2):
		pwd = toks[1]
		_pwd = ObscurePhrase.ObscurePhraseAsHex(ObscurePhrase.ObscurePhrase(pwd))
		print 'Copy and paste this password into the database.yml file (%s)' % (_pwd)
elif (sys.argv[1].find('--yml=') > -1):
	toks = splitToksFrom(sys.argv[1],'=')
	if (len(toks) == 2):
		try:
			y = readYML.ymlReader(toks[1])
			y.read()
			yObj = y.objects
			for yo in y.objects:
			    print str(yo)
			    print '==========' * 5
			list = y.objectsNamed('process')
			print 'list=' + str(list)
			_use = ''
			_projName = ''
			_verbose = False
			for l in list:
			    print str(l)
			    _use = l.attrValueForName('use')
			    print 'use=[%s]' % _use
			    print '==========' * 6
			    _projName = l.attrValueForName('project-name')
			    print 'project-name=[%s]' % _use
			    print '==========' * 6
			    _target = l.attrValueForName('target')
			    print 'target=[%s]' % _target
			    print '==========' * 6
			    _targetPath = l.attrValueForName('target-path').replace('\\','/')
			    print 'targetPath=[%s]' % _targetPath
			    print '==========' * 6
			    v = l.attrValueForName('verbose')
			    if ( (v == 1) or (v == '1') or (v == 'True') or (v == 'true') ):
				    _verbose = True
			    print 'verbose=[%s]' % _verbose
			    print '==========' * 6
			if ( (len(_use) > 0) and (len(_projName) > 0) ):
				list = y.objectsNamed(_use)
				print 'list=' + str(list)
				print '==========' * 5
				for l in list:
					print 'Recap: (%s)' % (str(l))
					print '==========' * 6
					run(_verbose,_projName,l,_target,_targetPath)
		except Exception, details:
			print 'ERROR due to (%s)' % str(details)

