# http://www.sqlalchemy.org/docs/05/ormtutorial.html
import sys

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.classes.SmartObject import PyroSmartObject as SmartObject

from vyperlogix.sql.sqlalchemy import SQLAgent

from sqlalchemy import types as sqltypes

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

import wp_tables

####################################################################################################
## Notes: Eventually this module should become an object to allow for data to be cached for the
##        lifetime of the object - this reduces interactions with the database and speeds data access.
####################################################################################################

class Jos_Menu(SQLAgent.BaseObject):
    pass

from django.conf import settings
from vyperlogix.django import django_utils

conn_str = 'mysql://%s:%s@%s:%s/%s' % (settings.DATABASE_USER,settings.DATABASE_PASSWORD,settings.DATABASE_HOST,settings.DATABASE_PORT,settings.DATABASE_NAME1)

try:
    agent = SQLAgent.SQLAgent(conn_str)
except SQLAgent.sqlalchemy.exc.OperationalError, details:
    print >>sys.stderr, _utils.formattedException(details=details)

def new_agent(connStr):
    try:
        agent = SQLAgent.SQLAgent(connStr)
    except SQLAgent.sqlalchemy.exc.OperationalError, details:
        print >>sys.stderr, _utils.formattedException(details=details)
    return agent

def menu_items(menutype,cls,tbl,func,filter_by='',order_by=''):
    agent.add_mapper(cls,tbl)
    items = agent.session.query(cls).filter("menutype='%s'%s" % (menutype,filter_by)).order_by(order_by).all()
    
    menu_items = []
    for item in items:
        try:
            menu_items.append(func(item))
        except Exception, details:
            info_string = _utils.formattedException(details=details)
            print info_string
    return menu_items

def topmenu_items():
    func = lambda item:tuple([item.name,item.link])
    return menu_items('topmenu',Jos_Menu,jos_tables.jos_menu,func,filter_by=' and published=True',order_by="ordering")

def featured_products_items():
    func = lambda item:tuple([item.name,item.link])
    return menu_items('featured-products',Jos_Menu,jos_tables.jos_menu,func,filter_by=' and published=True',order_by="ordering")

def mainmenu_items():
    func = lambda item:SmartObject({'id':item.id,'name':item.name,'parent':item.parent,'link':item.link,'params':item.params})
    return menu_items('mainmenu',Jos_Menu,jos_tables.jos_menu,func,filter_by=' and published=True',order_by="ordering")

def menu_title(menutype):
    agent.add_mapper(Jos_Menu_Types,jos_tables.jos_menu_types)
    items = agent.session.query(Jos_Menu_Types).filter("menutype='%s'" % (menutype)).order_by("menutype").all()
    
    menu_items = []
    for item in items:
        menu_items.append(item.title)
    return menu_items

def featured_products_title():
    return menu_title('featured-products')

def mainmenu_title():
    return menu_title('mainmenu')

def categories(alias=None,section=None):
    agent.add_mapper(Jos_Categories,jos_tables.jos_categories)
    qry = agent.session.query(Jos_Categories)
    _filter = []
    if (isinstance(alias,str)):
        _filter.append("alias='%s'" % (alias))
    if (isinstance(section,str)):
        _filter.append("section='%s'" % (section))
    qry = qry.filter("%s%s published=True" % (' and '.join(_filter),' and' if (len(_filter) > 0) else ''))
    return qry.order_by("alias").all()

def categories_for_section(section):
    return categories(section='%s' % section)

def category_and_section(cat_id,sect_id):
    agent.add_mapper(Jos_Categories,jos_tables.jos_categories)
    if (cat_id is not None):
        cat_id = int(str(cat_id))
    else:
        cat_id = -1
    if (sect_id is not None):
        sect_id = int(str(sect_id))
    else:
        sect_id = -1
    categories = agent.session.query(Jos_Categories).filter("id=:cat_id and section=:sect_id and published=:published").params(cat_id=cat_id, sect_id=sect_id, published=True).order_by("ordering").all()
    return categories

def section_by_id(sect_id):
    agent.add_mapper(Jos_Sections,jos_tables.jos_sections)
    if (sect_id is not None):
        sect_id = int(str(sect_id))
    else:
        sect_id = -1
    sections = agent.session.query(Jos_Sections).filter("id=:sect_id").params(sect_id=sect_id).all()
    return sections[0] if (len(sections) > 0) else sections

