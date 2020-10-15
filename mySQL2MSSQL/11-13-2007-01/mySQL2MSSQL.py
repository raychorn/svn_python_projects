import os
import sys
import psyco
import pyodbc
import lib.threadpool
import lib._pyodbc
import lib.readYML
import threading
import win32api
import win32con

_isVerbose = False
_isCommit = False
_createTables = False
_migrateData = False
_dataTypes = False

_sourceDSN = ''
_destDSN = ''
_programName = ''
_yml_filename = 'odbc.yml'

_type_conversions = {}

_pool = lib.threadpool.Pool(500)

_mssql_connection_string = 'DRIVER={SQL Server};SERVER=UNDEFINED2;DATABASE=reports_development;CommandTimeout=0;UID=sa;PWD=peekab00'
_mysql_connection_string = 'DRIVER={MySQL ODBC 3.51 Driver};SERVER=localhost;DATABASE=reports_development;CommandTimeout=0;UID=root;PWD=peekaboo'

_sourceDSN = _mysql_connection_string
_destDSN = _mssql_connection_string

const_table_symbol = 'TABLE'

const_table_name_symbol = '_table_name'
const_column_name_symbol = '_column_name'
const_column_size_symbol = '_column_size'
const_type_name_symbol = '_type_name'
const_is_nullable_symbol = '_is_nullable'
const_auto_symbol = '_auto'

const_data_type_map_symbol = 'data_type_map.txt'

dst_table_names = {}

def getComputerNamesDict():
    cNameEx = {}
    cNameEx['win32con.ComputerNameDnsDomain'] = win32api.GetComputerNameEx(win32con.ComputerNameDnsDomain)
    cNameEx['win32con.ComputerNameDnsFullyQualified'] = win32api.GetComputerNameEx(win32con.ComputerNameDnsFullyQualified)
    cNameEx['win32con.ComputerNameDnsHostname'] = win32api.GetComputerNameEx(win32con.ComputerNameDnsHostname)
    cNameEx['win32con.ComputerNameNetBIOS'] = win32api.GetComputerNameEx(win32con.ComputerNameNetBIOS)
    cNameEx['win32con.ComputerNamePhysicalDnsDomain'] = win32api.GetComputerNameEx(win32con.ComputerNamePhysicalDnsDomain)
    cNameEx['win32con.ComputerNamePhysicalDnsFullyQualified'] = win32api.GetComputerNameEx(win32con.ComputerNamePhysicalDnsFullyQualified)
    cNameEx['win32con.ComputerNamePhysicalDnsHostname'] = win32api.GetComputerNameEx(win32con.ComputerNamePhysicalDnsHostname)
    cNameEx['win32con.ComputerNamePhysicalNetBIOS'] = win32api.GetComputerNameEx(win32con.ComputerNamePhysicalNetBIOS)
    return cNameEx

def getTypeInfo(dsn,type):
    d = {}
    try:
        dbh = pyodbc.connect(dsn)
        _cursor = dbh.cursor()
        for r in _cursor.getTypeInfo(type):
            try:
                d['type_name'] = r.type_name
            except:
                d['type_name'] = 'unknown'
            try:
                d['data_type'] = r.data_type
            except:
                d['data_type'] = 'unknown'
            try:
                d['column_size'] = r.column_size
            except:
                d['column_size'] = 'unknown'
            try:
                d['literal_prefix'] = r.literal_prefix
            except:
                d['literal_prefix'] = 'unknown'
            try:
                d['literal_suffix'] = r.literal_suffix
            except:
                d['literal_suffix'] = 'unknown'
            try:
                d['create_params'] = r.create_params
            except:
                d['literal_suffix'] = 'unknown'
            try:
                d['nullable'] = r.nullable
            except:
                d['nullable'] = 'unknown'
            try:
                d['case_sensitive'] = r.case_sensitive
            except:
                d['case_sensitive'] = 'unknown'
            try:
                d['searchable'] = r.searchable
            except:
                d['searchable'] = 'unknown'
            try:
                d['unsigned_attribute'] = r.unsigned_attribute
            except:
                d['unsigned_attribute'] = 'unknown'
            try:
                d['fixed_prec_scale'] = r.fixed_prec_scale
            except:
                d['fixed_prec_scale'] = 'unknown'
            try:
                d['auto_unique_value'] = r.auto_unique_value
            except:
                d['auto_unique_value'] = 'unknown'
            try:
                d['local_type_name'] = r.local_type_name
            except:
                d['local_type_name'] = 'unknown'
            try:
                d['minimum_scale'] = r.minimum_scale
            except:
                d['minimum_scale'] = 'unknown'
            try:
                d['maximum_scale'] = r.maximum_scale
            except:
                d['maximum_scale'] = 'unknown'
            try:
                d['sql_data_type'] = r.sql_data_type
            except:
                d['sql_data_type'] = 'unknown'
            try:
                d['sql_datetime_sub'] = r.sql_datetime_sub
            except:
                d['sql_datetime_sub'] = 'unknown'
            try:
                d['num_prec_radix'] = r.num_prec_radix
            except:
                d['num_prec_radix'] = 'unknown'
            try:
                d['interval_precision'] = r.interval_precision
            except:
                d['interval_precision'] = 'unknown'
    except Exception, details:
        print '(getTypeInfo) :: "%s".' % (str(details))
    dbh.close()
    return d

