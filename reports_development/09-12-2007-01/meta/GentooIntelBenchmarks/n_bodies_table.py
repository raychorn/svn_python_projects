from sqlalchemy import *
from sqlalchemy.orm import *

def init_n_bodies_table(metadata):
	n_bodies_table = Table('n_bodies', metadata,
		Column('id', Float, nullable=True),
		Column('name', String(255), nullable=True),
		Column('cpu_rank', Float, nullable=True),
		Column('ram_use', Float, nullable=True),
		Column('gzip_bytes', Float, nullable=True)
		)
	return n_bodies_table
