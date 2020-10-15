from sqlalchemy import *
from sqlalchemy.orm import *

def init_recursives_table(metadata):
	recursives_table = Table('recursives', metadata,
		Column('id', Float, nullable=True),
		Column('name', String(255), nullable=True),
		Column('cpu_rank', Float, nullable=True),
		Column('ram_use', Float, nullable=True),
		Column('gzip_bytes', Float, nullable=True)
		)
	return recursives_table
