from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import get_template

from vyperlogix.misc import _utils

from vyperlogix.products import keys

import os, sys

from vyperlogix.django import django_utils

from vyperlogix.xml import xml_utils

from vyperlogix.mail.mailServer import GoDaddyServer

isMolten = lambda email:(email.lower().split('@')[-1] != 'magma-da.com')

_title = 'MagmaSF'

def formatTimeStr():
    return '%m/%d/%Y %H:%M:%S'

def formatYYYYStr():
    return '%Y'

now = _utils.getAsDateTimeStr(_utils.today_localtime(),fmt=formatTimeStr())

def default(request):
    from xml.dom.minidom import parse, parseString

    t_content = get_template('soap_response_success.xml')
    try:
	from maglib.salesforce.cred import credentials
	from maglib.salesforce.auth import CredentialTypes
	from maglib.salesforce.auth import magma_molten_passphrase
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	html = t_content.render(Context({'current_date': now, 'the_title': _title, 'INFO':info_string}))
	return HttpResponse(html)
    
    from vyperlogix.sf.sf import SalesForceQuery
    from vyperlogix.sf.cases import SalesForceCases
    from vyperlogix.sf.case_comments import SalesForceCaseComments
    from vyperlogix.sf.contacts import SalesForceContacts

    from vyperlogix.mail.validateEmail import validateEmail
    from vyperlogix.mail.validateEmail import make_email_chars_valid
    from vyperlogix.mail.validateEmail import delimiters
    
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)

    info_string = ''
    _info_string = ''
    Email_subject = ''
    Email_content = ''
    CaseNumber = ''
    case_id = ''
    docs = []
    sources = []
    cc_list = []
    try:
        for k,v in request.POST.iteritems():
            _v = ''.join(''.join(v).split('\n'))
            _v = '%s %s' % (k,_v)
            _v = _v.replace('<?xml version "1.0" encoding="UTF-8"?>','')
            sources.append(_v)
    except Exception, _details:
        info_string += '\n%s' % _utils.formattedException(details=_details)
        
    if (len(sources) > 0):
        try:
            docs.append(xml_utils.xml2dict(sources[-1]))
        except Exception, _details:
	    info_string += '\n%s' % _utils.formattedException(details=_details)
        
    _isStaging = 'staging' in url_toks
    
    info_string += '\n(???) _isStaging=%s' % (_isStaging)

    __sf_account__ = credentials(magma_molten_passphrase,CredentialTypes.Magma_RHORN_Production.value if (not _isStaging) else CredentialTypes.Magma_RHORN_Sandbox.value)

    #info_string += '\n(???) %s/%s' % (__sf_account__['username'],__sf_account__['password'])
	
    fRep = _utils.stringIO()
    for doc in docs:
        d = doc['soapenv:Body']['notifications']['Notification']['sObject']
        d.prettyPrint(fOut=fRep)

        from vyperlogix.wx.pyax.SalesForceLoginModel import SalesForceLoginModel
        sf_login_model = SalesForceLoginModel(username=__sf_account__['username'],password=__sf_account__['password'])

	_endpoint = sf_login_model.get_endpoint(sf_login_model.sfServers['production' if (not _isStaging) else 'sandbox'])
	info_string += '\n(???) %s' % (_endpoint)
	
	sf_login_model.isStaging = _isStaging
	sf_login_model.perform_login(end_point=_endpoint)

	if (sf_login_model.isLoggedIn):
	    info_string += '\nSuccessful login to S.F.'
	    sf_query = SalesForceQuery(sf_login_model.sfdc)
	    sf_cases = SalesForceCases(sf_query)
	    sf_comments = SalesForceCaseComments(sf_query)
	    sf_contacts = SalesForceContacts(sf_query)
	    
	    case_id = d['sf:ParentId']
	    cases = sf_cases.getAllCasesById(case_id,names=['Id', 'CaseNumber', 'CC__c', 'Subject', 'ContactId', 'Last_Comment__c'])
	    if (cases is not None) and (len(cases) > 0):
		CaseNumber = cases[0]['CaseNumber']
		_cc = cases[0]['CC__c']
		cc_list = []
		anItem = ''
		#info_string += '\n(***) delimiters is "%s"' % (delimiters)
		for ch in _cc:
		    if (ch in delimiters):
			cc_list.append(str(anItem).strip())
			#info_string += '\n(***) cc_list is "%s"' % (cc_list)
			anItem = ''
		    else:
			anItem += ch
			#info_string += '\n(***) anItem is "%s"' % (anItem)
		cc_list.append(str(anItem).strip())
		cc_list = [cc for cc in cc_list if (len(str(cc).strip()) > 0)]
		#cc_list = [cc.strip() for cc in cc_list.split(',') if (validateEmail(make_email_chars_valid(cc)))] if (isinstance(cc_list,str)) else []
		if (len(cc_list) > 0):
		    contact_id = cases[0]['ContactId']
		    contacts = sf_contacts.getContactById(contact_id)
		    if (contacts is not None) and (len(contacts) > 0):
			comment_id = d['sf:Id']
			comments = sf_comments.getAnyCommentsById(comment_id)
			if (comments is not None) and (len(comments) > 0):
			    aComment = comments[0]['CommentBody']
			    aComment = aComment.strip() if (isinstance(aComment,str)) else ''
			    if (len(aComment) > 0):
				t_Email_Subj = get_template('email_subject.txt')
				Email_context = {'CaseNumber':CaseNumber, 'Case_Subject':cases[0]['Subject']}
				Email_subject = t_Email_Subj.render(Context(Email_context))

				t_Email = get_template('email.txt')
				Email_context['Contact_Name'] = '%s %s' % (contacts[0]['FirstName'],contacts[0]['LastName'])
				Email_context['Case_Last_Case_Comment'] = aComment
				Email_content = t_Email.render(Context(Email_context))
			    else:
				info_string += '\n(***) There are no Comment(s) for Case %s, are there any published comments ?' % (case_id)
			else:
			    info_string += '\nThis condition does not matter: Cannot fetch Comment(s) for %s' % (comment_id)
		    else:
			info_string += '\n(***) Cannot fetch Contact for %s' % (contact_id)
		else:
		    _info_string += '\nINFO: Nothing to do, there is no CC__c (%s) <-- "%s".' % (cc_list,_cc)
		    _info_string += '\nINFO: %s' % (str(cases[0]))
	    else:
		info_string += '\n(***) Cannot fetch Case for %s' % (case_id)
	else:
	    info_string += '\n(***) Cannot login to S.F.'
	break

    _notice = 'A notice has been sent to salesforce-support@Magma-DA.COM due to some errors.'
    aNotice = Email_content if (len(Email_content) > 0) else _notice if (len(cc_list) > 0) else ''

    _source = sources[-1] if (len(sources) > 0) else ''
    
    fOut = _utils.stringIO()
    try:
	print >>fOut, '%s :: %s\nGET: %s\nSOURCE: %s\ninfo_string: %s\n' % (now,url_toks,'&'.join(['%s=%s' % (k,v) for k,v in request.GET.iteritems()]),_source,info_string)
	print >>fOut, 'INFO: %s' % (_info_string)
	print >>fOut, '%s' % (fRep.getvalue())
	print >>fOut, '\n'
	print >>fOut, '%s' % (aNotice)
	print >>fOut, '%s' % (cc_list)
	print >>fOut, '%s' % ('-'*80)
	print >>fOut, '\n'
    finally:
	logText = fOut.getvalue()
    
    try:
	smtp = GoDaddyServer(keys.decode('F7E5E2EDE1F3F4E5F2C0EDE1E7EDE1ADF3E6AEEEE5F4'), keys.decode('F0E5E5EBE1E2B0B0'))
	if (len(Email_content) > 0):
	    try:
		for cc in cc_list:
		    if (isMolten(cc)):
			_link = 'https://molten.magma-da.com/cases/show/%s' % (case_id)
		    else:
			_link = 'https://na6.salesforce.com/%s' % (case_id)
		    if (validateEmail(cc)):
			t_Email_Final = get_template('email_link.txt')
			Email_Final_context = {'EMAIL_BODY':aNotice, 'CASE_LINK':_link}
			Email_Final = t_Email_Final.render(Context(Email_Final_context))
			smtp.sendEmail(cc, 'do-not-respond@magma-sf.net', Email_subject, Email_Final)
		    else:
			t_Error_Email = get_template('email_error.txt')
			Error_context = {'CaseNumber':CaseNumber, 'EmailAddress':cc, 'CASE_LINK':_link}
			Error_Email = t_Error_Email.render(Context(Error_context))
			smtp.sendEmail('salesforce-support@Magma-DA.COM', 'do-not-respond@magma-sf.net', _notice, Error_Email)
	    except Exception, _details:
		info_string += '\n%s' % _utils.formattedException(details=_details)
	elif (len(_source) > 0):
	    smtp.sendEmail('salesforce-support@Magma-DA.COM', 'do-not-respond@magma-sf.net', aNotice, logText)
    except Exception, _details:
	print >>fOut, _utils.formattedException(details=_details)
    finally:
	print >>fOut, '%s' % ('='*80)
	logText = fOut.getvalue()
    
    dname = os.path.dirname(os.path.dirname(__file__))
    fname = os.path.join(dname,'logs','%s_logger_%s.txt' % (_title,_utils.timeStampForFileName().split('_')[0]))
    _utils.makeDirs(fname)
    fOut = open(fname,'a')
    try:
	print >>fOut, logText
    finally:
	fOut.flush()
	fOut.close()
	
    html = t_content.render(Context({'current_date': now, 'the_title': _title + ' (%s)' % (dname)}))
    return HttpResponse(html)

def handle_404(request):
    return HttpResponseNotFound('<h1>404</h1>')

