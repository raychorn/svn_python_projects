from sqlalchemy import *
from sqlalchemy.orm import *

def init_reverse_complements_table(metadata):
	reverse_complements_table = Table('reverse_complements', metadata,
		Column('id', Float, nullable=True),
		Column('name', String(255), nullable=True),
		Column('cpu_rank', Float, nullable=True),
		Column('ram_use', Float, nullable=True),
		Column('gzip_bytes', Float, nullable=True)
		)
	return reverse_complements_table
