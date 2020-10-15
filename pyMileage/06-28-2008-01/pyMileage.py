from vyperlogix.hash import lists
from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint
from vyperlogix.misc import _utils
from vyperlogix.misc.safely_mkdir import *
from vyperlogix.logging import standardLogging
from vyperlogix.money import floatValue

from Job import *

import os, sys
import logging
import traceback
import datetime
from decimal import *
import random

random.seed()

_isVerbose = False
default_year = 2011
_year = default_year

_home_address = '825 Stoneridge Circle, Fairfield, CA 94534'

_mailbox = '1630 North Main Street #264, Walnut Creek, CA 94596'

_compute_round_trip = lambda miles:(floatValue.floatValue('%2.2f' % (miles * 2)) + floatValue.floatValue('%2.2f' % random.uniform(0.1, 5))).quantize(Decimal('0.1'))

_date_range_for_year = []

_data1 = {
    '2011':Job({
        'job':{'company_name': 'SmitchMicro (S&D Engineering)', 'start_date': _utils.getFromSimpleDateStr('04/29/2011'), 'end_date': _utils.getFromSimpleDateStr('10/28/2011'), 'miles':72, 'from_address':_home_address, 'to_address':'Smith Micro Software Inc, 2023 Stierlin Ct # 2, Mountain View, CA 94043'}}),
}

__company_name__ = 'Vyper Logix Corp'

data = lists.HashedLists(_data1)

_data2 = {}

_data3 = {}

_ordering = (('job_date','Date'), ('job_weekday_name','Day of Week'), ('job_company_name','Client'), ('job_from_address','Travel From'), ('job_to_address','Travel To'), ('job_miles','Trip Mileage'))
_csv_headings = lists.HashedOrderedList(_ordering)

_no_work_holidays = lists.HashedOrderedList((('new_years','01/01'), ('independence_day','07/04'), ('memorial_day','last_monday_in_may'), ('labor_day','first_monday_in_september'), ('thanksgiving_day','fourth_thursday_in_november'), ('thanksgiving_day2','day_after_thanksgiving_day'), ('christmas_day','december_25_unless_sunday_then_december_26'), ('christmas_day2','day_after_christmas_day')))

_no_mail_holidays = lists.HashedLists2({'new_years':'01/01_if_saturday', 'independence_day':'07/04_if_saturday'})

_actual_no_work_holidays = lists.HashedLists2()
_actual_no_mail_holidays = lists.HashedLists2()

_months_of_year = lists.HashedLists2()

def normalizeMiles(m):
    s = '%-10.1f' % m
    t = s.strip()
    toks = t.split('.')
    if (len(toks) == 2):
	e = int(toks[-1])
	if (e == 0):
	    e = random.uniform(0.1, 0.9)
	    toks[-1] = '%d' % (e * 10)
	    t = '.'.join(toks)
    return floatValue.floatValue(t).quantize(Decimal('0.1'))

def isDateWithinRangeForYear(dt):
    return (dt >= _date_range_for_year[0]) and (dt <= _date_range_for_year[-1])

def isDateBeforeBeginningRangeForYear(dt):
    return (dt <= _date_range_for_year[0])

def isDateAfterEndingRangeForYear(dt):
    return (dt >= _date_range_for_year[-1])

def last_DayOfWeek_for_month(dow,mm,yyyy):
    one_day = datetime.timedelta(days=1)
    dt = _utils.getFromSimpleDateStr('%02d/%02d/%04d' % (mm+1,1,yyyy)) - one_day
    while (1):
	if (_utils.getFullWeekdayName(dt) == dow):
	    return dt
	dt -= one_day
    return None

_nth_verbs = ['first','second','third','fourth','fifth']

def first_DayOfWeek_for_month(dow,mm,yyyy,nth=None):
    one_day = datetime.timedelta(days=1)
    dt = _utils.getFromSimpleDateStr('%02d/%02d/%04d' % (mm,1,yyyy))
    _skip_count = -1
    if (str(nth).isdigit()):
	_skip_count = int(nth)
    elif (nth in _nth_verbs):
	_skip_count = _nth_verbs.index(nth)
    while (1):
	if (_utils.getFullWeekdayName(dt) == dow):
	    if (_skip_count > 0):
		_skip_count -= 1
	    else:
		return dt
	dt += one_day
    return None

