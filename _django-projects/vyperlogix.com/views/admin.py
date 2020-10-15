from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.conf import settings
from django.db.models import Q

from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.list_detail import object_detail
from content import models as content_models

from vyperlogix.django import django_utils

from vyperlogix.misc import SequenceMatcher

import difflib

import utils

import sys

from vyperlogix.lists import ListWrapper

import os
import re

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

from vyperlogix.hash import lists
from vyperlogix.misc import ReportTheList

from vyperlogix.enum.Enum import Enum

class Actions(Enum):
    none = 0
    analysis = 1
    update = 2

from vyperlogix.html import myOOHTML as oohtml

from vyperlogix.sql.sqlalchemy.utils import handlers as sqlAlchemy_handlers

from sqlalchemy import types as sqltypes
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper,relation

from vyperlogix.sql.sqlalchemy import SQLAgent

import sql2005_tables
import sqlalchemy_models_sql2005

import web20082_tables
import sqlalchemy_models_web20082

conn_str = ''
conn_str2 = ''

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()

_anchor_expected_target = lambda foo:'/%s/' % ('/'.join(foo))
anchor_expected_target = lambda foo,bar:_anchor_expected_target(foo+bar)

if (_cname == 'undefined3'):
    conn_str = 'mysql://root:peekab00@SQL2005:3307/vyperlogix2'
    
if (_cname == 'undefined3'):
    conn_str2 = 'mysql://root:peekab00@127.0.0.1:3306/vyperlogix2'

def get_new_agent(conn_str):
    try:
        agent = SQLAgent.SQLAgent(conn_str)
    except SQLAgent.sqlalchemy.exc.OperationalError, details:
        output.append(oohtml.render_SPAN(_utils.formattedException(details=details),class_='errornote'))
    return agent

def get_agents(output):
    try:
        agent = SQLAgent.SQLAgent(conn_str)
    except SQLAgent.sqlalchemy.exc.OperationalError, details:
        output.append(oohtml.render_SPAN(_utils.formattedException(details=details),class_='errornote'))
    
    try:
        agent2 = SQLAgent.SQLAgent(conn_str2)
    except SQLAgent.sqlalchemy.exc.OperationalError, details:
        output.append(oohtml.render_SPAN(_utils.formattedException(details=details),class_='errornote'))
    return agent,agent2

def get_model_mappings():
    d_models = lists.HashedLists2()
    d_models['content_content'] = sqlalchemy_models_sql2005.Content,sql2005_tables.content_content
    d_models['content_menutype'] = sqlalchemy_models_sql2005.MenuType,sql2005_tables.content_menutype
    d_models['content_role'] = sqlalchemy_models_sql2005.Role,sql2005_tables.content_role
    d_models['content_snippet'] = sqlalchemy_models_sql2005.Snippet,sql2005_tables.content_snippet
    d_models['content_snippettype'] = sqlalchemy_models_sql2005.SnippetType,sql2005_tables.content_snippettype
    d_models['content_content_sites'] = sqlalchemy_models_sql2005.ContentSites,sql2005_tables.content_content_sites
    d_models['content_snippet_sites'] = sqlalchemy_models_sql2005.SnippetSites,sql2005_tables.content_snippet_sites

    d_models2 = lists.HashedLists2()
    d_models2['content_content'] = sqlalchemy_models_web20082.Content,web20082_tables.content_content
    d_models2['content_menutype'] = sqlalchemy_models_web20082.MenuType,web20082_tables.content_menutype
    d_models2['content_role'] = sqlalchemy_models_web20082.Role,web20082_tables.content_role
    d_models2['content_snippet'] = sqlalchemy_models_web20082.Snippet,web20082_tables.content_snippet
    d_models2['content_snippettype'] = sqlalchemy_models_web20082.SnippetType,web20082_tables.content_snippettype
    d_models2['content_content_sites'] = sqlalchemy_models_web20082.ContentSites,web20082_tables.content_content_sites
    d_models2['content_snippet_sites'] = sqlalchemy_models_web20082.SnippetSites,web20082_tables.content_snippet_sites

    return d_models,d_models2

def set_model_mappings(agent,d_models,output):
    try:
        for k,v in d_models.iteritems():
            agent.add_mapper(v[0],v[-1])
    except SQLAgent.sqlalchemy.exc.OperationalError, details:
        output.append(oohtml.render_SPAN(_utils.formattedException(details=details),class_='errornote'))

