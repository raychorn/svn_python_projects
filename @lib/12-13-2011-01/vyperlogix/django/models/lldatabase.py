from django.conf import settings

def connect(database):
    """
    Takes a database name, uses that name to grab settings for that database
    """
    dbargs = {}
    fields = ('ENGINE', 'USER', 'HOST', 'PASSWORD', 'NAME', 'PORT')
    for i in range(len(fields)):
        dbargs['%s_%s' % ("DATABASE", fields[i])] = \
            settings.__getitem__('%s_%s_%s' % (database.upper(), "DB", fields[i]))
    #Note: this must be called before doing any further database related imports
    if settings.configured:
        fields = ("DATABASE_NAME",
                  "DATABASE_USER",
                  "DATABASE_HOST",
                  "DATABASE_PORT",
                  "DATABASE_ENGINE",
                  "DATABASE_PASSWORD")
        current_db = {}
        for i in range(len(fields)):
            current_db.update( { fields[i]: getattr(settings, fields[i]) } )
        # If we are already connect to the exact same database, do nothing
        if current_db != dbargs:
            from django.db import connection
            connection.close()
            for key, value in dbargs.items():
                setattr(settings, key, value)
    else:
        settings.configure(**dbargs)

def disconnect():
    connect(config.DEFAULT_DATABASE)

def flush_table(table):
    rows = table.objects.all()
    rows.delete()
    