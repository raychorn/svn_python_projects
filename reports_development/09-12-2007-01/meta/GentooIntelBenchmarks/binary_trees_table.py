from sqlalchemy import *
from sqlalchemy.orm import *

def init_binary_trees_table(metadata):
	binary_trees_table = Table('binary_trees', metadata,
		Column('id', Float, nullable=True),
		Column('name', String(255), nullable=True),
		Column('cpu_rank', Float, nullable=True),
		Column('ram_use', Float, nullable=True),
		Column('gzip_bytes', Float, nullable=True)
		)
	return binary_trees_table
