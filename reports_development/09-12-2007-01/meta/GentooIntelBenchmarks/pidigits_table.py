from sqlalchemy import *
from sqlalchemy.orm import *

def init_pidigits_table(metadata):
	pidigits_table = Table('pidigits', metadata,
		Column('id', Float, nullable=True),
		Column('name', String(255), nullable=True),
		Column('cpu_rank', Float, nullable=True),
		Column('ram_use', Float, nullable=True),
		Column('gzip_bytes', Float, nullable=True)
		)
	return pidigits_table
