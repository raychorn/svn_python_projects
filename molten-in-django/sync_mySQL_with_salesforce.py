import os, sys

import molten_tables
import sqlalchemy_models

from vyperlogix.daemon.daemon import Log
from vyperlogix.daemon.daemon import EchoLog

from vyperlogix.sf.cases import SalesForceCases
from vyperlogix.sf.contacts import SalesForceContacts
from vyperlogix.sf.accounts import SalesForceAccounts
from vyperlogix.sf.record_types import SalesForceRecordTypes

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.misc.ReportTheList import reportTheList

from vyperlogix.enum import Enum

from maglib.salesforce.cred import credentials
from maglib.salesforce.auth import CredentialTypes
from maglib.salesforce.auth import magma_molten_passphrase

_use_staging = False

__sf_account__ = credentials(magma_molten_passphrase,CredentialTypes.Magma_RHORN_Production)

from vyperlogix.wx.pyax.SalesForceLoginModel import SalesForceLoginModel
sf_login_model = SalesForceLoginModel(username=__sf_account__['username'],password=__sf_account__['password'])

__root__ = os.path.dirname(sys.argv[0])

_bash_name = '%s.sh' % (os.path.splitext(os.path.basename(sys.argv[0]))[0])

_bash_job = '''
export PYTHONPATH=/opt/ActivePython-2.5/lib:/home/admin/molten_utils/VyperLogixLib-1.0-py2.5.egg:/home/admin/molten_utils/VyperLogixMagmaLib-1.0-py2.5.egg:%s:/home/admin/molten_utils/pyax:$PYTHONPATH

export PYTHON_EGG_CACHE=/home/admin/python-eggs

svn update /home/admin/molten_utils/pyax

'''

_account_names = ['Micron','Toshiba','Stream Processors','IDT','Server Engines','Tensilica','Uniquify','Silicon Blue','ARM','Beceem']

# Notes:
#
# Problems:
# 
# 1). Make sure all records in mySQL exist in SalesForce.
# 2). Make sure all records that exist in SalesForce have been downloaded to mySQL.
#
# All Cases that are in SalesForce gets downloaded however Cases that are in mySQL get removed before being downloaded.
# --> Remove all Cases from mySQL for the Accounts before considering SalesForce because we are downloading Cases.

def determine_data_dictionary(sf_keys,case_from_mySQL):
    d_reportTheList = lists.HashedLists2()
    d_xlator = lists.HashedLists2()

    _cannot_locate_these = []

    _case_keys_set = set(case_from_mySQL.__dict__.keys())
    for _case in [case_from_mySQL]:
        for key in sf_keys:
            _key = key.lower()
            if (key.lower() == 'id'):
                _key = 'sf_id'
                try:
                    _case.__getattribute__(_key)
                    _exists = True
                    _case_keys_set.remove(_key)
                    d_xlator[key] = _key
                except AttributeError:
                    _cannot_locate_these.append(key)
                    _exists = False
            elif (key.lower() == 'type'):
                _key = 'sf_type'
                try:
                    _case.__getattribute__(_key)
                    _exists = True
                    _case_keys_set.remove(_key)
                    d_xlator[key] = _key
                except AttributeError:
                    _cannot_locate_these.append(key)
                    _exists = False
            else:
                try:
                    _case.__getattribute__(_key)
                    _exists = True
                    _case_keys_set.remove(_key)
                    _key_ = _utils.de_camel_case(key,delim='_',method=_utils.DeCamelCaseMethods.force_lower_case)
                    if (_key != _key_):
                        try:
                            _case.__getattribute__(_key_)
                            _case_keys_set.remove(_key_)
                            d_xlator[key] = [_key,_key_]
                        except AttributeError:
                            d_xlator[key] = _key
                    else:
                        d_xlator[key] = _key
                except AttributeError:
                    _key = _key.replace('__c','_id__c')
                    try:
                        _case.__getattribute__(_key)
                        _exists = True
                        _case_keys_set.remove(_key)
                        d_xlator[key] = _key
                    except AttributeError:
                        _key = _utils.de_camel_case(key,delim='_',method=_utils.DeCamelCaseMethods.force_lower_case)
                        try:
                            _case.__getattribute__(_key)
                            _exists = True
                            _case_keys_set.remove(_key)
                            d_xlator[key] = _key
                        except AttributeError:
                            try:
                                _case.__getattribute__(_key)
                                _exists = True
                                _case_keys_set.remove(_key)
                                d_xlator[key] = _key
                            except AttributeError:
                                _cannot_locate_these.append(key)
                                _exists = False
    if (len(_case_keys_set) > 0) and (d_reportTheList['_case_keys_set'] is None):
        ignore_mySQL_fields = ['_sa_instance_state']
        for item in ignore_mySQL_fields:
            _case_keys_set.remove(item)
        reportTheList(list(_case_keys_set), 'Cannot Locate these Fields from mySQL in SalesForce for sfCase.')
        d_reportTheList['_case_keys_set'] = True
    if (len(_cannot_locate_these) > 0) and (d_reportTheList['_cannot_locate_these'] is None):
        reportTheList(_cannot_locate_these, 'Cannot Locate these Fields from SalesForce in mySQL for sfCase.')
        d_reportTheList['_cannot_locate_these'] = True
    return d_xlator,_cannot_locate_these,list(_case_keys_set)

