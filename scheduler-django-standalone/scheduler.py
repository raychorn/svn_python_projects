#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys

import time

import logging

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix import scheduler

from vyperlogix.logging import standardLogging

__scheduler__ = scheduler.Scheduler(interval=5)

def remove_python_paths_matching(pattern):
    i = 0
    _i_ = -1
    for f in sys.path:
        if (f.find(pattern) > -1):
            _i_ = i
            break
        i += 1
    if (_i_ > -1):
        del sys.path[_i_]
    libs = [f for f in sys.path if (f.find(pattern) > -1)]
    print libs

remove_python_paths_matching('_django-projects\\')

print 'BEGIN:'
for f in sys.path:
    print f
print 'END!!!'

import django
assert(float('%s.%s'%(django.VERSION[0:3][0],''.join([str(i) for i in list(django.VERSION[0:3][1:])]))) >= 1.5)
print django.VERSION

from optparse import OptionParser

parser = OptionParser("usage: %prog -d DATABASE [-s]")
parser.add_option('-d', '--database', dest='database', help="DATABASE file name", metavar="DATABASE")
parser.add_option('-s', '--syncdb', dest='syncdb', action="store_true", help="should the database be created?")
parser.add_option('-r', '--repl', dest='repl', action="store_true", help="start a REPL with access to your models")
parser.add_option('--d', '--dumpdata', dest='dumpdata', action="store_true", help="django dumpdata")
parser.add_option('-i', '--inspectdb', dest='inspectdb', action="store_true", help="django inspectdb")
parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
parser.add_option('-t', '--test', dest='test', help="test type (1-24) specifies the number of hour offsets for test jobs, 24 means test all 24 hour offsets to simulate running a job in all 24 timezones.")
parser.add_option('-u', '--utc', dest='utc', help="use utc time base or scheduled jobs otherwise uses localtime function that auto-converts to utc; scheduler core always uses utc for now().", action="store_true")

options, args = parser.parse_args()

if not options.database:
    parser.error("You must specify the database name")
    _utils.terminate('Cannot continue without the database name on the command line.')

__cwd__ = os.path.expanduser("~")
name = _utils.getProgramName()
fpath = __cwd__
_log_path = _utils.safely_mkdir_logs(fpath=fpath)
_log_path = _utils.safely_mkdir(fpath=_log_path,dirname=_utils.timeStampLocalTimeForFileName(delimiters=('_','-'),format=_utils.formatSalesForceTimeStr()))
if (not os.path.exists(_log_path)):
    print >> sys.stderr, 'Logging path does not exist at "%s".' % (_log_path)

logFileName = os.sep.join([_log_path,'%s.log' % (name)])

print '(%s) :: Logging to "%s".' % (_utils.timeStampLocalTime(),logFileName)
    
from standalone.conf import settings

from vyperlogix.django import django_utils
DOMAIN_NAME = django_utils.socket.gethostname()
print '1.DOMAIN_NAME=%s' % (DOMAIN_NAME)
if (DOMAIN_NAME in ['HPDV7-6163us']):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': options.database,
            'USER' : 'root',
            'PASSWORD' : 'peekab00',
            'HOST' : '192.168.1.248',
            'PORT' : '3306',
        }
    }
elif (DOMAIN_NAME in ['HORNRA3','Alienware-PC','enterprise1701']):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': options.database,
            'USER' : 'raychorn',
            'PASSWORD' : 'peekab00',
            'HOST' : '127.0.0.1',
            'PORT' : '23337',
        }
    }
settings = settings(
    DATABASES = DATABASES
)

# build the models we want to have in the database
from standalone import models

class ScheduledJob(models.StandaloneModel):
    taskid = models.IntegerField(blank=False)
    taskname = models.CharField(max_length=128,blank=False)
    created_at = models.DateTimeField(blank=False)
    modified_at = models.DateTimeField(blank=False)
    run_at = models.DateTimeField(blank=False)
    info = models.TextField(blank=False)
    runnable = models.BooleanField(blank=False)
    class Meta:
        db_table = u'scheduledjob'
        
    def details(self):
        from django.forms.models import model_to_dict
        return str(model_to_dict(self))

from django.core.management import call_command

_isVerbose = False
if (options.verbose):
    _isVerbose = True

logger = logging.getLogger('scheduler')
handler = logging.FileHandler(logFileName)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler) 
print 'Logging to "%s".' % (handler.baseFilename)

ch = logging.StreamHandler()
ch_format = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(ch_format)
ch.setLevel(logging.INFO)
logger.addHandler(ch)

logging.getLogger().setLevel(logging.INFO)

if options.syncdb:
    # run a simple command - here syncdb - from the management suite
    call_command('syncdb')
    _utils.terminate('Done !!!')
elif options.repl:
    # start the shell, access to your models through import standalone.models
    call_command('shell')
    _utils.terminate('Done !!!')
elif options.dumpdata:
    call_command('dumpdata')
    sys.exit(1)
elif options.inspectdb:
    call_command('inspectdb')
    _utils.terminate('Done !!!')
    
__cache__ = SmartObject()

def db_callback():
    jobs = [job for job in ScheduledJob.objects.all() if (__cache__[job.taskid])]
    num = len(jobs)
    logger.info('There are %s runnable job(s).' % (num))
    return jobs

def callback(rec):
    assert(rec.runnable == True)
    d = {'id':rec.taskid,'taskname':rec.taskname,'time':rec.run_at,'task':rec.info}
    return d

def updater_callback(**kwargs):
    so = SmartObject(kwargs)
    jobs = [job for job in ScheduledJob.objects.all() if (job.runnable and (job.taskid == so.id))]
    logger.info('(1) Job %s is %s' % (so.id, so.reason))
    for job in jobs:
        job.runnable = so.reason.lower() != 'success'
        logger.info('(2) Job %s is %s' % (so.id, so.reason))
        job.save()
        __cache__[job.taskid] = job.runnable

jobs = ScheduledJob.objects.all()

for job in jobs:
    job.delete()

def __schedule_job__(taskid=1,offset=11):
    import datetime
    __secs__ = _utils.today_localtime_as_seconds()+offset
    if (options.utc):
        __secs__ = _utils.utc_datetime_as_seconds()+offset
    job = ScheduledJob()
    job.taskid = taskid
    job.taskname = 'Job_%s' % (job.taskid)
    job.created_at = job.modified_at = _utils.today_localtime() if (not options.utc) else datetime.datetime.utcnow()
    job.run_at = _utils.getFromNativeTimeStamp(_utils.getAsDateTimeStrFromTimeSeconds(__secs__),format=_utils._formatTimeStr())
    job.info = '''
        print "TESTING taskid is %s run_at is %s..."
    '''  % (taskid,job.run_at)
    job.runnable = True
    job.save()
    logger.info('Job created_at is %s.' % (job.created_at))

if (options.test and str(options.test).isdigit()):
    num_to_test = int(options.test)
    for i in xrange(1,num_to_test+1):
        __schedule_job__(taskid=i,offset=3600*(i-1))
else:
    __schedule_job__()

jobs = ScheduledJob.objects.all()

for job in jobs:
    print job.details()
    __cache__[job.taskid] = job.runnable
    
__scheduler__.logger = logger
__scheduler__.db_callback = db_callback
__scheduler__.callback = callback
__scheduler__.updater_callback = updater_callback
__scheduler__.run()

logger.info('Waiting on the scheduler...')
__scheduler__.join()

logger.info('DONE !!!')
_utils.terminate('Done !!!')

