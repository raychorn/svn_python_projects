# -*- coding: utf8 -*-
## File autogenerated by SQLAutoCode
## see http://code.google.com/p/sqlautocode/

from sqlalchemy import *
from sqlalchemy.databases.mysql import *

metadata = MetaData()


freeemailhost__c =  Table('freeemailhost__c', metadata,
    Column(u'id', MSInteger(display_width=11), primary_key=True, nullable=False),
            Column(u'IsActive__c', MSBit(length=1), primary_key=False, nullable=False),
            Column(u'Domain__c', MSString(length=128), primary_key=False, nullable=False),
    
    
    )
Index(u'index_Domain__c', freeemailhost__c.c.Domain__c, unique=True)

