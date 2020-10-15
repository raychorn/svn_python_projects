from sqlalchemy import *
from sqlalchemy.orm import *

def init_regex_dnas_table(metadata):
	regex_dnas_table = Table('regex_dnas', metadata,
		Column('id', Float, nullable=True),
		Column('name', String(255), nullable=True),
		Column('cpu_rank', Float, nullable=True),
		Column('ram_use', Float, nullable=True),
		Column('gzip_bytes', Float, nullable=True)
		)
	return regex_dnas_table
