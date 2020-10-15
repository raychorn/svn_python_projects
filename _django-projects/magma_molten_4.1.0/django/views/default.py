from django.template.loader import get_template
from django.template import Context
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound
from django.conf import settings
from django.views.decorators.cache import cache_page # @cache_page(60 * 15)

import urllib

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

from vyperlogix.hash import lists

from vyperlogix.enum.Enum import Enum

from maglib.molten import roles

from vyperlogix.html import myOOHTML as oohtml

from vyperlogix.pyro.sf_proxy import SalesForceProxy

from vyperlogix.django import django_utils

from config import ACCEPTED_ID
__sf__ = SalesForceProxy(settings.VERSION,ACCEPTED_ID)

home_verb = 'home'
login_verb = 'login'
logout_verb = 'logout'
forgot_password_verb = 'forgot_password'
signup_verb = 'signup'
status_form_verb = 'status_form'
faq_verb = 'FAQ'
changelog_verb = 'CHANGELOG'
custom_verb = 'custom'

non_login_verbs = [forgot_password_verb,signup_verb,status_form_verb,faq_verb,home_verb,changelog_verb,custom_verb]

molten_date = lambda apex_date:_utils.getFromApexDateTime(apex_date)

class MoltenPosts(Enum):
    none = 0
    articles = 2**0
    tips = 2**1

def formatTimeStr():
    return '%m/%d/%Y %H:%M:%S'

def formatYYYYStr():
    return '%Y'

def is_authenticated(request):
    try:
	return request.session.get('has_sf_login_success', False)
    except:
	pass
    return False

def get_support_cases(request):
    cases = []
    case_record_types,lastError = __sf__.recordTypes.getCaseRecordTypes(rtype="Support Case")

    if (isinstance(case_record_types,list)) and (len(case_record_types) == 1):
	case_record_types = case_record_types[0]
	contact = django_utils.get_from_session(request,'contact')
	cId = contact.Id
	cases,lastError = __sf__.cases.getCasesForContactById(cId,recordTypeId=case_record_types.Id)
	if (cases is None):
	    cases = []
    else:
	cases = []

    return (cases,lastError)

def getMoltenPostsByRecordTypeId(request,molten_post_type=MoltenPosts.none):
    if (molten_post_type == MoltenPosts.articles):
	record_types,lastError = __sf__.recordTypes.getMoltenPostArticlesRecordTypes()
    elif (molten_post_type == MoltenPosts.tips):
	record_types,lastError = __sf__.recordTypes.getMoltenTipsRecordTypes()
    record_types = record_types[0]

    molten_posts,lastError = __sf__.moltenPosts.getMoltenPostsByRecordTypeId(record_types.Id)

    return (molten_posts,lastError)

def get_news_articles(request):
    return getMoltenPostsByRecordTypeId(request,MoltenPosts.articles)

def get_tips(request):
    return getMoltenPostsByRecordTypeId(request,MoltenPosts.tips)

def get_new_solutions(request):
    solutions,lastError = __sf__.solutions.getNewSolutions(num_days=settings.NEW_SOLUTIONS_LAST_N_DAYS,limit=settings.SOLUTION_HOME_LIMIT+1)

    return (solutions,lastError)

def get_custom_home_pages(request):
    solutions = django_utils.get_from_session(request,'contact_custom_home_pages')
    lastError = django_utils.get_from_session(request,'contact_custom_home_pages_lastError')

    return (solutions,lastError)

def get_new_solutions_count(request):
    solutions,lastError = __sf__.solutions.getNewSolutionsCount(num_days=settings.NEW_SOLUTIONS_LAST_N_DAYS)

    solutions = solutions[0] if (isinstance(solutions,list)) and (len(solutions) > 0) else solutions
    
    return (solutions,lastError)