def sections(alias=None):
    agent.add_mapper(Jos_Sections,jos_tables.jos_sections)
    qry = agent.session.query(Jos_Sections)
    _filter = ''
    if (isinstance(alias,str)):
        _filter = "alias='%s'" % (alias)
    qry = qry.filter("%s%s published=True" % (_filter,' and' if (len(_filter) > 0) else ''))
    return qry.order_by("alias").all()

def category_by_id(cat_id):
    agent.add_mapper(Jos_Categories,jos_tables.jos_categories)
    if (cat_id is not None):
        cat_id = int(str(cat_id))
    else:
        cat_id = -1
    categories = agent.session.query(Jos_Categories).filter("id=:cat_id").params(cat_id=cat_id).all()
    return categories[0] if (len(categories) > 0) else categories

def content_items_filter(cat_id,section_id):
    now = _utils.timeStampLocalTime(format=_utils.format_mySQL_DateTimeStr())
    _filter = ''
    if (cat_id is not None):
        cat_id = _utils._int(cat_id)
        _filter += 'catid=%s' % (cat_id)
    if (cat_id is not None) and (section_id is not None):
        _filter += ' and '
    if (section_id is not None):
        section_id = _utils._int(section_id)
        _filter += 'sectionid=%s' % (section_id)
    if (cat_id is None) and (section_id is None):
        _filter += '1=1'
    _filter += ' and state=1'
    _filter += " and publish_up <= '%s'" % (now)
    _filter += " and (publish_down = '0000-00-00 00:00:00' OR publish_down <= '%s')" % (now)
    return _filter

def __content_items():
    agent.add_mapper(Jos_Content,jos_tables.jos_content)
    return agent.session.query(Jos_Content)

def _content_items(cat_id=None,section_id=None,order_by="ordering"):
    _filter = content_items_filter(cat_id,section_id)
    return __content_items().filter(_filter).order_by(order_by)

def content_items(cat_id,section_id,order_by="ordering"):
    qry = _content_items(cat_id=cat_id,section_id=section_id,order_by=order_by)
    items = qry.all()
    return items

def content_by_id(id):
    agent.add_mapper(Jos_Content,jos_tables.jos_content)
    _filter = 'id = %s' % (id)
    items = agent.session.query(Jos_Content).filter(_filter).all()
    return items

def content_items_with_author(cat_id,section_id,order_by="ordering"):
    agent.add_mapper(Jos_Content,jos_tables.jos_content)
    agent.add_mapper(Jos_Users,jos_tables.jos_users)
    now = _utils.timeStampLocalTime(format=_utils.format_mySQL_DateTimeStr())
    _filter = content_items_filter(cat_id,section_id)
    items = agent.session.query(Jos_Content, Jos_Users).filter("jos_content.created_by=jos_users.id").filter(_filter).order_by(order_by).all()
    return items

def docman_item_by_gid(gid):
    agent.add_mapper(Jos_Docman,jos_tables.jos_docman)
    items = agent.session.query(Jos_Docman).filter("jos_docman.id=%s" % (gid)).all()
    return items

def docman_license_by_id(id):
    agent.add_mapper(Jos_Docman_Licenses,jos_tables.jos_docman_licenses)
    items = agent.session.query(Jos_Docman_Licenses).filter("jos_docman_licenses.id=%s" % (id)).all()
    return items

def docman_items():
    agent.add_mapper(Jos_Docman,jos_tables.jos_docman)
    agent.add_mapper(Jos_Docman_Licenses,jos_tables.jos_docman_licenses)
    items = agent.session.query(Jos_Docman, Jos_Docman_Licenses).filter("jos_docman.dmlicense_id=jos_docman_licenses.id").filter("jos_docman.published=1").filter("jos_docman.approved=1").order_by('jos_docman.dmname').all()
    return items

def content_items_for_grid(cat_id,section_id,order_by="ordering"):
    return content_items_with_author(cat_id,section_id,order_by=order_by)

