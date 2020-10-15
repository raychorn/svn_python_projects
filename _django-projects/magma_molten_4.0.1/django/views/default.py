from django.template.loader import get_template
from django.template import Context
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound

from django.views.decorators.cache import cache_page # @cache_page(60 * 15)

import urllib

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

from vyperlogix.enum.Enum import Enum

from maglib.molten import roles

from vyperlogix.html import myOOHTML as oohtml

home_verb = 'home'
login_verb = 'login'
logout_verb = 'logout'
forgot_password_verb = 'forgot_password'
signup_verb = 'signup'
status_form_verb = 'status_form'
faq_verb = 'FAQ'
changelog_verb = 'CHANGELOG'

non_login_verbs = [forgot_password_verb,signup_verb,status_form_verb,faq_verb,home_verb,changelog_verb]

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

def is_method_post(request):
    try:
	return request.method == 'POST'
    except:
	pass
    return False

def get_from_session(request,name,default=None):
    try:
	return request.session.get(name, default)
    except:
	pass
    return ''

def get_from_post(request,name,default=None):
    try:
	return request.POST[name]
    except:
	pass
    return default

def get_support_cases(request):
    #from vyperlogix.sf.ReConnection import ReConnection
    #sessionid = get_from_session(request,'sfdc_session_id')
    #server_url = get_from_session(request,'sfdc_server_url')
    #sfdc = ReConnection.connect(sessionid,server_url)
    
    sfdc = relogin(request).sfdc

    from vyperlogix.sf.sf import SalesForceQuery
    sfQuery = SalesForceQuery(sfdc)

    from vyperlogix.sf.record_types import SalesForceRecordTypes
    sf_record_types = SalesForceRecordTypes(sfQuery)
    case_record_types = sf_record_types.getCaseRecordTypes(rtype='Support Case')

    cases = []
    if (len(case_record_types) > 0):
	from vyperlogix.sf.cases import SalesForceCases
	sf_cases = SalesForceCases(sfQuery)
	cId = get_from_session(request,'_contact_Id')
	cases = sf_cases.getCasesForContactById(cId,recordTypeId=case_record_types[0]['Id'])
	if (cases is None):
	    cases = []

    return (cases,sfQuery.lastError)

def getMoltenPostsByRecordTypeId(request,molten_post_type=MoltenPosts.none):
    sfdc = relogin(request).sfdc

    from vyperlogix.sf.sf import SalesForceQuery
    sfQuery = SalesForceQuery(sfdc)

    if (molten_post_type == MoltenPosts.articles):
	from vyperlogix.sf.record_types import SalesForceRecordTypes
	sf_record_types = SalesForceRecordTypes(sfQuery)
	record_types = sf_record_types.getMoltenPostArticlesRecordTypes()
    elif (molten_post_type == MoltenPosts.tips):
	from vyperlogix.sf.record_types import SalesForceRecordTypes
	sf_record_types = SalesForceRecordTypes(sfQuery)
	record_types = sf_record_types.getMoltenTipsRecordTypes()

    from vyperlogix.sf.magma.molten_posts import SalesForceMoltenPosts
    sf_molten_posts = SalesForceMoltenPosts(sfQuery)
    molten_posts = sf_molten_posts.getMoltenPostsByRecordTypeId(record_types[0]['Id'])

    return (molten_posts,sfQuery.lastError)

def get_news_articles(request):
    return getMoltenPostsByRecordTypeId(request,MoltenPosts.articles)

def get_tips(request):
    return getMoltenPostsByRecordTypeId(request,MoltenPosts.tips)

def get_new_solutions(request):
    from settings import NEW_SOLUTIONS_LAST_N_DAYS
    from settings import SOLUTION_HOME_LIMIT
    
    sfdc = relogin(request).sfdc

    contact_account_name = get_from_session(request,'_contact_account_Name')
    
    from vyperlogix.sf.sf import SalesForceQuery
    sfQuery = SalesForceQuery(sfdc)

    from vyperlogix.sf.solutions import SalesForceSolutions
    sf_solutions = SalesForceSolutions(sfQuery)
    solutions = sf_solutions.getNewSolutions(num_days=NEW_SOLUTIONS_LAST_N_DAYS,limit=SOLUTION_HOME_LIMIT+1)

    return (solutions,sfQuery.lastError)

def get_new_solutions_count(request):
    from settings import NEW_SOLUTIONS_LAST_N_DAYS
    
    sfdc = relogin(request).sfdc

    contact_account_name = get_from_session(request,'_contact_account_Name')

    from vyperlogix.sf.sf import SalesForceQuery
    sfQuery = SalesForceQuery(sfdc)

    from vyperlogix.sf.solutions import SalesForceSolutions
    sf_solutions = SalesForceSolutions(sfQuery)
    solutions = sf_solutions.getNewSolutionsCount(num_days=NEW_SOLUTIONS_LAST_N_DAYS)

    return (solutions,sfQuery.lastError)

