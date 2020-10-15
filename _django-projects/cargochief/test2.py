import sys

l = [f for f in sys.path if (f.find('vyperlogix') > -1)]
print '--> len(l)=%s' % (len(l))
if (len(l) == 0):
    print '--> INSERT #1 !!!'
    sys.path.insert(0, '/usr/local/cargochief/vyperlogix_2_7_0.zip')
l = [f for f in sys.path if (f.find('vyperlogix') > -1)]
if (len(l) == 0):
    print '--> PROBLEM #1 !!!'

l = [f for f in sys.path if (f.find('_Django-1.3_Multi-Threaded') > -1)]
print '--> len(l)=%s' % (len(l))
if (len(l) == 0):
    print '--> INSERT #2 !!!'
    sys.path.insert(1, '/usr/local/cargochief/_Django-1.3_Multi-Threaded')
l = [f for f in sys.path if (f.find('_Django-1.3_Multi-Threaded') > -1)]
if (len(l) == 0):
    print '--> PROBLEM #2 !!!'

l = [f for f in sys.path if (f.find('cargochief') > -1)]
print '--> len(l)=%s' % (len(l))
if (len(l) == 0):
    print '--> INSERT #3 !!!'
    sys.path.insert(1, '/usr/local/cargochief/cargochief')
l = [f for f in sys.path if (f.find('cargochief') > -1)]
if (len(l) == 0):
    print '--> PROBLEM #3 !!!'

for f in sys.path:
    print f

from vyperlogix.django import django_utils
print django_utils.socket.gethostname()

import django
print 'django.VERSION=',django.VERSION
assert list(django.VERSION)[0:3] == [1,3,0], 'Oops, something went wrong with the Django installation...'
try:
	import psycopg2
	print 'psycopg2.apilevel=%s' % (psycopg2.apilevel)
except:
	print 'Must not be running in Linux or missing the psycopg2 package...'

try:
	import settings
except:
	print 'Cannot import settings...'
