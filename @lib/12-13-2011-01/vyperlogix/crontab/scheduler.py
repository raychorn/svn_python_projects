#!/usr/bin/env python
"""
See also: http://code.activestate.com/recipes/577466-cron-like-triggers/

This module provides a class for cron-like scheduling systems, and
exposes the function used to convert static cron expressions to Python
sets.

CronExpression objects are instantiated with a cron formatted string
that represents the times when the trigger is active. When using
expressions that contain periodic terms, an extension of cron created
for this module, a starting epoch should be explicitly defined. When the
epoch is not explicitly defined, it defaults to the Unix epoch. Periodic
terms provide a method of recurring triggers based on arbitrary time
periods.


Standard Cron Triggers:
>>> job = CronExpression("0 0 * * 1-5/2 find /var/log -delete")
>>> job.check_trigger((2010, 11, 17, 0, 0))
True
>>> job.check_trigger((2012, 12, 21, 0 , 0))
False

Periodic Trigger:
>>> job = CronExpression("0 %9 * * * Feed 'it'", (2010, 5, 1, 7, 0, -6))
>>> job.comment
"Feed 'it'"
>>> job.check_trigger((2010, 5, 1, 7, 0), utc_offset=-6)
True
>>> job.check_trigger((2010, 5, 1, 16, 0), utc_offset=-6)
True
>>> job.check_trigger((2010, 5, 2, 1, 0), utc_offset=-6)
True
"""

import datetime
import calendar

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName
from vyperlogix.classes.SmartObject import SmartObject

__all__ = ["CronExpression", "parse_atom", "DEFAULT_EPOCH", "SUBSTITUTIONS"]
__license__ = "Public Domain"

DAY_NAMES = zip(('sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'), xrange(7))
MINUTES = (0, 59)
HOURS = (0, 23)
DAYS_OF_MONTH = (1, 31)
MONTHS = (1, 12)
DAYS_OF_WEEK = (0, 6)
L_FIELDS = (DAYS_OF_WEEK, DAYS_OF_MONTH)
FIELD_RANGES = (MINUTES, HOURS, DAYS_OF_MONTH, MONTHS, DAYS_OF_WEEK)
MONTH_NAMES = zip(('jan', 'feb', 'mar', 'apr', 'may', 'jun',
                   'jul', 'aug', 'sep', 'oct', 'nov', 'dec'), xrange(1, 13))
DEFAULT_EPOCH = (1970, 1, 1, 0, 0, 0)
SUBSTITUTIONS = {
    "@yearly": "0 0 1 1 *",
    "@anually": "0 0 1 1 *",
    "@monthly": "0 0 1 * *",
    "@weekly": "0 0 * * 0",
    "@daily": "0 0 * * *",
    "@midnight": "0 0 * * *",
    "@hourly": "0 * * * *"
}

