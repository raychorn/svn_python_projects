
def __init__():
    try:
        from django.contrib.sites.models import Site
        newsite = Site(name="djangocloud",domain="djangocloud.vyperlogix.com")
        newsite.save()
    except:
        pass

if (__name__ == '__main__'):
    __init__()