def get_popular_solutions(request):
    from settings import MOST_POPULAR_LAST_N_DAYS
    from settings import MOST_POPULAR_LIMIT
    
    sfdc = relogin(request).sfdc

    contact_account_name = get_from_session(request,'_contact_account_Name')

    from vyperlogix.sf.sf import SalesForceQuery
    sfQuery = SalesForceQuery(sfdc)

    from vyperlogix.sf.solutions import SalesForceSolutions
    sf_solutions = SalesForceSolutions(sfQuery)
    l_freqs,d_freqs,d = sf_solutions.getSolutionsViewsFrequencies(num_days=MOST_POPULAR_LAST_N_DAYS)
    
    ids = []
    for num in l_freqs[-5:]:
	ids += d_freqs[num]
    ids = misc.reverse(list(set(ids)))[-MOST_POPULAR_LIMIT:]

    solutions = sf_solutions.getSpecificSolutions(solutions=ids)
    return (solutions,sfQuery.lastError)

def getSalesForceServerEndPoints():
    from vyperlogix.wx.pyax import SalesForceLoginModel
    sf_login_model = SalesForceLoginModel.SalesForceLoginModel()

    servers = []
    for k,v in sf_login_model.sfServers.iteritems():
	_endpoint = sf_login_model.get_endpoint(v)
	if (isinstance(v,list)):
	    v.append(_endpoint)
	else:
	    v = [v,_endpoint]
	servers += [v]
    return servers

def cookie_failure(c):
    t = get_template('_no_cookies.html')
    return t.render(c)

def default(request,msg=''):
    from settings import NEW_SOLUTIONS_LAST_N_DAYS
    from settings import MEDIA_URL
    from settings import __version__
    from settings import __title__
    toks = [urllib.unquote_plus(t) for t in request.path.split('/') if (len(t) > 0)]
    now = _utils.timeStamp(format=formatTimeStr())
    _title = '%s %s' % (__title__,__version__)
    _is_authenticated = is_authenticated(request)
    c = Context({'current_date': now,
                 'the_title': _title,
                 'MEDIA_URL':'http://media.vyperlogix.com/magma/',
                 'IMAGES_URL':'http://media.vyperlogix.com/magma/images/',
                 'ICON_URL':'http://media.vyperlogix.com/',
		 'MOLTEN_VERSION':__version__,
		 'EXPIRES_ON':_utils.timeStamp(_utils.timeSeconds()-(86400*365.25*20),format=_utils.formatMetaHeaderExpiresOn()),
		 'MODIFIED_ON':_utils.timeStamp(_utils.timeSeconds(),format=_utils.formatMetaHeaderExpiresOn())
                 })
    css_t = get_template('default.css')
    default_css = css_t.render(c)
    c.update({'default_css':default_css})
    message_content = '' if (len(msg) == 0) else msg
    if (len(toks) > 0) and (login_verb not in toks) and (get_from_session(request,'has_sf_login_success',default=None) is not None) and (not _is_authenticated):
	t = get_template('_login_failure.html')
	contact_remember = get_from_session(request,'contact_remember',default='')
	c.update({ 'username':get_from_session(request,'contact_username',default=''),
		   'password':get_from_session(request,'contact_password',default=''),
		   'remember_me_checked':'' if (len(contact_remember) == 0) else 'checked="checked"'
		})
	message_content = t.render(c)
    elif (get_from_session(request,'has_sf_login_success',default=None) is None) and (not _is_authenticated):
	if (get_from_session(request,'has_sf_login_success',default=None) is None):
	    request.session['has_sf_login_success'] = False
	#if ( (len(toks) > 0) and (toks[0] == home_verb) ) or (get_from_session(request,'has_sf_login_success',default=None) is None):
	if (get_from_session(request,'has_sf_login_success',default=None) is None):
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
	#h.cycle_func = oohtml.HtmlCycler.shaded_class_cycler_function3()
	h.html_simple_table(items,width='100%') # ,class_='listing'
	return h.toHtml()
    
    def render_partial_list_of_items(items=[],url_prefix='',id_selector='Id',item_name_selector='SolutionName',name_limit=-1,limit=-1,use_table=False):
	from settings import MORE_NEW_SOLUTIONS
	from settings import MORE_NEW_SOLUTIONS_LINK

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
		    rows.append(oohtml.renderAnchor('%s' % (MORE_NEW_SOLUTIONS_LINK),_utils.truncate_if_necessary(MORE_NEW_SOLUTIONS,max_width=name_limit)))
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
    
    def render_partial_molten_posts(articles=[],name_limit=-1,limit=-1):
	from settings import ARTICLE_LIMIT
	from settings import ARTICLE_LIST_TITLE_LENGTH
	return render_partial_list_of_items(items=articles,url_prefix='articles/show',id_selector='Id',item_name_selector=['Name','LastModifiedDate'],limit=ARTICLE_LIMIT,name_limit=-1,use_table=True)
    
    def render_partial_solutions(solutions=[],name_limit=-1,limit=-1):
	return render_partial_list_of_items(items=solutions,url_prefix='solutions/show',id_selector='Id',item_name_selector='SolutionName',name_limit=name_limit,limit=limit,use_table=True)
    
    def render_partial_popular_solutions(solutions=[]):
	from settings import SOLUTION_NAME_LIMIT
	from settings import MOST_POPULAR_LIMIT
	return render_partial_solutions(solutions=solutions,name_limit=SOLUTION_NAME_LIMIT,limit=MOST_POPULAR_LIMIT)
    
    def render_partial_new_solutions(solutions=[]):
	from settings import SOLUTION_NAME_LIMIT
	from settings import SOLUTION_HOME_LIMIT
	return render_partial_solutions(solutions=solutions,name_limit=SOLUTION_NAME_LIMIT,limit=SOLUTION_HOME_LIMIT)
    
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
	
	t3 = get_template('_logout_link.html')
	html3 = t3.render(c)
	
	if (len(toks) > 0) and (toks[-1] == changelog_verb):
	    t2 = get_template('CHANGELOG.txt')
	    html4 = '<br/>'.join(t2.render(c).split('\n'))
	else:
	    cases = get_support_cases(request)
	    dashboard_content = render_partial_recent_cases(cases)
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
		      'NEW_SOLUTIONS_CONTENT':new_solutions_content,
		      'POPULAR_SOLUTIONS_CONTENT':popular_solutions_content,
		      'MAGMA_NEWS_CONTENT':magma_news_content,
		      'MOLTEN_TIPS_CONTENT':molten_tips_content,
		      'NEW_SOLUTIONS_COUNT':solutions_count[0],
		      'NEW_SOLUTIONS_LAST_N_DAYS':NEW_SOLUTIONS_LAST_N_DAYS
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

