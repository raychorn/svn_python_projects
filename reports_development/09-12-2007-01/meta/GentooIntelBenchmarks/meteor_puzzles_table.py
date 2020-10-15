from sqlalchemy import *
from sqlalchemy.orm import *

def init_meteor_puzzles_table(metadata):
	meteor_puzzles_table = Table('meteor_puzzles', metadata,
		Column('id', Float, nullable=True),
		Column('name', String(255), nullable=True),
		Column('cpu_rank', Float, nullable=True),
		Column('ram_use', Float, nullable=True),
		Column('gzip_bytes', Float, nullable=True)
		)
	return meteor_puzzles_table
