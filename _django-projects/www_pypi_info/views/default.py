from django.template.loader import get_template
from django.template import Context
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound
from django.conf import settings

from django.db.models import Q

from feeds import models as feed_models

from views import models as views_models

from vyperlogix.django.decorators import cache

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.html import myOOHTML as oohtml

from vyperlogix.lists.ListWrapper import ListWrapper

from vyperlogix.misc import ObjectTypeName

from vyperlogix.html import anchors
from vyperlogix.html.strip import strip_tags

from vyperlogix.django import django_utils

from vyperlogix.misc import jsmin

from vyperlogix.django import pages

from vyperlogix.products import keys

from vyperlogix.django import captcha

from vyperlogix.decorators.TailRecursive import tail_recursion

from vyperlogix.mail import validateEmail

from vyperlogix.django.sqlalchemy import post_vars

import os
import urllib
import random
import mimetypes

import md5

import sqlalchemy_model

import utils

from settings import _navigation_tabs

from settings import _navigation_menu_type

view_verb_symbol = 'view'
category_symbol = 'category'
section_symbol = 'section'
sectionid_symbol = 'sectionid'
doc_download_verb_symbol = 'doc_download'

grid_verb_symbol = 'grid'

_not_yet_subscriber = '<br/><br/><BIG><b>You are not yet a Subscriber to this site... <a href="/register/" target="_top"><BIG>So Register already !</BIG></a></b></BIG>'

_usertype_options = [('Super Administrator', 'Super Administrator'), ('Administrator', 'Administrator'), ('Registered', 'Registered'), ('Author', 'Author'), ('Editor', 'Editor'), ('Publisher', 'Publisher'), ('Manager', 'Manager')]

#################################################################################################
## To-Do:
##
##    1). Email the Exception reports to support@vyperlogix.com as they happen.
##
#################################################################################################

_rss_feed = 'http://pypi.python.org/pypi?%3Aaction=rss'

_media_prefix = 'http://media.vyperlogix.com'

_title = 'www.pypi.info Your Python Premier Information&trade;'

_fully_qualified_http_host = ''

_domain = '%s' % (_fully_qualified_http_host if (_utils.isBeingDebugged) else '/')

normalize = lambda item:item.replace(chr(0x99),'&trade;').replace(chr(0xae),'&trade;')

normalize_images = lambda foo:foo.replace('/plugins/editors/tinymce/jscripts/tiny_mce/plugins/emotions/images/','%s/images/emotions/' % (_media_prefix))

normalize_domain = lambda url:_domain if (url.find('http://') == -1) else ''

d_popular = lists.HashedLists()
d_favs = lists.HashedLists()

def has_not_sent_email_recently(request,from_email,reason):
    _now = _utils.timeStampLocalTime()
    now = _utils.getFromTimeStampForFileName(_now)
    _ts = django_utils.get_from_session(request,'has_sent_%s_email_%s' % (reason,from_email),default=None)
    if (_ts is not None):
	ts = _utils.getFromTimeStampForFileName(_ts)
    else:
	ts = _ts
    if (ts is None):
	return True
    diff = now - ts
    return diff.days > 0

def formatTimeStr():
    return '%m/%d/%Y %H:%M:%S'

def formatYYYYStr():
    return '%Y'

def render_anchor_appropriately(url,text,params=''):
    s_url = anchors.parse_href(anchors.rewrite_anchor(url,params=params,callback=rewrite_anchor,isDebug=False))
    is_local_url = (s_url.find('://') == -1)
    s_url = '/'.join([t for t in s_url.split('/') if (len(t) > 0)]) if (is_local_url) else s_url
    link = oohtml.renderAnchor('%s%s/' % (_domain if (is_local_url) else '',s_url),text,target='_blank' if (not is_local_url) else '_top')
    return link

def topmenu_content():
    items = sqlalchemy_model.topmenu_items()
    h = oohtml.Html()
    ul = h.tag(oohtml.oohtml.UL)
    for item in items:
        ul._tagLI(render_anchor_appropriately(item[1],item[0]))
    content = h.toHtml()
    return content

@tail_recursion
def reorder_nodes(nodes,p_nodes):
    for aNode in nodes:
        if (p_nodes.has_key(aNode.id)):
            d_nodes = lists.HashedLists()
            for item in p_nodes[aNode.id]:
                d_nodes[item.id] = item
            aNode.nodes = d_nodes
            reorder_nodes(p_nodes[aNode.id],p_nodes)
            del p_nodes[aNode.id]

def reorder_menuitems(items):
    parent = 0
    p_nodes = lists.HashedLists()
    for item in items:
        p_nodes[item.parent] = item
    reorder_nodes(p_nodes[0],p_nodes)
    return p_nodes

@tail_recursion
def render_nodes(h,nodes):
    for k,items in nodes.iteritems():
        ul = h.tag(oohtml.oohtml.UL)
        for item in items:
            link = render_anchor_appropriately(item.link,item.name,item.params)
            ul._tagLI(link) # oohtml.renderAnchor('%s%s' % (normalize_domain(item.link),item.link),normalize(item.name))
            if (item.nodes):
                render_nodes(ul,item.nodes)

def featured_products_content(s_content):
    _items = sqlalchemy_model.featured_products_title()
    menu_items = sqlalchemy_model.featured_products_items()

    h = oohtml.Html()
    for item in _items:
        h.tagH3(item)
    items = [[s_content],[h.toHtml()]]

    h = oohtml.Html()
    ul = h.tag(oohtml.oohtml.UL)
    for item in menu_items:
        ul._tagLI(oohtml.renderAnchor('%s%s' % (normalize_domain(item[-1]),item[-1]),normalize(item[0])))
    items += [[h.toHtml()]]

    #_items = sqlalchemy_model.mainmenu_title()

    #h = oohtml.Html()
    #for item in _items:
        #h.tagH3(item)
    #items += [[h.toHtml()]]

    #menu_items = sqlalchemy_model.mainmenu_items()
    #nodes = reorder_menuitems(menu_items)
    #h = oohtml.Html()
    #render_nodes(h,nodes)

    #items += [[h.toHtml()]]
    
    #items += [[rss_content(_rss_feed)]]

    items += [[rss_content2()]]
    
    h = oohtml.Html()
    h.html_simple_table(items)
    content = h.toHtml()
    return content

def rewrite_anchor(d):
    isDebug = False
    args = []
    verb = view_verb_symbol
    if (d.has_key('task')):
        if (d.has_key('id')):
            d[d['task']] = d['id']
            del d['task']
            del d['id']
            del d['option']
        elif (d['task'] == 'register'):
            verb = d['task']
            del d['task']
            del d['option']
        elif (d['task'] == 'doc_download'):
            verb = d['task']
            del d['task']
            del d['option']
        else:
            isDebug = True
            print '%s :: 3.1 %s' % (misc.funcName(),str(d))
    elif ((d.has_key('option'))):
        if (d['option'] == 'com_search'):
            verb = 'search'
            deletions = []
            for k,v in d.iteritems():
                if (len(v) == 0):
                    deletions.append(k)
            for key in deletions:
                del d[key]
            del d['option']
        elif (d['option'] == 'com_content'):
            if (d.has_key(view_verb_symbol)) and (d[view_verb_symbol] == 'article'):
                verb = 'view/article'
                for k,v in d.iteritems():
                    if (isinstance(v,str)) and (v.find(':') > -1):
                        d[k] = v.split(':')[0]
                del d['option']
                del d[view_verb_symbol]
            elif (d.has_key(view_verb_symbol)) and (d[view_verb_symbol] == 'section'):
                verb = 'view/section'
                del d['option']
                del d[view_verb_symbol]
            elif (d.has_key(view_verb_symbol)) and (d[view_verb_symbol] == 'frontpage'):
                verb = 'view/frontpage'
                del d['option']
                del d[view_verb_symbol]
            elif (d.has_key(view_verb_symbol)) and (d[view_verb_symbol] == 'category'):
                verb = 'view/category'
                del d['option']
                del d[view_verb_symbol]
                del d['params']
            else:
                isDebug = True
                print '%s :: 7.1 %s' % (misc.funcName(),str(d))
            pass
        elif (d['option'] == 'com_alphacontent'):
            verb = 'view/alphacontent'
            del d['option']
        elif (d['option'] == 'com_docman'):
            verb = 'view'
	    args.append('downloads')
            del d['option']
        elif (d['option'] == 'com_wrapper'):
            verb = 'view/wrapper'
            del d['option']
            del d[view_verb_symbol]
        else:
            isDebug = True
            print '%s :: 5.1 %s' % (misc.funcName(),str(d))
    elif (len(d) > 0):
        isDebug = True
        print '%s :: 6.1 %s' % (misc.funcName(),str(d))
    if (d.has_key('params')):
        for k,v in d['params'].iteritems():
            if (len(v) > 0):
                d[k] = v
        del d['params']
    for k,v in d.iteritems():
        args.append(k)
        args.append(v)
    if (len(verb) > 0):
        href = 'href="/%s/%s/"' % (verb,'/'.join(args) if (len(args) > 0) else '')
    else:
        href = 'href="/%s/"' % ('/'.join(args) if (len(args) > 0) else '')
    if (isDebug):
        print '%s :: %s' % (misc.funcName(),href)
        print '-'*40
    return href

def get_newsflash_items(isNavigation_only=False):
    js = '''
    var current_news_num = 1;
    var max_news_num = %d;
    function render_news_navigation(_id) {
        var _div = 'div_%s_nav';
        var o_div = $(_div,document);
        if (o_div) {
            var i = 1;
            var c_i = _id;
            var links = [];
            var link;
            if (c_i == 1) {
                link = 'Start';
                links[links.length+1] = link;
                link = 'Prev';
                links[links.length+1] = link;
            } else {
                link = '<a href="#Start" onclick="switch_news_div(1);">Start</a>';
                links[links.length+1] = link;
                link = '<a href="#Prev" onclick="switch_prev_news_div();">Prev</a>';
                links[links.length+1] = link;
            }
            var per_page_num = 15;
            var ppNum = (int(c_i / per_page_num) + 1) * per_page_num;
            max_items = ((max_news_num > per_page_num) ? (per_page_num-1) : max_news_num);
            i = ppNum - max_items - 1;
            if (i < 1) {
                i = 1;
            }
            max_items += ((i > 1) ? i : 0);
            max_items = Math.min(max_items,max_news_num)
            for (; i <= max_items; i++) {
                if (i == c_i) {
                    link = i;
                } else {
                    link = '<a href="#' + i + '" onclick="switch_news_div(' + i + ');">' + i + '</a>';
                }
                links[links.length+1] = link;
            }
            if (i < max_news_num) {
                i = int(i);
                link = '<a href="#' + i + '" onclick="switch_news_div(' + i + ');">' + i + '+</a>';
                links[links.length+1] = link;
            }
            if (c_i == max_news_num) {
                link = 'Next';
                links[links.length+1] = link;
                link = 'End';
                links[links.length+1] = link;
            } else {
                link = '<a href="#Next" onclick="switch_next_news_div();">Next</a>';
                links[links.length+1] = link;
                link = '<a href="#Prev" onclick="switch_news_div(' + max_news_num + ');">End</a>';
                links[links.length+1] = link;
            }
            html = links.join('&nbsp;|&nbsp;') + '&nbsp;|&nbsp;';
            o_div.innerHTML = html.replace('&nbsp;|&nbsp;&nbsp;|&nbsp;','&nbsp;|&nbsp;');
        } else {
            alert('WARNING: Some kind of JavaScript Error has happened; shutdown your browser and go back to bed because your browser is just not working...');
        }
    }
    function switch_news_div(_id) {
        current_news_num = _id;
        for (j = 1; j < max_news_num; j++) {
            _div = 'div_%s_' + j;
            o_div = $(_div,document);
            if (o_div) {
                o_div.style.display = 'none';
            }
        }
        _div = 'div_%s_' + _id;
        o_div = $(_div,document);
        if (o_div) {
            o_div.style.display = 'inline';
        }
        render_news_navigation(_id);
    }
    function switch_prev_news_div() {
        current_news_num--;
        if (current_news_num < 0) {
            current_news_num = 1;
        }
        switch_news_div(current_news_num);
    }
    function switch_next_news_div() {
        current_news_num++;
        if (current_news_num > max_news_num) {
            current_news_num = max_news_num;
        }
        switch_news_div(current_news_num);
    }
    switch_news_div(1);
    '''
    #js = '''
