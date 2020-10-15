from sqlalchemy import *
from sqlalchemy.orm import *

def init_sessions_table(metadata):
    sessions_table = Table('sessions', metadata,
                    Column('id', Integer, nullable=False, autoincrement=True), 
                    Column('uuid', String(40), nullable=False, primary_key=True),
                    Column('theDate', DateTime, nullable=False)
                )
    return sessions_table