def writeDataTypes(list):
    try:
        fHand = open('data_types.txt','w')
        fHand.writelines('\n'.join(list))
        fHand.close()
    except:
        pass

def readDataTypeMap():
    d = {}
    list = []
    try:
        fHand = open(const_data_type_map_symbol,'r')
        list = [l.strip() for l in fHand.readlines()]
        fHand.close()
    except:
        pass
    for l in list:
        toks = l.split('=')
        d[toks[0]] = toks[-1]
    return d

@lib.threadpool.threadpool(_pool)
def processSQLStatement(sql):
    lib._pyodbc.exec_and_process_sql(_destDSN,sql,None,useCommit=_isCommit,useClose=True)

@lib.threadpool.threadpool(_pool)
def processSQLCode(list):
    for l in list:
        processSQLStatement('\n'.join(l))

def handleNullValues(val):
    if (str(val.__class__).find("'NoneType'") > -1):
        return 'NULL'
    return val

def convertSourceDataIntoDestDataUsing(data_list,srcTypes,dstTypes):
    print '(convertSourceDataIntoDestDataUsing) :: [%s] :: data_list=(%s)' % (str(data_list.__class__),str(data_list))
    print '(convertSourceDataIntoDestDataUsing) :: [%s] :: srcTypes=(%s)' % (str(srcTypes.__class__),str(srcTypes))
    print '(convertSourceDataIntoDestDataUsing) :: [%s] :: dstTypes=(%s)' % (str(dstTypes.__class__),str(dstTypes))
    print '\n'
    for i in xrange(len(srcTypes)):
        isConversionRequired = False
        toks = dstTypes[i].split(' ')
        #print '(convertSourceDataIntoDestDataUsing).1 :: _type_conversions.has_key(srcTypes[%s])=(%s)' % (i,_type_conversions.has_key(srcTypes[i]))
        if (_type_conversions.has_key(srcTypes[i])):
            #print '(convertSourceDataIntoDestDataUsing).2 :: toks[0]=(%s), srcTypes[%s]=(%s), _type_conversions[%s]=(%s)' % (toks[0],i,srcTypes[i],srcTypes[i],_type_conversions[srcTypes[i]])
            if (toks[0] == _type_conversions[srcTypes[i]]):
                pass
            else:
                isConversionRequired = True
        else:
            isConversionRequired = True
        #print '(convertSourceDataIntoDestDataUsing).3 :: isConversionRequired=(%s)' % (isConversionRequired)
        if (isConversionRequired):
            if ( (srcTypes[i] == 'datetime.datetime') and (toks[0] == 'bigint') ):
                d = data_list[i]
                v = d.toordinal()
                print '(convertSourceDataIntoDestDataUsing) :: Converting from "%s" (%s) to "%s" (%s) !' % (srcTypes[i],d,toks[0],v)
            else:
                print '(convertSourceDataIntoDestDataUsing) :: Conversion from "%s" to "%s" required !' % (srcTypes[i],toks[0])

def dataTypesDictFor(dstDSN,table_name):
    dbh = pyodbc.connect(dstDSN)
    _cursor = dbh.cursor()
    dataTypesDict = {}
    for c in _cursor.columns(table=table_name):
        dataTypesDict[c.column_name] = getTypeInfo(dstDSN,c.data_type)
    dbh.close()
    return dataTypesDict

def specificDataTypesFrom(dict):
    dataTypesDict = {}
    for k in dict.keys():
        d = dict[k]
        if (d.has_key('type_name')):
            dataTypesDict[k] = d['type_name'].lower()
    return dataTypesDict

