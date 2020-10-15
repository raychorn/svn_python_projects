''' Copyright (c) 2006-2007, PreFab Software Inc. '''


from django.conf import settings
from django.db import connection

migration_list = [
    'init',
    'ConsolidatePubDate',
    'AddTrackbackStatus',
    'AddTrackbackUrl',
    'LongerTrackbackStatusLink',
    'TrackbackMessageIsText',
    'LongerEntrySlug',
    'MakeBlogPackage',
    'MoreBlogPackage',
]

def pre_init():
    ''' See if we need to run the init migration.
        This allows migrations to be run on existing databases that don't
        have the migration history table.
    '''
    return not hasTable(connection, 'blogmaker_entry')


if settings.DATABASE_ENGINE in ('postgresql_psycopg2', 'postgresql'):
    def hasTable(conn, name):
        ''' Does the database contain a table with the given name? '''
        sql = '''\
        SELECT c.oid
        FROM pg_catalog.pg_class c
             LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relname = %s
          AND n.nspname = 'public'
          AND pg_catalog.pg_table_is_visible(c.oid)
        '''
        c = conn.cursor()
        c.execute(sql, [name])
        return c.rowcount == 1

elif settings.DATABASE_ENGINE == 'sqlite3':
    def hasTable(conn, name):
        ''' Does the database contain a table with the given name? '''
        sql = '''SELECT name FROM sqlite_master WHERE type='table' AND name=?'''
        c = conn.cursor()
        c.execute(sql, [name])
        return len(c.fetchall()) == 1

else:
    raise NotImplementedError('Unsupported database engine: ' + settings.DATABASE_ENGINE)