def initHolidaysIn(d,dest):
    if (len(dest) == 0):
	one_day = datetime.timedelta(days=1)
	for k,v in d.iteritems():
	    try:
		dt = None
		_dt = [00,00,_year]
		toks = v.split('_')
		_toks = v.split('/')
		month_name = toks[0].capitalize()
		_verb = month_name.lower()
		if (_months_of_year[month_name]):
		    _dt[0] = _months_of_year[month_name]
		    if (toks[1].isdigit()):
			_dt[1] = toks[1]
		elif (_verb in ['first','last']) or (_verb in _nth_verbs):
		    _dow_name = toks[1].capitalize()
		    month_name = toks[-1].capitalize()
		    if (_verb == 'last'):
			dt = last_DayOfWeek_for_month(_dow_name,_months_of_year[month_name],_year)
		    elif (_verb in _nth_verbs):
			dt = first_DayOfWeek_for_month(_dow_name,_months_of_year[month_name],_year,nth=_verb)
		    else:
			dt = first_DayOfWeek_for_month(_dow_name,_months_of_year[month_name],_year)
		elif (len(_toks) == 2) and (all([str(n).isdigit() and (int(n) > 0) for n in _toks])):
		    _dt[0] = int(_toks[0])
		    _dt[1] = int(_toks[1])
		    dt = _utils.getFromSimpleDateStr('%02d/%02d/%04d' % (_dt[0],_dt[1],_dt[2]))
		elif (toks[0] == 'day') and (toks[1] == 'after'):
		    dt = d['_'.join(toks[2:])]
		    if (dt):
			dt += one_day
		elif (toks[1] == 'if'):
		    _toks = toks[0].split('/')
		    if (len(_toks) == 2) and (all([str(n).isdigit() and (int(n) > 0) for n in _toks])):
			_dt[0] = int(_toks[0])
			_dt[1] = int(_toks[1])
			_dt_ = _utils.getFromSimpleDateStr('%02d/%02d/%04d' % (_dt[0],_dt[1],_dt[2]))
			if (_utils.getFullWeekdayName(_dt_).lower() == toks[-1]):
			    dt = _dt_
			else:
			    dt = None
			    _dt = []
		if (len(_dt) == 3) and (all([str(n).isdigit() and (int(n) > 0) for n in _dt])):
		    _dt = [int(n) for n in _dt]
		    dt = _utils.getFromSimpleDateStr('%02d/%02d/%04d' % (_dt[0],_dt[1],_dt[2]))
		    if (len(toks) > 2) and (toks[2] == 'unless'):
			_name_of_weekday = _utils.getFullWeekdayName(dt).capitalize()
			if (toks[3].capitalize() == _name_of_weekday):
			    if (toks[4] == 'then'):
				_month_name = toks[5].capitalize()
				if (_months_of_year[_month_name]) and (toks[6].isdigit()):
				    _dt[0] = _months_of_year[_month_name]
				    _dt[1] = int(toks[6])
				    dt = _utils.getFromSimpleDateStr('%02d/%02d/%04d' % (_dt[0],_dt[1],_dt[2]))
		dest[k] = dt
	    except:
		pass
	    pass

def isDateNoWorkHoliday(dt):
    global _actual_no_work_holidays
    if (len(_actual_no_work_holidays) == 0):
	initHolidaysIn(_no_work_holidays,_actual_no_work_holidays)
	d = _actual_no_work_holidays.asDict(insideOut=True)
	_actual_no_work_holidays += d
    return _actual_no_work_holidays[dt] != None

def isDateNoMailHoliday(dt):
    global _actual_no_mail_holidays
    if (len(_actual_no_mail_holidays) == 0):
	initHolidaysIn(_no_mail_holidays,_actual_no_mail_holidays)
	d = _actual_no_mail_holidays.asDict(insideOut=True)
	_actual_no_mail_holidays += d
    return _actual_no_mail_holidays[dt] != None