class ReplicationMethods(Enum.Enum):
    none = 2**0
    check = 2**1
    replicate = 2**2

def make_value_appropriate(d,aKey,value):
    '''This function performs a two-way transformation taking SalesForce data into mySQL data and vice-versa.'''
    aField = d[aKey]
    aField_soapType = aField['soapType']
    if (value is None):
        if (aField_soapType in ['tns:ID','xsd:string']):
            value = ''
        elif (aField_soapType in ['xsd:double','xsd:date','xsd:dateTime']):
            pass # do nothing - pass along the None value...
        else:
            pass
    elif (aField_soapType in ['xsd:boolean']):
        if (not isinstance(value,bool)):
            value = True if (value == '1') else False
        else:
            value = '1' if (value == True) else '0'
    elif (aField_soapType in ['xsd:dateTime']):
        if (ObjectTypeName.typeClassName(value).find('.datatype.apexdatetime.ApexDatetime') > -1):
            value = _utils.getAsDateTimeStr(_utils.getDatetimeFromApexDatetime(value),fmt=_utils.format_mySQL_DateTimeStr())
        elif (isinstance(value,str)):
            value = _utils.getFromDateTimeStr(value,_utils.format_mySQL_DateTimeStr())
    elif (aField_soapType in ['xsd:double']):
        if (isinstance(value,float)):
            value = str(value)
    elif (aField_soapType in ['xsd:string']):
        if (isinstance(value,str)):
            if (all([ch.isdigit() for ch in value])):
                value = long(value)
    elif (aField_soapType in ['tns:ID']):
        if (isinstance(value,str)) and (len(value) == 0):
            value = None
    else:
        pass
    return value

