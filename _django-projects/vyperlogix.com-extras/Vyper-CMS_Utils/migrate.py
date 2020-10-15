import sys

from vyperlogix.lists import ListWrapper

_ignore_these = ['content_content_sites','content_country','content_cssnode','content_cssnodetype','content_cssparent','content_image','content_sitename','content_snippet_sites','content_state','content_url','content_url_sites','content_user','content_useractivity']

_path_list = ListWrapper.ListWrapper(sys.path)
i = _path_list.findFirstContaining('SQLAlchemy')
if (i == -1):
    print 'Connecting with SqlAlchemy...'
    sys.path.append('Z:\python projects\@SQLAlchemy-0_5_3\lib')

import os
import re

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

from vyperlogix.hash import lists
from vyperlogix.misc import ReportTheList

from vyperlogix.sql.sqlalchemy.utils import handlers as sqlAlchemy_handlers

from sqlalchemy import types as sqltypes
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

from vyperlogix.sql.sqlalchemy import SQLAgent

import sql2005_tables
import sqlalchemy_models_sql2005

import web20082_tables
import sqlalchemy_models_web20082

conn_str = ''
conn_str2 = ''

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()
if (_cname == 'undefined3'):
    conn_str = 'mysql://root:peekab00@SQL2005:3307/vyperlogix2'
else:
    print >>sys.stderr, 'Cannot determine the machine name from "%s".' % (_cname)
    sys.exit()
    
if (_cname == 'undefined3'):
    conn_str2 = 'mysql://root:peekab00@127.0.0.1:3306/vyperlogix2'
else:
    print >>sys.stderr, 'Cannot determine the machine name from "%s".' % (_cname)
    sys.exit()
    
try:
    agent = SQLAgent.SQLAgent(conn_str)
except SQLAgent.sqlalchemy.exc.OperationalError, details:
    print >>sys.stderr, _utils.formattedException(details=details)

try:
    agent2 = SQLAgent.SQLAgent(conn_str2)
except SQLAgent.sqlalchemy.exc.OperationalError, details:
    print >>sys.stderr, _utils.formattedException(details=details)

def items_callback(items,i,num):
    ReportTheList.reportTheList(items,'items %d of %d' % (i,num))

def main():
    tables = [table for table in agent.table_names if (table.startswith('content_')) and (table not in _ignore_these)]
    ReportTheList.reportTheList(tables,'SQL2005 Tables')
    
    print
    print 'Checking web20082...'
    print

    tables2 = [table for table in agent2.table_names if (table.startswith('content_')) and (table not in _ignore_these)]
    ReportTheList.reportTheList(tables,'web20082 Tables')

    print
    print 'Performing Analysis...'
    print
    
    diff = set(tables) - set(tables2)
    if (len(diff) > 0):
        print 'Something wrong with the table lists...  Better check this out.'
        sys.exit(1)
    
    d_models = lists.HashedLists2()
    d_models['content_content'] = sqlalchemy_models_sql2005.Content,sql2005_tables.content_content
    d_models['content_menutype'] = sqlalchemy_models_sql2005.MenuType,sql2005_tables.content_menutype
    d_models['content_role'] = sqlalchemy_models_sql2005.Role,sql2005_tables.content_role
    d_models['content_snippet'] = sqlalchemy_models_sql2005.Snippet,sql2005_tables.content_snippet
    d_models['content_snippettype'] = sqlalchemy_models_sql2005.SnippetType,sql2005_tables.content_snippettype
    
    d_models2 = lists.HashedLists2()
    d_models2['content_content'] = sqlalchemy_models_web20082.Content,web20082_tables.content_content
    d_models2['content_menutype'] = sqlalchemy_models_web20082.MenuType,web20082_tables.content_menutype
    d_models2['content_role'] = sqlalchemy_models_web20082.Role,web20082_tables.content_role
    d_models2['content_snippet'] = sqlalchemy_models_web20082.Snippet,web20082_tables.content_snippet
    d_models2['content_snippettype'] = sqlalchemy_models_web20082.SnippetType,web20082_tables.content_snippettype
    
    if (len(d_models) != len(tables)):
        print 'Warning 101:  Something is wrong with the table lists - was a model or two added but not accounted for in %s.' % (__name__)
        sys.exit(1)

    d_models['content_content_sites'] = sqlalchemy_models_sql2005.ContentSites,sql2005_tables.content_content_sites

    if (len(d_models2) != len(tables)):
        print 'Warning 201:  Something is wrong with the table lists - was a model or two added but not accounted for in %s.' % (__name__)
        sys.exit(1)

    d_models2['content_content_sites'] = sqlalchemy_models_web20082.ContentSites,web20082_tables.content_content_sites

    for k,v in d_models.iteritems():
        agent.add_mapper(v[0],v[-1])

    for k,v in d_models2.iteritems():
        agent2.add_mapper(v[0],v[-1])

    criterion = "content_content.id = content_content_sites.content_id"
    qry = agent.session.query(sqlalchemy_models_sql2005.Content,sqlalchemy_models_sql2005.ContentSites).filter(criterion)
    print 'INFO: There are %d records in the source table.' % (qry.count())
    for aContent in qry:
        criterion = "content_content.menu_tag='%s' and content_content.menutype_id='%s' and content_content.url='%s' and content_content.target='%s' and content_content.admin_mode=%d and content_content.id = content_content_sites.content_id and content_content_sites.site_id = %d" % (aContent.Content.menu_tag,aContent.Content.menutype_id,aContent.Content.url,aContent.Content.target,aContent.Content.admin_mode,aContent.ContentSites.site_id)
        qry2 = agent2.session.query(sqlalchemy_models_web20082.Content,sqlalchemy_models_web20082.ContentSites).filter(criterion)
        if (qry2.count() == 0):
            print '(+++)  Add this record to the target database. Source=%d' % (aContent.Content.id)
        else:
            assert (qry2.count() == 1), 'Oops, Something went wrong with the following: (%d) %s' % (qry2.count(),criterion)
        for aContent2 in qry2:
            if (aContent.Content.content != aContent2.Content.content):
                print '(***)  Update this record in the target database using the source. Source=%d, Site=%d | Dest=%d, Site=%d' % (aContent.Content.id,aContent.ContentSites.site_id,aContent2.Content.id,aContent2.ContentSites.site_id)
    print '='*40

if (__name__ == '__main__'):
    pass