def initMonthsOfYear():
    for mm in xrange(1,13):
	dt = _utils.getFromSimpleDateStr('%02d/01/%04d' % (mm,_year))
	_months_of_year[mm] = _utils.getMonthName(dt)
	_months_of_year[_months_of_year[mm]] = mm
    pass

def performGapAnalysis(_days_of_year,_date_range,isVerbose=False,isCSV=False):
    _csv = []
    if (isCSV):
	_csv.append(['"%s"' % h for h in _csv_headings.values()])
    _zero = _miles = floatValue.floatValue('0.0')
    a_date = b_date = _date_range[0]
    _one_day = datetime.timedelta(days=1)
    max_days = (_date_range[-1] + _one_day) - b_date
    if (isVerbose):
	print '(%s) :: There are %s days in %s' % (_utils.funcName(),max_days.days,_year)
    for num in xrange(1,max_days.days+1):
	x_date = _utils.getAsSimpleDateStr(a_date)
	dt = _days_of_year[x_date]
	if (not dt):
	    _days_of_year[x_date] = Job({'job':{'date':a_date, 'weekday': _utils.getWeekday(a_date), 'weekday_name': _utils.getWeekdayName(a_date)}})
	    if (isVerbose):
		print '(%s) :: Gap date on %s' % (_utils.funcName(),x_date)
	else:
	    if (not dt.job_miles):
		if (dt.job_weekday == 6) and (not isDateNoMailHoliday(a_date)):
		    dt.job_miles = normalizeMiles(_compute_round_trip(21.5))
		    dt.job_company_name = __company_name__
		    dt.job_from_address = _home_address
		    dt.job_to_address = _mailbox
		else:
		    #dt.job_miles = normalizeMiles(Decimal('%2.1f' % random.uniform(0.1, 10)).quantize(Decimal('0.1')))
		    #dt.job_company_name = __company_name__
		    #dt.job_from_address = _home_address
		    #dt.job_to_address = 'Errands around town.'
		    pass
		pass
	    _miles += _zero if (dt.job_miles == None) else dt.job_miles
	if (isVerbose):
	    print '(%s) :: date of %s has %s' % (_utils.funcName(),x_date,dt)
	if (isCSV):
	    _csv_data = [dt[h] for h in _csv_headings.keys()]
	    _csv_data = [d if isinstance(d,str) else _utils.getAsSimpleDateStr(d) if isinstance(d,datetime.date) else str(d) if (d is not None) else '' for d in _csv_data]
	    _csv.append(['"%s"' % d for d in _csv_data])
	a_date += _one_day
    if (isVerbose):
	print '(%s) :: _miles is %-10.1f' % (_utils.funcName(),_miles.quantize(Decimal('0.1')))
    if (isCSV):
	print '\n'.join([','.join(n) for n in _csv])
	print '"Total Miles","%s"' % ('%-10.1f' % _miles.quantize(Decimal('0.1'))).strip()

def actOnDataForYear(d_list,isVerbose=False):
    _days_of_year = lists.HashedLists2()
    try:
	_one_day = datetime.timedelta(days=1)
	for d in d_list:
	    b_dt = d.job_start_date
	    e_dt = d.job_end_date
	    if (isDateWithinRangeForYear(e_dt)):
		_begin_dt = _date_range_for_year[0] if (isDateBeforeBeginningRangeForYear(b_dt)) else b_dt
		_end_dt = _date_range_for_year[-1] if (isDateAfterEndingRangeForYear(e_dt)) else e_dt
		delta = _end_dt - _begin_dt
		b_doy = _utils.getDayOfYear(_begin_dt)
		a_date = _begin_dt
		for _day in xrange(b_doy,b_doy+delta.days-1):
		    _d = Job(d.asDict())
		    _d.job_miles = normalizeMiles(_compute_round_trip(_d.job_miles))
		    _d.job_date = a_date
		    _d.job_weekday = _utils.getWeekday(a_date)
		    _d.job_weekday_name = _utils.getWeekdayName(a_date)
		    if (not _utils.isWorkWeekDay(a_date)) or (isDateNoWorkHoliday(a_date)):
			_d.job_end_date = None
			_d.job_company_name = None
			_d.job_start_date = None
			_d.job_miles = floatValue.floatValue('0.0')
			_d.job_from_address = None
			_d.job_to_address = None
		    _days_of_year[_utils.getAsSimpleDateStr(a_date)] = _d
		    if (isVerbose):
			print '\t(%s) :: %s' % (_utils.funcName(),_utils.getAsSimpleDateStr(a_date))
		    a_date += _one_day
		if (isVerbose):
		    print '(%s) :: _begin_dt=%s, _end_dt=%s' % (_utils.funcName(),_utils.getAsSimpleDateStr(_begin_dt),_utils.getAsSimpleDateStr(_end_dt))
		    print '(%s) :: \n%s' % (_utils.funcName(),str(d))
	performGapAnalysis(_days_of_year,_date_range_for_year)
	if (isVerbose):
	    print ''
	    print '='*80
	    print ''
	performGapAnalysis(_days_of_year,_date_range_for_year,isCSV=True)
    except:
	exc_info = sys.exc_info()
	info_string = '\n'.join(traceback.format_exception(*exc_info))
	logging.warning(info_string)

