# http://www.sqlalchemy.org/docs/05/ormtutorial.html
import sys

from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.sql.sqlalchemy import SQLAgent

from sqlalchemy import types as sqltypes

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

import vypertwitz_tables

####################################################################################################
## Notes: Eventually this module should become an object to allow for data to be cached for the
##        lifetime of the object - this reduces interactions with the database and speeds data access.
####################################################################################################

class Prepositions(SQLAgent.BaseObject):
    pass

class Products(SQLAgent.BaseObject):
    pass

class Phrases(SQLAgent.BaseObject):
    pass

class UsedLinks(SQLAgent.BaseObject):
    pass

class Sources(SQLAgent.BaseObject):
    pass

class Bitlys(SQLAgent.BaseObject):
    pass

class Feeds(SQLAgent.BaseObject):
    pass

class Sponsors(SQLAgent.BaseObject):
    pass

class ProductIndexes(SQLAgent.BaseObject):
    pass

class ProductKeywords(SQLAgent.BaseObject):
    pass

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()

def agentProducts(db_handle):
    try:
        agent = SQLAgent.SQLAgent(db_handle.conn_str,classObj=Products,tableDef=vypertwitz_tables.products)
        agent.add_mapper(ProductIndexes,vypertwitz_tables.product_indexes)
        agent.add_mapper(ProductKeywords,vypertwitz_tables.product_keywords)
        return agent
    except SQLAgent.sqlalchemy.exc.OperationalError, details:
        print >>sys.stderr, _utils.formattedException(details=details)
        sys.exit(1)

def agentPrepositions(db_handle):
    try:
        return SQLAgent.SQLAgent(db_handle.conn_str,classObj=Prepositions,tableDef=vypertwitz_tables.prepositions)
    except SQLAgent.sqlalchemy.exc.OperationalError, details:
        print >>sys.stderr, _utils.formattedException(details=details)
        sys.exit(1)

def agentPhrases(db_handle):
    try:
        return SQLAgent.SQLAgent(db_handle.conn_str,classObj=Phrases,tableDef=vypertwitz_tables.phrases)
    except SQLAgent.sqlalchemy.exc.OperationalError, details:
        print >>sys.stderr, _utils.formattedException(details=details)
        sys.exit(1)

def agentUsedLinks(db_handle):
    try:
        return SQLAgent.SQLAgent(db_handle.conn_str,classObj=UsedLinks,tableDef=vypertwitz_tables.used_links)
    except SQLAgent.sqlalchemy.exc.OperationalError, details:
        print >>sys.stderr, _utils.formattedException(details=details)
        sys.exit(1)

def agentSources(db_handle):
    try:
        agent = SQLAgent.SQLAgent(db_handle.conn_str,classObj=Sources,tableDef=vypertwitz_tables.sources)
        agent.add_mapper(Bitlys,vypertwitz_tables.bitlys)
        agent.add_mapper(Feeds,vypertwitz_tables.feeds)
        return agent
    except SQLAgent.sqlalchemy.exc.OperationalError, details:
        print >>sys.stderr, _utils.formattedException(details=details)
        sys.exit(1)

def agentSponsors(db_handle):
    try:
        return SQLAgent.SQLAgent(db_handle.conn_str,classObj=Sponsors,tableDef=vypertwitz_tables.sponsors)
    except SQLAgent.sqlalchemy.exc.OperationalError, details:
        print >>sys.stderr, _utils.formattedException(details=details)
        sys.exit(1)

#def agentProductIndexes(db_handle):
    #try:
        #return SQLAgent.SQLAgent(db_handle.conn_str,classObj=ProductIndexes,tableDef=vypertwitz_tables.product_indexes)
    #except SQLAgent.sqlalchemy.exc.OperationalError, details:
        #print >>sys.stderr, _utils.formattedException(details=details)
        #sys.exit(1)
    