def perform_analysis_for_content(url_toks,action=Actions.analysis):
    output = []
    
    agent,agent2 = get_agents(output)
    d_models,d_models2 = get_model_mappings()
    set_model_mappings(agent,d_models,output)
    set_model_mappings(agent2,d_models2,output)

    d_output = lists.HashedLists2()
    s_expected_target = _anchor_expected_target(url_toks)
    try:
        criterion = "content_content.id = content_content_sites.content_id"
        qry = agent.session.query(sqlalchemy_models_sql2005.Content,sqlalchemy_models_sql2005.ContentSites).filter(criterion)
        output.append('INFO: There are %d records in the source table.' % (qry.count()))
        for aContent in qry:
            criterion = "content_content.menu_tag='%s' and content_content.menutype_id='%s' and content_content.url='%s' and content_content.target='%s' and content_content.admin_mode=%d and content_content.id = content_content_sites.content_id and content_content_sites.site_id = %d" % (aContent.Content.menu_tag,aContent.Content.menutype_id,aContent.Content.url,aContent.Content.target,aContent.Content.admin_mode,aContent.ContentSites.site_id)
            qry2 = agent2.session.query(sqlalchemy_models_web20082.Content,sqlalchemy_models_web20082.ContentSites).filter(criterion)
            if (qry2.count() == 0):
                if (action == Actions.analysis):
                    aKey = '%d' % (aContent.Content.id)
                    if (d_output[aKey] is None):
                        d_output[aKey] = oohtml.render_SPAN('(Preview) Add this record to the target database. Source=%d' % (aContent.Content.id),class_='additions')
                elif (action == Actions.update):
                    output.append('%s has not yet been implemented.' % (action))
            elif (qry2.count() != 1):
                output.append(oohtml.render_SPAN('Oops, Something went wrong with the following: (%d) %s' % (qry2.count(),criterion),class_='errors'))
            for aContent2 in qry2:
                if (aContent.Content.content != aContent2.Content.content):
                    if (action == Actions.analysis):
                        s_expected_target = anchor_expected_target(url_toks,['%d' % (aContent.Content.id)])
                        s = '(Preview) Update this record in the target database using the source. Source=%d | Dest=%d' % (aContent.Content.id,aContent2.Content.id)
                        a = oohtml.renderAnchor(s_expected_target,s,target='_top')
                        aKey = '%d,%d' % (aContent.Content.id,aContent2.Content.id)
                        if (d_output[aKey] is None):
                            ratios = SequenceMatcher.computeAllRatios(aContent.Content.content, aContent2.Content.content)
                            diff = difflib.HtmlDiff()
                            diff_tab = diff.make_table(aContent.Content.content,aContent2.Content.content)
                            d_output[aKey] = oohtml.renderSPAN(a,class_='modifications')+oohtml.renderSPAN('%s' % (str(list(ratios))),class_='modifications')+diff_tab
                    elif (action == Actions.update):
                        output.append('%s has not yet been implemented.' % (action))
    except SQLAgent.sqlalchemy.exc.OperationalError, details:
        output.append(oohtml.render_SPAN(_utils.formattedException(details=details),class_='errornote'))

    for k,v in d_output.iteritems():
        output.append(v[0] if (misc.isList(v)) else v)
    
    h = oohtml.Html()
    ul = h.tagUL()
    for item in output:
        ul.tag_LI(item)

    s_expected_target = anchor_expected_target(url_toks,['update'])
    a = oohtml.renderAnchor(s_expected_target,'Perform Update(s)',target='_top')
    ul.tag_LI(a)
    return h.toHtml()