def copyDataFromTo(_srcDSN,_sql_statement,_dstDSN,_table_name,_cols):
    def handleSourceData(rows):
        if (str(rows.__class__).find("'pyodbc.Cursor'") > -1):
            if (_isVerbose):
                print '(handleSourceData) :: _table_name=(%s)' % _table_name
                print '(handleSourceData) :: _dstDSN=(%s)' % _dstDSN
                print '(handleSourceData) :: rows.description=(%s)' % str(rows.description)
            colNames = []
            colTypes = []
            for col in rows.description:
                colNames.append(col[0])
                toks = str(col[1]).lower()[1:-1].replace("'","").split(' ')
                colTypes.append(toks[-1])
            rowCnt = 0
            sql = ''
            try:
                dbhDst = pyodbc.connect(_dstDSN)
                _cursorDst = dbhDst.cursor()
                dataTypesDst = {}
                for c in _cursorDst.columns(table=_table_name):
                    dataTypesDst[c.column_name] = getTypeInfo(_dstDSN,c.data_type)
                colTypesDst = []
                for n in colNames:
                    if (dataTypesDst.has_key(n)):
                        d = dataTypesDst[n]
                        if (d.has_key('type_name')):
                            colTypesDst.append(d['type_name'].lower())
                for row in rows:
                    data_elements = []
                    for i in xrange(len(colNames)):
                        data_elements.append(row[i])
                    convertSourceDataIntoDestDataUsing(data_elements,colTypes,colTypesDst)
                    for i in xrange(len(colNames)):
                        if (colTypes[i] == 'str'):
                            data_elements[i] = "'%s'" % handleNullValues(data_elements[i]).replace("'","''")
                        elif (colTypes[i] == 'datetime.datetime'):
                            data_elements[i] = "'%s'" % handleNullValues(data_elements[i])
                        else:
                            data_elements[i] = '%s' % handleNullValues(data_elements[i])
                    sql = "INSERT INTO %s (%s) VALUES (%s)" % (_table_name,','.join(colNames),','.join(data_elements))
                    _cursorDst.execute(sql)
                    dbhDst.commit()
                    rowCnt += 1
            except Exception, details:
                print '(handleSourceData).ERROR :: "%s"\nSQL_STATEMENT=[%s]\ncolTypes=(%s).\n' % (details,sql,str(colTypes))
            print '(handleSourceData) :: _table_name=(%s), rowCnt=(%s)' % (_table_name,rowCnt)
            dbhDst.close()
    if (_table_name.startswith('utt_') == False):
        if (_isVerbose):
            print '(copyDataFromTo) :: _srcDSN=(%s)' % _srcDSN
            print '(copyDataFromTo) :: _sql_statement=(%s)' % _sql_statement
            print '(copyDataFromTo) :: _dstDSN=(%s)' % _dstDSN
            print '(copyDataFromTo) :: _table_name=(%s)' % _table_name
            print '(copyDataFromTo) :: _cols=(%s)' % str(_cols)
            print '\n'
        lib._pyodbc.exec_and_process_sql(_sourceDSN,_sql_statement,handleSourceData,useCommit=False,useClose=False)
        print '\n'