class CronExpression(object):
    def __init__(self, line, epoch=DEFAULT_EPOCH, epoch_utc_offset=0):
        """
        Instantiates a CronExpression object with an optionally defined epoch.
        If the epoch is defined, the UTC offset can be specified one of two
        ways: as the sixth element in 'epoch' or supplied in epoch_utc_offset.
        The epoch should be defined down to the minute sorted by
        descending significance.
        """
        for key, value in SUBSTITUTIONS.items():
            if line.startswith(key):
                line = line.replace(key, value)
                break

        fields = line.split(None, 5)
        if len(fields) == 5:
            fields.append('')

        minutes, hours, dom, months, dow, self.comment = fields if ((misc.isTuple(fields) or misc.isList(fields)) and (len(fields) == 6)) else ('', '', '', '', '', '')

        dow = dow.replace('7', '0').replace('?', '*')
        dom = dom.replace('?', '*')

        for monthstr, monthnum in MONTH_NAMES:
            months = months.lower().replace(monthstr, str(monthnum))

        for dowstr, downum in DAY_NAMES:
            dow = dow.lower().replace(dowstr, str(downum))

        self.string_tab = [minutes, hours, dom.upper(), months, dow.upper()]
        self.compute_numtab()
        if len(epoch) == 5:
            y, mo, d, h, m = epoch
            self.epoch = (y, mo, d, h, m, epoch_utc_offset)
        else:
            self.epoch = epoch

    def __str__(self):
        base = self.__class__.__name__ + "(%s)"
        cron_line = self.string_tab + [str(self.comment)]
        if not self.comment:
            cron_line.pop()
        arguments = '"' + ' '.join(cron_line) + '"'
        if self.epoch != DEFAULT_EPOCH:
            return base % (arguments + ", epoch=" + repr(self.epoch))
        else:
            return base % arguments

    def __repr__(self):
        return str(self)

    def compute_numtab(self):
        """
        Recomputes the sets for the static ranges of the trigger time.

        This method should only be called by the user if the string_tab
        member is modified.
        """
        self.numerical_tab = []

        for field_str, span in zip(self.string_tab, FIELD_RANGES):
            split_field_str = field_str.split(',')
            if len(split_field_str) > 1 and "*" in split_field_str:
                raise ValueError("\"*\" must be alone in a field.")

            unified = set()
            for cron_atom in split_field_str:
                # parse_atom only handles static cases
                for special_char in ('%', '#', 'L', 'W'):
                    if special_char in cron_atom:
                        break
                else:
                    __atom__ = parse_atom(cron_atom, span)
                    if (__atom__):
                        unified.update(__atom__)

            self.numerical_tab.append(unified)

        if self.string_tab[2] == "*" and self.string_tab[4] != "*":
            self.numerical_tab[2] = set()

    def check_trigger(self, date_tuple, utc_offset=0):
        """
        Returns boolean indicating if the trigger is active at the given time.
        The date tuple should be in the local time. Unless periodicities are
        used, utc_offset does not need to be specified. If periodicities are
        used, specifically in the hour and minutes fields, it is crucial that
        the utc_offset is specified.
        """
        year, month, day, hour, mins = date_tuple
        given_date = datetime.date(year, month, day)
        zeroday = datetime.date(*self.epoch[:3])
        last_dom = calendar.monthrange(year, month)[-1]
        dom_matched = True

        # In calendar and datetime.date.weekday, Monday = 0
        given_dow = (datetime.date.weekday(given_date) + 1) % 7
        first_dow = (given_dow + 1 - day) % 7

        # Figure out how much time has passed from the epoch to the given date
        utc_diff = utc_offset - self.epoch[5]
        mod_delta_yrs = year - self.epoch[0]
        mod_delta_mon = month - self.epoch[1] + mod_delta_yrs * 12
        mod_delta_day = (given_date - zeroday).days
        mod_delta_hrs = hour - self.epoch[3] + mod_delta_day * 24 + utc_diff
        mod_delta_min = mins - self.epoch[4] + mod_delta_hrs * 60

        # Makes iterating through like components easier.
        quintuple = zip(
            (mins, hour, day, month, given_dow),
            self.numerical_tab,
            self.string_tab,
            (mod_delta_min, mod_delta_hrs, mod_delta_day, mod_delta_mon,
             mod_delta_day),
            FIELD_RANGES)

        for value, valid_values, field_str, delta_t, field_type in quintuple:
            # All valid, static values for the fields are stored in sets
            if value in valid_values:
                continue

            # The following for loop implements the logic for context
            # sensitive and epoch sensitive constraints. break statements,
            # which are executed when a match is found, lead to a continue
            # in the outer loop. If there are no matches found, the given date
            # does not match expression constraints, so the function returns
            # False as seen at the end of this for...else... construct.
            for cron_atom in field_str.split(','):
                if (misc.isStringValid(cron_atom)) and (cron_atom[0] == '%'):
                    if not(delta_t % int(cron_atom[1:])):
                        break

                elif field_type == DAYS_OF_WEEK and '#' in cron_atom:
                    D, N = int(cron_atom[0]), int(cron_atom[2])
                    # Computes Nth occurence of D day of the week
                    if (((D - first_dow) % 7) + 1 + 7 * (N - 1)) == day:
                        break

                elif field_type == DAYS_OF_MONTH and cron_atom[-1] == 'W':
                    target = min(int(cron_atom[:-1]), last_dom)
                    lands_on = (first_dow + target - 1) % 7
                    if lands_on == 0:
                        # Shift from Sun. to Mon. unless Mon. is next month
                        target += 1 if target < last_dom else -2
                    elif lands_on == 6:
                        # Shift from Sat. to Fri. unless Fri. in prior month
                        target += -1 if target > 1 else 2

                    # Break if the day is correct, and target is a weekday
                    if target == day and (first_dow + target - 7) % 7 > 1:
                        break

                elif field_type in L_FIELDS and cron_atom.endswith('L'):
                    # In dom field, L means the last day of the month
                    target = last_dom

                    if field_type == DAYS_OF_WEEK:
                        # Calculates the last occurence of given day of week
                        desired_dow = int(cron_atom[:-1])
                        target = (((desired_dow - first_dow) % 7) + 29)
                        target -= 7 if target > last_dom else 0

                    if target == day:
                        break
            else:
                # See 2010.11.15 of CHANGELOG
                if field_type == DAYS_OF_MONTH and self.string_tab[4] != '*':
                    dom_matched = False
                    continue
                elif field_type == DAYS_OF_WEEK and self.string_tab[2] != '*':
                    # If we got here, then days of months validated so it does
                    # not matter that days of the week failed.
                    return dom_matched

                # None of the expressions matched which means this field fails
                return False

        # Arriving at this point means the date landed within the constraints
        # of all fields; the associated trigger should be fired.
        return True