#function switch_divs() {
        #_num = %d;
        #_id = rand(_num);
        #for (j = 1; j < _num; j++) {
            #_div = 'div_%s_' + j;
            #o_div = $(_div,document);
            #if (o_div) {
                #o_div.style.display = 'none';
            #}
        #}
        #_div = 'div_%s_' + _id;
        #o_div = $(_div,document);
        #if (o_div) {
            #o_div.style.display = 'inline';
        #}
    #}
    #var _tid = setInterval("switch_divs()", 30000);
    #switch_divs();
    #'''
    js = ''
    name = 'newsflash'
    cats = sqlalchemy_model.categories(name)
    cat = cats[0]
    items = sqlalchemy_model.content_items(cat.id,int(cat.section))
    h = oohtml.Html()
    div = h.tag(oohtml.oohtml.DIV)
    if (isNavigation_only):
        span = div.tag(oohtml.oohtml.SPAN, id='div_%s_nav' % (name))
    id = 1
    current_id = 1
    links = []
    _display_style = ['none','inline']
    old_emotions = 'plugins/editors/tinymce/jscripts/tiny_mce/plugins/emotions/images/'
    new_emotions = 'http://media.vyperlogix.com/tiny_mce/plugins/emotions/img/'
    max_items = 14 if (len(items) > 14) else len(items)-1
    max_items = max_items if (max_items >= 14) else 14
    _choice = random.randint(1, max_items)
    for item in items[0:max_items if (isNavigation_only) else len(items)]:
        if (not isNavigation_only):
            _div = div.tag(oohtml.oohtml.DIV, id='div_%s_%d' % (name,id), style='display: %s;' % (_display_style[0 if (id != _choice) else 1]))
            html = anchors.rewrite_anchors(_utils.ascii_only(normalize_images(str(item.introtext))),callback=rewrite_anchor,isDebug=False).replace(old_emotions,new_emotions)
            _div.text(str(item.title) + '<br/>' + html)
            #if (_display_style == 'inline'):
                #_display_style = 'none'
        id += 1
    html_extra = ''
    if (isNavigation_only):
        if (len(js) > 0):
            h.tagSCRIPT(jsmin.jsmin(js % (len(items),name,name)))
    return h.toHtml()

def render_article(item,articles,items_name,selector,request=None):
    isRenderingAnArticle = False
    isContentJosContent = False
    domain = _domain if ((len(_domain) > 0) and (_domain.startswith('/'))) else '/'
    try:
        aContent = item.Jos_Content
    except:
        aContent = item
	isContentJosContent = ObjectTypeName.typeClassName(aContent).find('Jos_Content') > -1
        isRenderingAnArticle = True if (not isContentJosContent) else False
    _id = aContent.id
    _title = aContent.title
    aTitle = normalize(strip_tags(_title,make_carriage_returns='<BR/>'))
    article_link = aTitle if (isRenderingAnArticle) else oohtml.renderAnchor('%s' % ('%s%s/%s/%s/' % (domain,'view',selector,_id)),aTitle,target='_top')
    article_pdf_link = '' if (isRenderingAnArticle) else oohtml.renderAnchor('%s' % ('%s%s/pdf/%s/' % (domain,selector,_id)),'<img src="%s/images/pdf-icon_20x20.png">' % (_media_prefix))
    article_pdf_link = ''
    articles.append(['<table width="100%%" bgcolor="#585858"><tr><td width="80%%" align="left"><span style="color: cyan; font-size: medium; font-weight: bold; font-family: Verdana, Geneva, Arial, Helvetica, sans-serif;">%s</span></td><td width="20%%" align="right">%s</td></tr></table>' % (article_link,article_pdf_link)])
    aUser = sqlalchemy_model.user_by_id(aContent.created_by)
    _user = aUser[0].name if (len(aUser) > 0) else 'UNKNOWN'
    _date = aContent.created if (aContent.modified is None) else aContent.modified
    updated_on = _utils.getAsDateTimeStr(_date,fmt='%s, %s' % (_utils.formatShortBlogDateStr(),_utils.formatSimpleBlogTimeStr()))
    articles.append(['<small>By %s, on %s</small>' % (_user,updated_on)])
    _hits = aContent.hits
    articles.append(['<small>Views : %d</small>' % (_hits)])
    aFavored = sqlalchemy_model.favored_item_by_id(_id)
    _favs = aFavored if (len(aFavored) > 0) else None
    if (_favs is not None):
        articles.append(['<small>Favoured : %d</small>' % (len(_favs))])
    else:
        articles.append(['<small>Favoured : None</small>'])
    if (isRenderingAnArticle) or (isContentJosContent):
        introtext = normalize(aContent.introtext)
        fulltext = normalize(aContent.fulltext) if (utils.is_authenticated(request)) else _not_yet_subscriber
        articles.append(['<table width="100%%"><tr><td width="80%%" align="left"><span style="color: white; font-size: smaller; font-weight: normal; font-family: Verdana, Geneva, Arial, Helvetica, sans-serif;">%s</span></td></tr></table>' % (introtext+fulltext)])
    isAddingToFavs = True
    try:
        sect_id = item.Jos_Sections.id
        sect_title = item.Jos_Sections.title
        section_link = oohtml.renderAnchor('%s' % ('%ssection/%s/' % (domain,sect_id)),normalize(sect_title),target='_top')
        cat_id = item.Jos_Categories.id
        cat_title = item.Jos_Categories.title
        cat_link = oohtml.renderAnchor('%s' % ('%scategory/%s+%s/' % (domain,sect_id,cat_id)),normalize(cat_title),target='_top')
        articles.append(['<span style="font-size: smaller;">Published in : %s, %s</span>' % (section_link,cat_link)])
        into_text = aContent.introtext
        articles.append(['<small>%s</small>' % (normalize(strip_tags(into_text,make_carriage_returns='<BR/>')))])
        articles.append(['<small>Last update : %s</small>' % (updated_on)])
        articles.append(['<hr align="left" color="#ffff00" width="80%"/>'])
    except:
        isAddingToFavs = False
    
    if (isAddingToFavs):
        d_popular['%d'%_hits] = article_link
        if (_favs is not None):
            d_favs['%d'%len(_favs)] = article_link
    elif (utils.is_authenticated(request)):
        t_socials = get_template('_socials.html')
        html_socials = t_socials.render(Context({'ARTICLE_LINK':urllib.quote_plus(items_name), 'ARTICLE_TITLE':urllib.quote_plus(aTitle)}))
        articles.append([html_socials])

#Do not cache this function... better to optimize the records being viewed to only those being viewed.
def _get_frontpage_items(pageNo=1,numPerPage=10):
    try:
	items = sqlalchemy_model.frontpage_items(pageNo=pageNo,numPerPage=numPerPage)
    except:
	items = []
    return items

def get_frontpage_items(pageNo=1,numPerPage=10,maxPages=15):
    items = _get_frontpage_items(pageNo=pageNo,numPerPage=numPerPage)

    content = django_utils.paginate(items,'Articles','article',pageNo=pageNo,numPerPage=numPerPage,maxPages=maxPages,callback=render_article)
    return content

@cache.cache(settings.CACHE_TIMER)
def rss_content(url):
    from vyperlogix.rss import reader

    try:
	rss = reader.read_feed_links(url)
    except:
	rss = '(News is Offline at this time...)'
    items = [['<h3 align="center">www.python.org/pypi</h3>']]

    h = oohtml.Html()
    ul = h.tag(oohtml.oohtml.UL)
    if (misc.isList(rss)):
	for item in rss:
	    rss_link = oohtml.renderAnchor('%s' % (item[1]),item[0])
	    words = item[2].split()
	    item[2] = ' '.join(words[0:20])
	    ul._tagLI('%s<br/><small>%s</small>' % (rss_link,'<br/>'.join(item[2:])))
    else:
	ul._tagLI(rss)
    items += [[h.toHtml()]]

    h = oohtml.Html()
    h.html_simple_table(items)
    content = h.toHtml()
    return content

def _rss_pypi_link():
    return '/feeds/rss-pypi/'

def _rss_pypi_link_img():
    return oohtml.render_IMG(src='/static/rss/rss-feed_16x16.gif')

def rss_pypi_link(isOneLine=False):
    img = _rss_pypi_link_img()
    return oohtml.renderAnchor(_rss_pypi_link(),'%s%s' % (img, '' if (isOneLine) else '<br/>RSS 2.0'), target="_blank")

def rss_content2():
    rss = feed_models.PyPI.objects.all()

    _link = rss_pypi_link()
    items = [['<h3 align="center">Python Package Index</h3>&nbsp;%s' % (_link)]]

    h = oohtml.Html()
    ul = h.tag(oohtml.oohtml.UL)
    for item in rss:
	ts = _utils.getAsDateTimeStr(item.timestamp,fmt=_utils.formatDjangoDateTimeStr()).replace('Pacific Daylight Time','PDT (GMT-7)')
	_link = '/view/pypi-feed/%d/' % (item.id)
	rss_link = oohtml.renderAnchor('%s' % (_link),'%s %s' % (item.name,item.version), target="_top")
	ul._tagLI('%s (<small>%s</small>)<br/><small>%s</small>' % (rss_link,ts,item.descr))
    items += [[h.toHtml()]]

    h = oohtml.Html()
    h.html_simple_table(items)
    content = h.toHtml()
    return content