#def agentProductKeywords(db_handle):
    #try:
        #return SQLAgent.SQLAgent(db_handle.conn_str,classObj=ProductKeywords,tableDef=vypertwitz_tables.product_keywords)
    #except SQLAgent.sqlalchemy.exc.OperationalError, details:
        #print >>sys.stderr, _utils.formattedException(details=details)
        #sys.exit(1)
    
def get_qry_by_parts(qry,callback=None):
    items = []
    try:
        num_items = qry.count()
        one_percent = (num_items / 100)
        if (one_percent < 200):
            one_percent = 200
        num_items_part = one_percent if (num_items > 10000) else num_items
        for i in xrange(num_items):
            item = SQLAgent.instance_as_SmartObject(qry[i])
            items.append(item)
            if (i > 0) and ((i % num_items_part) == 0):
                if (callable(callback)):
                    try:
                        callback(items)
                    finally:
                        items = []
        if (len(items) > 0):
            if (callable(callback)):
                try:
                    callback(items)
                finally:
                    items = []
    except Exception, details:
        print >>sys.stderr, _utils.formattedException(details=details)
    return items

def put(agent,anObj,logging=None):
    agent.beginTransaction()
    agent.add(anObj)
    agent.commit()
    if (agent.lastError.find('rollback') > -1):
        if (logging is not None):
            try:
                logging.warning(agent.lastError)
            except:
                pass
        agent.session.rollback()

def get_prepositions_query(agent):
    qry = agent.session.query(Prepositions)
    return qry

def get_query(agent,cls):
    qry = agent.session.query(cls)
    return qry

def get_sources_with_joins_query(agent):
    qry = agent.session.query(Sources,Bitlys,Feeds).filter("sources.feed=feeds.id and sources.bitly=bitlys.id").order_by("sources.feed ASC")
    return qry

def get_phrases_query(agent):
    qry = get_query(agent,Phrases).order_by("phrase_type ASC")
    return qry

def get_least_used_phrases_query(agent,phrase_type):
    qry = get_query(agent,Phrases).filter("phrase_type=:phrase_type").params(phrase_type=phrase_type).order_by("last_used ASC")
    return qry

def get_used_link_query(agent,link,source_id):
    qry = get_query(agent,UsedLinks).filter("link=:link and source=:source").params(link=link,source=source_id)
    return qry

def get_used_links_query(agent,source_id):
    qry = get_query(agent,UsedLinks).filter("source=:source").params(source=source_id)
    return qry

def get_sponsor_query(agent,sponsor_type):
    qry = get_query(agent,Sponsors).filter("sponsor_type=:sponsor_type").params(sponsor_type=sponsor_type).order_by("last_used ASC")
    return qry

def get_product_index_by_name_query(agent,name):
    qry = get_query(agent,ProductIndexes).filter("name=:name").params(name=name)
    return qry

def get_products_query(agent):
    qry = agent.session.query(Products,ProductIndexes,ProductKeywords).filter("products.indx=product_indexes.id and products.indx=product_keywords.indx")
    return qry

def get_product_keywords_query(agent):
    qry = agent.session.query(ProductIndexes,ProductKeywords).filter("product_keywords.indx=product_indexes.id")
    return qry

def get_product_keywords_by_index_query(agent,indx):
    qry = get_query(agent,ProductKeywords).filter("indx=:indx").params(indx=indx)
    return qry

#def get_countries(callback=None):
    #qry = agent_countries.session.query(IsoCountries).filter("iso3<>:value").params(value='USA').order_by("printable_name ASC")
    #items = get_qry_by_parts(qry,callback=callback)
    #qry2 = agent_countries.session.query(IsoCountries).filter("iso3=:value").params(value='USA').order_by("printable_name ASC")
    #items2 = get_qry_by_parts(qry2,callback=callback)
    #return items2+items

#def get_states(callback=None):
    #qry = agent_states.session.query(IsoStates).order_by("name ASC")
    #items = get_qry_by_parts(qry,callback=callback)
    #return items