def perform_analysis_for_snippet(url_toks,action=Actions.analysis):
    output = []
    
    agent,agent2 = get_agents(output)
    d_models,d_models2 = get_model_mappings()
    set_model_mappings(agent,d_models,output)
    set_model_mappings(agent2,d_models2,output)

    d_output = lists.HashedLists2()
    s_expected_target = _anchor_expected_target(url_toks)
    try:
        criterion = "content_snippet.id = content_snippet_sites.snippet_id"
        qry = agent.session.query(sqlalchemy_models_sql2005.Snippet,sqlalchemy_models_sql2005.SnippetSites).filter(criterion)
        output.append('INFO: There are %d records in the source table.' % (qry.count()))
        for aSnippet in qry:
            criterion = "content_snippet.snippet_tag='%s' and content_snippet.id = content_snippet_sites.snippet_id and content_snippet_sites.site_id = %d" % (aSnippet.Snippet.snippet_tag,aSnippet.SnippetSites.site_id)
            qry2 = agent2.session.query(sqlalchemy_models_web20082.Snippet,sqlalchemy_models_web20082.SnippetSites).filter(criterion)
            if (qry2.count() == 0):
                if (action == Actions.analysis):
                    aKey = '%d' % (aSnippet.Snippet.id)
                    if (d_output[aKey] is None):
                        d_output[aKey] = oohtml.render_SPAN('(Preview) Add this record to the target database. Source=%d' % (aSnippet.Snippet.id),class_='additions')
                elif (action == Actions.update):
                    output.append('%s has not yet been implemented.' % (action))
            elif (qry2.count() != 1):
                output.append(oohtml.render_SPAN('Oops, Something went wrong with the following: (%d) %s' % (qry2.count(),criterion),class_='errors'))
            for aSnippet2 in qry2:
                if (aSnippet.Snippet.content != aSnippet2.Snippet.content):
                    aKey = '%d,%d' % (aSnippet.Snippet.id,aSnippet2.Snippet.id)
                    if (action == Actions.analysis):
                        if (d_output[aKey] is None):
                            s_expected_target = anchor_expected_target(url_toks,['%d' % (aSnippet.Snippet.id)])
                            s = '(Preview) Update this record in the target database using the source. Source=%d | Dest=%d' % (aSnippet.Snippet.id,aSnippet2.Snippet.id)
                            a = oohtml.renderAnchor(s_expected_target,s,target='_top')
                            d_output[aKey] = oohtml.renderSPAN(a,class_='modifications')
                    elif (action == Actions.update):
                        if (d_output[aKey] is None):
                            is_error = False
                            try:
                                _agent = get_new_agent(conn_str2)
                                mapper(sqlalchemy_models_web20082.Snippet, web20082_tables.content_snippet, properties={ 'snippet_type':relation(sqlalchemy_models_web20082.SnippetType) }, non_primary=True)
                                #_agent.add_mapper(sqlalchemy_models_web20082.Snippet,web20082_tables.content_snippet)
                                #_agent.add_mapper(sqlalchemy_models_web20082.SnippetType,web20082_tables.content_snippettype)
                                _criterion = "content_snippet.id = %d" % (aSnippet2.Snippet.id)
                                _qry = _agent.session.query(sqlalchemy_models_web20082.Snippet).filter(_criterion)
                                if (_qry.count() == 1):
                                    _snippet = _qry[0]
                                    _snippet.content = aSnippet.Snippet.content
                                    _agent.beginTransaction()
                                    if (len(_agent.lastError) > 0):
                                        output.append(oohtml.render_SPAN('ERROR: Cannot update #%d because %s.' % (aSnippet2.Snippet.id,_agent.lastError),class_='errornote'))
                                    else:
                                        _agent.update(_snippet)
                                        if (len(_agent.lastError) > 0):
                                            output.append(oohtml.render_SPAN('ERROR: Cannot update #%d because %s.' % (aSnippet2.Snippet.id,_agent.lastError),class_='errornote'))
                                        else:
                                            _agent.commit()
                                            if (len(_agent.lastError) > 0):
                                                output.append(oohtml.render_SPAN('ERROR: Cannot update #%d because %s.' % (aSnippet2.Snippet.id,_agent.lastError),class_='errornote'))
                                else:
                                    output.append(oohtml.render_SPAN('ERROR: Cannot update #%d.' % (aSnippet2.Snippet.id),class_='errornote'))
                                    
                                _agent = get_new_agent(conn_str2)
                                _agent.add_mapper(sqlalchemy_models_web20082.Snippet,web20082_tables.content_snippet)
                                _criterion = "content_snippet.id = %d" % (aSnippet2.Snippet.id)
                                _qry = _agent.session.query(sqlalchemy_models_web20082.Snippet).filter(_criterion)
                                if (_qry.count() == 1):
                                    _snippet = _qry[0]
                                    if (_snippet.content != aSnippet.Snippet.content):
                                        output.append(oohtml.render_SPAN('ERROR: Validation failed for #%d.' % (aSnippet2.Snippet.id),class_='errornote'))
                                    else:
                                        output.append(oohtml.renderSPAN('Successfully validated update for #%d --> #%d.' % (aSnippet.Snippet.id,aSnippet2.Snippet.id),class_='modifications'))
                                else:
                                    output.append(oohtml.render_SPAN('ERROR: Cannot update #%d.' % (aSnippet2.Snippet.id),class_='errornote'))
                            except Exception, details:
                                is_error = True
                                output.append(oohtml.render_SPAN(_utils.formattedException(details=details),class_='errornote'))
                            if (not is_error):
                                output.append(oohtml.renderSPAN('Successfully updated #%d --> #%d.' % (aSnippet.Snippet.id,aSnippet2.Snippet.id),class_='modifications'))
                                d_output[aKey] = 1
    except SQLAgent.sqlalchemy.exc.OperationalError, details:
        output.append(oohtml.render_SPAN(_utils.formattedException(details=details),class_='errornote'))
        
    for k,v in d_output.iteritems():
        output.append(v[0] if (misc.isList(v)) else v)
    
    h = oohtml.Html()
    ul = h.tagUL()
    for item in output:
        ul.tag_LI(item)
        
    if (action != Actions.update):
        s_expected_target = anchor_expected_target(url_toks,['update'])
        a = oohtml.renderAnchor(s_expected_target,'Perform Update(s)',target='_top')
        #ul.tag_LI(a)
    return h.toHtml()

