import os, sys, uuid
import stat
import re

from django.conf import settings

from vyperlogix.misc import _utils
from vyperlogix.lists import ListWrapper
from vyperlogix.misc import ObjectTypeName

from vyperlogix.hash import lists

from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.products import keys

from vyperlogix.html import myOOHTML as oohtml

from content import models as content_models

from django.db.models import Q

d1 = lists.HashedFuzzyLists2({'username':keys._decode('52686F726E36'),'password':keys._decode('7065656B61623030')})
zone_edit_auth = lists.HashedFuzzyLists2({'vyperlogix.com':d1})

_styles_ = 'color:black; background-color:white;'
_styles = ' style="%s"' % (_styles_)

captcha_choices='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

_anchor_expected_target = lambda foo:'/%s/' % ('/'.join(foo))
anchor_expected_target = lambda foo,bar:_anchor_expected_target(foo[0:-1]+bar)

_reSVN = re.compile("[._]svn|thumbs.db",re.IGNORECASE)

def choose_ribbon_image():
    import random
    ribbons_path = settings.RIBBONS_ROOT
    _ribbons_path = os.path.dirname(settings.MEDIA_ROOT)
    files = [os.path.join(ribbons_path,f).replace(_ribbons_path,'').replace(os.sep,'/') for f in os.listdir(ribbons_path) if (not _reSVN.search(f))]
    return random.choice(files)

def default_role_id():
    '''Default Role is "Member" which is a user with minimal access or a typical user.'''
    try:
	roles = content_models.Role.objects.filter(name='Member')
	if (roles.count() > 0):
	    return roles[0].id
    except:
	pass
    return -1

def admin_role_id():
    '''Admin Role is "Member" which is a super-user who can build sites.'''
    try:
	roles = content_models.Role.objects.filter(name='Administrator')
	if (roles.count() > 0):
	    return roles[0].id
    except:
	pass
    return -1

def get_user_roles():
    roles = content_models.Role.objects.all()
    return roles
	
def get_admin_user_role():
    roles = content_models.Role.objects.filter(name='Administrator')
    return roles[0] if (roles.count() > 0) else None
	
def get_member_user_role():
    roles = content_models.Role.objects.filter(name='Member')
    return roles[0] if (roles.count() > 0) else None
	
def get_sitenames_count():
    import time
    begin_ts = time.mktime(_utils.getFromDateStr('06/01/2009',format=_utils.formatDate_MMDDYYYY_slashes()).timetuple())
    now_ts = time.mktime(_utils.getFromNativeTimeStamp(_utils.timeStamp()).timetuple())
    ticks = now_ts - begin_ts
    num = int(ticks / 1000)
    i = content_models.SiteName.objects.count()
    i += num
    return i
	
def get_sitename_for_current_site(aUser):
    sitenames = content_models.SiteName.objects.filter(user=aUser)
    if (sitenames.count() > 0):
	return sitenames[0]
    return None
	
def get_sitename_for_SITE_ID(SITE_ID):
    sitenames = content_models.SiteName.objects.filter(site=SITE_ID)
    if (sitenames.count() > 0):
	return sitenames[0]
    return None
	
def _is_domain_valid(dname):
    from vyperlogix.process import Popen

    buf = _utils.stringIO()
    opt = '-n' if (sys.platform == 'win32') else '-c'
    shell = Popen.Shell(['ping %s 3 %s' % (opt,dname)],isExit=True,isWait=True,isVerbose=True,fOut=buf)
    lines = ListWrapper.ListWrapper([l for l in buf.getvalue().split('\n') if (len(l.strip()) > 0)])
    targets = ['could not find host','could not find','could not','not find','unknown host']
    _f = all([lines.findFirstContaining(t,returnIndexes=True) == -1 for t in targets])
    return _f

def is_domain_valid(dname):
    tests = ListWrapper.ListWrapper()
    for i in xrange(0,10):
	_bool = _is_domain_valid(dname)
	tests.append(_bool)
	if (tests.findFirstMatching([True,True]) > -1):
	    return True
	elif (tests.findFirstMatching([False,False]) > -1):
	    return False
    return False