def main(data):
    initMonthsOfYear()
    data += _data2
    data += _data3
    actOnDataForYear(data['%d' % _year])

if (__name__ == '__main__'):
    #from vyperlogix.misc import _psyco
    #_psyco.importPsycoIfPossible('main')
    
    _version = _utils.getFloatVersionNumber()
    if (_version >= 2.5):
	def ppArgs():
	    pArgs = [(k,args[k]) for k in args.keys()]
	    pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	    pPretty.pprint()
    
	args = {'--help':'displays this help text.','--verbose':'output more stuff.','--year=?':'[2005,2006,2007,2011]'}
	_argsObj = Args.Args(args)
	if (_isVerbose):
	    print '_argsObj=(%s)' % str(_argsObj)
    
	if ( (len(sys.argv) == 1) or (sys.argv[-1] == args.keys()[0]) ):
	    ppArgs()
	else:
	    _progName = _argsObj.programName
	    _isVerbose = False
	    try:
		_isVerbose = _argsObj.booleans['isVerbose']
		_isVerbose = _isVerbose if (isinstance(_isVerbose,bool)) else False
	    except:
		_isVerbose = False
		
	    _year = default_year
	    try:
		_year = _argsObj.arguments['year']
		_year = int(_year) if (str(_year).isdigit()) else _year
		_samples = _argsObj.args['--year=?']
		if (_samples != None):
		    try:
			_samples = eval(_samples)
			_year = _year if (_year in _samples) else default_year
		    except:
			pass
	    except:
		_year = default_year
		
	    _date_range_for_year.append(_utils.getFromSimpleDateStr('01/01/%04d' % _year))
	    _date_range_for_year.append(_utils.getFromSimpleDateStr('12/31/%04d' % _year))
		
	    _cwd = ''
	    if (os.environ.has_key('cwd')):
		_cwd = os.environ['cwd']
	    elif (len(sys.argv) > 0):
		_cwd = os.path.dirname(sys.argv[0])
		
	    if (len(_cwd) == 0):
		_cwd = os.curdir
	    
	    print '_cwd=%s' % _cwd
	    
	    if (len(_cwd) > 0) and (os.path.exists(_cwd)):
		name = _utils.getProgramName()
		_log_path = safely_mkdir(_cwd)
		logFileName = os.sep.join([_log_path,'%s.log' % (name)])
		
		_logging_level = logging.WARNING if (_isVerbose == False) else logging.INFO
		
		standardLogging.standardLogging(logFileName,_level=_logging_level,isVerbose=_isVerbose)
		
		logging.info('Logging to "%s" using level of "%s".' % (logFileName,standardLogging.explainLogging(_logging_level)))
    
		main(data)
	    else:
		print >>sys.stderr, 'ERROR: Unable to determine where to put the logs based on this "%s".' % _cwd
    else:
	print >>sys.stderr, 'ERROR: This program requires Python version 2.5 or later rather than version %s.' % sys.version_info
    pass
