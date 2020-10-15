from sqlalchemy import *
from sqlalchemy.orm import *

def init_users_table(metadata):
    users_table = Table('users', metadata,
                    Column('id', Integer, nullable=False, autoincrement=True), 
                    Column('session_id', Integer, nullable=False),
                    Column('name', String(200), nullable=False, primary_key=True),
                    Column('email', String(200), nullable=False),
                    Column('hashed_password', String(40), nullable=False),
                    Column('username', String(200), nullable=False),
                    Column('remember_token_expires_at', DateTime, nullable=True),
                    Column('remember_token', String(40), nullable=True),
                    Column('salt', String(40), nullable=False)
                )
    return users_table