def _get_most_items(title,d,n):
    items = [['<h3 align="center">%s</h3>' % (title)]]

    h = oohtml.Html()
    try:
        ul = h.tag(oohtml.oohtml.UL)
        p = misc.reverse(misc.sort(d.keys()[0:n]))
        for item in p:
            links = d[item]
            for link in links:
                ul._tagLI('<small>%s</small>' % (link))
        items += [[h.toHtml()]]
    
        h = oohtml.Html()
        h.html_simple_table(items)
        content = h.toHtml()
    except:
        pass
    return content

def get_populars():
    return _get_most_items('Most Popular',d_popular,10)

def get_favs():
    return _get_most_items('Favorites',d_favs,10)

def get_category_and_section_content(request,name,category,cat_id,sect_id,width=500):
    from vyperlogix.html.flexigrid import script
    items = [['<h2 align="left">%s</h2>' % (category.title)]]

    h = oohtml.Html()
    h.tag(oohtml.oohtml.HR)
    span = h.tag(oohtml.oohtml.SPAN)
    span.text(category.description)

    div = h.tag(oohtml.oohtml.DIV)
    div.text(script.script_content(name,width=width))
    
    items += [[h.toHtml()]]

    h = oohtml.Html()
    h.html_simple_table(items)
    content = h.toHtml()
    return content

def get_display_select_content():
    items = []

    h = oohtml.Html()
    options = []
    for i in xrange(5,55,5):
        options.append(('%d'%i,'%d'%i))
    options.append(('100','100'))
    options.append(('all','all'))
    options = tuple(options)
    h.tagSELECT(options, "5", id="select_display_num")

    items += [[h.toHtml()]]

    h = oohtml.Html()
    h.html_simple_table(items, border="1")
    content = h.toHtml()
    return content

def filter_tabs(request,tabs):
    url_toks = django_utils.parse_url_parms(request)
    test = lambda tab, toks:True
    if (len(url_toks) > 0):
	test = lambda tab, toks:(tab.find('/%s/' % (toks[0])) == -1)
    tabs = [tab for tab in _navigation_tabs]
    if (utils.is_authenticated(request)):
	tabs = [tab for tab in tabs if (tab[0].find('/login/') == -1) and test(tab[0],url_toks)]
	tabs = [tab for tab in tabs if (tab[0].find('/register/') == -1) and test(tab[0],url_toks)]
    else:
	tabs = [tab for tab in tabs if (tab[0].find('/logout/') == -1) and test(tab[0],url_toks)]
    if (not utils.is_SuperAdministrator(request)):
	tabs = [tab for tab in tabs if (tab[0].find('/administrator/') == -1) and test(tab[0],url_toks)]
    else:
	tabs = [tab for tab in tabs if (tab[0].find('/logout/') > -1) or test(tab[0],url_toks) and (tab[0].find('://') == -1) and (tab[0].find('/about/') == -1) and (tab[0].find('/problems/') == -1)]
    return tabs

def _default(request,center_content,head=[],gid=None,tabs=_navigation_tabs):
    url_toks = django_utils.parse_url_parms(request)

    left_content = topmenu_content()
    featured_content = featured_products_content(left_content)
    top_content = get_newsflash_items()
    newsflash_nav = get_newsflash_items(isNavigation_only=True)
    right_content = ''

    html_newsflash = ''
    if (len(url_toks) == 0):
        t_newsflash = get_template('_newsflash.html')
        html_newsflash = t_newsflash.render(Context({'top_content':top_content,'NEWSFLASH_NAVIGATION':newsflash_nav}))
    else:
        h = oohtml.Html()
        div = h.tag(oohtml.oohtml.DIV)
        div.text(oohtml.renderAnchor('/','HOME',target='_top'))
        
        t_newsflash = get_template('_breadcrumbs.html')
        html_newsflash = t_newsflash.render(Context({'BREADCRUMBS':h.toHtml()}))
    
    ctx = {'left_content':featured_content, 
           'center_content':center_content,
           'right_content':right_content,
           'NEWSFLASH':html_newsflash
           }
    js_list = ['http://media.vyperlogix.com/js/constants.js','http://media.vyperlogix.com/js/$.js','http://media.vyperlogix.com/js/rand.js','http://media.vyperlogix.com/js/int.js']
    tabs = filter_tabs(request,tabs)
    return pages.render_the_page(request,'%s' % (_title),'_home.html',_navigation_menu_type,tabs,template_folder='site_template',context=ctx,js=js_list,head=head)

def default(request,SSL=False):
    global _fully_qualified_http_host
    global _domain
    
    _fully_qualified_http_host = django_utils.get_fully_qualified_http_host(request)
    _domain = '%s' % ('/' if (_utils.isBeingDebugged) else '/')
    
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    
    #pageNo = 1
    #numPerPage = 15
    #if (len(url_toks) == 4) and (url_toks[0] == 'article') and (url_toks[1] in ['page','next']) and (str(url_toks[2]).isdigit()) and (str(url_toks[3]).isdigit()):
	#pageNo = int(url_toks[2])
	#numPerPage = int(url_toks[3])

    #frontpage_content = get_frontpage_items(pageNo=pageNo,numPerPage=numPerPage)
    frontpage_content = oohtml.render_IFRAME(src="http://blog.vyperlogix.com", title="The Vyper Logix Blog", frameborder="0", width="1000", height="3000", scrolling="auto")
    return _default(request,frontpage_content)

def about(request,SSL=False):
    tabs = filter_tabs(request,_navigation_tabs)
    return pages.render_the_page(request,'About - %s' % (_title),'_about.html',_navigation_menu_type,tabs,template_folder='site_template',context={})

def grid_head():
    from vyperlogix.html.flexigrid import script
    head_list = script.head_list('/static/flexigrid')
    return head_list

def jqGrid_head(head):
    from vyperlogix.html.jqgrid import scripts
    head_list = script.head_list('/static/jqGrid',head)
    return head_list

def render_author_info(modified,author):
    items = []

    modified_on = _utils.getAsDateTimeStr(modified,fmt='%s, %s' % (_utils.formatShortBlogDateStr(),_utils.formatSimpleBlogTimeStr()))
    
    h = oohtml.Html()
    h.tagSPAN(modified_on, style='font-size: 9px;')
    h.tagSPAN('&nbsp;by&nbsp;')
    h.tagSPAN(author, style='font-size: 9px;')
    items += [[h.toHtml()]]

    h = oohtml.Html()
    h.html_simple_table(items, border="0")
    return h.toHtml()

def render_download_article(request,article):
    h = oohtml.Html()
    try:
        _title = article.Jos_Content.title
    except:
        _title = article.Jos_Docman.dmname
    article_link = oohtml.renderAnchor('%s' % ('/%s/%s/%s/' % ('view','article',article.Jos_Content.id)),_title,target='_top')
    h._tagH3(article_link)
    try:
        _text = article.Jos_Content.introtext
        _text = _text.replace('<strong>{xtypo_download}</strong>','').replace('<strong>{/xtypo_download}</strong>','')
    except:
        url_toks = django_utils.parse_url_parms(request)
        _text = oohtml.renderAnchor('/%s/%s/' % ('/'.join(url_toks),'/'.join(['%d' % (article.Jos_Docman.id),'%d' % (article.Jos_Docman_Licenses.id)])),'More...',target='_top')
    span = h.tagSPAN('')
    html = anchors.rewrite_anchors(_utils.ascii_only(normalize_images(_text)),callback=rewrite_anchor,isDebug=False)
    span.text(html)
    try:
        h.tagDIV(render_author_info(article.Jos_Content.modified,article.Jos_Users.name))
    except:
        pass
    h.tagHR()
    return h.toHtml()

def render_downloads_blog_content(request,title,articles,callback=render_download_article):
    items = []

    h = oohtml.Html()
    h.tagH3(title)
    h.tagHR()
    
    items += [[h.toHtml()]]

    h = oohtml.Html()
    h.html_simple_table(items, border="0")
    content = h.toHtml()

    items = []
    items += [[h.toHtml()]]
    
    _items = []
    for article in articles:
	if (callable(callback)):
	    items += [[callback(request,article)]]
	else:
	    render_article(article,_items,'http%s://%s/%s' % ('' if (request.META['SERVER_PORT'] != 443) else 's',request.META['HTTP_HOST'],request.path),'article',request=request)
	    
    for _item in _items:
	items += [_item]

    h = oohtml.Html()
    h.html_simple_table(items, border="0")
    content = h.toHtml()
        
    return content

def render_download(item,articles,items_name,selector,request=None):
    isAble2Download = False
    try:
	item = item.Jos_Docman
    except:
	isAble2Download = True
    _id = item.id
    _title = item.dmname
    article_link = oohtml.renderAnchor('%s' % ('/view/downloads/%s/%s/' % (selector,_id)),normalize(strip_tags(_title,make_carriage_returns='<BR/>')),target='_top')
    article_pdf_link = ''
    articles.append(['<table width="100%%" bgcolor="#585858"><tr><td width="80%%" align="left"><span style="color: cyan; font-size: medium; font-weight: bold; font-family: Verdana, Geneva, Arial, Helvetica, sans-serif;">%s</span></td><td width="20%%" align="right">%s</td></tr></table>' % (article_link,article_pdf_link)])
    aUser = sqlalchemy_model.user_by_id(item.dmsubmitedby)
    _user = aUser[0].name if (len(aUser) > 0) else 'UNKNOWN'
    _date = item.dmdate_published
    updated_on = _utils.getAsDateTimeStr(_date,fmt='%s, %s' % (_utils.formatShortBlogDateStr(),_utils.formatSimpleBlogTimeStr()))
    articles.append(['<small>By %s, on %s</small><br/>' % (_user,updated_on)])
    into_text = item.dmdescription
    articles.append(['<small>%s</small><br/>' % (normalize(strip_tags(into_text,make_carriage_returns='<BR/>')))])
    articles.append(['<small>Last update : %s</small><br/>' % (updated_on)])
    if (isAble2Download):
	if (utils.is_authenticated(request)):
	    h = oohtml.Html()
	    h.tag_IMG(src='/static/administrator/images/download_f2.png')
	    download_link = oohtml.renderAnchor('%s' % ('/%s/%s/' % (selector,_id)),h.toHtml(),target='_top')
	    articles.append(['<table width="100%%" bgcolor="#585858"><tr><td width="80%%" align="center"><span style="color: cyan; font-size: medium; font-weight: bold; font-family: Verdana, Geneva, Arial, Helvetica, sans-serif;">%s</span></td></tr></table>' % (download_link)])
	else:
	    t_subscribe = get_template('_Subscribe.htm')
	    html_subscribe = t_subscribe.render(Context({}))
	    articles.append(html_subscribe)
    articles.append(['<hr align="left" color="#ffff00" width="80%"/>'])

