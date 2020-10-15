from vyperlogix import misc
from vyperlogix.django import django_utils

def is_authenticated(request):
    try:
	return django_utils.get_from_session(request,'has_joomla_login_success',default=False)
    except:
	pass
    return False

def is_SuperAdministrator(request):
    try:
	return django_utils.get_from_session(request,'is_SuperAdministrator',default=False)
    except:
	pass
    return False

def _is_SuperAdministrator(request):
    from vyperlogix.classes import SmartObject
    if (is_authenticated(request)) and (not is_SuperAdministrator(request)):
	try:
	    fxname = misc.funcName().split('_')[-1]
	    users = django_utils.get_from_session(request,'joomla_user',default=[])
	    for aUser in users:
		if (''.join(aUser.usertype.split(' ')) == fxname):
		    return True
	    return False
	except:
	    pass
    return False

def get_errors(request):
    try:
	return django_utils.get_from_session(request,'ERRORS',default='')
    except:
	pass
    return False

if (__name__ == '__main__'):
    import sys, os
    fpath = 'Z:\@myFiles\@Python+Compressed'
    files = [os.path.join(fpath,f) for f in os.listdir(fpath) if (f.startswith('Python '))]

    for f1 in files:
	f2 = os.path.join(os.path.dirname(f1),os.path.basename(f1).replace('Python ',''))
	print 'Renaming %s -> %s' % (f1,f2)
	os.rename(f1,f2)
    pass