def check_or_replicate_data(aCase,_case,d_xlator,d_metadata_by_names=lists.HashedFuzzyLists2(),sf_cannot_locate=None,method=ReplicationMethods.none):
    d = lists.HashedLists2()
    if (sf_cannot_locate is not None):
        d_sf_cannot_locate = lists.HashedLists2(dict([(item,item) for item in sf_cannot_locate]))
    _ignored = []
    _cannot_locate = []
    _count = 1
    _expected_key_count = 0
    for aKey in aCase.keys():
        if (d_xlator.has_key(aKey)):
            try:
                d_key = d_xlator[aKey]
                v = aCase[aKey]
                if (isinstance(d_key,list)):
                    for item in d_key:
                        if (method == ReplicationMethods.check):
                            _v = _case.__getattribute__(item)
                            try:
                                v = make_value_appropriate(d_metadata_by_names,aKey,v)
                            except Exception, _details:
                                info_string = _utils.formattedException(details=_details)
                                pass
                            try:
                                if (v != _v):
                                    k = '%s --> %s' % (aKey,item)
                                    d[k] = '%s != %s' % (v,_v)
                            except TypeError:
                                if (type(v) != type(_v)) and (ObjectTypeName.typeClassName(_v).find('.datetime') > -1) and (ObjectTypeName.typeClassName(v).find('.ApexDatetime') > -1):
                                    if (v.isoformat().split('+')[0] != _v.isoformat().split('+')[0]):
                                        k = '%s --> %s' % (aKey,d_key)
                                        d[k] = '%s != %s' % (v,_v)
                                else:
                                    pass
                            except Exception, _details:
                                info_string = _utils.formattedException(details=_details)
                                print >>sys.stderr, info_string
                        elif (method == ReplicationMethods.replicate):
                            v = make_value_appropriate(d_metadata_by_names,aKey,v)
                            _case.__setattr__(item,v)
                            k = '%s --> %s' % (aKey,item)
                            d[k] = str(v) if (v is None) else v
                        _expected_key_count += 1
                else:
                    if (method == ReplicationMethods.check):
                        _v = _case.__getattribute__(d_key)
                        try:
                            v = make_value_appropriate(d_metadata_by_names,aKey,v)
                            if (ObjectTypeName.typeClassName(v) != ObjectTypeName.typeClassName(_v)):
                                if (ObjectTypeName.typeClassName(_v) == 'str'):
                                    v = str(v)
                                elif (ObjectTypeName.typeClassName(v) == 'str'):
                                    _v = str(_v)
                        except Exception, _details:
                            info_string = _utils.formattedException(details=_details)
                            pass
                        try:
                            if (v != _v):
                                k = '%s --> %s' % (aKey,d_key)
                                d[k] = '%s != %s' % (v,_v)
                        except TypeError:
                            if (type(v) != type(_v)) and (ObjectTypeName.typeClassName(_v).find('.datetime') > -1) and (ObjectTypeName.typeClassName(v).find('.ApexDatetime') > -1):
                                if (v.isoformat().split('+')[0] != _v.isoformat().split('+')[0]):
                                    k = '%s --> %s' % (aKey,d_key)
                                    d[k] = '%s != %s' % (v,_v)
                            else:
                                pass
                        except Exception, _details:
                            info_string = _utils.formattedException(details=_details)
                            print >>sys.stderr, info_string
                    elif (method == ReplicationMethods.replicate):
                        v = make_value_appropriate(d_metadata_by_names,aKey,v)
                        _case.__setattr__(d_key,v)
                        k = '%s --> %s' % (aKey,d_key)
                        d[k] = str(v) if (v is None) else v
                    _expected_key_count += 1
                _count += 1
            except Exception, _details:
                print >>logger, _utils.formattedException(details=_details)
        elif (sf_cannot_locate is not None):
            if (not d_sf_cannot_locate.has_key(aKey)):
                _cannot_locate.append(aKey)
                print >>logger, '%d :: Cannot locate the SF-->mySQL Mapping for "%s".' % (len(_cannot_locate),aKey)
            else:
                _ignored.append(aKey)
                print >>logger, '%d :: Ignoring the SF-->mySQL Mapping for "%s".' % (len(_ignored),aKey)
    if (sf_cannot_locate is not None):
        if (len(d_xlator.keys()) != _expected_key_count):
            print >>logger, 'WARNING :: Sanity check on d_xlator has failed, expected %d keys but got %d keys.' % (len(d_xlator.keys()),len(d.keys()))
    return d

def replicate_data(aCase,_case,d_xlator,d_metadata_by_names,sf_cannot_locate):
    return check_or_replicate_data(aCase,_case,d_xlator,d_metadata_by_names=d_metadata_by_names,sf_cannot_locate=sf_cannot_locate,method=ReplicationMethods.replicate)

def check_data(aCase,_case,d_xlator,d_metadata_by_names,sf_cannot_locate=None):
    return check_or_replicate_data(aCase,_case,d_xlator,d_metadata_by_names=d_metadata_by_names,sf_cannot_locate=sf_cannot_locate,method=ReplicationMethods.check)

def sanity_check(conn_str,_id,aCase,d_xlator,d_metadata_by_names,d_synopsis,operation,i_case_num,count,l_case_num,account):
    '''operation must be some kind of symbol such as "*" or "+".'''
    isError = False
    info_string = ''
    anotherAgent = sqlalchemy_models.new_agent(conn_str)
    anotherAgent.add_mapper(sqlalchemy_models.Cases,molten_tables.sfcase)
    _check_cases = sqlalchemy_models.get_case_by_id(_id,session=anotherAgent.session)
    if (len(_check_cases) > 0):
        for _case in _check_cases:
            _d_ = check_data(aCase,_case,d_xlator,d_metadata_by_names)
            if (len(_d_) > 0):
                isError = True
                info_string = str(_d_)
    else:
        isError = True
        info_string = 'MISSING DATA'
    if (isError):
        print >>logger, '(!%s!) %d/%d/%d :: %s :: %s ::' % (operation,i_case_num,count,l_case_num,account['Name'],aCase['Id'])
        d_synopsis['(!%s!)' % (operation)] = _id,info_string
        print >>logger, '-'*40
    anotherAgent.close()