def get_popular_solutions(request):
    objs,lastError = __sf__.solutions.getSolutionsViewsFrequencies(num_days=settings.MOST_POPULAR_LAST_N_DAYS)
    l_freqs,d_freqs,d = objs
    
    ids = []
    for num in l_freqs[-5:]:
	ids += d_freqs[num]
    ids = misc.reverse(list(set(ids)))[-settings.MOST_POPULAR_LIMIT:]

    solutions,lastError = __sf__.solutions.getSpecificSolutions(solutions=ids)
    
    return (solutions,lastError)

def cookie_failure(c):
    t = get_template('_no_cookies.html')
    return t.render(c)

def system_failure(c):
    t_system_failure = get_template('_system_failure.html')
    html_system_failure = t_system_failure.render(c)
    #c.update({'CONTENT':html_system_failure})
    #t = get_template('login_form.html')
    #return t.render(c)
    return html_system_failure

def default(request,msg=''):
    toks = [urllib.unquote_plus(t) for t in request.path.split('/') if (len(t) > 0)]
    now = _utils.timeStamp(format=formatTimeStr())
    _title = '%s %s' % (settings.TITLE,settings.VERSION)
    _is_authenticated = is_authenticated(request)
    c = Context({'current_date': now,
                 'the_title': _title,
                 'MEDIA_URL':'http://media.vyperlogix.com/magma/',
                 'IMAGES_URL':settings.IMAGES_URL,
                 'ICON_URL':'http://media.vyperlogix.com/',
		 'MOLTEN_VERSION':settings.VERSION,
		 'EXPIRES_ON':_utils.timeStamp(_utils.timeSeconds()-(86400*365.25*20),format=_utils.formatMetaHeaderExpiresOn()),
		 'MODIFIED_ON':_utils.timeStamp(_utils.timeSeconds(),format=_utils.formatMetaHeaderExpiresOn())
                 })
    css_t = get_template('default.css')
    default_css = css_t.render(c)
    c.update({'default_css':default_css})
    message_content = ''
    if (callable(msg)):
	try:
	    message_content = msg(c)
	except:
	    pass
    elif (len(msg) > 0):
	message_content = str(msg)
    if (len(toks) > 0) and (login_verb not in toks) and (django_utils.get_from_session(request,'has_sf_login_success',default=None) is not None) and (not _is_authenticated):
	t = get_template('_login_failure.html')
	contact_remember = django_utils.get_from_session(request,'contact_remember',default='')
	c.update({ 'username':django_utils.get_from_session(request,'contact_username',default=''),
		   'password':django_utils.get_from_session(request,'contact_password',default=''),
		   'remember_me_checked':'' if (len(contact_remember) == 0) else 'checked="checked"'
		})
	message_content = t.render(c)
    elif (django_utils.get_from_session(request,'has_sf_login_success',default=None) is None) and (not _is_authenticated):
	if (django_utils.get_from_session(request,'has_sf_login_success',default=None) is None):
	    request.session['has_sf_login_success'] = False
	if (django_utils.get_from_session(request,'has_sf_login_success',default=None) is None):
	    message_content = cookie_failure(c)
    else:
	javascript_content = '''
	'''
	c.update({'JAVASCRIPT_CODE':javascript_content})

    def render_partial_login_form(c):
	t2 = get_template('_login_form.html')
	html2 = t2.render(c)
	c.update({'CONTENT':html2})
	
    def render_partial_recent_cases(cases=[],map={'Case #':'CaseNumber','Subject':'Subject','Type':'Type','Priority':'Priority','Status':'Status','Last Updated':'LastModifiedDate'},func_map={'Subject':lambda foo:tuple([foo,'style="width: 48%;"']),'Last Updated':molten_date}):
	col_headers = ['Case #','Subject','Type','Priority','Status','Last Updated']
	items = [col_headers]
	
	i_subject = misc.findInListSafely(col_headers,'Subject')

	for case in cases[0]:
	    data = [[case[map[colName]] if (not func_map.has_key(colName)) else func_map[colName](case[map[colName]]) for colName in col_headers if (map.has_key(colName)) and case.has_key(map[colName])]]
	    if (i_subject > -1) and (case.has_key('Id')):
		data[0][i_subject] = list(data[0][i_subject])
		data[0][i_subject][0] = oohtml.renderAnchor('/cases/show/%s/' % (case['Id']),data[0][i_subject][0],target="_top")
		data[0][i_subject] = tuple(data[0][i_subject])
	    items += data
	
	h = oohtml.HtmlCycler()
	h.use_cycler = True
	h.html_simple_table(items,width='100%') # ,class_='listing'
	return h.toHtml()
    
    def render_partial_custom_home_page_link(aContact,aContactAccount):
	h = oohtml.Html()
	for aSolution in aContactAccount.custom_home_pages:
	    h3 = h.tagH3('')
	    img = oohtml.tag_IMG(src='%sicons/bullet_go.png' % (settings.IMAGES_URL),style='vertical-align:middle')
	    a = h3.tagA('',href='/home/custom/',target='_top')
	    a.text('%sView the %s customized home page' % (img,aSolution.Account_Name__c))
	return h.toHtml()
	
    def render_partial_list_of_items(items=[],url_prefix='',id_selector='Id',item_name_selector='SolutionName',name_limit=-1,limit=-1,use_table=False):
	rows = []
	
	h = oohtml.HtmlCycler()

	try:
	    if (isinstance(items[0],list)):
		for item in items[0][0:limit]:
		    _name_extra = []
		    if (isinstance(item_name_selector,str)):
			_name = _utils.truncate_if_necessary(item[item_name_selector],max_width=name_limit)
		    else:
			item_name_selector = list(item_name_selector)
			_name = _utils.truncate_if_necessary(item[item_name_selector[0]],max_width=name_limit)
			for _item in item_name_selector[1:]:
			    _name_extra.append(item[_item] if (ObjectTypeName.typeClassName(item[_item]).find('.apexdatetime.ApexDatetime') == -1) else 'Posted %s' % (molten_date(item[_item])))
		    _name_extra.insert(0,oohtml.renderAnchor('%s' % ('/%s/%s/' % (url_prefix,item[id_selector])),_name))
		    rows.append(_name_extra)
		if (len(items[0]) > limit):
		    rows.append(oohtml.renderAnchor('%s' % (settings.MORE_NEW_SOLUTIONS_LINK),_utils.truncate_if_necessary(settings.MORE_NEW_SOLUTIONS,max_width=name_limit)))
	except:
	    pass
	
	if (use_table):
	    h.use_cycler = True
	    h.html_simple_table([[row] if (not isinstance(row,list)) else row for row in rows],width='100%')
	else:
	    ul = h.tag(oohtml.oohtml.UL)
	    ul.use_cycler = True
	    for row in rows:
		ul._tagLI(row[0] if (isinstance(row,list)) else row)

	return h.toHtml()
    
    def render_partial_molten_tips(tips=[]):
	rows = []
	h = oohtml.Html()
	for item in tips[0]:
	    rows.append('<h3>%s</h3>' % (item['Name']))
	    rows.append(item['body__c'])
	h.html_simple_table([[row] if (not isinstance(row,list)) else row for row in rows],width='100%')
	return h.toHtml()
    
    def render_partial_custom_home_page(aContact,aContactAccount):
	h = oohtml.Html()
	if (len(aContactAccount.custom_home_pages) == 0):
	    h.tagP('A custom home page does not exist for this company.')
	else:
	    for solution in aContactAccount.custom_home_pages:
		div = h.tagDIV('')
		div.text(solution.SolutionNote)
	return h.toHtml()
    
    def render_partial_molten_posts(articles=[],name_limit=-1,limit=-1):
	l = settings.ARTICLE_LIST_TITLE_LENGTH
	return render_partial_list_of_items(items=articles,url_prefix='articles/show',id_selector='Id',item_name_selector=['Name','LastModifiedDate'],limit=settings.ARTICLE_LIMIT,name_limit=-1,use_table=True)
    
    def render_partial_solutions(solutions=[],name_limit=-1,limit=-1):
	return render_partial_list_of_items(items=solutions,url_prefix='solutions/show',id_selector='Id',item_name_selector='SolutionName',name_limit=name_limit,limit=limit,use_table=True)
    
    def render_partial_popular_solutions(solutions=[]):
	return render_partial_solutions(solutions=solutions,name_limit=settings.SOLUTION_NAME_LIMIT,limit=settings.MOST_POPULAR_LIMIT)
    
    def render_partial_new_solutions(solutions=[]):
	return render_partial_solutions(solutions=solutions,name_limit=settings.SOLUTION_NAME_LIMIT,limit=settings.SOLUTION_HOME_LIMIT)
    
    t = get_template('login_form.html' if (not _is_authenticated) and (signup_verb not in toks) and (status_form_verb not in toks) else 'home.html')
    if ( (not _is_authenticated) and (len(toks) == 0) ) or ( (len(toks) > 0) and (toks[-1] not in non_login_verbs) ):
	render_partial_login_form(c)
    elif (len(toks) > 0) and (toks[-1] == forgot_password_verb):
	t2 = get_template('_forgot_password.html')
	html2 = t2.render(c)
	breadcrumbs_content = oohtml.renderAnchor('/login/','Home',target="_top")
	c.update({'CONTENT':html2,
		  'BREADCRUMBS':breadcrumbs_content
		})
    elif (len(toks) > 0) and (toks[-1] == signup_verb):
	t2 = get_template('_signup_form.html')
	html2 = t2.render(c)
	c.update({'MAIN_CONTENT':html2,
		})
    elif (len(toks) > 0) and (toks[-1] == status_form_verb):
	t2 = get_template('_status_form.html')
	html2 = t2.render(c)
	c.update({'MAIN_CONTENT':html2,
		})
    elif (len(toks) > 0) and (toks[-1] == faq_verb):
	t2 = get_template('FAQ.html')
	html2 = t2.render(c)
	return HttpResponse(html2)
    elif (_is_authenticated):
	t2 = get_template('_home_nav.html')
	html2 = t2.render(c)
	
	aContact = django_utils.get_from_session(request,'contact')
	aContactAccount = django_utils.get_from_session(request,'contact_account')
	
	t3 = get_template('_logout_link.html')
	c.update({'LOGGED_IN_AS':aContact.Email
		})
	html3 = t3.render(c)
	
	c.update({'ACCOUNT_NAME':aContactAccount.Name
		})

	if (len(toks) > 0) and (toks[-1] == changelog_verb):
	    t2 = get_template('CHANGELOG.txt')
	    html4 = '<br/>'.join(t2.render(c).split('\n'))
	elif (len(toks) > 0) and (toks[-1] == custom_verb):
	    solutions = get_custom_home_pages(request)
	    custom_home_page_content = render_partial_custom_home_page(aContact,aContactAccount)
	    t4 = get_template('_custom_home_page.html')
	    c.update({'CUSTOM_HOME_PAGE_CONTENT':custom_home_page_content
		    })
	    html4 = t4.render(c)
	else:
	    cases = get_support_cases(request)
	    dashboard_content = render_partial_recent_cases(cases)
	    custom_home_page_link = render_partial_custom_home_page_link(aContact,aContactAccount)
	    solutions = get_new_solutions(request)
	    new_solutions_content = render_partial_new_solutions(solutions)
	    solutions_count = get_new_solutions_count(request)
	    popular_solutions = get_popular_solutions(request)
	    popular_solutions_content = render_partial_popular_solutions(popular_solutions)
	    molten_posts = get_news_articles(request)
	    magma_news_content = render_partial_molten_posts(molten_posts)
	    molten_tips = get_tips(request)
	    molten_tips_content = render_partial_molten_tips(molten_tips)
	    t4 = get_template('_molten_dashboard.html')
	    c.update({'DASHBOARD_CONTENT':dashboard_content,
		      'CUSTOM_HOME_PAGE_LINK_CONTENT':custom_home_page_link,
		      'NEW_SOLUTIONS_CONTENT':new_solutions_content,
		      'POPULAR_SOLUTIONS_CONTENT':popular_solutions_content,
		      'MAGMA_NEWS_CONTENT':magma_news_content,
		      'MOLTEN_TIPS_CONTENT':molten_tips_content,
		      'NEW_SOLUTIONS_COUNT':solutions_count[0] if (isinstance(solutions_count,tuple)) or (isinstance(solutions_count,list)) else solutions_count,
		      'NEW_SOLUTIONS_LAST_N_DAYS':settings.NEW_SOLUTIONS_LAST_N_DAYS
		    })
	    html4 = t4.render(c)
	
	c.update({'NAV_CONTENT':html2,
		  'LOGOUT_CONTENT':html3,
		  'MAIN_CONTENT':html4,
		})
    else:
	render_partial_login_form(c)
    c.update({'FAILURE':message_content})
    html = t.render(c)
    return HttpResponse(html)

