''' Copyright (c) 2006-2007, PreFab Software Inc. '''


from django.db import connection

migration_list = [
    'init',
    'AddCommentType',
    'SeparateTrackbackFields',
    'DropApproved',
    'RestoreApproved',  # Dropping this breaks deployment
    'DropApprovedAgain',
]

def pre_init():
    ''' See if we need to run the init migration.
        This allows migrations to be run on existing databases that don't
        have the migration history table.
    '''
    return not hasTable(connection, 'comments_comment')


def hasTable(conn, name):
    ''' Does the database contain a table with the given name?
        Returns the oid of the table if found, or None'''
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
    if c.rowcount == 1:
        return c.fetchone()[0]
    return None