def view(request,SSL=False):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    if (params.has_key(view_verb_symbol)):
        area = params[view_verb_symbol]
        cat_id = None
        section_id = None
        title = ''
        content = '<h3>Under Construction</h3>'
        if (area == 'section'):
            section_id = params['id']
            section = sqlalchemy_model.section_by_id(section_id)
            try:
                title = section.title
            except:
                pass
            pass
        else:
            cat_id = params['id']
        if (cat_id is not None) or (section_id is not None):
            items = sqlalchemy_model.content_items_with_author(cat_id,section_id,order_by='modified DESC')
            content = render_downloads_blog_content(request,title,items)
        elif ( (lists.isDict(area)) and (area.has_key('downloads')) ):
	    if (area.has_key('download')):
		gid = int(area['download'])
		items = sqlalchemy_model.docman_item_by_gid(gid)
		_content = []
		for item in items:
		    render_download(item,_content,'Python Downloads','download')
		content = ''.join([''.join(item) if (misc.isList(item)) else item for item in _content])
        elif (lists.isDict(area)) and (area.has_key('article')):
            article_id = area['article']
            articles = sqlalchemy_model.content_by_id(article_id)
            _articles = []
	    for item in articles:
		render_article(item,_articles,'http%s://%s/%s' % ('' if (request.META['SERVER_PORT'] != 443) else 's',request.META['HTTP_HOST'],request.path),'',request=request)
	    if (not utils.is_authenticated(request)):
		t_subscribe = get_template('_Subscribe.htm')
		html_subscribe = t_subscribe.render(Context({}))
		_articles.append(html_subscribe)
            content = '<br/>'.join([''.join(item) if (misc.isList(item)) else item for item in _articles])
        elif (lists.isDict(area)) and (area.has_key('pypi-feed')):
	    _id = area['pypi-feed']
	    _id = int(_id) if (str(_id).isdigit()) else _id
	    feeds = feed_models.PyPI.objects.filter(id=_id)
	    t_feed = get_template('_pypi-feed.html')
	    c = Context({'source':'www.python.org/pypi'})
	    if (feeds.count() > 0):
		aFeed = feeds[0]
		c['name'] = aFeed.name
		c['version'] = aFeed.version
		c['descr'] = aFeed.descr
		c['link'] = oohtml.renderAnchor('%s' % (aFeed.link),aFeed.name) if (utils.is_authenticated(request)) else _not_yet_subscriber
		c['timestamp'] = _utils.getAsDateTimeStr(aFeed.timestamp,fmt=_utils.formatDjangoDateTimeStr())
	    content = t_feed.render(c)
	else:
	    try:
		isAreaDownload = (lists.isDict(area)) and (area.has_key('download'))
	    except:
		isAreaDownload = False
	    if (area == 'downloads') or (isAreaDownload):
		items = sqlalchemy_model.docman_items()
		pageNo = 1
		numPerPage = 10
		if (len(url_toks) == 5) and (url_toks[0] == 'view') and (url_toks[1] == 'download') and (url_toks[2] in ['page','next']) and (str(url_toks[3]).isdigit()) and (str(url_toks[4]).isdigit()):
		    pageNo = int(url_toks[3])
		    numPerPage = int(url_toks[4])
		content = django_utils.paginate(items,'Python Downloads','view/download',pageNo=pageNo,numPerPage=numPerPage,maxPages=10,callback=render_download)
        return _default(request,content)
    elif (url_toks[0] == view_verb_symbol):
        d_parms = lists.HashedLists2(url_toks[1:])
        cat_id = d_parms[category_symbol]
        sect_id = d_parms[sectionid_symbol]
        grid_width = 450
        grid_height = 350
        if (cat_id) and (sect_id):
            content = ''
            categories = sqlalchemy_model.category_and_section(cat_id,sect_id)
            grid_name = 'table_articles_grid'
            for category in categories:
                content += get_category_and_section_content(request,grid_name,category,cat_id,sect_id,width=grid_width)
            content += grid_content_articles(request,grid_name,cat_id,sect_id,width=grid_width,height=grid_height)
            return _default(request,content,head=grid_head())
    elif (url_toks[0] in ['section','category']):
	isSection = url_toks[0] == 'section'
	isCategory = url_toks[0] == 'category'
	try:
	    ids = [int(url_toks[-1].split(' ')[-1])]
	except:
	    toks = url_toks[-1].split(' ')
	    ids = [int(t) for t in toks if (str(t).isdigit())]
	content = ''
	someItems = [sqlalchemy_model.section_by_id(anId) if (isSection) else sqlalchemy_model.category_by_id(anId) for anId in ids]
	someItems = [item for item in someItems if (item is not None) and (item != [])]
	if (len(someItems) > 0):
	    items = []
	    titles = []
	    for item in someItems:
		items += sqlalchemy_model.content_items(None if (isSection) else item.id,item.id if (isSection) else None,order_by="ordering")
		titles.append(item.title)
	    content = render_downloads_blog_content(request,'%s: %s' % (url_toks[0].capitalize(),':'.join(titles)),items,callback=None)
	return _default(request,content)
    else:
        print '%s :: Unknown "%s".' % (misc.funcName(),url_toks)
    return HttpResponseNotFound()

def get_license_agreement_content(request):
    h = oohtml.Html()
    form = h.tagFORM(name='license_agreement',action="%s%ssubmit/license-signature/" % (request.path,'/' if (not request.path.endswith('/')) else ''))
    form.tagRADIO('no_agreement','0',"I don't agree", isCHECKED=True, id="radio_agreement")
    form.tagRADIO('yes_agreement','1',"I agree completely", isCHECKED=False, id="radio_agreement")
    form.tagSUBMIT('Click here to proceed', value='Click here to proceed')
    return h.toHtml()

def get_docman_license_content(request,license):
    h = oohtml.Html()
    h.tagH3(license.name)
    h.tagBR()
    html = anchors.rewrite_anchors(license.license,callback=rewrite_anchor,isDebug=False)
    h.tagP(html)
    div = h.tagDIV('')
    div.text(get_license_agreement_content(request))
    return h.toHtml()

def get_docman_content(request,item):
    h = oohtml.Html()
    h.tagH3(item.dmname)
    h.tagHR()
    content = ''
    licenses = sqlalchemy_model.docman_license_by_id(item.dmlicense_id)
    for license in licenses:
        content += get_docman_license_content(request,license)
        h.tagDIV(content)
    h.tagHR()
    return h.toHtml()

def doc_download(request):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    if (params.has_key(doc_download_verb_symbol)):
        d_parms = params[doc_download_verb_symbol]
        if (lists.isDict(d_parms)):
            if (d_parms.has_key('gid')):
                items = sqlalchemy_model.docman_item_by_gid(d_parms['gid'])
                if (d_parms.has_key('submit')) and  (d_parms['submit'] == 'license-signature'):
                    pass
                else:
                    content = ''
                    for item in items:
                        content += get_docman_content(request,item)
                return _default(request,content)
        else:
            url = '\\'.join(url_toks[len(url_toks)-3:-1]).replace('\\"','')
            return HttpResponseRedirect(url)
    else:
        print '%s :: Unknown "%s".' % (misc.funcName(),url_toks)

def register(request):
    _allow_urls = ['/']
    tabs = [tab for tab in _navigation_tabs]
    return _default(request,'',tabs=tabs)

def search(request):
    return _default(request,'')

def send_email(from_addrs, to_addrs, msg_content, subject):
    from vyperlogix.mail.message import Message
    msg = Message(from_addrs, to_addrs, msg_content, subject=subject)

    from vyperlogix.mail.mailServer import AdhocServer
    smtp = AdhocServer(settings._SMTP_SERVER)
    smtp.sendEmail(msg)

def render_email_addendum():
    t_content = get_template('CONFIDENTIALITY-NOTICE.html')
    t_context = {}
    return t_content.render(Context(t_context))

def send_problem_email(request,email_address, name, problem):
    t_content = get_template('pypi_Problem_Email.txt')
    msg_context = {'NAME':name, 'PROBLEM':problem, 'CONFIDENTIALITYNOTICE':render_email_addendum()}
    msg_content = t_content.render(Context(msg_context))

    try:
	send_email(email_address, 'support@vyperlogix.com', msg_content, "This is my problem with www.pypi.info.")
	request.session['has_sent_problem_email_%s' % (email_address)] = _utils.timeStampLocalTime()
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	return info_string

    return 'Your email was successfully sent...'

def send_registration_email(email_address, product_name, product_link, site_link):
    t_EULA = get_template('pypi_EULA.txt')
    EULA_context = {'PRODUCT_NAME':product_name, 'COMPANY_NAME':'Vyper Logix Corp.'}
    EULA_content = t_EULA.render(Context(EULA_context))

    t_content = get_template('pypi_Registration_Email.txt')
    msg_context = {'PRODUCT_NAME':product_name, 'PRODUCT_LINK':product_link, 'SITE_LINK':site_link, 'EULA':EULA_content, 'CONFIDENTIALITYNOTICE':render_email_addendum()}
    msg_content = t_content.render(Context(msg_context))

    try:
	send_email('support@vyperlogix.com', email_address, msg_content, "We have received %s Registration Request." % (product_name))
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	return info_string

    try:
	send_email(email_address, 'sales@vyperlogix.com', msg_content, "We have received %s Registration Request from %s." % (product_name,email_address))
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	return info_string

    return None

def send_password_email(email_address, product_name, product_link, site_link, password):
    t_content = get_template('pypi_Password_Email.txt')
    msg_context = {'PRODUCT_NAME':product_name, 'PRODUCT_LINK':product_link, 'SITE_LINK':site_link, 'PASSWORD':password, 'CONFIDENTIALITYNOTICE':render_email_addendum()}
    msg_content = t_content.render(Context(msg_context))

    try:
	send_email('support@vyperlogix.com', email_address, msg_content, "We have received %s Password Retrieval Request." % (product_name))
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	return info_string

    try:
	send_email(email_address, 'sales@vyperlogix.com', msg_content, "We have received %s Password Retrieval Request from %s." % (product_name,email_address))
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	return info_string

    return None

def send_username_email(email_address, product_name, product_link, site_link, username):
    t_content = get_template('pypi_Username_Email.txt')
    msg_context = {'PRODUCT_NAME':product_name, 'PRODUCT_LINK':product_link, 'SITE_LINK':site_link, 'USERNAME':username, 'CONFIDENTIALITYNOTICE':render_email_addendum()}
    msg_content = t_content.render(Context(msg_context))

    try:
	send_email('support@vyperlogix.com', email_address, msg_content, "We have received %s Username Retrieval Request." % (product_name))
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	return info_string

    try:
	send_email(email_address, 'sales@vyperlogix.com', msg_content, "We have received %s Username Retrieval Request from %s." % (product_name,email_address))
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	return info_string

    return None