def login(request,contact_username,contact_password):
    success = False
    isLoggedIn = __sf__.isLoggedIn()
    if (isLoggedIn):
	_is_contact_password_valid = False
	
	c_list,lastError = __sf__.contacts.getPortalContactByEmail(contact_username)
	if (c_list is not None):
	    for aContact in c_list:
		if (aContact.Portal_Password__c == contact_password):
		    _is_contact_password_valid = True
		    request.session['contact'] = aContact.asPythonDict()
		    a_list,lastError = __sf__.accounts.getAccountById(aContact.AccountId)
		    a_tree = __sf__.getMagmaAccountTree(aContact.AccountId,aContact.Portal_Privilege__c)
		    aContactAccount = a_list[0] if (isinstance(a_list,list)) else a_list
		    solutions,lastError = __sf__.solutions.getCustomHomePagesForAccount(account_id=aContactAccount.Id)
		    for solution in solutions:
			attachments,lastError = __sf__.attachments.getAttachmentByParentId(id=solution.Id)
			pass
		    aContactAccount.custom_home_pages = [solution.asPythonDict() for solution in solutions]
		    aContactAccount.custom_home_pages_lastError = lastError
		    request.session['contact_account'] = aContactAccount.asPythonDict()
		    request.session['contact_account_tree'] = a_tree
		    break
	
	success = _is_contact_password_valid
	request.session['contact_username'] = contact_username
	request.session['contact_password'] = contact_password
	request.session['has_sf_login_success'] = success
    return success

def contact(request):
    _username = django_utils.get_from_post(request,'email',default='')
    _password = django_utils.get_from_post(request,'password',default='')
    toks = [urllib.unquote_plus(t) for t in request.path.split('/') if (len(t) > 0)]
    if (toks[-1] == login_verb):
	request.session['contact_remember'] = django_utils.get_from_post(request,'remember_me',default='')
	if (not login(request,_username,_password)):
	    return default(request,msg=system_failure)
	else:
	    return HttpResponseRedirect("/home/")
    elif (toks[-1] == logout_verb):
	request.session['has_sf_login_success'] = None
    elif (toks[-1] == forgot_password_verb):
	return default(request)
    elif (toks[-1] == signup_verb):
	return default(request)
    elif (toks[-1] == status_form_verb):
	return default(request)
    else:
	return HttpResponseNotFound('<h1>Page not found or system error.</h1>')
    return HttpResponseRedirect("/")

def default_404(request):
    return HttpResponseNotFound(pages._render_the_page(request,'%s' % (___title__),'404_content.html',_navigation_menu_type,_navigation_tabs,context={}))