def main(srcDSN,dstDSN):
    print '(main) :: srcDSN=(%s)' % srcDSN
    print '(main) :: dstDSN=(%s)' % dstDSN

    unique_type_names = {}

    try:
        dbhSrc = pyodbc.connect(srcDSN)
        dbhDst = pyodbc.connect(dstDSN)

        _cursorSrc = dbhSrc.cursor()

        _cursorDst = dbhDst.cursor()

        tables = _cursorSrc.tables()

        tables_names = []
        for row in tables:
            if (str(row.table_type).upper() == const_table_symbol):
                tables_names.append([row.table_cat,row.table_schem,row.table_name,row.table_type])

        tables = _cursorDst.tables()

        for row in tables:
            if (str(row.table_type).upper() == const_table_symbol):
                dst_table_names[row.table_name] = [row.table_cat,row.table_schem,row.table_name,row.table_type]

        print '(main) :: len(tables_names)=(%s)' % (len(tables_names))

        print '(main) :: len(dst_table_names)=(%s)' % (len(dst_table_names))

        data_type_map = readDataTypeMap()

        tables_list = []
        i = 0
        for row in tables_names:
            i += 1
            dTable = {}
            dTable[const_table_name_symbol] = row[2]
            dCols = []
            if (_isVerbose):
                print '(%s) :: (main) :: cat=(%s), schema=(%s), name=(%s), type=(%s)\n' % (i,row[0],row[1],row[2],row[3])
            for col in _cursorSrc.columns(table=row[2],catalog=row[0],schema=row[1]):
                if (_isVerbose):
                    print '\t(main) :: column_name=(%s)' % (col.column_name)
                    print '\t(main) :: column_size=(%s)' % (col.column_size)
                    print '\t(main) :: buffer_length=(%s)' % (col.buffer_length)
                    print '\t(main) :: decimal_digits=(%s)' % (col.decimal_digits)
                    print '\t(main) :: num_prec_radix=(%s)' % (col.num_prec_radix)
                    print '\t(main) :: nullable=(%s)' % (col.nullable)
                    print '\t(main) :: remarks=(%s)' % (col.remarks)
                    if (col.column_def):
                        print '\t(main) :: column_def=(%s)' % (col.column_def)
                    if (col.sql_datetime_sub):
                        print '\t(main) :: sql_datetime_sub=(%s)' % (col.sql_datetime_sub)
                    if (col.char_octet_length):
                        print '\t(main) :: char_octet_length=(%s)' % (col.char_octet_length)
                    print '\t(main) :: ordinal_position=(%s)' % (col.ordinal_position)
                    print '\t(main) :: is_nullable=(%s)' % (col.is_nullable)
                    print '\t\t(main) :: type_name=(%s)' % (col.type_name)
                _type_name = col.type_name
                if (_type_name == 'varchar'):
                    _type_name = '[%s](%s)' % (_type_name,col.column_size)
                if (unique_type_names.has_key(_type_name) == False):
                    unique_type_names[_type_name] = col.data_type
                if (_isVerbose):
                    print '\t\t(main) :: sql_data_type=(%s)' % (col.sql_data_type)
                    print '\t\t(main) :: data_type=(%s)' % (col.data_type)
                dTypes = getTypeInfo(srcDSN,col.data_type)
                isAuto = False
                for k in dTypes.keys():
                    if ( (dTypes[k]) and (str(dTypes[k]).lower() != 'unknown') ):
                        if (k == 'type_name'):
                            isAuto = (dTypes[k].lower().find('auto_increment') > -1)
                        if (_isVerbose):
                            print '\t\t(main.dTypes) :: %s=(%s)' % (k,dTypes[k])
                dCols.append(col.column_name)
                dCol = {}
                dCol[const_column_name_symbol] = col.column_name
                dCol[const_column_size_symbol] = col.column_size
                if (data_type_map.has_key(_type_name)):
                    dCol[const_type_name_symbol] = data_type_map[_type_name]
                else:
                    dCol[const_type_name_symbol] = _type_name
                dCol[const_is_nullable_symbol] = (col.is_nullable.upper() == 'YES')
                dCol[const_auto_symbol] = isAuto
                dTable[col.column_name] = dCol
                if (_isVerbose):
                    print '\n'
            dTable['_cols'] = dCols
            tables_list.append(dTable)
            if (_isVerbose):
                print '\n'

        _sql_code = []

        print '(main) :: len(tables_list)=(%s)\n' % (len(tables_list))
        if (_createTables):
            for d in tables_list:
                sql_statement = []
                table_name = d[const_table_name_symbol]
                if (dst_table_names.has_key(table_name)):
                    sql_statement.append('DROP TABLE [dbo].[%s];' % table_name)
                    sql_statement.append('')
                sql_statement.append('CREATE TABLE [dbo].[%s]' % table_name)
                sql_statement.append('(')
                cols = d['_cols']
                for c in cols:
                    dCol = d[c]
                    _null_option = 'NOT NULL'
                    if (dCol[const_is_nullable_symbol] == True):
                        _null_option = 'NULL'
                    _comma = ','
                    if (c == cols[-1]):
                        _comma = ''
                    if (dCol[const_type_name_symbol].find('varchar') > -1):
                        sql_statement.append('[%s] %s %s%s' % (dCol[const_column_name_symbol],dCol[const_type_name_symbol],_null_option,_comma))
                    else:
                        sql_statement.append('[%s] [%s] %s%s' % (dCol[const_column_name_symbol],dCol[const_type_name_symbol],_null_option,_comma))
                sql_statement.append(');')
                sql_statement.append('')
                _sql_code.append(sql_statement)

        print '(main) :: len(_sql_code)=(%s)' % len(_sql_code)
        processSQLCode(_sql_code)
        _pool.join()

        print '\n'
        if (_migrateData):
            for d in tables_list:
                sql_statement = ''
                table_name = d[const_table_name_symbol]
                typesDst = dataTypesDictFor(dstDSN,table_name)
                specTypesDst = specificDataTypesFrom(typesDst)
                print '(main) :: specTypesDst=(%s)' % str(specTypesDst)
                typesSrc = dataTypesDictFor(srcDSN,table_name)
                print '(main) :: typesSrc=(%s)' % str(typesSrc)
                specTypesSrc = specificDataTypesFrom(typesSrc)
                print '(main) :: specTypesSrc=(%s)' % str(specTypesSrc)
                column_list = []
                cols = d['_cols']
                for c in cols:
                    dCol = d[c]
                    column_list.append(dCol[const_column_name_symbol])
                sql_statement += 'SELECT %s FROM %s' % (','.join(column_list),table_name)
                print '(main) :: sql_statement=[%s]' % sql_statement
                copyDataFromTo(srcDSN,sql_statement,dstDSN,table_name,cols)

        _pool.join()

        dbhSrc.close()
        dbhDst.close()
    except Exception, details:
        print '(main).Error_1 :: (%s)' % (str(details))

    if (_dataTypes):
        writeDataTypes(unique_type_names.keys())

    _pool.join()

