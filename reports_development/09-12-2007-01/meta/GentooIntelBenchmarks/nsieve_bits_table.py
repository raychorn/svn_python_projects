from sqlalchemy import *
from sqlalchemy.orm import *

def init_nsieve_bits_table(metadata):
	nsieve_bits_table = Table('nsieve_bits', metadata,
		Column('id', Float, nullable=True),
		Column('name', String(255), nullable=True),
		Column('cpu_rank', Float, nullable=True),
		Column('ram_use', Float, nullable=True),
		Column('gzip_bytes', Float, nullable=True)
		)
	return nsieve_bits_table