def frontpage_items_qry(month=-1,year=-1):
    agent.add_mapper(Jos_Content,jos_tables.jos_content)
    agent.add_mapper(Jos_Content_Frontpage,jos_tables.jos_content_frontpage)
    agent.add_mapper(Jos_Categories,jos_tables.jos_categories)
    agent.add_mapper(Jos_Sections,jos_tables.jos_sections)
    qry = agent.session.query(Jos_Content, Jos_Content_Frontpage, Jos_Categories, Jos_Sections).filter("jos_content_frontpage.content_id=jos_content.id").filter("jos_content.catid=jos_categories.id").filter("jos_content.sectionid=jos_sections.id").order_by("jos_content.created DESC")
    if (month > -1) and (year > -1):
        days = _utils.daysInMonth(month=month,year=year,format=_utils.formatDate_MMDDYYYY_dashes())
        beginDt = _utils.timeStampLocalTime(tsecs=_utils.timeSeconds(month=month,day=1,year=year,format=_utils.formatDate_MMDDYYYY_dashes()),format=_utils.format_mySQL_DateTimeStr())
        endDt = _utils.timeStampLocalTime(tsecs=_utils.timeSeconds(month=month,day=days,year=year,format=_utils.formatDate_MMDDYYYY_dashes()),format=_utils.format_mySQL_DateTimeStr())
        _filter = 'state=1'
        _filter += " and publish_up >= '%s'" % (beginDt)
        _filter += " and publish_up <= '%s'" % (endDt)
        qry = qry.filter(_filter)
    return qry

def frontpage_items(pageNo=-1,numPerPage=-1):
    '''
    pageNo=-1 to by-pass the normal slicing operation on the result set.
    numPerPage=-1 to by-pass the normal slicing operation on the result set.
    '''
    _start = (pageNo-1)*numPerPage
    _stop = _start + numPerPage
    qry = frontpage_items_qry()
    if (pageNo == -1) and (numPerPage == -1):
        items = agent.asSmartObjects(qry.all())
    else:
        num = qry.count()
        items = [i for i in xrange(0,num)]
        _items = agent.asSmartObjects(qry.slice(_start,_stop))
        items[_start:_stop] = _items
    return items

def content_items_qry(id=-1,order_by='jos_content.created DESC'):
    agent.add_mapper(Jos_Content,jos_tables.jos_content)
    agent.add_mapper(Jos_Categories,jos_tables.jos_categories)
    agent.add_mapper(Jos_Sections,jos_tables.jos_sections)
    agent.add_mapper(Jos_Users,jos_tables.jos_users)
    qry = agent.session.query(Jos_Content, Jos_Users, Jos_Categories, Jos_Sections).filter("jos_content.created_by=jos_users.id").filter("jos_content.catid=jos_categories.id").filter("jos_content.sectionid=jos_sections.id")
    if (id > -1):
        _filter = 'jos_content.id = %s' % (id)
        qry = qry.filter(_filter)
    if (isinstance(order_by,str)):
        qry = qry.order_by(order_by)
    return qry

def content_items(id=-1,asSmartObjects=True):
    qry = content_items_qry(id=id)
    items = agent.asSmartObjects(qry.all()) if (asSmartObjects) else qry.all()
    return items

def content_item_by_id(id,asSmartObjects=False):
    return content_items(id=id,asSmartObjects=asSmartObjects)

def unique_feeds(format=_utils.formatDate_MMYYYY()):
    d = lists.HashedLists2()
    items = frontpage_items_qry().all()
    for item in items:
        d[_utils.getAsDateTimeStr(item.Jos_Content.publish_up,fmt=format)] = item
    return misc.sort(d.keys())

def favored_items():
    agent.add_mapper(Jos_MXC_Favoured,jos_tables.jos_mxc_favoured)
    items = agent.session.query(Jos_MXC_Favoured).all()
    d = lists.HashedLists()
    for item in items:
        d[item.id_content] = item
    return d

def users():
    agent.add_mapper(Jos_Users,jos_tables.jos_users)
    items = agent.session.query(Jos_Users).all()
    d = lists.HashedLists()
    for item in items:
        d[item.id] = item
    return d

def user_by_id(id):
    agent.add_mapper(Jos_Users,jos_tables.jos_users)
    try:
        id = int(id)
    except:
        id = -1
    items = agent.session.query(Jos_Users).filter("jos_users.id=%d" % (id)).all()
    return items

def get_max_user_gid():
    agent.add_mapper(Jos_Users,jos_tables.jos_users)
    aUser = agent.session.query(Jos_Users).order_by('gid DESC').first()
    return int(aUser.gid)

def user_by_username(username):
    agent.add_mapper(Jos_Users,jos_tables.jos_users)
    items = agent.session.query(Jos_Users).filter("jos_users.username='%s'" % (username)).all()
    return items

