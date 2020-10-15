from django.template.loader import get_template
from django.template import Context
from django.http import Http404, HttpResponse, HttpResponseRedirect

from vyperlogix.misc import _utils

try:
    from settings import MEDIA_URL
except ImportError:
    MEDIA_URL = '/static/'

try:
    from settings import __title__
except ImportError:
    __title__ = '+++'

def formatTimeStr():
    return '%m/%d/%Y %H:%M:%S'

def formatYYYYStr():
    return '%Y'

def _getCompetitorsList(self):
    #from vyperlogix.sf.sf import SalesForceQuery
    #sfQuery = SalesForceQuery(self.__login_dialog__.sf_login_model)
    #from vyperlogix.sf.magma.competitors import SalesForceMagmaCompetitors
    #competitors = SalesForceMagmaCompetitors(sfQuery)
    #c_list = competitors.getCompetitorsList()

    data = []
    #if (c_list is not None):
	#for item in c_list:
	    #data.append(tuple([str(item['Company_Name__c']).lower()]))
    return data

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

def default(request):
    from settings import MEDIA_URL
    from settings import __version__
    from settings import __title__
    now = _utils.timeStamp(format=formatTimeStr())
    _title = '%s %s' % (__title__,__version__)
    t = get_template('home.html')
    has_sf_login_success = request.session.get('has_sf_login_success', False)
    t_login = get_template('home_login.html' if (not has_sf_login_success) else 'home_logged_in.html')
    options = ''
    servers = getSalesForceServerEndPoints()
    for server in servers:
	options += '<option value ="%s;%s">%s</option>' % (server[0],server[-1],server[-1])
    c_login = Context({'options_for_endpoint':options})
    c = Context({'current_date': now,
                 'the_title': _title,
                 #'MEDIA_URL':'http://media.vyperlogix.com/media/',
                 'MEDIA_URL':MEDIA_URL,
                 'BOXES_URL':'http://media.vyperlogix.com/boxes/',
                 'ICON_URL':'http://media.vyperlogix.com/icons/salesforce/',
		 'content':t_login.render(c_login)
                 })
    html = t.render(c)
    return HttpResponse(html)

def login(request):
    from vyperlogix.wx.pyax import SalesForceLoginModel
    sf_login_model = SalesForceLoginModel.SalesForceLoginModel()
    _username = request.POST['username']
    _password = request.POST['password']
    __endpoint = request.POST['endpoint']
    _endpoint = __endpoint.split(';')[-1]
    sf_login_model.username = _username
    sf_login_model.password = _password
    sf_login_model.perform_login(_endpoint)
    success = sf_login_model.isLoggedIn
    request.session['sf_username'] = _username
    request.session['sf_password'] = _password
    request.session['sf_endpoint'] = __endpoint
    request.session['has_sf_login_success'] = success
    return HttpResponseRedirect("/")

def default_404(request):
    return HttpResponseNotFound(pages._render_the_page(request,'%s' % (___title__),'404_content.html',_navigation_menu_type,_navigation_tabs,context={}))
