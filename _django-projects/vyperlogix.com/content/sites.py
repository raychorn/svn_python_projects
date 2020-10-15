from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _, gettext

from django.db.models import Q

from vyperlogix.html import myOOHTML as oohtml

from vyperlogix.django import captcha

from vyperlogix.django import django_utils

from models import Site

import utils

def map_site_to_snippets(aSite,snippets):
    for aSnippet in snippets:
	foo = aSnippet.sites.filter(domain=aSite.domain)
	if (len(foo) == 0):
	    aSnippet.sites.add(aSite)

def accept_site_name(request,user=None,onSuccess=''):
    from django.template import loader
    from vyperlogix.django import django_utils
    
    import models as content_models

    _error_msg = ''
    if (request.method.lower() == 'POST'.lower()):
	site_name = django_utils.get_from_post(request,'site_name','').lower()
	site_title = django_utils.get_from_post(request,'site_title','')
	primary_domain = django_utils.get_server_name(request)
	if (len(site_name) > 0):
	    aSite = None
	    domain_name = '%s.%s' % (site_name,primary_domain)
	    sites = content_models.Site.objects.filter(domain=domain_name)
	    if (sites.count() > 0):
		aSite = sites[0]
	    sitenames = []
	    if (aSite is not None):
		sitenames = [aSiteName for aSiteName in content_models.SiteName.objects.filter(site=aSite) if (aSiteName.user != user)]
	    if (len(sitenames) == 0):
		if (utils.perform_domain_check(domain_name,zone_name=primary_domain)):
		    try:
			if (aSite is None):
			    sitenames = content_models.SiteName.objects.filter(user=user)
			    if (sitenames.count() > 0):
				aSite = sitenames[0].site
			    else:
				aSite = content_models.Site(domain=domain_name,name=site_title)
			_name_to_remove = aSite.domain
			try:
			    aSite.domain = domain_name
			    aSite.name = site_title
			    aSite.save()
			    sitenames = content_models.SiteName.objects.filter(site=aSite,user=user)
			    if (sitenames.count() == 0):
				aSiteName = content_models.SiteName(site=aSite,user=user)
				aSiteName.save()
			    # Map the common snippets to the new site.
			    head_snippets = utils.get_head_snippets().filter(snippet_tag='*')
			    map_site_to_snippets(aSite,head_snippets)
			    
			    snippets = utils.get_snippets_for_user_register()
			    map_site_to_snippets(aSite,snippets)
			    
			    snippets = utils.get_snippets_for_wiki()
			    map_site_to_snippets(aSite,snippets)
			    
			    snippets = utils.get_javascript_snippets().filter(Q(snippet_tag='/user/login/') | Q(snippet_tag='*'))
			    map_site_to_snippets(aSite,snippets)
			finally:
			    if (not utils.perform_domain_check(_name_to_remove,zone_name=primary_domain)):
				utils.remove_domain_name(_name_to_remove,zone_name=primary_domain)
			    utils.add_domain_name(domain_name,zone_name=primary_domain)
			success = (True,'Your site name of "%s" as been reserved for your use.' % (domain_name))
		    except Exception, e:
			success = (False,'Your site name of "%s" cannot be reserved for your use because "%s".' % (domain_name,str(e)))
		    if (isinstance(success,tuple)):
			success, _error_msg = success
			if (success is True):
			    request.session['_error_msg'] = _error_msg
			    return HttpResponseRedirect(onSuccess)
		    else:
			_error_msg = 'Unable to save site name due to some kind of technical issue... try back later...'
		else:
		    _error_msg = 'Unable to reserve your site name because it is no longer available or is presently being used by you... please choose another site name, if you really wish to change your site name...'
	    else:
		_error_msg = 'WARNING: Cannot use the site name of "%s" because someone else is already using it.' % (site_name)
	#else: # delete the site name... because the user erased the entry in the input field...
	    #sitenames = content_models.SiteName.objects.filter(user=user)
	    #for aSiteName in sitenames:
		#if (not utils.perform_domain_check(aSiteName.site.domain,zone_name=primary_domain)):
		    #utils.remove_domain_name(aSiteName.site.domain,zone_name=primary_domain)
		#aSiteName.site.delete()
		#aSiteName.delete()
    request.session['_error_msg'] = _error_msg
    return HttpResponseRedirect('/'.join(onSuccess.split('/')[0:-1]))
