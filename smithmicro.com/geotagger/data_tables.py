# -*- coding: utf8 -*-

from sqlalchemy import *
from sqlalchemy.databases import mysql

metadata = MetaData()

geotagger_sample1_table =  Table('sample-data', metadata,
                                 Column(u'id', mysql.MSInteger(display_width=11), primary_key=True, nullable=False),
                                 Column(u'heat_lat', mysql.MSInteger(display_width=11), primary_key=False, nullable=False),
                                 Column(u'heat_lng', mysql.MSInteger(display_width=11), primary_key=False, nullable=False),
                                 Column(u'heat_x', mysql.MSInteger(display_width=11), primary_key=False, nullable=False),
                                 Column(u'heat_y', mysql.MSInteger(display_width=11), primary_key=False, nullable=False),
                                 Column(u'heat_num', mysql.MSInteger(display_width=11), primary_key=False, nullable=False),
                                 Column(u'num_connections', mysql.MSInteger(display_width=11), primary_key=False, nullable=False),
                                 Column(u'num_failures', mysql.MSInteger(display_width=11), primary_key=False, nullable=False),
                          )

gps1M_table =  Table('gps_1M', metadata,
                     Column(u'id', Integer(), primary_key=True, nullable=False),
                     Column(u'heat_gps', String(length=128, convert_unicode=False, assert_unicode=None), primary_key=False, nullable=False),
                     Column(u'heat_lat', Integer(), primary_key=False, nullable=False),
                     Column(u'heat_lng', Integer(), primary_key=False, nullable=False),
                     Column(u'heat_x', Integer(), primary_key=False, nullable=False),
                     Column(u'heat_y', Integer(), primary_key=False, nullable=False),
                     Column(u'heat_num', Integer(), primary_key=False, nullable=False),
                     Column(u'num_connections', Integer(), primary_key=False, nullable=False),
                     Column(u'num_failures', Integer(), primary_key=False, nullable=False),
                )

