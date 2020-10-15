''' Utility to attempt current trackbacks logging the results 

Copyright (c) 2006-2007, PreFab Software Inc.

'''

from __future__ import with_statement

import datetime, logging, sys
from cStringIO import StringIO
from itertools import chain, imap, islice

from django.conf import settings
import blogcosm.django_setup
from django.core.mail import send_mail

from blogmaker.blog.models import Entry
from blogmaker.util import logToData
from blogmaker.util.trap_errors import error_trapping


def main():
    ''' Attempt all current trackbacks. 
        Email the results to settings.MANAGERS.
    '''
    logToData('trackback.log')
    
    # Set up to capture logging info for email
    log = getLogger()
    buf = StringIO()
    handler = logging.StreamHandler(buf)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    
    # The actual attempt
    log.info('--------------------- Start Trackback Attempt for %s ------------------' % settings.DATABASE_NAME)
    attempts = attempt_all_current()
    
    # Email the results if any
    log.removeHandler(handler)
    if attempts:
        results = buf.getvalue()
        toaddrs  = [manager_tuple[1] for manager_tuple in settings.MANAGERS]

        with error_trapping('sending email'):
            send_mail('Trackback Results %s' % datetime.date.today(), results, 
                settings.DEFAULT_FROM_EMAIL, toaddrs, fail_silently=False)
    

def attempt_all_current():
    ''' Find all current entries.
        Update their trackback list to reflect their current links.
        Attempt all eligible trackbacks for the entries.
        Returns a count of the number of trackbacks attempted. '''
    log = getLogger()
    now = datetime.datetime.now()
    startDate = now - datetime.timedelta(days=7)
    attempts = 0
    
    for entry in Entry.objects.exclude(pub_date__gt=now).exclude(pub_date__lt=startDate):
        entry.update_trackbacks()
        for tb in entry.trackbacks.all():
            if tb.eligible:
                with error_trapping():
                    attempts += 1
                    log.info('Attempting trackback for "%s" (%s)' % (tb.entry.headline, tb.link))
                    tb.attempt()
                    if tb.message:
                        log.info('Result: %s: %s', tb.get_status_display(), tb.message)
                    else:
                        log.info('Result: %s', tb.get_status_display())
                    if tb.status=='NoLink' and hasattr(tb, 'page_data'):
                        count = logPossibles(log, tb.page_data)
                        if count:
                            tb.appendMessage("%s candidate(s) found; see email for details" % count)
                        else:
                            tb.appendMessage("No candidates found")
                        tb.save()
                    log.info('')
    return attempts
    

def logPossibles(log, data):
    ''' Log possible trackbacks and return a count of how many were found. '''
    log.info('Possible trackbacks:')
    found = False
    count = 0
    for prev, curr, next in triples(data.splitlines()):
        if 'trackback' in curr.lower():
            log.info('    ' + prev)
            log.info('    ' + curr)
            log.info('    ' + next)
            found = True
            count += 1
    if not found:
        log.info('    None')
    return count

def triples(seq, fill=''):
    ''' Yield walking triples of items in seq.
        Each item in seq appears once as the middle item.
        End triples are filled with fill.
    '''
    iters = [ chain([fill], iter(seq)), 
              iter(seq), 
              chain(islice(seq, 1, sys.maxint), [fill]) ]
    return imap(None, *iters)
        
        
def getLogger():
    return logging.getLogger('blogmaker.blog.trackback_update')
    
    
if __name__ == '__main__':
    main()