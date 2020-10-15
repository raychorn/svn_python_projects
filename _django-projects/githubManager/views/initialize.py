
def __init__():
    try:
        from django.contrib.sites.models import Site
        newsite = Site(name="githubManager",domain="githubManager.vyperlogix.com")
        newsite.save()
    except:
        pass

if (__name__ == '__main__'):
    __init__()
