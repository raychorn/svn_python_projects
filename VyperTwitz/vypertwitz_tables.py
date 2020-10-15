# -*- coding: utf8 -*-
## File autogenerated by SQLAutoCode
## see http://code.google.com/p/sqlautocode/
from sqlalchemy import *
from sqlalchemy.databases.mysql import *
metadata = MetaData()
bitlys =  Table('bitlys', metadata,
    Column(u'id', MSInteger(display_width=11), primary_key=True, nullable=False),
            Column(u'api_login', MSString(length=64), primary_key=False, nullable=False),
            Column(u'api_key', MSString(length=64), primary_key=False, nullable=False),
    
    
    )
Index(u'indx_api_login', bitlys.c.api_login, unique=True)
Index(u'indx_api_key', bitlys.c.api_key, unique=True)
feeds =  Table('feeds', metadata,
    Column(u'id', MSInteger(display_width=11), primary_key=True, nullable=False),
            Column(u'name', MSString(length=64), primary_key=False, nullable=False),
            Column(u'username', MSString(length=64), primary_key=False, nullable=False),
            Column(u'password', MSString(length=64), primary_key=False, nullable=False),
            Column(u'last_used', MSTimeStamp(timezone=False), primary_key=False, nullable=False),
            Column(u'frequency', MSInteger(display_width=11), primary_key=False, nullable=False),
    
    
    )
Index(u'indx_name', feeds.c.name, unique=True)
Index(u'indx_username', feeds.c.username, unique=True)
phrases =  Table('phrases', metadata,
    Column(u'id', MSInteger(display_width=11), primary_key=True, nullable=False),
            Column(u'phrase_type', MSTinyInteger(display_width=4), primary_key=False, nullable=False),
            Column(u'phrase', MSString(length=120), primary_key=False, nullable=False),
            Column(u'last_used', MSTimeStamp(timezone=False), primary_key=False),
    
    
    )
Index(u'indx_phrase', phrases.c.phrase, unique=True)
prepositions =  Table('prepositions', metadata,
    Column(u'id', MSInteger(display_width=11), primary_key=True, nullable=False),
            Column(u'preposition', MSString(length=32), primary_key=False, nullable=False),
            Column(u'last_used', MSTimeStamp(timezone=False), primary_key=False),
    
    
    )
Index(u'indx_prep', prepositions.c.preposition, unique=True)
product_indexes =  Table('product_indexes', metadata,
    Column(u'id', MSInteger(display_width=11), primary_key=True, nullable=False),
            Column(u'name', MSString(length=32), primary_key=False, nullable=False),
            Column(u'product', MSString(length=64), primary_key=False, nullable=False),
    
    
    )
Index(u'indx_name', product_indexes.c.name, unique=True)
product_keywords =  Table('product_keywords', metadata,
    Column(u'id', MSInteger(display_width=11), primary_key=True, nullable=False),
            Column(u'indx', MSInteger(display_width=11), primary_key=False, nullable=False),
            Column(u'keyword', MSString(length=64), primary_key=False, nullable=False),
    
    
    )
Index(u'indx', product_keywords.c.indx, unique=False)
products =  Table('products', metadata,
    Column(u'id', MSInteger(display_width=11), primary_key=True, nullable=False),
            Column(u'indx', MSInteger(display_width=11), primary_key=False, nullable=False),
            Column(u'asin', MSString(length=32), primary_key=False, nullable=False),
            Column(u'url', MSString(length=256), primary_key=False),
            Column(u'group', MSString(length=128), primary_key=False),
            Column(u'title', MSString(length=256), primary_key=False),
            Column(u'last_used', MSTimeStamp(timezone=False), primary_key=False),
    
    
    )
Index(u'indx_title', products.c.title, unique=False)
Index(u'indx_lastused', products.c.last_used, unique=False)
Index(u'indx', products.c.indx, unique=False)
Index(u'indx_asin', products.c.asin, unique=False)
sources =  Table('sources', metadata,
    Column(u'id', MSInteger(display_width=11), primary_key=True, nullable=False),
            Column(u'source_type', MSString(length=16), primary_key=False, nullable=False),
            Column(u'bitly', MSInteger(display_width=11), primary_key=False, nullable=False),
            Column(u'source', MSString(length=512), primary_key=False, nullable=False),
            Column(u'feed', MSInteger(display_width=11), primary_key=False, nullable=False),
    ForeignKeyConstraint([u'feed'], [u'vypertwitz.feeds.id'], name=u'fkey_feed'),
            ForeignKeyConstraint([u'bitly'], [u'vypertwitz.bitlys.id'], name=u'fkey_bitlys'),
    
    )
Index(u'indx_source', sources.c.source, unique=True)
Index(u'fkey_bitlys', sources.c.bitly, unique=False)
Index(u'fkey_feed', sources.c.feed, unique=False)
sponsors =  Table('sponsors', metadata,
    Column(u'id', MSInteger(display_width=11), primary_key=True, nullable=False),
            Column(u'sponsor_type', MSInteger(display_width=11), primary_key=False, nullable=False),
            Column(u'url', MSString(length=512), primary_key=False, nullable=False),
            Column(u'freq_secs', MSInteger(display_width=11), primary_key=False, nullable=False),
            Column(u'last_used', MSTimeStamp(timezone=False), primary_key=False),
    
    
    )
Index(u'indx_url', sponsors.c.url, unique=True)
used_links =  Table('used_links', metadata,
    Column(u'id', MSInteger(display_width=11), primary_key=True, nullable=False),
            Column(u'source', MSInteger(display_width=11), primary_key=False, nullable=False),
            Column(u'link', MSString(length=512), primary_key=False, nullable=False),
    
    
    )
Index(u'indx_link', used_links.c.link, unique=True)