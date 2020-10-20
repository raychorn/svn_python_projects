import os, sys

from vyperlogix import misc
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.misc import _utils

from vyperlogix.hash import lists

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
def open_browser():
    import mechanize
    
    b = mechanize.Browser(
	factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True)
	)
    b.set_handle_robots(False)
    return b

def get_packages(browser,url,username,password,logging=None):
    '''Returns a list of items as follows:
    (u'/pypi?%3Aaction=logout', {u'/pypi': {u'%3Aaction': u'logout'}}, u'Logout')
    '''
    import urllib2
    from vyperlogix.url import _urllib2
    
    browser.add_password(url, username, password)

    packages = []
    
    try:
	req = urllib2.Request(url)
	req.add_header("Referer", url.split('?')[0])
	browser.open(req)
	for aLink in browser.links():
	    d_attrs = lists.HashedFuzzyLists2(dict(aLink.attrs))
	    _href = d_attrs['href']
	    toks = _urllib2.parse_href_into_parms(_href)[-1]
	    if (all([isinstance(t,list) for t in toks])):
		try:
		    d_parms = lists.HashedFuzzyLists2(dict([tuple(t) for t in toks]))
		except:
		    d_parms = lists.HashedFuzzyLists2()
		if ( (d_parms[':action']) or (d_parms['%3Aaction']) ) and (d_parms['name']):
		    href = aLink.url
		    text = aLink.text
		    toks = [[x.split('=') for x in tt] for tt in [t.split('&') for t in href.split('?')]]
		    d = lists.HashedLists2()
		    d[toks[0][0][0]] = lists.HashedLists2(dict([tuple(t) for t in toks[-1]]))
		    _datum = tuple([href,d,text])
		    dd = d[d.keys()[0]]
		    if (dd is not None) and (misc.isString(str(dd['name']) if (dd['name'] is not None) else dd['name'])):
			packages.append(_datum)
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        if (logging is not None):
            logging.warning(info_string)
        print >>sys.stderr, info_string
    return packages

def get_package_details2(browser,_url,url,logging=None):
    import urllib2
    from vyperlogix.misc import ObjectTypeName
    from vyperlogix import misc
    
    req = urllib2.Request(url)
    req.add_header("Referer", url.split('?')[0])
    browser.open(req)
    
    d = lists.HashedLists2()
    
    _forms = []
    for form in browser.forms():
        elements = form.controls
	_forms.append(tuple([len(elements),elements]))
    d_forms = dict(_forms)
    keys = misc.sort(d_forms.keys())
    elements = d_forms[keys[-1]]
    if (len(elements) > 0):
	inputs = [c for c in [(ele,ObjectTypeName.typeClassName(ele)) for ele in elements] if (c[-1].find('ClientForm.') > -1) and (c[-1] not in ['ClientForm.SubmitControl'])]
	for item in inputs:
	    ele,cname = item
	    d_attrs = ele.attrs
	    if (cname == 'ClientForm.SelectControl'):
		choice = [choice for choice in ele.get_items() if (choice._selected)]
		d[d_attrs['name']] = ','.join([a['label'] for a in [choice.attrs for choice in ele.get_items() if (choice._selected)]])
	    elif (cname == 'ClientForm.TextareaControl'):
		for p in ele.pairs():
		    d[p[0]] = p[-1]
	    else:
		try:
		    d[d_attrs['name']] = d_attrs['value']
		except Exception, e:
		    info_string = _utils.formattedException(details=e)
		    pass
	return d,form.attrs
    return d,[]

def get_package_details(browser,_url,url,logging=None):
    import urllib2
    
    req = urllib2.Request(url)
    req.add_header("Referer", url.split('?')[0])
    browser.open(req)

    _d = lists.HashedLists2()
    form_attrs = []

    for anchor in browser.links():
	try:
	    href = anchor.url
	    toks = [[x.split('=') for x in tt] for tt in [t.split('&') for t in href.split('?')]]
	    d = {}
	    d[toks[0][0][0]] = dict([tuple(t) for t in toks[-1]])
	    if (d.has_key('/pypi')):
		dd = lists.HashedLists2(d['/pypi'])
		if (len(dd) > 1) and ( ( (dd.has_key(':action')) and (dd[':action'] == 'submit_form') ) or ( (dd.has_key('%3Aaction')) and (dd['%3Aaction'] == 'submit_form') ) ):
		    _datum = tuple([href,d,anchor.text])
		    url, d, details = _datum
		    url = '%s%s' % (_url,url)
		    return get_package_details2(browser,_url,url,logging=logging)
	except Exception, e:
	    info_string = _utils.formattedException(details=e)
	    pass
    return _d,form_attrs

def edit_a_package(browser,_url,pkg,callback=None,logging=None):
    from vyperlogix.url._urllib2 import http_post_authenticated

    if (logging is not None):
        logging.info(pkg)
    else:
        print >>sys.stderr, pkg

    url, d, details = pkg
    dd = d[d.keys()[0]]
    if (dd.has_key('%3Aaction')) and (dd['%3Aaction'] == 'pkg_edit'):
        url = '%s%s' % (_url,url)
        d,form_attrs = get_package_details(_url,url,username,password,logging=logging)
        if (callable(callback)):
            try:
                callback(d)
            except:
                pass
            d_attrs = lists.HashedLists2(dict(form_attrs))
            url = '%s%s' % (_url,d_attrs['action'])
            http_post_authenticated(url,d,username,password,logging=logging)
            info_string = 'Updated! (%s)' % (d['version'])
            if (logging is not None):
                logging.info(info_string)
            else:
                print >>sys.stderr, info_string
                print '='*80

