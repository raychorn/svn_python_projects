
if (__name__ == '__main__'):
    import django
    version = django.get_version()
    assert version == '1.7', 'Wrong Django version, requires 1.7'
    print 'Django Version is %s.' % (version)
    