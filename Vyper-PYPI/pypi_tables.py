# -*- coding: utf8 -*-
## File autogenerated by SQLAutoCode
## see http://code.google.com/p/sqlautocode/
from sqlalchemy import *
from sqlalchemy.databases.mysql import *
metadata = MetaData()
classifiers =  Table('classifiers', metadata,
    Column(u'id', MSInteger(display_width=11), primary_key=True, nullable=False),
            Column(u'classifier', MSString(length=128), primary_key=False, nullable=False),
    
    
    )
Index(u'index_classifier', classifiers.c.classifier, unique=True)
package_classifiers =  Table('package_classifiers', metadata,
    Column(u'id', MSInteger(display_width=11), primary_key=True, nullable=False),
            Column(u'pid', MSInteger(display_width=11), primary_key=False, nullable=False),
            Column(u'cid', MSInteger(display_width=11), primary_key=False, nullable=False),
    
    
    )
Index(u'fk_package', package_classifiers.c.pid, unique=False)
Index(u'fk_classfier', package_classifiers.c.cid, unique=False)
packages =  Table('packages', metadata,
    Column(u'id', MSInteger(display_width=11), primary_key=True, nullable=False),
            Column(u'name', MSString(length=128), primary_key=False, nullable=False),
            Column(u'version', MSString(length=128), primary_key=False, nullable=False),
            Column(u'author', MSString(length=128), primary_key=False),
            Column(u'author_email', MSString(length=256), primary_key=False),
            Column(u'maintainer', MSString(length=128), primary_key=False),
            Column(u'maintainer_email', MSString(length=256), primary_key=False),
            Column(u'home_page', MSString(length=512), primary_key=False),
            Column(u'license', MSText(), primary_key=False),
            Column(u'summary', MSText(), primary_key=False),
            Column(u'description', MSText(), primary_key=False),
            Column(u'keywords', MSString(length=128), primary_key=False),
            Column(u'platform', MSText(), primary_key=False),
            Column(u'download_url', MSString(length=512), primary_key=False),
            Column(u'action', MSString(length=128), primary_key=False),
            Column(u'_pypi_hidden', MSString(length=32), primary_key=False),
            Column(u'requires', MSText(), primary_key=False),
            Column(u'provides', MSText(), primary_key=False),
            Column(u'obsoletes', MSText(), primary_key=False),
    
    
    )
Index(u'index_name', packages.c.name, unique=True)