def relogin(request):
    if (request.__dict__.has_key('__sf_login_model__')):
	sf_login_model = request.__dict__['__sf_login_model__']
    else:
	from vyperlogix.wx.pyax import SalesForceLoginModel
	sf_login_model = SalesForceLoginModel.SalesForceLoginModel()
	sf_login_model.username = get_from_session(request,'sf_username')
	sf_login_model.password = get_from_session(request,'sf_password')
	sf_login_model.perform_login(get_from_session(request,'sfdc_server_url'))
	request.__dict__['__sf_login_model__'] = sf_login_model
    return sf_login_model

def login(request,sf_username,sf_password,contact_username,contact_password,sf_endpoint):
    from vyperlogix.wx.pyax import SalesForceLoginModel
    sf_login_model = SalesForceLoginModel.SalesForceLoginModel()
    sf_login_model.username = sf_username
    sf_login_model.password = sf_password
    sf_login_model.perform_login(sf_endpoint)

    _is_contact_password_valid = False
    
    from vyperlogix.sf.sf import SalesForceQuery
    sfQuery = SalesForceQuery(sf_login_model)
    from vyperlogix.sf.contacts import SalesForceContacts
    contacts = SalesForceContacts(sfQuery)
    c_list = contacts.getPortalContactByEmail(contact_username)
    if (c_list is not None):
	for aContact in c_list:
	    if (aContact['Portal_Password__c'] == contact_password):
		_is_contact_password_valid = True
		for k in aContact.keys():
		    request.session['_contact_%s' % k] = str(aContact[k])
		from vyperlogix.sf.accounts import SalesForceAccounts
		accounts = SalesForceAccounts(sfQuery)
		a_list = accounts.getAccountById(aContact['AccountId'])
		for anAccount in a_list:
		    for k in anAccount.keys():
			request.session['_contact_account_%s' % k] = str(anAccount[k])
		    ancestors_list = accounts.getAccountAncestors(anAccount)
		    pass
		break
    
    success = sf_login_model.isLoggedIn and _is_contact_password_valid
    request.session['sf_username'] = sf_username
    request.session['sf_password'] = sf_password
    request.session['sf_endpoint'] = sf_endpoint
    request.session['contact_username'] = contact_username
    request.session['contact_password'] = contact_password
    request.session['has_sf_login_success'] = success
    if (success):
	request.session['sfdc_session_id'] = sf_login_model.sfdc.session_id
	request.session['sfdc_server_url'] = sf_login_model.sfdc.server_url

def contact(request):
    from settings import __sf_account__
    from settings import USE_SALESFORCE_STAGING
    _username = get_from_post(request,'email',default='')
    _password = get_from_post(request,'password',default='')
    toks = [urllib.unquote_plus(t) for t in request.path.split('/') if (len(t) > 0)]
    if (toks[-1] == login_verb):
	servers = getSalesForceServerEndPoints()
	criteria = 'test.' if (USE_SALESFORCE_STAGING) else 'www.'
	endpoint = [s[-1] for s in servers if (s[0].find(criteria) > -1)]
	suffix = '.stag' if (USE_SALESFORCE_STAGING) else ''
	request.session['contact_remember'] = get_from_post(request,'remember_me',default='')
	login(request,__sf_account__['username']+suffix,__sf_account__['password'],_username,_password,endpoint[-1])
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