def main(connstr=None,port=None,accountName=None):
    from vyperlogix.sf.sf import SalesForceQuery
    sfQuery = SalesForceQuery(sf_login_model)

    cases = SalesForceCases(sfQuery)
    accounts = SalesForceAccounts(sfQuery)
    recordTypes = SalesForceRecordTypes(sfQuery)
    
    recs = recordTypes.getCaseRecordTypes(rtype='Support Case')
    if (recs is None):
        print >>logger, 'ERROR: Cannot determine the Support Case record type.'
        sys.exit(0)
    case_record_type = recs[0]['Id']
    
    d_xlator = lists.HashedLists2()

    d_synopsis = lists.HashedLists()
    
    l_case_num = 1
    if (accountName is not None):
        conn_str = sqlalchemy_models.get_conn_str(port=port) if (len(connstr) == 0) else connstr
        if (port is not None) and (str(port).isdigit()) and (int(port) != 3306):
            print >>logger, 'Tunneling over port %s.' % (port)
        print >>logger, 'Using connection string of "%s".' % (conn_str)
        some_accounts = accounts.getAccountsLikeName(accountName)
	if (accounts.contains_sf_objects(some_accounts)):
	    for account in some_accounts:
		try:
		    count_cases = cases.getAllCasesCountByAccountId(account['Id'],recordTypeId=case_record_type)
		    if (count_cases is not None):
			count_cases = count_cases[0]
			count = int(count_cases['size'][0])
		    else:
			count = -1
		    print >>logger, 'Account "%s" has %s cases to consider.' % (account['Name'],count)
		    if (count > 0):
			some_case_ids = cases.getAllCasesByAccountId(account['Id'],names=['Id'],recordTypeId=case_record_type)
			i_case_num = 1
			if (some_case_ids is not None):
			    for anId in some_case_ids:
				_id = anId['Id']
				some_cases = cases.getAllCasesById(_id,names=d_xlator.keys())
				if (some_cases is not None):
				    if (len(d_xlator) == 0):
					for aCase in some_cases[0:1]:
					    _id = aCase['Id']
					    _some_cases = sqlalchemy_models.get_case_by_id(_id)
					    if (len(_some_cases) > 0):
						d_xlator,sf_cannot_locate,mySQL_cannot_locate = determine_data_dictionary(aCase.keys(),_some_cases[0])
						break
				    print >>logger, 'Account "%s" has %d cases to consider.' % (account['Name'],len(some_cases))
	    
				    for aCase in some_cases:
					anAgent = sqlalchemy_models.new_agent(conn_str)
					anAgent.add_mapper(sqlalchemy_models.Cases,molten_tables.sfcase)
					_some_cases = sqlalchemy_models.get_case_by_id(_id,session=anAgent.session)
					if (len(_some_cases) > 0):
					    print >>logger, '\n'
					    keys = aCase.keys()
					    for _case in _some_cases:
						print >>logger, '(*) %d/%d/%d :: %s :: %s ::' % (i_case_num,count,l_case_num,account['Name'],aCase['Id'])
						_d_ = replicate_data(aCase,_case,d_xlator,cases.metadata_by_names,sf_cannot_locate)
						_d_.prettyPrint(title='SalesForce --> mySQL',prefix='\t',fOut=logger)
						d_synopsis['(*)'] = _id
						print >>logger, '-'*40
					    anAgent.commit()
					    anAgent.flush()
					    anAgent.close()
					    
					    sanity_check(conn_str,_id,aCase,d_xlator,cases.metadata_by_names,d_synopsis,'*',i_case_num,count,l_case_num,account)
					else:
					    anotherAgent = sqlalchemy_models.new_agent(conn_str)
					    anotherAgent.add_mapper(sqlalchemy_models.Cases,molten_tables.sfcase)
					    new_case = sqlalchemy_models.Cases()
					    print >>logger, '(+) %d/%d/%d :: %s :: %s ::' % (i_case_num,count,l_case_num,account['Name'],aCase['Id'])
					    _d_ = replicate_data(aCase,new_case,d_xlator,cases.metadata_by_names,sf_cannot_locate)
					    _d_.prettyPrint(title='SalesForce --> mySQL',prefix='\t',fOut=logger)
					    anotherAgent.add(new_case)
					    anotherAgent.commit()
					    anotherAgent.flush()
					    anotherAgent.close()
					    d_synopsis['(+)'] = _id
					    print >>logger, '-'*40
					    
					    sanity_check(conn_str,_id,aCase,d_xlator,cases.metadata_by_names,d_synopsis,'+',i_case_num,count,l_case_num,account)
					i_case_num += 1
					l_case_num += 1
			else:
			    print >>logger, 'WARNING :: %d/%d/%d :: Cannot locate SF Cases for Account # %s.' % (i_case_num,count,l_case_num,account['Id'])
			    print >>logger, '-'*40
		except KeyError, _details:
		    print >>logger, 'ERROR: Some Accounts is "%s".\n%s' % (some_accounts,_utils.formattedException(details=_details))
	else:
	    print >>logger, 'WARNING :: Cannot locate SF Cases for Account "%s".' % (accountName)
	    print >>logger, '-'*40
    
        #d_xlator.prettyPrint(title='SalesForce --> mySQL',fOut=logger)
        
        sqlalchemy_models.agent.close()
    
        d_synopsis.prettyPrint(title='(*) Means Updated and (+) Means Added',fOut=logger)
        
        print >>logger, 'DONE!'
    else:
        print >>logger, 'ERROR: Nothing can be done with account of "%s".' % (str(accountName))
    
