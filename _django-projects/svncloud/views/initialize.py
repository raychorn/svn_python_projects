
def __init__():
    try:
        from django.contrib.sites.models import Site
        newsite = Site(name="SVNCloud",domain="svncloud.vyperlogix.com")
        newsite.save()
    except:
        pass

if (__name__ == '__main__'):
    __init__()
