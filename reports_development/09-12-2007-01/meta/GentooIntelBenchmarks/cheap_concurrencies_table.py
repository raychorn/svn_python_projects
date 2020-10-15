from sqlalchemy import *
from sqlalchemy.orm import *

def init_cheap_concurrencies_table(metadata):
	cheap_concurrencies_table = Table('cheap_concurrencies', metadata,
		Column('id', Float, nullable=True),
		Column('name', String(255), nullable=True),
		Column('cpu_rank', Float, nullable=True),
		Column('ram_use', Float, nullable=True),
		Column('gzip_bytes', Float, nullable=True)
		)
	return cheap_concurrencies_table