def _domain_test(dname,_is_domain_valid):
    _is_domain_valid = _is_domain_valid if (isinstance(_is_domain_valid,bool)) else False
    anchor = ''
    msg1 = '<span class="greenFg">online</span> and <span class="greenFg">ready</span>'
    msg2 = 'for you to proceed to build your site'
    if (not _is_domain_valid):
	anchor = oohtml.renderAnchor('#','Check again...',title='Do another Domain Name Check...',target='_top',onClick='perform_domain_check();')
	msg1 = '<span class="errorBg">not yet online</span> <span class="greenFg">and</span> <span class="errorBg">not yet ready</span>'
	msg2 = 'however if you would be willing to wait until our network engineers can get your domain name online you will be good to go shortly.  You may need to wait 1-2 business days, perhaps a bit less.  Once your chosen domain name has been made available and it passes the "ping" test you will see some additional buttons on the Menu Bar and you will be able to resume setting up your site. %s' % (anchor)
    s = '<p>Your domain "%s" is %s %s.</p>' % (dname,msg1,msg2)
    return s

def domain_test(dname):
    return _domain_test(is_domain_valid(dname))

def get_current_user(request,activated=1):
    try:
	user_id = request.session.get('user_id', '')
	users = content_models.User.objects.filter(Q(email_address=user_id), Q(activated=activated))
	if (users.count() > 0):
	    return users[0]
	return None
    except:
	pass
    return None

def get_user_by_email(email,activated=1):
    try:
	users = content_models.User.objects.filter(Q(email_address=email), Q(activated=activated))
	if (users.count() > 0):
	    return users[0]
	return None
    except:
	pass
    return None

def get_sitename_for_user(aUser):
    sitenames = content_models.SiteName.objects.filter(user=aUser)
    if (sitenames.count() > 0):
	return sitenames[0]
    return None
	
def get_current_site(request,aUser):
    '''SITE_ID is the id of the Site for the site being visited by someone other than an Administrator of a site.'''
    SITE_ID = settings.SITE_ID
    try:
	if (aUser is None):
	    hostname = request.META['HTTP_HOST'].split(':')[0].lower()
	    sites = content_models.Site.objects.filter(domain=hostname)
	    if (sites.count() > 0):
		SITE_ID = sites[0].id
    except:
	pass
    return SITE_ID

def get_user_owner(SITE_ID):
    try:
	aSiteName = get_sitename_for_SITE_ID(SITE_ID)
	if (aSiteName is not None):
	    return aSiteName.user
	return None
    except:
	pass
    return None

def get_header_snippets():
    aSnippetType = content_models.get_header_snippet_type()
    return content_models.Snippet.objects.filter(snippet_type=aSnippetType)

def get_title_snippets():
    title_snippet_type = content_models.get_title_snippet_type()
    return content_models.Snippet.objects.filter(snippet_type=title_snippet_type)

def get_snippets_by_tag(snippet_tag):
    return content_models.Snippet.objects.filter(snippet_tag=snippet_tag)

def get_snippets_for_user_register(snippet_tag='/user/register/'):
    return get_snippets_by_tag(snippet_tag)

def get_snippets_for_wiki(snippet_tag='wiki-layout'):
    return get_snippets_by_tag(snippet_tag)

def get_head_snippets():
    head_snippet_type = content_models.get_head_snippet_type()
    return content_models.Snippet.objects.filter(snippet_type=head_snippet_type)

def get_javascript_snippets():
    javascript_snippet_type = content_models.get_javascript_snippet_type()
    return content_models.Snippet.objects.filter(snippet_type=javascript_snippet_type)

def get_snippet_types(admin=0):
    return content_models.SnippetType.objects.filter(admin=admin)

def get_snippet_types_list(admin=0):
    return [aSnippet.snippet_type for aSnippet in get_snippet_types(admin=admin)]

allowed_media_file_types = ['.jpg', '.jpeg', '.gif', '.png']
acceptable_media_mimes = ['image/jpeg','image/jpeg','image/pjpeg','image/gif','image/png']

normalize_image_fname = lambda f:f.replace(settings.MEDIA_ROOT,settings.MEDIA_URL).replace(os.sep,'/').replace(settings.MEDIA_URL+'/',settings.MEDIA_URL)

def media_table_refresh(h,files):
    t = ObjectTypeName.typeClassName(h)
    h = h if (h is not None) and (t.find('.html.myOOHTML.') > -1) else oohtml.HtmlCycler()
    rows = [['&nbsp;name&nbsp;','&nbsp;image&nbsp;','&nbsp;date&nbsp;','&nbsp;size&nbsp;']]
    for f in files:
	fname = os.path.basename(f[0])
	url = normalize_image_fname(f[0])
	img = oohtml.render_IMG(src=url,border=0,width=32)
	link = oohtml.renderAnchor(url,fname,title='Right-Click copy-n-paste to get this link into your content.')
	ts = _utils.timeStamp(f[-1][stat.ST_CTIME],format=_utils.formatMySQLDateTimeStr())
	size = f[-1][stat.ST_SIZE]
	rows.append([link,img,ts,size])
    h.html_simple_table_with_header(rows,border='1')