if ( (len(sys.argv) == 1) or (sys.argv[1] == '--help') ):
    print '--help                      ... displays this help text.'
    print '--verbose                   ... output more stuff.'
    print '--tables                    ... creates tables.'
    print '--commit                    ... commits database actions.'
    print '--data                      ... migrates data.'
    print '--types                     ... scans for data types (removes --tables, --commit and --data).'
    print '--yml=yml_filename          ... yml file name (may use in-place of --sourceDSN and --destDSN).'
    print '--sourceDSN=data_source_spec... data source spec (may use in-place of --yml).'
    print '--destDSN=data_source_spec  ... data source spec (may use in-place of --yml).'
else:
    toks = sys.argv[0].split(os.sep)
    _programName = toks[-1]
    for i in xrange(len(sys.argv)):
        bool = ( (sys.argv[i].find('--sourceDSN=') > -1) or (sys.argv[i].find('--destDSN=') > -1) or (sys.argv[i].find('--yml=') > -1) )
        if (bool): 
            toks = sys.argv[i].split('=')
            if (sys.argv[i].find('--sourceDSN=') > -1):
                _sourceDSN = toks[1]
            elif (sys.argv[i].find('--destDSN=') > -1):
                _destDSN = toks[1]
            elif (sys.argv[i].find('--yml=') > -1):
                _yml_filename = toks[1]
                ymlReader = lib.readYML.ymlReader(_yml_filename)
                ymlReader.read()
                cName = win32api.GetComputerName()
                try:
                    n = 'source_%s' % cName
                    yml = ymlReader.objectsNamed(n)
                    _sourceDSN = (yml[0]).attrValueForName('connection_string')
                    print '(init) :: n=(%s), sourceDSN=(%s)' % (n,_sourceDSN)
                    n = 'dest_%s' % cName
                    yml = ymlReader.objectsNamed(n)
                    _destDSN = (yml[0]).attrValueForName('connection_string')
                    print '(init) :: n=(%s), destDSN=(%s)' % (n,_destDSN)
                    yml = ymlReader.objectsNamed('type_conversions')
                    _type_conversions = {}
                    for y in yml[0].ymlAttrs():
                        _type_conversions[y.key] = y.value
                    print '(init) :: type_conversions=(%s)' % str(_type_conversions)
                except Exception, details:
                    print '(init).ERROR_READING_YML_FILE :: "%s"' % str(details)
        elif (sys.argv[i].find('--verbose') > -1):
            _isVerbose = True
        elif (sys.argv[i].find('--commit') > -1):
            _isCommit = True
        elif (sys.argv[i].find('--tables') > -1):
            _createTables = True
        elif (sys.argv[i].find('--data') > -1):
            _migrateData = True
        if (sys.argv[i].find('--types') > -1):
            _dataTypes = True
            _migrateData = False
            _isCommit = False
            _createTables = False;
psyco.bind(main)
main(_sourceDSN,_destDSN)