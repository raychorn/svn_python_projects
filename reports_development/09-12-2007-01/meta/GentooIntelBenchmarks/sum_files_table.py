from sqlalchemy import *
from sqlalchemy.orm import *

def init_sum_files_table(metadata):
	sum_files_table = Table('sum_files', metadata,
		Column('id', Float, nullable=True),
		Column('name', String(255), nullable=True),
		Column('cpu_rank', Float, nullable=True),
		Column('ram_use', Float, nullable=True),
		Column('gzip_bytes', Float, nullable=True)
		)
	return sum_files_table