@staff_member_required
def default(request):
    url_toks = [item for item in django_utils.parse_url_parms(request) if (len(item) > 0)]

    is_performing_analysis = False
    is_performing_drill_into = False
    is_performing_updates = False
    
    refs = request.session.get('REFERERS',[])
    ref = request.META['HTTP_REFERER']
    ref_toks = [t for t in refs[0].split('/') if (len(t) > 0)] if (len(refs) > 0) else []
    do_pop = any([ref.find(r) > -1 for r in refs]) and (len(refs) > 1)
    if (not do_pop):
        if (url_toks == ['admin','migrate-content']):
            refs = []
            refs.append(request.META['HTTP_REFERER'])
            request.session['REFERERS'] = refs
            is_performing_analysis = True
        elif (url_toks[0:-1] == ['admin','migrate-content']) and (str(url_toks[-1]).isdigit()):
            refs.append(request.META['HTTP_REFERER'])
            request.session['REFERERS'] = refs
            is_performing_drill_into = True
        elif (url_toks == ['admin','migrate-content','update']):
            is_performing_updates = True
    else:
        refs.pop()
        request.session['REFERERS'] = refs
    
    t_content = get_template('new-admin/migrate-content.html')
    d = {}
    d['REFERER'] = refs[-1]
    d['REFERER_TEXT'] = refs[-1].replace('http://%s' % (request.META['HTTP_HOST']),'')
    
    if (is_performing_analysis):
        d['CONTENT'] = 'ERROR: Programming error.'
        if (_cname != 'undefined3'):
            d['CONTENT'] = 'Cannot perform this operation from any machine other than the one...'
        if (d['REFERER'].endswith('/admin/content/content/')) or (d['REFERER'].endswith('/admin/content/snippet/')):
            s = 'PROGRAMMING ERROR while Performing Analysis'
            if (len(ref_toks) > 0):
                if (ref_toks[-1] == 'content'):
                    s = perform_analysis_for_content(url_toks,action=Actions.analysis)
                elif (ref_toks[-1] == 'snippet'):
                    s = perform_analysis_for_snippet(url_toks,action=Actions.analysis)
            else:
                pass
            d['CONTENT'] = s
        request.session['analysis'] = d['CONTENT']
    elif (is_performing_drill_into):
        id = int(url_toks[-1]) if (str(url_toks[-1]).isdigit()) else -1
        rows = [['UNKNOWN']]
        if (ref_toks[-1] == 'content'):
            objects = content_models.Content.objects.filter(id=id)
            if (objects.count() > 0):
                rows = [['%d' % (id)]]
                for anObject in objects:
                    # admin_mode
                    h = oohtml.Html()
                    ul = h.tagUL()
                    li = ul.tagLI('Admin_mode:')
                    ol = li.tagOL()
                    ol.tagLI(str(anObject.admin_mode))
                    rows.append([h.toHtml()])
                    h = oohtml.Html()
                    ul = h.tagUL()
                    li = ul.tagLI('Sites:')
                    ol = li.tagOL()
                    for aSite in anObject.sites.all():
                        ol.tagLI(aSite.domain)
                    rows.append([h.toHtml()])
                    # menutype
                    h = oohtml.Html()
                    ul = h.tagUL()
                    li = ul.tagLI('Menutype:')
                    ol = li.tagOL()
                    ol.tagLI(str(anObject.menutype))
                    rows.append([h.toHtml()])
                    # menu_tag
                    h = oohtml.Html()
                    ul = h.tagUL()
                    li = ul.tagLI('Menu_tag:')
                    ol = li.tagOL()
                    ol.tagLI(str(anObject.menu_tag))
                    rows.append([h.toHtml()])
                    # URL
                    h = oohtml.Html()
                    ul = h.tagUL()
                    li = ul.tagLI('URL:')
                    ol = li.tagOL()
                    ol.tagLI(str(anObject.url))
                    rows.append([h.toHtml()])
                    # Descr
                    h = oohtml.Html()
                    ul = h.tagUL()
                    li = ul.tagLI('Descr:')
                    ol = li.tagOL()
                    ol.tagLI(str(anObject.descr))
                    rows.append([h.toHtml()])
                    # Content
                    h = oohtml.Html()
                    ul = h.tagUL()
                    li = ul.tagLI('Content:')
                    ol = li.tagOL()
                    li = ol.tag_LI('')
                    li.tagTEXTAREA(anObject.content,columns="100",rows="20",readonly="readonly",styles="width:800px;height:400px;")
                    rows.append([h.toHtml()])
        elif (ref_toks[-1] == 'snippet'):
            objects = content_models.Snippet.objects.filter(id=id)
            if (objects.count() > 0):
                rows = [['%d' % (id)]]
                for anObject in objects:
                    # sites
                    h = oohtml.Html()
                    ul = h.tagUL()
                    li = ul.tagLI('Sites:')
                    ol = li.tagOL()
                    for aSite in anObject.sites.all():
                        ol.tagLI(aSite.domain)
                    rows.append([h.toHtml()])
                    # snippet_type
                    h = oohtml.Html()
                    ul = h.tagUL()
                    li = ul.tagLI('SnippetType:')
                    ol = li.tagOL()
                    ol.tagLI(str(anObject.snippet_type))
                    rows.append([h.toHtml()])
                    # descr
                    h = oohtml.Html()
                    ul = h.tagUL()
                    li = ul.tagLI('Descr:')
                    ol = li.tagOL()
                    ol.tagLI(str(anObject.descr))
                    rows.append([h.toHtml()])
                    # snippet_tag
                    h = oohtml.Html()
                    ul = h.tagUL()
                    li = ul.tagLI('SnippetTag:')
                    ol = li.tagOL()
                    ol.tagLI(str(anObject.snippet_tag))
                    rows.append([h.toHtml()])
                    # Content
                    h = oohtml.Html()
                    ul = h.tagUL()
                    li = ul.tagLI('Content:')
                    ol = li.tagOL()
                    li = ol.tag_LI('')
                    li.tagTEXTAREA(anObject.content,columns="150",rows="20",readonly="readonly",styles="width:800px;height:400px;")
                    rows.append([h.toHtml()])
        h = oohtml.Html()
        h.html_table(rows,width='100%')
        d['CONTENT'] = h.toHtml()
    elif (is_performing_updates):
        s = 'PROGRAMMING ERROR while Performing Updates.'
        if (len(ref_toks) > 0):
            if (ref_toks[-1] == 'content'):
                s = perform_analysis_for_content(url_toks,action=Actions.update)
            elif (ref_toks[-1] == 'snippet'):
                s = perform_analysis_for_snippet(url_toks,action=Actions.update)
        else:
            pass
        d['CONTENT'] = s
    else:
        d['CONTENT'] = request.session.get('analysis','<span class="errors">WARNING: Cannot retrieve the contents of the previous analysis at this time.</span>')
        #del request.session['analysis']

    c_content = Context(d, autoescape=False)
    content = t_content.render(c_content)
    
    return HttpResponse(content)