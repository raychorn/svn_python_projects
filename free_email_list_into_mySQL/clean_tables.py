# Reads the Free Email List and pumps it into mySQL using SQLAlchemy Models.

from vyperlogix.misc import _utils

if (__name__ == '__main__'):
    fname = 'free_email_tables.py'
    
    _utils.cleanup_sqlautocode(fname)