def get_uploads_path(aSitename):
    uploads_path = None
    try:
	_uuid = aSitename.site.uuid
	if (_uuid is None) or (len(_uuid) == 0):
	    _uuid = str(uuid.uuid4())
	    aSitename.site.uuid = _uuid
	    aSitename.site.save()
	uploads_path = os.path.join(settings.MEDIA_ROOT,'uploads',_uuid)
	_utils._makeDirs(uploads_path)
    except:
	pass
    return uploads_path

def perform_domain_check(check,zone_name='vyperlogix.com'):
    from vyperlogix.zones.dns import ZoneEdit
    from vyperlogix.zones.dns import ZoneEditProxy

    auth = zone_edit_auth[zone_name]
    zo = ZoneEditProxy(ZoneEdit(auth['username'],auth['password']))
    zones = ListWrapper.ListWrapper(zo.zones())
    i = zones.findFirstMatching(zone_name)
    resp = False
    check = str(check).replace('.'+zone_name,'').lower()
    if (i > -1):
	cnames = ListWrapper.ListWrapper(zo.zone(zones[i]).cnames())
	j = cnames.findFirstMatching(check)
	resp = False if (j > -1) else True
    else:
	zone_name = '%s.%s' % (check,zone_name)
	sitenames = content_models.SiteName.objects.filter(Q(site_name=zone_name), Q(user=aUser))
	resp = False if (sitenames.count() > 0) else True
    return resp

def remove_domain_name(domain_name,zone_name='vyperlogix.com'):
    from vyperlogix.zones.dns import ZoneEdit
    from vyperlogix.zones.dns import ZoneEditProxy

    auth = zone_edit_auth[zone_name]
    zo = ZoneEditProxy(ZoneEdit(auth['username'],auth['password']))
    zones = ListWrapper.ListWrapper(zo.zones())
    i = zones.findFirstMatching(zone_name)
    resp = False
    if (i > -1):
	check = domain_name.replace('.'+zone_name,'').lower()
	cnames = ListWrapper.ListWrapper(zo.zone(zones[i]).cnames())
	j = cnames.findFirstMatching(check)
	if (j > -1):
	    try:
		zo.drill_into_Zone(zone_name,facet='CNAME')
		elements = zo.zone_proxy.d_tuples[check]
		d_form = {}
		for e in elements[-1]:
		    d_form[e['name']] = e['value']
		d_form['Delete'] = 'Delete Selected'
		zo.delete_from_Zone(d_form,zo.zone_proxy.d_newForm_actions['edit'])
		resp = True
	    except:
		pass
    return resp

def add_domain_name(domain_name,zone_name='vyperlogix.com'):
    from vyperlogix.zones.dns import ZoneEdit
    from vyperlogix.zones.dns import ZoneEditProxy

    auth = zone_edit_auth[zone_name]
    zo = ZoneEditProxy(ZoneEdit(auth['username'],auth['password']))
    zones = ListWrapper.ListWrapper(zo.zones())
    i = zones.findFirstMatching(zone_name)
    resp = False
    if (i > -1):
	check = domain_name.replace('.'+zone_name,'').lower()
	cnames = ListWrapper.ListWrapper(zo.zone(zones[i]).cnames())
	j = cnames.findFirstMatching(check)
	if (j == -1):
	    try:
		zo.drill_into_Zone(zone_name,facet='CNAME')
		new_cname = check
		if (cnames.findFirstMatching(new_cname) == -1):
		    zo.zone_proxy.d_newForm['dnsfrom'] = new_cname
		    zo.zone_proxy.d_newForm['dnsto'] = 'www.%s' % (zone_name)
		    zo.add_to_Zone(zo.zone_proxy.d_newForm,zo.zone_proxy.d_newForm_actions['add'])
		resp = True
	    except:
		pass
    return resp

def get_site_handle(request):
    so = SmartObject()
    so.aUser = get_current_user(request)
    so.SITE_ID = get_current_site(request,so.aUser)
    so.aSiteName = get_sitename_for_SITE_ID(so.SITE_ID)
    if (so.aSiteName is not None):
	so.aUser = so.aSiteName.user
    else:
	so.aSiteName = get_sitename_for_user(so.aUser)
    so.aUserOwner = get_user_owner(so.SITE_ID)
    so.is_admin_role = False
    if (so.aUser is not None):
	so.is_admin_role = so.aUser.role.id == admin_role_id()
    return so