def parse_atom(parse, minmax):
    """
    Returns a set containing valid values for a given cron-style range of
    numbers. The 'minmax' arguments is a two element iterable containing the
    inclusive upper and lower limits of the expression.

    Examples:
    >>> parse_atom("1-5",(0,6))
    set([1, 2, 3, 4, 5])

    >>> parse_atom("*/6",(0,23))
    set([0, 6, 12, 18])

    >>> parse_atom("18-6/4",(0,23))
    set([18, 22, 0, 4])

    >>> parse_atom("*/9",(0,23))
    set([0, 9, 18])
    """
    parse = parse.strip()
    increment = 1
    if parse == '*':
        return set(xrange(minmax[0], minmax[1] + 1))
    elif parse.isdigit():
        # A single number still needs to be returned as a set
        value = int(parse)
        if value >= minmax[0] and value <= minmax[1]:
            return set((value,))
        else:
            raise ValueError("Invalid bounds: \"%s\"" % parse)
    elif '-' in parse or '/' in parse:
        divide = parse.split('/')
        subrange = divide[0]
        if len(divide) == 2:
            # Example: 1-3/5 or */7 increment should be 5 and 7 respectively
            increment = int(divide[1])

        if '-' in subrange:
            # Example: a-b
            prefix, suffix = [int(n) for n in subrange.split('-')]
            if prefix < minmax[0] or suffix > minmax[1]:
                raise ValueError("Invalid bounds: \"%s\"" % parse)
        elif subrange == '*':
            # Include all values with the given range
            prefix, suffix = minmax
        else:
            raise ValueError("Unrecognized symbol: \"%s\"" % subrange)

        if prefix < suffix:
            # Example: 7-10
            return set(xrange(prefix, suffix + 1, increment))
        else:
            # Example: 12-4/2; (12, 12 + n, ..., 12 + m*n) U (n_0, ..., 4)
            noskips = list(xrange(prefix, minmax[1] + 1))
            noskips+= list(xrange(minmax[0], suffix + 1))
            return set(noskips[::increment])

from vyperlogix.misc import threadpool
__Q__ = threadpool.ThreadQueue(1)
        