def get_accounts_for_molten_contacts():
    '''This has to be a separate process because it takes a really long time.'''
    from vyperlogix.sf.sf import SalesForceQuery
    sfQuery = SalesForceQuery(sf_login_model)

    print >>logger, 'INFO: Fetching the Contacts who have Molten Access.'
    
    contacts = SalesForceContacts(sfQuery)
    molten_contacts = contacts.getPortalContacts()

    print >>logger, 'INFO: Collecting the Account Id values for Contacts who have Molten access.'
    
    ids = []
    if (molten_contacts is not None):
	ids = [c['AccountId'] for c in molten_contacts]
	_ids = set(ids)
	ids = list(_ids)

    print >>logger, 'INFO: Fetching Accounts for Contacts who have Molten access.'
    
    accounts = SalesForceAccounts(sfQuery)
    molten_accounts = accounts.getAccountsByIds(ids)
    
    if (molten_accounts is not None):
	pass
    
def rewrite_bash_job():
    ts = _utils.timeStampLocalTimeForFileName()

    _logPath = __root__
    logPath = os.path.join(_logPath,'logs')
    logPath = os.path.join(logPath,ts)
    _utils._makeDirs(logPath)
    
    n_logPath = logPath.replace(_logPath,'')
    
    fOut = open(os.path.join(__root__,_bash_name),'w')
    try:
	print >>fOut, _bash_job % (__root__)
	for account in _account_names:
	    print >>fOut, '/opt/ActivePython-2.5/bin/python2.5 %s/sync_mySQL_with_salesforce.pyc --account="%s" --connstr="mysql://molten2:2molten@localhost:3306/molten_production" > %s%s/report-%s.txt 2>%s%s/reports-%s-err.txt' % (__root__,account,__root__,n_logPath,'_'.join(account.split()),__root__,n_logPath,'_'.join(account.split()))
	print >>fOut, "/opt/ActivePython-2.5/bin/python2.5 %s/sync_mySQL_with_salesforce.pyc --bash" % (__root__)
    finally:
	fOut.flush()
	fOut.close()