def user_by_email(email):
    agent.add_mapper(Jos_Users,jos_tables.jos_users)
    items = agent.session.query(Jos_Users).filter("jos_users.email='%s'" % (email)).all()
    return items

def user_by_username_and_email(username,email):
    agent.add_mapper(Jos_Users,jos_tables.jos_users)
    items = agent.session.query(Jos_Users).filter("jos_users.username='%s' and jos_users.email='%s'" % (username,email)).all()
    return items

def favored_item_by_id(id_content):
    agent.add_mapper(Jos_MXC_Favoured,jos_tables.jos_mxc_favoured)
    try:
        id = int(id_content)
    except:
        id = -1
    items = agent.session.query(Jos_MXC_Favoured).filter("jos_mxc_favoured.id_content=%d" % (id_content)).all()
    return items

def insert_new_user(user):
    gid = get_max_user_gid()
    agent.add_mapper(Jos_Users,jos_tables.jos_users)
    user.gid = gid+1
    agent.beginTransaction()
    agent.add(user)
    agent.commit()
    return agent

def update_user(user):
    agent.add_mapper(Jos_Users,jos_tables.jos_users)
    agent.beginTransaction()
    agent.update(user)
    agent.commit()
    return agent

def update_content(content):
    agent.add_mapper(Jos_Content,jos_tables.jos_content)
    agent.beginTransaction()
    agent.update(content)
    agent.commit()
    return agent

def migrate_jos_users_to_django():
    from vyperlogix.products import keys
    from views import models as view_models
    
    agent.add_mapper(Jos_Users,jos_tables.jos_users)
    users = agent.session.query(Jos_Users).all()
    
    for user in users:
        a = []
        _password = None
        for k,v in user.__dict__.iteritems():
            if (not k.startswith('_sa_')) and (k not in ['params','gid','id']):
                if (k in ['block','sendEmail']):
                    a.append(str(k)+"="+str(v))
                elif (k in ['password']):
                    _password = v
                    a.append(str(k)+"="+chr(34)+keys._encode(str(v))+chr(34))
                else:
                    a.append(str(k)+"="+chr(39)+str(v)+chr(39))
        s = ','.join(a)
        aUser = eval("view_models.User(%s)" % (s))
        try:
            if (len(aUser.lastvisitDate) > 0) and (aUser.lastvisitDate != 'None'):
                aUser.lastVisitDate = _utils.getFromDateTimeStr(aUser.lastvisitDate,format=_utils.format_mySQL_DateTimeStr())
            elif (aUser.lastvisitDate == 'None'):
                aUser.lastvisitDate = None
        except Exception, e:
            info_string = _utils.formattedException(details=e)
            print info_string
        try:
            if (len(aUser.registerDate) > 0) and (aUser.registerDate != 'None'):
                aUser.registerDate = _utils.getFromDateTimeStr(aUser.registerDate,format=_utils.format_mySQL_DateTimeStr())
            elif (aUser.registerDate != 'None'):
                aUser.registerDate = None
        except Exception, e:
            info_string = _utils.formattedException(details=e)
            print info_string
        aUser.activation = None if (len(aUser.activation) == 0) else aUser.activation
        aUser.password = keys._decode(aUser.password)
        assert _password == aUser.password, 'Oops - Password failure !'
        aUser.save()

#####################################################################################################################

import freeemail_tables

from vyperlogix.sql import query

class FreeEmailHost(SQLAgent.BaseObject):
    pass

conn_str2 = 'mysql://%s:%s@%s:%s/%s' % (settings.DATABASE_USER,settings.DATABASE_PASSWORD,settings.DATABASE_HOST,settings.DATABASE_PORT,settings.DATABASE_NAME2)

try:
    agent2 = SQLAgent.SQLAgent(conn_str2)
except SQLAgent.sqlalchemy.exc.OperationalError, details:
    print >>sys.stderr, _utils.formattedException(details=details)

def get_freehosts(callback=None):
    agent2.add_mapper(FreeEmailHost,freeemail_tables.freeemailhost__c)
    items = agent2.session.query(FreeEmailHost).filter("IsActive__c=:value").params(value=1).order_by("Domain__c ASC").all()
    return items

def get_freehost_by_name(domain_name):
    agent2.add_mapper(FreeEmailHost,freeemail_tables.freeemailhost__c)
    items = agent2.session.query(FreeEmailHost).filter("IsActive__c=:value and Domain__c=:domain_name").params(value=1,domain_name=domain_name).all()
    return items