def crontab(config,jsonHandler=None,callback=None,logging_callback=None,default=None,threaded=False):
    import os, sys, time, signal
    from vyperlogix.misc import _utils
    from vyperlogix.process.shell import SmartShell
    from vyperlogix.lists.ListWrapper import ListWrapper
    
    normalize = lambda items:[s for s in [''.join(ll[0:ll.findFirstMatching('#') if (ll.findFirstMatching('#') > -1) else len(ll)]).strip() for ll in [ListWrapper(l) for l in items if (len(l) > 0)]] if (len(s) > 0)]
    
    def __logger__(msg):
	if (callable(logging_callback)):
	    try:
		logging_callback(msg)
	    except:
		pass

    def __crontab__(config,jsonHandler=jsonHandler,callback=callback,logging_callback=logging_callback,default=default):
        __lines__ = ''
        
	__logger__('INFO.1.1: verbose="%s" (%s).' % (config.verbose,ObjectTypeName.typeClassName(config.verbose)))
	try:
	    __logger__('INFO.1.2: config="%s".' % (config))
	    if (config.verbose):
		__logger__('INFO.1.3: JSON FPath ?: "%s".' % (config.jsonFpath))
	    if (callable(jsonHandler)):
		try:
		    __config__ = jsonHandler(config.jsonFpath)
		except Exception, ex:
		    __config__ = SmartObject()
	    __file__ = config.schedulefpath if (misc.isStringValid(config.schedulefpath)) else None
	    if (config.verbose):
		__logger__('INFO.1.4: Crontab ?: "%s".' % (__file__))
	    if (os.path.exists(__file__)):
		if (config.verbose):
		    __logger__('INFO.1.5: Crontab Exists: "%s".' % (__file__))
		__lines__ = _utils._readFileFrom(__file__)
		if (config.verbose):
		    __logger__('INFO.1.6: Crontab Content: "%s".' % (__lines__))
	except Exception, ex:
	    __logger__('EXCEPTION.1: "%s".' % (_utils.formattedException(details=ex)))
        
	__logger__('INFO.1.6.1: config.isRunning="%s".' % (config.isRunning))
        while (config.isRunning and threaded):
            jobs = [CronExpression(__line__) for __line__ in normalize(__lines__) if (misc.isStringValid(__line__))]
            config.isRunning = callback(jobs) if (callable(callback)) else True
            if (config.isRunning):
                for job in jobs:
                    if (config.verbose):
			__logger__('INFO.1.7: Job: "%s".' % (job))
                    if job.check_trigger(time.gmtime(time.time())[:5]):
                        if (config.dryrun):
			    __logger__('INFO.1.8: Execute: %s' % (job.comment))
                        else:
			    import tempfile
			    __cmd__ = tempfile.NamedTemporaryFile().name
			    __sysout__ = _utils.stringIO()

			    def __callback__(ss,data=None):
				global __begin__
				if (data) and (misc.isString(data)) and (len(data) > 0):
				    __logger__('INFO.1.9: %s' % (data))
				return
			
			    def __onExit__(ss):
				__logger__('INFO.1.10: __onExit__')
				__logger__('INFO.1.11: %s' % (__sysout__.getvalue()))
				if (os.path.exists(__cmd__)):
				    os.remove(__cmd__)
    
			    wfHandle = open(__cmd__,'w')
			    print >>wfHandle, '@echo on\n'
			    print >>wfHandle, '%s\n' % (job.comment)
			    wfHandle.flush()
			    wfHandle.close()
			    ss = SmartShell(__cmd__,callback=__callback__,isDebugging=True,onExit=__onExit__,sysout=__sysout__)
			    ss.execute()
            
		if (threaded):
		    if (config.verbose):
			__logger__('INFO.1.12: Sleeping for %s secs...' % (config.resolution))
		    time.sleep(config.resolution if (isinstance(config.resolution,float) or isinstance(config.resolution,int)) else 60)
		    
		    if (callable(jsonHandler)):
			try:
			    __config__ = jsonHandler(config.jsonFpath)
			except Exception, ex:
			    __config__ = SmartObject()
		    __file__ = config.schedulefpath if (misc.isStringValid(config.schedulefpath)) else None
		    if (os.path.exists(__file__)):
			if (config.verbose):
			    __logger__('INFO.1.13: Crontab Exists: "%s".' % (__file__))
			__lines__ = _utils._readFileFrom(__file__)
			if (config.verbose):
			    __logger__('INFO.1.14: Crontab Content: "%s".' % (__lines__))
	else:
	    __logger__('WARNING.1.15: Cannot execute crontab unless threaded is %s (true).' % (threaded))
        return config.isRunning
            
    __logger__('INFO.1: threaded="%s".' % (threaded))
    if (threaded):
        @threadpool.threadify(__Q__)
        def threaded_crontab(config,jsonHandler=jsonHandler,callback=callback,logging_callback=logging_callback,default=default):
            return __crontab__(config,jsonHandler=jsonHandler,callback=callback,logging_callback=logging_callback,default=default)
        threaded_crontab(config,jsonHandler=jsonHandler,callback=callback,logging_callback=logging_callback,default=default)
	__logger__('INFO.2: isRunning="%s".' % (config.isRunning))
        if (not config.isRunning):
            if (config.verbose):
                if (callable(logging_callback)):
                    try:
                        logging_callback('INFO: Cannot run due to application defined criteria expressed via the callback.')
                    except:
                        pass
	    __logger__('INFO.3: TERMINATING !!!')
            pid = os.getpid()
            os.kill(pid,signal.SIGTERM)
    else:
	__logger__('INFO.3: threaded="%s".' % (threaded))
        __crontab__(config,jsonHandler=jsonHandler,callback=callback,logging_callback=logging_callback,default=default)
        
if (__name__ == '__main__'):
    import time
    __crontab__ = '''
# Minute   Hour   Day of Month       Month          Day of Week        Command    
# (0-59)  (0-23)     (1-31)    (1-12 or Jan-Dec)  (0-6 or Sun-Sat)                
    */5        *          *             *               *             dir  # comment this  
    '''
    __file__ = r'C:\@2\crontab'
    crontab(__file__,dry_run=True,threaded=True,verbose=True)
        
    s_begin = time.time()
    while ((time.time() - s_begin) < 900.0):
        print '(+++)'
        time.sleep(10)