def send_change_email(old_email, new_email, product_name, product_link, site_link):
    t_content = get_template('pypi_Change_Email.txt')
    msg_context = {'PRODUCT_NAME':product_name, 'PRODUCT_LINK':product_link, 'SITE_LINK':site_link, 'CONFIDENTIALITYNOTICE':render_email_addendum()}
    msg_context['NEW_EMAIL'] = new_email if (isinstance(new_email,str)) else old_email
    msg_context['TO_FROM'] = 'to' if (isinstance(new_email,str)) else 'from'
    msg_content = t_content.render(Context(msg_context))

    try:
	send_email('support@vyperlogix.com', old_email, msg_content, "Your Email Address has been changed for %s." % (product_name))
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	return info_string

    try:
	send_email(old_email, 'sales@vyperlogix.com', msg_content, "An Email Address has been changed for %s from %s." % (product_name,old_email))
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	return info_string

    return None

def login(request):
    use_django_models = True
    
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    area = params['login']
    t_loginForm = get_template('_UserLoginForm.htm')
    c = Context({'HTTP_HOST':'http%s://%s' % ('s' if (settings.SESSION_COOKIE_SECURE) else '',request.META['HTTP_HOST'] if (request.META.has_key('HTTP_HOST')) else '')})
    c['PAYMENT_OPTIONS'] = ''
    tabs = [tab for tab in _navigation_tabs if (tab[0].find('/%s/' % (url_toks[0])) == -1)]
    if (area is not None):
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
	    form = area['form']
	    if (form == 'submit'):
		_is_request_https = True if (django_utils.is_Production or django_utils.is_Staging) else django_utils.is_request_HTTPS(request)
		if (_is_request_https):
		    username = django_utils.get_from_post(request,'username','')
		    passwd = django_utils.get_from_post(request,'passwd','')
		    remember = django_utils.get_from_post(request,'remember','')
		    items = sqlalchemy_model.user_by_username(username) if (not use_django_models) else views_models.User.objects.filter(username=username)
		    if (len(items) == 0):
			request.session['has_joomla_login_success'] = False
			request.session['joomla_user'] = []
			request.session['is_SuperAdministrator'] = False
			c['ERROR'] = 'INVALID User Name or Password.'
		    else:
			if (captcha.is_captcha_form_valid(request)):
			    aUser = items[0]
			    if (aUser.block == 0):
				parts = aUser.password.split(':')
				crypt = parts[-1]
				salt = parts[0]
				_pwd = md5.new(salt+passwd).hexdigest()
				if (_pwd == crypt):
				    request.session['has_joomla_login_success'] = True
				    _items = [item.asPythonDict() for item in sqlalchemy_model.agent.asSmartObjects(items)] if (not use_django_models) else items
				    request.session['joomla_user'] = _items
				    request.session['is_SuperAdministrator'] = utils._is_SuperAdministrator(request)
				    aUser.lastvisitDate = _utils.getFromDateTimeStr(_utils.timeStampMySQL(),format=_utils.formatMySQLDateTimeStr())
				    if (use_django_models):
					try:
					    aUser.save()
					except Exception, e:
					    send_problem_email(request,'do-not-respond@vyperlogix.com', '%s (%s)' % (misc.funcName(),url_toks), _utils.formattedException(details=e))
				    else:
					anAgent = sqlalchemy_model.update_user(aUser)
					if (len(anAgent.lastError) > 0):
					    send_problem_email(request,'do-not-respond@vyperlogix.com', '%s (%s)' % (misc.funcName(),url_toks), anAgent.lastError)
				    return HttpResponseRedirect("/")
				else:
				    request.session['has_joomla_login_success'] = False
				    request.session['joomla_user'] = []
				    request.session['is_SuperAdministrator'] = False
				    c['ERROR'] = 'INVALID User Name or Password.'
			    else:
				c['ERROR'] = 'Your user account is blocked pending receipt of your Subscription payment.  Please take some time to ensure your payment has processed before returning to Login again.'
				t_subscribe = get_template('_Subscribe.htm')
				html_subscribe = t_subscribe.render(Context({}))
				c['PAYMENT_OPTIONS'] = html_subscribe
			else:
			    c['ERROR'] = 'INVALID Captcha - PLS try again, try to enter the correct characters.'
		else:
		    c['ERROR'] = 'You CANNOT login until your request has been secured.'
        else:
	    c['ERROR'] = 'Please enable browser cookies and try again.'
    elif (not utils.is_authenticated(request)):
	if (url_toks[0] == 'register'):
	    area = params['register']
	    t_loginForm = get_template('_UserRegisterForm.htm')
	    if (area is not None):
		form = area['form']
		if (form == 'submit'):
		    username = django_utils.get_from_post(request,'username','')
		    passwd = django_utils.get_from_post(request,'passwd','')
		    name = django_utils.get_from_post(request,'name','')
		    email = django_utils.get_from_post(request,'email','')
		    users1 = sqlalchemy_model.user_by_username(username)
		    if (validateEmail.validateEmail(email)):
			users2 = sqlalchemy_model.user_by_email(email) if (not use_django_models) else views_models.User.objects.filter(email='raychorn@vyperlogix.com')
			if (len(users1) == 0) and (len(users2) == 0):
			    domain_name = validateEmail.parseEmail(email)[0]
			    freehosts = sqlalchemy_model.get_freehost_by_name(domain_name)
			    isDomainOk = True if (not settings.DISALLOW_FREEHOSTS) else (len(freehosts) == 0)
			    if (isDomainOk):
				if (captcha.is_captcha_form_valid(request)):
				    from vyperlogix.misc import GenPasswd
				    
				    salt = GenPasswd.GenPasswd(length=16)
				    _pwd = md5.new(salt+passwd).hexdigest()
				    
				    if (use_django_models):
					aUser = views_models.User(username=username,password=salt+':'+_pwd,name=name,email=email,block=1,sendEmail=1,usertype='Registered',registerDate=_utils.getFromDateTimeStr(_utils.timeStampMySQL(),format=_utils.formatMySQLDateTimeStr()),lastvisitDate=_utils.getFromDateTimeStr(_utils.timeStampMySQL(),format=_utils.formatMySQLDateTimeStr()),activation='')
					try:
					    aUser.save()
					except Exception, e:
					    send_problem_email(request,'do-not-respond@vyperlogix.com', '%s (%s)' % (misc.funcName(),url_toks), _utils.formattedException(details=e))
				    else:
					aUser = sqlalchemy_model.Jos_Users(username=username,password=salt+':'+_pwd,name=name,email=email,block=1,sendEmail=1,usertype='Registered',registerDate=_utils.getFromDateTimeStr(_utils.timeStampMySQL(),format=_utils.formatMySQLDateTimeStr()),lastvisitDate=_utils.getFromDateTimeStr(_utils.timeStampMySQL(),format=_utils.formatMySQLDateTimeStr()),activation='',params='')
					anAgent = sqlalchemy_model.insert_new_user(aUser)
					if (len(anAgent.lastError) > 0):
					    send_problem_email(request,'do-not-respond@vyperlogix.com', '%s (%s)' % (misc.funcName(),url_toks), anAgent.lastError)
				    t_subscribe = get_template('_Subscribe.htm')
				    html_subscribe = t_subscribe.render(Context({}))
				    c['SUBSCRIBE'] = html_subscribe
				    t_loginForm = get_template('_UserRegistered.htm')
				    t = send_registration_email(email, 'Your Premier Python Information (www.pypi.info)', '', 'http://%s' % (django_utils.get_fully_qualified_http_host(request)))
				    h = oohtml.Html()
				    h.tagP('Successful Registration')
				    c['STATUS'] = h.toHtml()
				    h = oohtml.Html()
				    h.tagP(t)
				    c['ERROR'] = h.toHtml()
				else:
				    c['ERROR'] = 'INVALID Captcha - PLS try again, try to enter the correct characters.'
			    else:
				c['ERROR'] = 'INVALID Email - You cannot use an email address from a FREE Email Service, Sorry but this is no place to be anonymous.'
			else:
			    c['ERROR'] = 'INVALID Username or Email - You cannot reuse existing Usernames or Emails.'
		    else:
			c['ERROR'] = 'INVALID Email - You cannot use an invalid email address.'
	elif (url_toks[0] == 'subscribe'):
	    t_loginForm = get_template('_Subscribe.htm')
	elif (url_toks[0] == 'forgot'):
	    t_loginForm = get_template('_UserForgot%sForm.htm' % (str(url_toks[1]).capitalize()))
	    if (url_toks[-1] == 'submit'):
		if (url_toks[1] == 'password'):
		    username = django_utils.get_from_post(request,'username','')
		    email = django_utils.get_from_post(request,'email','')
		    users = sqlalchemy_model.user_by_username_and_email(username,email) if (not use_django_models) else views_models.User.objects.filter(Q(email=email) and Q(username=username))
		    if (len(users) == 1):
			if (captcha.is_captcha_form_valid(request)):
			    aUser = users[0]
			    from vyperlogix.misc import GenPasswd
			    
			    salt = GenPasswd.GenPasswd(length=16).replace(':','')
			    passwd = GenPasswd.GenPasswdFriendly(maxlength=15,uniquely=True)
			    _pwd = md5.new(salt+passwd).hexdigest()
			    
			    aUser.password = '%s:%s' % (salt,_pwd)
			    
			    if (use_django_models):
				aUser.save()
			    else:
				sqlalchemy_model.agent.commit()
				    
			    t = send_password_email(email, 'Your Premier Python Information (www.pypi.info)', '', 'http://%s' % (django_utils.get_fully_qualified_http_host(request)),passwd)
			    h = oohtml.Html()
			    h.tagP(t)
			    c['ERROR'] = h.toHtml()
			    t_loginForm = get_template('_UserForgot%sSent.htm' % (str(url_toks[1]).capitalize()))
			else:
			    c['ERROR'] = 'INVALID Captcha - PLS try again, try to enter the correct characters.'
		    else:
			c['ERROR'] = 'INVALID Username or Email - You must give the correct Username and Email Address.'
			t_loginForm = get_template('_UserForgot%sForm.htm' % (str(url_toks[1]).capitalize()))
		elif (url_toks[1] == 'username'):
		    email = django_utils.get_from_post(request,'email','')
		    users = sqlalchemy_model.user_by_email(email) if (not use_django_models) else views_models.User.objects.filter(email=email)
		    if (len(users) == 1):
			t = send_username_email(email, 'Your Premier Python Information (www.pypi.info)', '', 'http://%s' % (django_utils.get_fully_qualified_http_host(request)),users[0].username)
			h = oohtml.Html()
			h.tagP(t)
			c['ERROR'] = h.toHtml()
			t_loginForm = get_template('_UserForgot%sSent.htm' % (str(url_toks[1]).capitalize()))
		    else:
			c['ERROR'] = 'INVALID Email - You must give the correct Email Address.'
			t_loginForm = get_template('_UserForgot%sForm.htm' % (str(url_toks[1]).capitalize()))
	elif (url_toks[0] == 'change'):
	    t_loginForm = get_template('_UserChange%sForm.htm' % (str(url_toks[1]).capitalize()))
	    if (url_toks[-1] == 'submit'):
		if (url_toks[1] == 'email'):
		    username = django_utils.get_from_post(request,'username','')
		    password = django_utils.get_from_post(request,'password','')
		    old_email = django_utils.get_from_post(request,'old_email','')
		    new_email = django_utils.get_from_post(request,'new_email','')
		    users = sqlalchemy_model.user_by_username_and_email(username,old_email) if (not use_django_models) else views_models.User.objects.filter(Q(email=old_email) and Q(username=username))
		    if (validateEmail.validateEmail(new_email)):
			if (len(users) == 1):
			    domain_name = validateEmail.parseEmail(new_email)[0]
			    freehosts = sqlalchemy_model.get_freehost_by_name(domain_name)
			    isDomainOk = True if (not settings.DISALLOW_FREEHOSTS) else (len(freehosts) == 0)
			    if (isDomainOk):
				if (captcha.is_captcha_form_valid(request)):
				    aUser = users[0]
				    parts = aUser.password.split(':')
				    crypt = parts[-1]
				    salt = parts[0]
				    _pwd = md5.new(salt+password).hexdigest()
				    if (_pwd == crypt):
					aUser.email = new_email
					if (use_django_models):
					    aUser.save()
					else:
					    sqlalchemy_model.agent.commit()
					t = send_change_email(old_email, new_email, 'Your Premier Python Information (www.pypi.info)', '', 'http://%s' % (django_utils.get_fully_qualified_http_host(request)))
					send_change_email(old_email, None, 'Your Premier Python Information (www.pypi.info)', '', 'http://%s' % (django_utils.get_fully_qualified_http_host(request)))
					t_loginForm = get_template('_%sChanged.htm' % (str(url_toks[1]).capitalize()))
					c['STATUS'] = 'Your email address has been changed.'
					h = oohtml.Html()
					h.tagP(t)
					c['ERROR'] = h.toHtml()
				else:
				    c['ERROR'] = 'INVALID Captcha - PLS try again, try to enter the correct characters.'
			    else:
				c['ERROR'] = 'INVALID Email - You cannot use an email address from a FREE Email Service, Sorry but this is no place to be anonymous.'
			else:
			    c['ERROR'] = 'INVALID Username or Email - You must give the correct Username and Email Address.'
		    else:
			c['ERROR'] = 'INVALID Email - You cannot use an invalid new email address.'
    elif (utils.is_authenticated(request)):
	if (url_toks[0] == 'logout'):
	    request.session['has_joomla_login_success'] = False
	    request.session['joomla_user'] = []
	    request.session['is_SuperAdministrator'] = False
	    return HttpResponseRedirect("/")
    if (len(c['PAYMENT_OPTIONS']) == 0):
	c['PAYMENT_OPTIONS'] = '<h3>Having trouble logging in ?  Did you pay your Subscription fee ?!?  <a href="/subscribe/" style="font-size: 16px;">Subscribe !</a></h3>'
    request.session.set_test_cookie()
    h = oohtml.Html()
    h.tagDIV(captcha.render_captcha_form(request,form_name='captcha_form_fields.html',font_name='BerrysHandegular.ttf',font_size=32,choices=utils.captcha_choices,fill=(255,255,255)))
    c['CAPTCHA'] = h.toHtml()
    html_loginForm = t_loginForm.render(c)
    return _default(request,html_loginForm,tabs=tabs)

