import os, sys

from vyperlogix.daemon.daemon import Log
from vyperlogix.daemon.daemon import EchoLog

from vyperlogix.sf.cases import SalesForceCases
from vyperlogix.sf.contacts import SalesForceContacts
from vyperlogix.sf.accounts import SalesForceAccounts
from vyperlogix.sf.record_types import SalesForceRecordTypes
from vyperlogix.sf.case_comments import SalesForceCaseComments

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
sf_login_model = SalesForceLoginModel(username=__sf_account__['username'],password=__sf_account__['password'], api_version='12.0')

__root__ = os.path.dirname(sys.argv[0])

def main(molten_contacts):
    from vyperlogix.sf.sf import SalesForceQuery
    sfQuery = SalesForceQuery(sf_login_model)

    cases = SalesForceCases(sfQuery)
    accounts = SalesForceAccounts(sfQuery)
    recordTypes = SalesForceRecordTypes(sfQuery)
    case_comments = SalesForceCaseComments(sfQuery)
    
    recs = recordTypes.getCaseRecordTypes(rtype='Support Case')
    if (recs is None):
        print >>logger, 'ERROR: Cannot determine the Support Case record type.'
        sys.exit(0)
    case_record_type = recs[0]['Id']
    
    print >>logger, 'case_record_type is "%s".' % (case_record_type)
    
    d_contacts = lists.HashedLists2()
    
    for aContact in molten_contacts:
	anId = aContact['Id']
	d_contacts[anId] = lists.HashedLists()
	support_cases = cases.getAllCasesForContactById(anId,recordTypeId=case_record_type)
	for aCase in support_cases:
	    case_id = aCase['Id']
	    comments = case_comments.getCommentsByParentId(case_id)
	    if (comments is not None):
		comments = [c for c in comments if (c['CommentBody'] is not None) and (len(c['CommentBody']) > 0)]
		if (len(comments) > 0):
		    d_contacts[anId][case_id] = comments
		    print >>logger, 'There are %s Support Cases for Contact Id "%s".' % (len(support_cases),anId)
		    print >>logger, 'There are %s Case Comments for Support Case %s for Contact Id "%s".' % (len(comments),case_id,anId)
		    
    for aContactId, d_cases in d_contacts.iteritems():
	if (len(d_cases) > 0):
	    print >>logger, 'https://na6.salesforce.com/servlet/servlet.Integration?lid=00b30000000k0Ce&eid=%s&ic=1' % (aContactId[0:len(aContactId)-3])
	    for k,v in d_cases.iteritems():
		print >>logger, 'https://molten.magma-da.com/cases/show/%s' % (k)
	    print >>logger, '='*40
	    print >>logger, '\n'
    
def get_molten_contacts(like_account_name=None):
    '''This has to be a separate process because it takes a really long time.'''
    from vyperlogix.sf.sf import SalesForceQuery
    sfQuery = SalesForceQuery(sf_login_model)

    print >>logger, 'INFO: Fetching the Contacts who have Molten Access.'

    accounts = SalesForceAccounts(sfQuery)
    accounts_matching = []
    if (isinstance(like_account_name,str)) and (len(like_account_name.strip()) > 0):
	accounts_matching = accounts.getAccountsLikeName(like_account_name.strip())
	accounts_matching = accounts_matching if (misc.isList(accounts_matching)) else [accounts_matching]
	accounts_matching = [a['Id'] for a in accounts_matching if (a is not None)]
    
    contacts = SalesForceContacts(sfQuery)
    count_molten_contacts = contacts.getPortalContactsCount(for_accounts=accounts_matching)
    n = int(count_molten_contacts[0].size[0])
    print 'There are %s Portal Contacts.' % (n)
    molten_contacts = contacts.getPortalContacts(for_accounts=accounts_matching)

    print 'There are actually %s Portal Contacts.' % (len(molten_contacts))
    
    return molten_contacts

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
	    '--debug':'debug mode.',
	    '--accounts=?':'specify an account name or account name fragment like "Magma" or "Toshiba".',
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
    
    _isDebug = False
    try:
	if _argsObj.booleans.has_key('isDebug'):
	    _isDebug = _argsObj.booleans['isDebug']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print >>logger, info_string
	_isDebug = False
	
    _accounts = None
    try:
	if _argsObj.arguments.has_key('accounts'):
	    _accounts = _argsObj.arguments['accounts']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print >>logger, info_string
	_accounts = None
	
    if (_use_staging):
        sf_login_model.isStaging = True
        sf_login_model.perform_login(end_point=sf_login_model.get_endpoint(sf_login_model.sfServers['sandbox']))
    else:
        sf_login_model.isStaging = False
        sf_login_model.perform_login(end_point=sf_login_model.get_endpoint(sf_login_model.sfServers['production']))
    if (sf_login_model.isLoggedIn):
        print >>logger, 'Logged-in Successfully.'
        print >>logger, '_isDebug is %s' % (_isDebug)
	if (_isDebug):
	    print '%s' % (__root__)
	else:
	    molten_contacts = get_molten_contacts(like_account_name=_accounts)
	    main(molten_contacts)
    else:
        print >>logger, sf_login_model.lastError
        print >>logger, str(sf_login_model)
    pass
    