def allow_one_instance(account_name):
    if (sys.platform != 'win32'):
        from vyperlogix.process import Popen
        
        _found_count = 0
        _seeking = os.path.join(__root__,'%s' % (os.path.basename(sys.argv[0])))
	
	print >>logger, '_seeking is "%s".' % (_seeking)
        
        shell, commands, tail = ('sh', ['ps -ef | grep python'], '\n')
    
	_text = ''
	
        a = Popen.Popen(shell, stdin=Popen.PIPE, stdout=Popen.PIPE)
        t = Popen.recv_some(a)
	_text += t
        #print '(**)', t,
        toks = t.split(_seeking)
        if (len(toks) > 1):
            _found_count += len(toks)-1
        for cmd in commands:
            Popen.send_all(a, cmd + tail)
            t = Popen.recv_some(a)
	    _text += t
            #print '(**)', t,
            toks = t.split(_seeking)
            if (len(toks) > 1):
                _found_count += len(toks)-1
        Popen.send_all(a, 'exit' + tail)
        a.wait()
        
        #print
        #print _found_count
	_target = '--account="%s"' % account_name
        if (_found_count > 1) and (_text.find(_target) > -1):
            print 'Already running - cannot run again.'
            sys.exit(1)

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)
    
    logger = EchoLog(sys.stdout,fOut=sys.stderr) if (not _utils.isBeingDebugged) else sys.stdout
    
    from vyperlogix.misc import Args
    from vyperlogix.misc import PrettyPrint

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--port=?':'port for the tunnel (typically 3307).',
	    '--account=?':'account name or partial account name.',
	    '--connstr=?':'connection string like "mysql://root:peekab00@sql2005:3306/molten_development".',
	    '--bash':'rewrite bash job for the next iteration.',
	    '--debug':'debug mode.',
	    }
    _argsObj = Args.Args(args)

    _progName = _argsObj.programName
    _isVerbose = False
    try:
	if _argsObj.booleans.has_key('isVerbose'):
	    _isVerbose = _argsObj.booleans['isVerbose']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print >>logger, info_string
	_isVerbose = False
    
    if (_isVerbose):
	print >>logger, '_argsObj=(%s)' % str(_argsObj)
	
    _isHelp = False
    try:
	if _argsObj.booleans.has_key('isHelp'):
	    _isHelp = _argsObj.booleans['isHelp']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print >>logger, info_string
	_isHelp = False
	
    if (_isHelp):
	ppArgs()
    
    _isBash = False
    try:
	if _argsObj.booleans.has_key('isBash'):
	    _isBash = _argsObj.booleans['isBash']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print >>logger, info_string
	_isBash = False
	
    _isDebug = False
    try:
	if _argsObj.booleans.has_key('isDebug'):
	    _isDebug = _argsObj.booleans['isDebug']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print >>logger, info_string
	_isDebug = False
	
    __port__ = 3306
    try:
	__port = _argsObj.arguments['port'] if _argsObj.arguments.has_key('port') else __port__
	__port__ = int(__port)
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print >>logger, info_string
    _port = __port__
    
    __account__ = ''
    try:
	__account = _argsObj.arguments['account'] if _argsObj.arguments.has_key('account') else __account__
	if (len(__account) == 0) and (not _isBash):
	    print >>logger, 'WARNING: Cannot use --account="%s".' % (__account)
	__account__ = __account
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print >>logger, info_string
    _account = __account__
    
    __connstr__ = ''
    try:
	__connstr = _argsObj.arguments['connstr'] if _argsObj.arguments.has_key('connstr') else __connstr__
	if (len(__connstr) == 0) and (not _isBash):
	    print >>logger, 'WARNING: Cannot use --connstr="%s".' % (__connstr)
	__connstr__ = __connstr
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print >>logger, info_string
    _connstr = __connstr__

    #if (len(_connstr) > 0) and ( (len(__port) == 0) or (not str(__port).isdigit()) ):
	#print >>logger, 'WARNING: Cannot use --port=%s.' % (__port)
    
    if (_use_staging):
        sf_login_model.isStaging = True
        sf_login_model.perform_login(end_point=sf_login_model.get_endpoint(sf_login_model.sfServers['sandbox']))
    else:
        sf_login_model.isStaging = False
        sf_login_model.perform_login(end_point=sf_login_model.get_endpoint(sf_login_model.sfServers['production']))
    if (sf_login_model.isLoggedIn):
        print >>logger, 'Logged-in Successfully.'
        print >>logger, '_isBash is %s' % (_isBash)
        print >>logger, '_isDebug is %s' % (_isDebug)
	if (len(_account) > 0) or (_isBash) or (_isDebug):
	    if (_account == '*'):
		#_accounts = get_accounts_for_molten_contacts()
		pass
	    if (_isBash):
		rewrite_bash_job()
	    elif (_isDebug):
		print '%s' % (__root__)
	    else:
		allow_one_instance(_account)
		main(connstr=_connstr,port=_port,accountName=_account)
	else:
	    print >>logger, 'WARNING: Nothing to do because no account was specified.'
    else:
        print >>logger, sf_login_model.lastError
        print >>logger, str(sf_login_model)
    pass
    