def problems(request):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    c = Context({'HTTP_HOST':'http%s://%s' % ('s' if (settings.SESSION_COOKIE_SECURE) else '',request.META['HTTP_HOST'] if (request.META.has_key('HTTP_HOST')) else '')})
    t_problems = get_template('_ProblemsForm.htm')
    area = params['problems']
    if (area is not None):
        form = area['form']
        if (form == 'submit'):
            name = django_utils.get_from_post(request,'name','')
            email = django_utils.get_from_post(request,'email','')
            problem = django_utils.get_from_post(request,'problem','')
	    c['NAME'] = name
	    c['EMAIL'] = email
	    c['PROBLEM'] = problem
	    if (captcha.is_captcha_form_valid(request)):
		if (validateEmail.validateEmail(email)):
		    domain_name = validateEmail.parseEmail(email)[0]
		    freehosts = sqlalchemy_model.get_freehost_by_name(domain_name)
		    isDomainOk = True if (not settings.DISALLOW_FREEHOSTS) else (len(freehosts) == 0)
		    if (isDomainOk):
			t_problems = get_template('_ProblemSent.htm')
			t = send_problem_email(request,email, name, problem)
			if (t is not None):
			    h = oohtml.Html()
			    h.tagP('Your problem has been reported and will be handled shortly.')
			    h.tagP("You may submit one problem report per day however please don't become a SPAMMER.")
			    c['STATUS'] = h.toHtml()
			    h = oohtml.Html()
			    h.tagP(t)
			    c['ERROR'] = h.toHtml()
			else:
			    c['STATUS'] = "Don't be a SPAMMER by submitting too many problem reports each day, try back later to see if the problem you wanted to report has been corrected before trying to submit another problem report."
		    else:
			c['ERROR'] = 'INVALID Email - You cannot use an email address from a FREE Email Service, Sorry but this is no place to be anonymous.'
		else:
		    c['ERROR'] = 'INVALID Email - You cannot use an invalid email address.'
	    else:
		c['ERROR'] = 'INVALID Captcha - PLS try again, try to enter the correct characters.'
    h = oohtml.Html()
    h.tagDIV(captcha.render_captcha_form(request,form_name='captcha_form_fields.html',font_name='BerrysHandegular.ttf',font_size=32,choices=utils.captcha_choices,fill=(255,255,255)))
    c['CAPTCHA'] = h.toHtml()
    html_problems = t_problems.render(c)
    return _default(request,html_problems)

def download(request):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    if (params.has_key('download')):
	try:
	    gid = int(params['download'])
	except:
	    gid = -1
	items = sqlalchemy_model.docman_item_by_gid(gid)
	if (len(items) > 0):
	    if (utils.is_authenticated(request)):
		item = items[0]
		toks = item.dmfilename.split('Link: ')
		url = toks[-1]
		parts = url.split('/')
		fname = os.path.join(settings.MEDIA_ROOT,os.sep.join(parts[3:]))
		
		if (not os.path.exists(fname)):
		    toks = fname.split(os.sep)
		    while (len(toks) > 1):
			toks = toks[0:-1]
			fname = os.sep.join(toks)
			if (os.path.exists(fname)):
			    break
		    files = [os.path.join(fname,f) for f in os.listdir(fname) if (f.lower().find('.zip') > -1)]
		    fname = files[0]
		_contents = _utils.readBinaryFileFrom(fname)
		
		mimetype = mimetypes.guess_type(fname)[0]
		response = HttpResponse(_contents, mimetype=mimetype)
		response['Content-Disposition'] = 'attachment; filename=%s' % (fname)
		return response
	    else:
		t_subscribe = get_template('_Subscribe.htm')
		html_subscribe = t_subscribe.render(Context({}))
		return _default(request,html_subscribe)
    return _default(request,'<BIG><b>Cannot Download the selected item due to some kind of system problem.</b></BIG>')

def _default_admin(request,center_content,scripts='',head=[],gid=None,tabs=_navigation_tabs):
    url_toks = django_utils.parse_url_parms(request)

    ctx = {'center_content':center_content,'SCRIPTS':scripts}
    js_list = []
    tabs = filter_tabs(request,tabs)
    return pages.render_the_page(request,'%s' % (_title),'_admin-home.html',_navigation_menu_type,tabs,template_folder='site_template',context=ctx,js=js_list,head=head)

def grid_content_users(request,name,id_=-1,width=500,height=350):
    from vyperlogix.html.flexigrid import script
    colModel = '''
{display: '#', id : 'id', width : 30, sortable : true, align: 'left', hide: false},
{display: 'Name', name : 'name', width : 100, sortable : true, align: 'left', hide: false},
{display: 'Username', username : 'username', width : 150, sortable : true, align: 'left', hide: false},
{display: 'Email', email : 'email', width : 120, sortable : true, align: 'left', hide: false},
{display: 'UserType', usertype : 'usertype', width : 100, sortable : true, align: 'left', hide: false},
{display: 'Block', block : 'block', width : 30, sortable : true, align: 'left', hide: false},
{display: 'SendEmail', sendemail : 'sendemail', width : 50, sortable : true, align: 'left', hide: false},
{display: 'RegisterDate', registerDate : 'registerDate', width : 100, sortable : true, align: 'left', hide: false},
{display: 'Last Visit Date', lastVisitDate : 'lastVisitDate', width : 100, sortable : true, align: 'left', hide: false},
{display: 'Activation', activation : 'activation', width : 100, sortable : true, align: 'left', hide: false},
    '''
    searchitems = '''
{display: 'Name', name : 'name'},
{display: 'Username', username : 'username'},
{display: 'Email', email : 'email'},
{display: 'UserType', usertype : 'usertype'},
{display: 'Block', block : 'block'},
{display: 'SendEmail', sendemail : 'sendemail'},
{display: 'RegisterDate', registerDate : 'registerDate'},
{display: 'Last Visit Date', lastVisitDate : 'lastVisitDate'},
{display: 'Activation', activation : 'activation'},
    '''
    url = 'http://%s/grid/users/' % (django_utils.get_fully_qualified_http_host(request))
    if (str(id_).isdigit()) and (id_ > -1):
	url = 'http://%s/grid/user/%d/' % (django_utils.get_fully_qualified_http_host(request),id_)
    js = script.script_head(name,url,'Users',colModel,searchitems,'username','asc',width=width,height=height)
    return js

