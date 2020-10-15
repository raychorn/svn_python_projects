from sqlalchemy import *
from sqlalchemy.orm import *

def init_partial_sums_table(metadata):
	partial_sums_table = Table('partial_sums', metadata,
		Column('id', Float, nullable=True),
		Column('name', String(255), nullable=True),
		Column('cpu_rank', Float, nullable=True),
		Column('ram_use', Float, nullable=True),
		Column('gzip_bytes', Float, nullable=True)
		)
	return partial_sums_table
