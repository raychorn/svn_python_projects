from sqlalchemy import *
from sqlalchemy.orm import *

def init_chameneos_table(metadata):
	chameneos_table = Table('chameneos', metadata,
		Column('id', Float, nullable=True),
		Column('name', String(255), nullable=True),
		Column('cpu_rank', Float, nullable=True),
		Column('ram_use', Float, nullable=True),
		Column('gzip_bytes', Float, nullable=True)
		)
	return chameneos_table