def grid_content_articles(request,name,id_=-1,width=500,height=350,extra=None):
    from vyperlogix.html.flexigrid import script
    colModel = '''
{display: '#', id : 'id', width : 30, sortable : true, align: 'left', hide: false},
{display: 'Title', title : 'title', width : 200, sortable : true, align: 'left', hide: false},
{display: 'Alias', alias : 'alias', width : 0, sortable : true, align: 'left', hide: true},
{display: 'State', state : 'state', width : 20, sortable : true, align: 'left', hide: false},
{display: 'Publish-Up', publish_up : 'publish_up', width : 120, sortable : true, align: 'left', hide: false},
{display: 'Publish-Down', publish_down : 'publish_down', width : 120, sortable : true, align: 'left', hide: false},
{display: 'Modified', modified : 'modified', width : 120, sortable : true, align: 'left', hide: false},
{display: 'Section', section : 'section', width : 100, sortable : true, align: 'left', hide: false},
{display: 'Category', category : 'category', width : 100, sortable : true, align: 'left', hide: false},
{display: 'User', username : 'username', width : 100, sortable : true, align: 'left', hide: false},
{display: 'UserType', usertype : 'usertype', width : 100, sortable : true, align: 'left', hide: false},
    '''
    searchitems = '''
{display: '#', name : 'jos_content.id'},
{display: 'Title', name : 'jos_content.title'},
{display: 'Alias', name : 'jos_content.alias'},
{display: 'State', name : 'jos_content.state'},
{display: 'Publish-Up', name : 'jos_content.publish_up'},
{display: 'Publish-Down', name : 'jos_content.publish_down'},
{display: 'Modified', name : 'jos_content.modified'},
{display: 'Section', name : 'jos_section.section'},
{display: 'Category', name : 'jos_category.category'},
{display: 'User', name : 'jos_user.username'},
{display: 'UserType', name : 'jos_user.usertype'},
    '''
    url = 'http://%s/grid/articles/%s' % (django_utils.get_fully_qualified_http_host(request),extra+'/' if (isinstance(extra,str)) else '')
    if (str(id_).isdigit()) and (id_ > -1):
	url = 'http://%s/grid/article/%d/' % (django_utils.get_fully_qualified_http_host(request),id_)
    js = script.script_head(name,url,'Articles',colModel,searchitems,'title','asc',width=width,height=height)
    return js

def grid(request):
    from vyperlogix.classes import SmartObject
    from vyperlogix.html.flexigrid.grid_handler import grid_handler
    
    url_toks = django_utils.parse_url_parms(request)
    articles = SmartObject.SmartObject()
    d_parms = _utils.get_dict_as_pairs(url_toks)
    _query = django_utils.get_from_post(request,'query','')
    _qtype = django_utils.get_from_post(request,'qtype','')
    if (len(url_toks) == 1) and (url_toks[0] == grid_verb_symbol):
        cat_id = _utils._int(d_parms[category_symbol])
        sect_id = _utils._int(d_parms[sectionid_symbol])
        articles = []
        num = 1
        _articles = sqlalchemy_model.content_items_for_grid(cat_id,sect_id)
        for article in _articles:
            link = '/%s/article/%d/category/%d/section/%d/' % (view_verb_symbol,article.Jos_Content.id,article.Jos_Content.catid,article.Jos_Content.sectionid)
            article_link = oohtml.renderAnchor('%s' % (link),article.Jos_Content.title,target='_top',class_='grid_link')
            d_rec = {'id':num, 'title':article_link, 'author':article.Jos_Users.name, 'hits':article.Jos_Content.hits}
            articles.append(SmartObject.SmartObject(d_rec))
            num += 1
	content = grid_handler(request,articles,lambda r:[r.id, r.title, r.author, r.hits])
    elif (d_parms[grid_verb_symbol] in ['users','user']):
	singleUser = d_parms[grid_verb_symbol] == 'user'
        items = []
        num = 1
	_users = sqlalchemy_model.users() if (not singleUser) else sqlalchemy_model.user_by_id(-1)
        for k,users in _users.iteritems():
	    for aUser in users:
		url = 'http://%s/administrator/user/%d/' % (django_utils.get_fully_qualified_http_host(request),aUser.id)
		_link = oohtml.renderAnchor(url,'%d' % (aUser.id),target='_top')
		d_rec = {'id':_link, 'username':aUser.username, 'name':aUser.name, 'email':aUser.email, 'usertype':aUser.usertype, 'block':aUser.block, 'sendemail':aUser.sendEmail, 'registerDate':_utils.getAsSimpleDateStr(aUser.registerDate,_utils.formatSalesForceDateTimeStr()) if (aUser.registerDate is not None) else '', 'lastVisitDate':_utils.getAsSimpleDateStr(aUser.lastvisitDate,_utils.formatSalesForceDateTimeStr()) if (aUser.lastvisitDate is not None) else '', 'activation':aUser.activation}
		items.append(SmartObject.SmartObject(d_rec))
		num += 1
	content = grid_handler(request,items,lambda r:[r.id, r.name, r.username, r.email, r.usertype, r.block, r.sendemail, r.registerDate, r.lastVisitDate, r.activation])
    elif (d_parms[grid_verb_symbol] in ['articles','article']) or ( (lists.isDict(d_parms[grid_verb_symbol])) and (d_parms[grid_verb_symbol].keys()[0] in ['articles','article']) ):
	_page = django_utils.get_from_post(request,'page',1)
	_rp = django_utils.get_from_post(request,'rp',10)
	_start = ((_page-1) * _rp)
	_stop = _start + _rp
	
	singleArticle = (d_parms[grid_verb_symbol] if (not lists.isDict(d_parms[grid_verb_symbol])) else d_parms[grid_verb_symbol].keys()[0]) == 'article'
        items = []
        num = 1
	_qry = sqlalchemy_model.content_items_qry()
	if (len(_qtype) > 0) and (len(_query) > 0):
	    _qry = _qry.filter("%s LIKE '%%%s%%'" % (_qtype,_query))
	if (len(url_toks) == 3):
	    _qry = _qry.order_by('jos_content.%s DESC' % (url_toks[-1]))
	_count = _qry.count()
	_articles = _qry.slice(_start,_stop) if (not singleArticle) else sqlalchemy_model.content_item_by_id(-1)
	for anArticle in _articles:
	    url = 'http://%s/administrator/article/%d/' % (django_utils.get_fully_qualified_http_host(request),anArticle.Jos_Content.id)
	    _link = oohtml.renderAnchor(url,'%d' % (anArticle.Jos_Content.id),target='_top')
	    d_rec = {'id':_link, 'title':_utils.ascii_only(anArticle.Jos_Content.title), 'alias':anArticle.Jos_Content.alias, 'state':str(anArticle.Jos_Content.state), 'section':anArticle.Jos_Sections.title, 'category':anArticle.Jos_Categories.title, 'username':anArticle.Jos_Users.username, 'usertype':anArticle.Jos_Users.usertype, 'publish_up':_utils.getAsSimpleDateStr(anArticle.Jos_Content.publish_up,_utils.formatSalesForceDateTimeStr()) if (anArticle.Jos_Content.publish_up is not None) else '','publish_down':_utils.getAsSimpleDateStr(anArticle.Jos_Content.publish_down,_utils.formatSalesForceDateTimeStr()) if (anArticle.Jos_Content.publish_down is not None) else '','modified':_utils.getAsSimpleDateStr(anArticle.Jos_Content.modified,_utils.formatSalesForceDateTimeStr()) if (anArticle.Jos_Content.modified is not None) else ''}
	    items.append(SmartObject.SmartObject(d_rec))
	    num += 1
	content = grid_handler(request,items,lambda r:[r.id, r.title, r.alias, r.state, r.publish_up, r.publish_down, r.modified, r.section, r.category, r.username, r.usertype],total=_count)
    else:
	info_string = '%s :: Unknown "%s".' % (misc.funcName(),url_toks)
	content = '<h3>%s</h3>' % (info_string)
    response = HttpResponse(content, mimetype="text/x-json")
    response['Expires'] = _utils.timeStampLocalTime(format=_utils.formatMetaHeaderExpiresOn())
    response['Last-Modified'] = _utils.timeStampLocalTime(format=_utils.formatMetaHeaderExpiresOn())
    response['Cache-Control'] = 'no-cache, must-revalidate'
    response['Pragma'] = 'no-cache'
    return response

