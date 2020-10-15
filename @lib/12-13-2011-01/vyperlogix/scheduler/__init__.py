'''
Created on Oct 5, 2011

@author: ray.c.horn@hp.com
'''
import os, sys
import time
from datetime import datetime, timedelta

from vyperlogix.misc import _utils
from vyperlogix.misc.threadpool import ThreadQueue, threadify

__Q__ = ThreadQueue(maxsize=1)
__QQ__ = ThreadQueue(maxsize=100)

@threadify(__QQ__)
def threaded_job_proxy(self,task,job):
    was_exception = False
    try:
        if (callable(task)):
            task()
    except Exception, ex:
        was_exception = True
        if (self.logger):
            self.logger.exception('Scheduler failed to execute %s.' % (job))
        if (callable(self.updater_callback)):
            try:
                self.updater_callback(id=job.get('id',None), reason='Exception')
            except:
                if (self.logger):
                    self.logger.exception('Something went wrong with the updater_callback, programmer check your logic !!!')
    finally:
        if (callable(self.updater_callback)):
            try:
                reason = 'Success'
                if (was_exception):
                    reason = 'Exception'
                self.updater_callback(id=job.get('id',None), reason=reason)
            except:
                if (self.logger):
                    self.logger.exception('Something went wrong with the updater_callback, programmer check your logic !!!')

@threadify(__QQ__)
def threaded_job_exec(self,task,job):
    was_exception = False
    try:
        __task__ = '''
was_exception = False
try:
    %s
except Exception, ex:
    was_exception = True
    if (logger):
        logger.exception('Scheduler failed to execute %%s.' %% (job))
    if (callable(updater_callback)):
        try:
            updater_callback(id=job.get('id',None), reason='Exception')
        except:
            if (logger):
                logger.exception('Something went wrong with the updater_callback, programmer check your logic !!!')
finally:
    if (callable(updater_callback)):
        try:
            reason = 'Success'
            if (was_exception):
                reason = 'Exception'
            updater_callback(id=job.get('id',None), reason=reason)
        except:
            if (logger):
                logger.exception('Something went wrong with the updater_callback, programmer check your logic !!!')
        ''' % (task)
        exec(__task__,{'logger':self.logger,'job':job,'updater_callback':self.updater_callback},{})
    except Exception, ex:
        was_exception = True
        if (self.logger):
            self.logger.exception('Scheduler failed to execute %s.' % (job))
        if (callable(self.updater_callback)):
            try:
                self.updater_callback(id=job.get('id',None), reason='Exception')
            except:
                if (self.logger):
                    self.logger.exception('Something went wrong with the updater_callback, programmer check your logic !!!')
    finally:
        if (callable(self.updater_callback)):
            try:
                reason = 'Success'
                if (was_exception):
                    reason = 'Exception'
                self.updater_callback(id=job.get('id',None), reason=reason)
            except:
                if (self.logger):
                    self.logger.exception('Something went wrong with the updater_callback, programmer check your logic !!!')

class Scheduler():
    def __init__(self,db_callback=None,callback=None,updater_callback=None,interval=60,usingLocalTime=True,logger=None):
        self.db_callback = db_callback
        self.interval = interval
        self.callback = callback
        self.logger = logger
        self.usingLocalTime = usingLocalTime
        self.updater_callback = updater_callback

    def db_callback():
        doc = "db_callback property"
        def fget(self):
            return self.db_callback
        def fset(self, db_callback):
            self.db_callback = db_callback
        return locals()
    db_callback = property(**db_callback())

    def interval():
        doc = "interval property"
        def fget(self):
            return self.interval
        def fset(self, interval):
            self.interval = interval
        return locals()
    interval = property(**interval())

    def callback():
        doc = "callback property"
        def fget(self):
            return self.callback
        def fset(self, callback):
            self.callback = callback
        return locals()
    callback = property(**callback())

    def updater_callback():
        doc = "updater_callback property"
        def fget(self):
            return self.updater_callback
        def fset(self, updater_callback):
            self.updater_callback = updater_callback
        return locals()
    updater_callback = property(**updater_callback())

    def usingLocalTime():
        doc = "usingLocalTime property"
        def fget(self):
            return self.usingLocalTime
        def fset(self, usingLocalTime):
            self.usingLocalTime = usingLocalTime
        return locals()
    usingLocalTime = property(**usingLocalTime())

    def get_jobs(self):
        jobs = []
        now = datetime.utcnow()
        try:
            for rec in self.db_callback() if (callable(self.db_callback)) else []:
                if (callable(self.callback)):
                    try:
                        d = self.callback(rec)
                    except:
                        if (self.logger):
                            self.logger.exception('Something went wrong with the callback, programmer check your logic !!!')
                jobs.append(d)
        except:
            if (self.logger):
                self.logger.exception('Programmer, check your logic.')
        if (self.logger):
            self.logger.info('There are %s runnable jobs.' % (len(jobs)))
        return jobs

    def sort_jobs(self,jobs):
        for job in jobs:
            t = job.get('time',None)
            if (t):
                now = datetime.utcnow()
                delta = (t - now) if (t > now) else (t - t)
                job['delta'] = delta.total_seconds()
        return sorted(jobs, key=lambda k: k['delta'])

    def execute_jobs(self,jobs):
        if (self.logger):
            self.logger.info('BEGIN:')
        for i in xrange(len(jobs)):
            job = jobs[i]
            if (self.logger):
                self.logger.info('job is %s' % (job))
            delta = job.get('delta',None)
            if (delta is not None) and (delta <= 0.0):
                if (self.logger):
                    self.logger.info('Execute job %s' % (job))
                task = job.get('task',None)
                if (task):
                    if (callable(task)):
                        threaded_job_proxy(self,task,job)
                    else:
                        threaded_job_exec(self,task,job)
                    time.sleep(self.interval)
        if (self.logger):
            self.logger.info('END !!!')

    @threadify(__Q__)
    def run(self):
        while (1):
            jobs = self.get_jobs()
            jobs = self.sort_jobs(jobs)
            jobs = self.execute_jobs(jobs)
            time.sleep(self.interval)

    def join(self):
        __Q__.join()

if (__name__ == '__main__'):
    print today_localtime()
    scheduler = Scheduler(interval=1)
    scheduler.run()
    __Q__.join()