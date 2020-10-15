from sqlalchemy import *
from sqlalchemy.orm import *

def init_spectral_norms_table(metadata):
	spectral_norms_table = Table('spectral_norms', metadata,
		Column('id', Float, nullable=True),
		Column('name', String(255), nullable=True),
		Column('cpu_rank', Float, nullable=True),
		Column('ram_use', Float, nullable=True),
		Column('gzip_bytes', Float, nullable=True)
		)
	return spectral_norms_table