def administrator(request,SSL=False):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    t_content = get_template('_Administrator.htm')
    c = Context({'REMOTE_ADDR':request.META['REMOTE_ADDR']})
    iconic_content = ''
    icons_content = ''
    if (utils.is_authenticated(request)) and (utils.is_SuperAdministrator(request)):
	_administrator = params['administrator']
	isEditing = (len(url_toks) > 1) and (url_toks[1] in ['user','article']) and (str(url_toks[-1]).isdigit())
	if (len(url_toks) == 1):
	    iconic_content = '''
	    <table width="100%">
	    <tr valign="top">
	    <td align="center">
	    <a href="/administrator/users/"><img src="/static/administrator/icons/icon-48-user.png" /><br/><strong>Users</strong></a>
	    </td>
	    <td align="center">
	    <a href="/administrator/articles/id/"><img src="/static/administrator/icons/icon-48-article.png" /><br/><strong>Articles (#)</strong></a>
	    </td>
	    <td align="center">
	    <a href="/administrator/articles/publish_up/"><img src="/static/administrator/icons/icon-48-article.png" /><br/><strong>Articles (publish_up)</strong></a>
	    </td>
	    </tr>
	    </table>
	    '''
	    c['ICONIC'] = iconic_content
	elif (url_toks[1] in (['users'] if (not isEditing) else ['user'])):
	    icons_content = '<a href="/administrator/"><img src="/static/administrator/images/cpanel.png" /><br/><strong>Administrator</strong></a>'
	    c['ICONS'] = icons_content

	    grid_name = 'table_users_grid'
	    grid_width = 800
	    grid_height = 200
	    _head = grid_head()

	    _id = -1
	    if (isEditing):
		_id = int(url_toks[-1])
		t_editor = get_template('_Administrator_EditUser.htm')
		c_editor = Context({'HTTP_HOST':'http%s://%s' % ('' if (request.META['SERVER_PORT'] != 443) else 's',django_utils.get_fully_qualified_http_host(request))})
		users = sqlalchemy_model.user_by_id(_id)
		from formalchemy import FieldSet
		fs = FieldSet(users[0])
		fs.configure(exclude=[fs.password,fs.params],options=[fs.gid.readonly(),fs.block.dropdown(options=[('Yes', 1), ('No', 0)]),fs.sendEmail.dropdown(options=[('Yes', 1), ('No', 0)]),fs.registerDate.readonly(),fs.lastvisitDate.readonly(),fs.usertype.dropdown(options=_usertype_options),fs.activation.readonly()])
		c_editor['FORM'] = fs.render()
		c_editor['SUBMIT_VALUE'] = 'Save User'
		html_editor = t_editor.render(c_editor)
		c['EDITOR'] = html_editor
	    else:
		content = ''
	
		h = oohtml.Html()
		h.html_simple_table([()],id=grid_name,style="display:inline;")
	
		content += h.toHtml()
		c['ICONIC'] = content

		c['ERRORS'] = '<br/>'.join(['<br/>'.join(item.split('\n')) for item in utils.get_errors(request)])
		
	    html_content = t_content.render(c)
	    return _default_admin(request,html_content,scripts=grid_content_users(request,grid_name,id_=_id,width=grid_width,height=grid_height),head=_head)
	elif (lists.isDict(_administrator)) and (_administrator['user'] == 'submit'):
	    d = lists.HashedLists()
	    for k,v in request.POST.iteritems():
		toks = k.split('-')
		_d = d[toks[1]]
		if (_d is None):
		    _d = lists.HashedLists2()
		    d[toks[1]] = _d
		else:
		    _d = _d[0]
		_d[toks[-1]] = v[0]
	    _errors = []
	    for k,v in d.iteritems():
		users = sqlalchemy_model.user_by_id(k)
		if (users is not None):
		    aUser = users[0]
		    for item in v:
			for item_k, item_v in item.iteritems():
			    try:
				aUser.__setattr__(item_k,item_v)
			    except Exception, e:
				_errors.append(_utils.formattedException(details=e))
		    sqlalchemy_model.update_user(aUser)
	    request.session['ERRORS'] = _errors
            return HttpResponseRedirect('/administrator/%ss/' % (url_toks[1]))
	elif (url_toks[1] in (['articles'] if (not isEditing) else ['article'])):
	    icons_content = '<a href="/administrator/"><img src="/static/administrator/images/cpanel.png" /><br/><strong>Administrator</strong></a>'
	    c['ICONS'] = icons_content

	    grid_name = 'table_articles_grid'
	    grid_width = 800
	    grid_height = 200
	    _head = grid_head()

	    _id = -1
	    if (isEditing):
		_id = int(url_toks[-1])
		t_editor = get_template('_Administrator_EditArticle.htm')
		c_editor = Context({'HTTP_HOST':'http%s://%s' % ('' if (request.META['SERVER_PORT'] != 443) else 's',django_utils.get_fully_qualified_http_host(request))})
		articles = sqlalchemy_model.content_item_by_id(_id)

		sections = sqlalchemy_model.sections()
		categories = sqlalchemy_model.categories_for_section(articles[0].Jos_Sections.id)
		
		from formalchemy import FieldSet
		from vyperlogix.formalchemy import render
		
		fs1 = FieldSet(articles[0].Jos_Content)
		fs1.configure(exclude=[fs1.created_by,fs1.created_by_alias,fs1.modified_by,fs1.checked_out,fs1.checked_out_time,fs1.images,fs1.urls,fs1.attribs,fs1.metakey,fs1.metadesc,fs1.metadata,fs1.sectionid,fs1.catid,fs1.mask,fs1.version,fs1.parentid,fs1.ordering,fs1.access],options=[fs1.id.hidden(),fs1.title.with_renderer(render.TextFieldRenderer),fs1.alias.with_renderer(render.TextFieldRenderer),fs1.introtext.textarea(size=(60,5)),fs1.fulltext.textarea(size=(80,20)),fs1.state.dropdown(options=[('Yes', 1), ('No', 0)]),fs1.sectionid.readonly(),fs1.catid.readonly(),fs1.hits.readonly(),fs1.created.readonly(),fs1.modified.readonly()])
		fs2 = FieldSet(articles[0].Jos_Users)
		fs2.configure(exclude=[fs2.password,fs2.block,fs2.sendEmail,fs2.gid,fs2.registerDate,fs2.lastvisitDate,fs2.activation,fs2.params],options=[fs2.name.readonly(),fs2.username.readonly(),fs2.email.readonly(),fs2.usertype.readonly()])
		fs3 = FieldSet(articles[0].Jos_Sections)
		fs3.configure(exclude=[fs3.name,fs3.image,fs3.scope,fs3.alias,fs3.image_position,fs3.description,fs3.checked_out,fs3.checked_out_time,fs3.ordering,fs3.access,fs3.count,fs3.params],options=[fs3.title.dropdown(options=[('%s' % (aSection.title),'%d' % (aSection.id)) for aSection in sections] if (misc.isList(sections)) else []),fs3.published.readonly()])
		fs4 = FieldSet(articles[0].Jos_Categories)
		fs4.configure(exclude=[fs4.parent_id,fs4.name,fs4.alias,fs4.image,fs4.image_position,fs4.description,fs4.section,fs4.checked_out,fs4.checked_out_time,fs4.ordering,fs4.editor,fs4.access,fs4.count,fs4.params],options=[fs4.title.dropdown(options=[('%s' % (aCategory.title),'%d' % (aCategory.id)) for aCategory in categories] if (misc.isList(categories)) else []),fs4.published.readonly()])
		c_editor['FORM'] = fs1.render()+'<hr align="left" width="20%"/><h3>User</h3><hr align="left" width="20%"/>'+fs2.render()+'<hr align="left" width="20%"/><h3>Section</h3><hr align="left" width="20%"/>'+fs3.render()+'<hr align="left" width="20%"/><h3>Category</h3><hr align="left" width="20%"/>'+fs4.render()
		c_editor['SUBMIT_VALUE'] = 'Save Article'
		
		c_editor['SECTION_ID'] = articles[0].Jos_Sections.id
		c_editor['SECTION_TITLE'] = articles[0].Jos_Sections.title
		
		c_editor['CATEGORY_ID'] = articles[0].Jos_Categories.id

		s_cats = '''
<script type="text/javascript">
//<![CDATA[
sect_cats = [];
cat_name = [];
{{ SECT_CATS }}
//]]>
</script>
		'''
		s = []
		for aSection in sections:
		    cats = sqlalchemy_model.categories_for_section(aSection.id)
		    t = []
		    for aCat in cats:
			t.append('%d' % (aCat.id))
			s.append("cat_name[%s] = '%s';" % (aCat.id,aCat.title))
		    s.append("sect_cats[%s] = [%s];" % (aSection.id,','.join(t)))
		c_editor['SECTIONS_CATS'] = django_utils.render_from_string(s_cats,context={'SECT_CATS':'\n'.join(s)})

		html_editor = t_editor.render(c_editor)
		c['EDITOR'] = html_editor
	    else:
		content = ''
	
		h = oohtml.Html()
		h.html_simple_table([()],id=grid_name,style="display:inline;")
	
		content += h.toHtml()
		c['ICONIC'] = content

		c['ERRORS'] = '<br/>'.join(['<br/>'.join(item.split('\n')) for item in utils.get_errors(request)])
		
	    html_content = t_content.render(c)
	    return _default_admin(request,html_content,scripts=grid_content_articles(request,grid_name,id_=_id,width=grid_width,height=grid_height,extra=url_toks[-1] if (len(url_toks) == 3) else None),head=_head)
	elif (lists.isDict(_administrator)) and (_administrator['article'] == 'submit'):
	    d = post_vars.post_from_sqlalchemy(request)
	    _errors = []
	    for item in d['Jos_Content'] if (d.has_key('Jos_Content')) else []:
		if (lists.isDict(item)):
		    for id,d_data in item.iteritems():
			articles = sqlalchemy_model.content_item_by_id(id)
			if (misc.isList(articles)):
			    aContent = articles[0]
			    _Jos_Content = aContent.__getattribute__('Jos_Content')
			    d_keys = lists.HashedLists2()
			    _keys = ListWrapper(d_data.keys())
			    r_keys = []
			    for key in _keys:
				toks = key.split('__')
				aValue = d_keys[toks[0]]
				if (len(toks) > 1):
				    if (aValue is None):
					d_keys[toks[0]] = lists.HashedLists()
					aValue = d_keys[toks[0]]
				    aValue[toks[-1]] = d_data[key]
				    i = _keys.findFirstMatching(key)
				    if (i > -1):
					r_keys.append(key)
			    for key in r_keys:
				i = _keys.findFirstMatching(key)
				if (i > -1):
				    del _keys[i]
			    for k in _keys:
				v = d_data[k]
				try:
				    _Jos_Content.__setattr__(k,v)
				except Exception, e:
				    _errors.append(_utils.formattedException(details=e))
			    try:
				for k,v in d_keys.iteritems():
				    s1 = '-'.join([v['year'][0],v['month'][0],v['day'][0]])
				    s2 = ':'.join([v['hour'][0],v['minute'][0],v['second'][0]])
				    s = s1+'T'+s2
				    try:
					ts = _utils.getFromDateTimeStr(s,format=_utils.formatSalesForceTimeStr())
					_Jos_Content.__setattr__(k,ts)
				    except ValueError:
					pass
			    except Exception, e:
				_errors.append(_utils.formattedException(details=e))
			    try:
				ts = _utils.getFromDateTimeStr(_utils.timeStampMySQL(),format=_utils.formatMySQLDateTimeStr())
				aContent.Jos_Content.modified = ts
			    except:
				_errors.append(_utils.formattedException(details=e))
			    import keywords
			    keywords.handle_keywords(aContent.Jos_Content.id,aContent.Jos_Content.introtext,1)
			    keywords.handle_keywords(aContent.Jos_Content.id,aContent.Jos_Content.fulltext,2)
			    _agent = sqlalchemy_model.update_content(aContent)
			    if (str(_agent.lastError) > 0):
				_errors.append(_agent.lastError)
	    request.session['ERRORS'] = _errors
            return HttpResponseRedirect('/administrator/%ss/' % (url_toks[1]))
    else:
	t_content = get_template('_Administrator-Invalid.htm')
    html_content = t_content.render(c)
    return _default_admin(request,html_content)

def feeds(request):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    if (request.GET.has_key('type')) and (request.GET.has_key('format')):
	return HttpResponseRedirect('/feeds/%s/' % (request.GET['type']))
    elif (len(url_toks) == 1) and (url_toks[0] == 'feeds'):
	fmt = '%Y-%m'
	keys = misc.reverseCopy(sqlalchemy_model.unique_feeds(fmt))

	items = [['RSS 2.0 Feeds'],[''],[''],['']]

	aContainer = []
	for k in keys:
	    toks = k.split('-')
	    if (len(toks) == 2):
		dt = _utils.getFromDateStr(k,fmt)
		s = _utils.getAsDateTimeStr(dt,fmt='%b %Y')
		aContainer.append('<a href="/feeds/rss/%s/%s/" target="_blank"><img src="/static/rss/rss-feed_32x32.gif" /><br/>%s</a>' % (toks[1],toks[0],s))
		if (len(aContainer) == 4):
		    items.append(aContainer)
		    aContainer = []
	
	h = oohtml.Html()
	h.html_simple_table(items,width='100%')
	html_content = h.toHtml()
	
	return _default(request,html_content)
    return HttpResponseRedirect('/')

def pypi_rss(request):
    h = oohtml.Html()
    _content = rss_content2()
    div = h.tagDIV(_content,style="background-color:#FF6; color: #00F; .h3 { color:#00F; font-size: 18px; }")
    return HttpResponse(h.toHtml())

def pypi(request,SSL=False):
    if (utils.is_authenticated(request)):
	t_members_content = get_template('_pypi_api_members.html')
	s_non_members_notice = ''
    else:
	t_members_content = get_template('_pypi_api_non-members.html')
	s_non_members_notice = '(for Members only - <a href="/register/" target="_top" style="color: #00F; font-size: 12px;">Get Registered</a>)'

    c = Context({})
    members_content = t_members_content.render(c)

    t_content1 = get_template('_pypi_page1.html')
    c = Context({'CONTENT':members_content, 'NON_MEMBERS_NOTICE':s_non_members_notice})
    content1 = t_content1.render(c)
    
    t_content = get_template('_pypi_page.html')
    c = Context({'page_content':content1})
    content = t_content.render(c)

    return _default(request,content)
