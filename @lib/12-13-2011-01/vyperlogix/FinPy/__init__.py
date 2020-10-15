#!/usr/bin/env python

__author__ = 'Ramesh Balasubramanian <ramesh@finpy.org>'
__version__ = "$Revision: 1.17 $"
__credits__ = 'functions in the datetools interface have a high degree of Matlab(TM) compatibility'

import datetime
import time
import math
import sys
import calendar
calendar.setfirstweekday(6)

if sys.version.find('.NET') != -1:
	__weekday = ((1, 'Sun'),(2, 'Mon'), (3, 'Tue'), (4, 'Wed'), (5, 'Thu'), (6, 'Fri'), (7, 'Sat'))
else:
	__weekday = ((2, 'Mon'), (3, 'Tue'), (4, 'Wed'), (5, 'Thu'), (6, 'Fri'), (7, 'Sat'), (1, 'Sun'))

def __fromordinal(gdays):
	if sys.version.find('.NET') != -1:
		import System
		add_days = gdays - datetime.date.today().toordinal()
		dt = System.DateTime.Today
		ret_dt = dt.AddDays(add_days)
		return datetime.datetime(ret_dt.Year, ret_dt.Month, ret_dt.Day, 0, 0, 0)
	else:
		return datetime.date.fromordinal(int(gdays))


__days = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
__leapDays = (0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
__dateFormat = ('%d-%b-%Y %H:%M:%S', \
				'%d-%b-%Y', \
				'%m/%d/%y', \
				'%b', \
				'', \
				'%m', \
				'%m/%d', \
				'%d', \
				'%a', \
				'', \
				'%Y', \
				'%y', \
				'%b%y', \
				'%H:%M:%S', \
				'%I:%M:%S %p', \
				'%H:%M', \
				'%I:%M %p', \
				'', \
				'', \
				'%d/%m', \
				'%d/%m/%y', \
				'%b.%d.%Y %H:%M:%S', \
				'%b.%d.%Y', \
				'%m/%d/%Y', \
				'%d/%m/%Y', \
				'%y/%m/%d', \
				'%Y/%m/%d', \
				'', \
				'%b%Y', \
				'%d-%b-%Y %H:%M')


def now():
	"""
	-------------------------------------------------------------------------------	
	Usage
	
	Notes
		now  returns the system date and time as a serial date number.

	Examples
		In [1]: import datetools
		
		In [2]: now = datetools.now()
		
		In [3]: print now
		733042.99
	-------------------------------------------------------------------------------
	"""
	(hour, minute, second) = datetime.datetime.now().timetuple()[3:6]
	
	return 366 + \
			datetime.date.today().toordinal() + \
			(((hour * 3600) + \
			(minute * 60) + \
			second)/86400.0)

def today():
	"""
	-------------------------------------------------------------------------------	
	Usage
	
	Notes
		today  returns the current date as a serial date number.

	Examples
		In [1]: import datetools
		
		In [2]: today = datetools.today()
		
		In [3]: print today
		733042
	-------------------------------------------------------------------------------
	"""
	return 366 + datetime.date.today().toordinal()

def datenum(p, *args):
	"""
	-------------------------------------------------------------------------------	
	Usage
		dateNumber = datenum(dateString)
		dateNumber = datenum(year, month, day, hour = 0, minute = 0, second = 0)
		
	Notes
		dateNumber = datenum(dateString) returns a serial date number given a 
		dateString.
		
		A dateString can take any one of the following formats
		'19-may-1999'
		'may 19, 1999'
		'19-may-99'
		'19-may' (current year assumed)
		'5/19/99'
		'5/19' (current year assumed)
		'19-may-1999, 18:37'
		'19-may-1999, 6:37 pm'
		'5/19/99/18:37'
		'5/19/99/6:37 pm'
		
		Date numbers are the number of days that has passed since a base date. 
		
		To match the MATLAB function with the same name, date number 1 is 
		January 1, 0000 A.D. If the input includes time components, the date number
		includes a fractional component.
				
		dateNumber = datenum(year, month, day, hour, minute, second) 
		returns a serial date number given year, month, day, hour, minute, and 
		second integers. hour, minute, second are optional (default to 0)
	
	Not Implemented
		Date strings with two-character years, e.g., 12-jun-12, are assumed to lie
		within the 100-year period centered about the current year.
		
	Examples
		In [1]: import datetools

		In [2]: datetools.datenum('19-may-1999')
		Out[2]: 730259.0

		In [3]: datetools.datenum('5/19/99')
		Out[3]: 730259.0

		In [4]: datetools.datenum('19-may-1999, 6:37 pm')
		Out[4]: 730259.78000000003

		In [5]: datetools.datenum('5/19/99/18:37')
		Out[5]: 730259.78000000003

		In [6]: datetools.datenum(1999,5,19)
		Out[6]: 730259.0

		In [7]: datetools.datenum(1999,5,19,18,37,0)
		Out[7]: 730259.78000000003

		In [8]: datetools.datenum(730259)
		Out[8]: 730259

	Known Bug(s)
		1. does not handle 0 to 693962
		2. does not handle 01-01-0000 to 12-31-0000
	-------------------------------------------------------------------------------		
	"""
	if len(args) == 0:
		if type(p) == str:
			return __string2num(p)
		elif type(p) == int or type(p) == float:
			try:
				datenum(datestr(p,29))
				return round(p, 4) 
			except ValueError:
				raise Exception("Invalid datenum. must be >= 693962")
		raise Exception("When invoked with 1 argument, datenum expects a string, int or float")
	elif len(args) <= 5:
		return __dateints2num(p, *args)
	else:
		raise Exception("datenum accepts 1, 3, 4, 5 or 6 arguments only")



def datestr(dateNumber, dateForm = -1):
	"""
	-------------------------------------------------------------------------------
	Usage
		dateString = datestr(dateNumber, dateForm)
		dateString = datestr(dateNumber)

	Notes
		dateString = datestr(dateNumber, dateForm) converts a date number or a date 
		string to a date string. DateForm specifies the format of DateString. 

		dateString = datestr(dateNumber) assumes dateForm is 1, 16, or 0 depending 
		on whether the date number contains a date, time, or both, respectively. 
		If date is a date string, the function assumes dateForm is 1.

		DateForm Format                 Example
		0        'dd-mmm-yyyy HH:MM:SS' 01-Mar-2000 15:45:17
		1        'dd-mmm-yyyy'          01-Mar-2000
		2        'mm/dd/yy'             03/01/00
		3        'mmm'                  Mar
		4        'm'                    M
		5        'mm'                   03
		6        'mm/dd'                03/01
		7        'dd'                   01
		8        'ddd'                  Wed
		9        'd'                    W
		10       'yyyy'                 2000
		11       'yy'                   00
		12       'mmmyy'                Mar00
		13       'HH:MM:SS'             15:45:17
		14       'HH:MM:SS PM'          3:45:17 PM
		15       'HH:MM'                15:45
		16       'HH:MM PM'             3:45 PM
		17       'QQ-YY'                Q1 01
		18       'QQ'                   Q1
		19       'dd/mm'                01/03
		20       'dd/mm/yy'             01/03/00
		21       'mmm.dd.yyyy HH:MM:SS' Mar.01,2000 15:45:17
		22       'mmm.dd.yyyy'          Mar.01.2000
		23       'mm/dd/yyyy'           03/01/2000
		24       'dd/mm/yyyy'           01/03/2000
		25       'yy/mm/dd'             00/03/01
		26       'yyyy/mm/dd'           2000/03/01
		27       'QQ-YYYY'              Q1-2001
		28       'mmmyyyy'              Mar2000
		29       'dd-mmm-yyyy HH:MM'    01-Mar-2000 15:45

	Examples
		In [1]: import datetools
	
		In [2]: datetools.datestr(730123, 1)
		Out[2]: '03-Jan-1999'
	
		In [3]: datetools.datestr(730123, 2)
		Out[3]: '01/03/99'
	
		In [4]: datetools.datestr(730123.776, 0)
		Out[4]: '03-Jan-1999 18:37:26'
	
		In [5]: datetools.datestr(730123)
		Out[5]: '03-Jan-1999'
		
		In [6]: datetools.datestr(730123.776)
		Out[6]: '03-Jan-1999 18:37:26'
		
		In [7]: datetools.datestr(730123)
		Out[7]: '03-Jan-1999'
		
		In [8]: datetools.datestr(.776)
		Out[8]: '06:37 PM'

	Known Bug(s)
		1. does not handle datenums 0 to 693961
	-------------------------------------------------------------------------------
	"""
	if dateForm == -1:
		# dateForm should be 0, 1 or 16 depending on datenum
		if __isFloat(dateNumber):
			if math.floor(dateNumber) == 0:
				# only time
				dateForm = 16
				timeObject = datetime.time(*__timeTuple(dateNumber))
				return timeObject.strftime(__dateFormat[dateForm])
			else:
				dateForm = 0
				dateTimeObject = __dateTime(dateNumber)
				return dateTimeObject.strftime(__dateFormat[dateForm])			
		elif __isInteger(dateNumber):
			datePart = __fromordinal(dateNumber-366)
			dateForm = 1 
			return datePart.strftime(__dateFormat[dateForm])
	else:
		dateTimeObject = __dateTime(dateNumber)
		if __dateFormat[dateForm] == '':
			raise NotImplementedError('dateForm ' + repr(dateForm))
		return dateTimeObject.strftime(__dateFormat[dateForm])


def datevec(date):
	"""
	-------------------------------------------------------------------------------
	Usage
		dateTuple = datevec(date)
		(year, month, day, hour, minute, second) = datevec(date)
		
	Notes
		dateVector = datevec(date) converts a date number or a date string to a
		date tuple whose elements are [year month day hour minute second]. All 
		six elements are integers
		
		(year, month, day, hour, minute, second) = datevec(date)  converts a 
		date number or a date string to a date tuple and returns the components
		of the date tuple as individual variables.
		
	Examples
		In [1]: import datetools
		
		In [2]: datetools.datevec('28-Jul-00')
		Out[2]: (2000, 7, 28, 0, 0, 0)
		
		In [3]: datetools.datevec(730695)
		Out[3]: (2000, 7, 28, 0, 0, 0)
		
		In [4]: datetools.datevec(730695.776)
		Out[4]: (2000, 7, 28, 18, 37, 26)
		
		In [5]: (year, month, day, hour, minute, second) = datetools.datevec(730695.776)
		
		In [6]: year
		Out[6]: 2000
		
		In [7]: month
		Out[7]: 7
		
		In [8]: day
		Out[8]: 28
		
		In [9]: hour
		Out[9]: 18
		
		In [10]: minute
		Out[10]: 37
		
		In [11]: second
		Out[11]: 26
	-------------------------------------------------------------------------------
	"""
	if type(date) in [list, tuple]:
		return tuple([datevec(_date) for _date in date])
	
	if type(date) == str:
		dateTimeValue = __dateParse(date)
	elif type(date) == int or type(date) == float:
		dateTimeValue = __dateTime(date)
	else:
		raise Exception("Argument for datevec must be a datenum/datestr or a list/tuple of datenum/datestr")
		
	return dateTimeValue.timetuple()[0:6]


year = lambda date: datevec(date)[0]
year.__doc__ = \
"""
-------------------------------------------------------------------------------
Usage
	year = year(date)  
	
Notes
	returns the year of a serial date number or a date string.
	
Examples

-------------------------------------------------------------------------------
"""


month = lambda date: datevec(date)[1]
month.__doc__ = \
"""
-------------------------------------------------------------------------------
Usage
	month = month(date)  

Notes
	returns the month of a serial date number or a date string.

Examples

-------------------------------------------------------------------------------
"""


day = lambda date: datevec(date)[2]
day.__doc__ = \
"""
-------------------------------------------------------------------------------
Usage
	day = day(date)  
	
Notes
	returns the day of a serial date number or a date string.

Examples

-------------------------------------------------------------------------------
"""


hour = lambda date: datevec(date)[3]
hour.__doc__ = \
"""
-------------------------------------------------------------------------------
Usage
	hour = hour(date)  

Notes
	returns the hour of the day given a serial date number or a date string.

Examples

-------------------------------------------------------------------------------
"""


minute = lambda date: datevec(date)[4]
minute.__doc__ = \
"""
-------------------------------------------------------------------------------
Usage
	minute = minute(date)  

Notes
	returns the minute of the day given a serial date number or a date string.
	
Examples

-------------------------------------------------------------------------------
"""


second = lambda date: datevec(date)[5]
second.__doc__ = \
"""
-------------------------------------------------------------------------------
Usage
	second = second(date)  

Notes
	returns the second of the day given a serial date number or a date string.

Examples

-------------------------------------------------------------------------------
"""


def eomdate(year, month):
	"""	
	-------------------------------------------------------------------------------
	Usage
		dayMonth = eomdate(year, month)
		
	Notes
		eomdate - Last date of month
		
		dayMonth = eomdate(year, month)  returns the serial date number of the 
		last date of the month for the given year and month. Enter Year as a 
		four-digit integer; enter Month as an integer from 1 through 12.
				
		Use the function datetools.datestr to convert serial date numbers to 
		formatted date strings.
	
	Examples
	
	-------------------------------------------------------------------------------
	"""
	return datenum(year,month,eomday(year, month))


def eomday(year, month):
	"""	
	-------------------------------------------------------------------------------
	Usage
		day = eomday(year, month)
		
	Notes
		eomday - Last day of month
		
		day= eomday(year, month)  the last day of the month for the given year 
		and month. Enter Year as a four-digit integer; enter Month as an 
		integer from 1 through 12.
		
		Either input argument can contain multiple values, but if so, the other 
		input must contain the same number of values or a single value that applies 
		to all.

	Examples
		In [1]: import datetools
		
		In [2]: datetools.eomday(2000, 2)
		Out[2]: 29
		
		In [3]: datetools.eomday([2000,2001,2002,2003,2004], 2)
		Out[3]: [29, 28, 28, 28, 29]
		
		In [4]: datetools.eomday(2000,[2,7,8,12])
		Out[4]: [29, 31, 31, 31]
		
		In [5]: datetools.eomday([2000,2001,2002,2003], [2,7,8,12])
		Out[5]: [29, 31, 31, 31]

	-------------------------------------------------------------------------------
	"""
	if type(year) in [list, tuple] and type(month) in [list, tuple] and len(year) == len(month):
		return tuple([(__isLeap(_year) and __leapDays[_month]) or __days[_month] for _year, _month in zip(year,month)])
	elif type(year) in [list, tuple] and type(month) == int:
		return tuple([(__isLeap(_year) and __leapDays[month]) or __days[month] for _year in year])
	elif type(year) == int and type(month) in [list, tuple]:
		return tuple([(__isLeap(year) and __leapDays[_month]) or __days[_month] for _month in month])
	elif type(year) == int and type(month) == int:
		return (__isLeap(year) and __leapDays[month]) or __days[month]
	else:
		raise Exception("Argument Exception: Invalid type(s) or combination of type(s)")

def weekday(date):
	"""
	-------------------------------------------------------------------------------
	Usage
		(dayNum, dayString) = weekday(date)
		
	Notes
		(dayNum, dayString) = weekday(date)  returns the day of the week in 
		numeric and string form given the date as a serial date number or date
		string. The days of the week have these values.
		
		dayNum	dayString	
		1		Sun		
		2		Mon		
		3		Tue		
		4		Wed		
		5		Thu		
		6		Fri		
		7		Sat

	Examples
	-------------------------------------------------------------------------------
	"""
	return __weekday[datetime.datetime(*datevec(date)).weekday()]


def daysact(startDate, endDate = None):
	"""
	-------------------------------------------------------------------------------
	Usage
		numDays = daysact(startDate, endDate)

	Notes
		daysact   - Actual number of days between dates

		startDate - Enter as serial date numbers or date strings.

		endDate   - (Optional) Enter as serial date numbers or date strings.

		numDays = daysact(startDate, endDate)  returns the actual number of days 
		between two dates.
		numDays is negative if EndDate is earlier than StartDate.

		numDays = daysact(startDate) returns the actual number of days between the 
		MATLAB base date and startDate. In MATLAB, the base date 1 is 1-1-0000 A.D.
		See datenum for a similar function.
		
		Either input can contain multiple values, but if so, the other must contain 
		the same number of values or a single value that applies to all. For example, 
		if startDate is an n-element character array of date strings, then endDate 
		must be an n-element character array of date strings or a single date. 
		numDays is then an n-element list of numbers.

	Examples
		In [1]: import datetools
		
		In [2]: datetools.daysact('9/7/2002')
		Out[2]: 731466.0
		
		In [3]: datetools.daysact(['09/07/2002', '10/22/2002', '11/05/2002'])
		Out[3]: [731466.0, 731511.0, 731525.0]
		
		In [4]: datetools.daysact('7-sep-2002',  '25-dec-2002')
		Out[4]: 109.0
		
		In [5]: datetools.daysact(['09/07/2002', '10/22/2002', '11/05/2002'], '12/25/2002')
		Out[5]: [109.0, 64.0, 50.0]
		
		In [6]: datetools.daysact('12/25/2002', ['09/07/2002', '10/22/2002', '11/05/2002'])
		Out[6]: [-109.0, -64.0, -50.0]

	-------------------------------------------------------------------------------
	"""
	if endDate == None:
		if type(startDate) in [list, tuple]:
			return tuple([daysact(_startDate) for _startDate in startDate])
		else:
			return datenum(startDate)
	else:
		if type(startDate) in [list, tuple]:
			if type(endDate) in [list, tuple]:
				assert len(startDate) == len(endDate), "len(startDate) != len(endDate)"
				return tuple([daysact(startDate, endDate) for startDate, endDate in zip(startDate, endDate)])
			else:
				return tuple([daysact(_startDate, endDate) for _startDate in startDate])
		elif type(endDate) in [list, tuple]:
			if type(startDate) in [list, tuple]:
				assert len(startDate) == len(endDate), "len(startDate) != len(endDate)"
				return tuple([daysact(startDate, endDate) for startDate, endDate in zip(startDate, endDate)])
			else:
				return tuple([daysact(startDate, _endDate) for _endDate in endDate])
		else:
			return datenum(endDate) - datenum(startDate)


def lweekdate(weekday, year, month, nextDay=0):
	"""
	Usage
		lastDate = lweekdate(weekday, year, month, nextDay) 

	Notes
		Date of last occurrence of weekday in month

		returns the serial date number for the last occurrence of Weekday in the given 
		year and month and in a week that also contains NextDay.

		Weekday Weekday whose date you seek. Enter as an integer from 1 through 7:	

			1	Sunday

			2	Monday

			3	Tuesday

			4	Wednesday

			5	Thursday

			6	Friday

			7	Saturday

		Year	Year. Enter as a four-digit integer.

		Month	Month. Enter as an integer from 1 through 12.

	Not Implemented
		NextDay	(Optional) Weekday that must occur after Weekday in the same week. 
		Enter as an integer from 0 through 7, where 0 = ignore (default) and 1 through 7 
		are the same as for Weekday.

		Any input can contain multiple values, but if so, all other inputs must contain 
		the same number of values or a single value that applies to all.

	See Also
		Use the function datestr to convert serial date numbers to formatted date strings.

	Examples

	"""
	assert weekday in range(1,8), "weekday must be in range(1,8)"
	assert month in range(1,13), "month must be in range(1,13)"
	assert year in range(0, 10000), "year must be in range(0,10000)"
	assert nextDay in range(0,8), "weekday must be in range(0,8)"
		
	day = calendar.monthcalendar(year,month)[-1][weekday-1]
	if day == 0:
		day = calendar.monthcalendar(year,month)[-2][weekday-1]
		
	return datenum(year, month, day)
	

drange = lambda start, end:[datestr(number) for number in range(datenum(start), datenum(end))]

dateobj = lambda datenum: datetime.date(*datevec(datenum)[0:3])

# -----------------------------------------------------------------------------
# private functions
# -----------------------------------------------------------------------------
		
def __string2num(dateString):
	dateTime = __dateParse(dateString)
	return __datenum(dateTime)

def __dateints2num(year, month, day, hour = 0, minute = 0, second = 0):
	"""
	"""
	assert year >= 0
	assert month >= 1 and month <= 12
	assert day >= 1 and day <= 31
	assert hour >= 0 and hour <= 23
	assert minute >= 0 and minute <= 59
	assert second >= 0 and second <= 59

	dateTime = datetime.datetime(year=year, month=month, day=day, 
								hour=hour, minute=minute, second=second)
	return __datenum(dateTime)
	
def __datenum(dateTime):
	return round(366 + datetime.date(dateTime.year, dateTime.month, dateTime.day).toordinal() + \
		(((dateTime.hour * 3600) + (dateTime.minute * 60) + dateTime.second)/86400.0), 4)
		

def __isLeap(year):
	if year % 400 == 0 or (year % 100 != 0 and year % 4 == 0):
		return True
	else:
		return False

def __ndays(year, months, day):
	if __isLeap(year):
		if __leapDays[months] < day:
			return __leapDays[months]
		else:
			return day
	else:
		if __days[months] < day:
			return __days[months]
		else:
			return day

def __dateParse(dateString):
	try: # '19-may-1999 18:37:26'
		return datetime.datetime(*time.strptime(dateString.lower(), "%d-%b-%Y %H:%M:%S")[0:6])
	except:
		pass

	try: # '19-may-1999, 18:37:26'
		return datetime.datetime(*time.strptime(dateString.lower(), "%d-%b-%Y, %H:%M:%S")[0:6])
	except:
		pass

	try: # '19-may-1999 6:37:26 pm'
		return datetime.datetime(*time.strptime(dateString.lower(), "%d-%b-%Y %I:%M:%S %p")[0:6])
	except:
		pass

	try: # '19-may-1999, 6:37:26 pm'
		return datetime.datetime(*time.strptime(dateString.lower(), "%d-%b-%Y, %I:%M:%S %p")[0:6])
	except:
		pass

	try: # '5-19-1999 18:37:26'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m-%d-%Y %H:%M:%S")[0:6])
	except:
		pass

	try: # '5-19-1999, 18:37:26'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m-%d-%Y, %H:%M:%S")[0:6])
	except:
		pass

	try: # '5-19-1999 6:37:26 pm'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m-%d-%Y %I:%M:%S %p")[0:6])
	except:
		pass

	try: # '5-19-1999, 6:37:26 pm'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m-%d-%Y, %I:%M:%S %p")[0:6])
	except:
		pass

	try: # '5/19/99/6:37:26 pm'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m/%d/%y/%I:%M:%S %p")[0:6])
	except:
		pass

	try: # '5/19/99 18:37:26'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m/%d/%y %H:%M:%S")[0:6])
	except:
		pass

	try: # '5-19-99 6:37:26 pm'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m-%d-%y %I:%M:%S %p")[0:6])
	except:
		pass

	try: # '5-19-99 18:37:26'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m-%d-%y %H:%M:%S")[0:6])
	except:
		pass

	try: # '5-19-99, 6:37:26 pm'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m-%d-%y, %I:%M:%S %p")[0:6])
	except:
		pass

	try: # '5-19-99, 18:37:26'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m-%d-%y, %H:%M:%S")[0:6])
	except:
		pass

	try: # '19-may-1999 6:37 pm'
		return datetime.datetime(*time.strptime(dateString.lower(), "%d-%b-%Y %I:%M %p")[0:5])
	except:
		pass

	try: # '19-may-1999, 6:37 pm'
		return datetime.datetime(*time.strptime(dateString.lower(), "%d-%b-%Y, %I:%M %p")[0:5])
	except:
		pass

	try: # '19-may-1999 18:37'
		return datetime.datetime(*time.strptime(dateString.lower(), "%d-%b-%Y %H:%M")[0:5])
	except:
		pass

	try: # '19-may-1999, 18:37'
		return datetime.datetime(*time.strptime(dateString.lower(), "%d-%b-%Y, %H:%M")[0:5])
	except:
		pass

	try: # '5-19-1999 6:37 pm'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m-%d-%Y %I:%M %p")[0:5])
	except:
		pass

	try: # '5-19-1999, 6:37 pm'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m-%d-%Y, %I:%M %p")[0:5])
	except:
		pass

	try: # '5-19-1999 18:37'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m-%d-%Y %H:%M")[0:5])
	except:
		pass

	try: # '5-19-1999, 18:37'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m-%d-%Y, %H:%M")[0:5])
	except:
		pass

	try: # '5/19/99/6:37 pm'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m/%d/%y/%I:%M %p")[0:5])
	except:
		pass

	try: # '5-19-99 6:37 pm'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m-%d-%y %I:%M %p")[0:5])
	except:
		pass

	try: # '5/19/99/18:37'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m/%d/%y/%H:%M")[0:5])
	except:
		pass

	try: # '5-19-99 18:37'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m-%d-%y %H:%M")[0:5])
	except:
		pass

	try: # '5/19/99'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m/%d/%y")[0:3])
	except:
		pass

	try: # '5-19-99'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m-%d-%y")[0:3])
	except:
		pass

	try: # '5/19/1999'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m/%d/%Y")[0:3])
	except:
		pass

	try: # '5-19-1999'
		return datetime.datetime(*time.strptime(dateString.lower(), "%m-%d-%Y")[0:3])
	except:
		pass

	try: # '19-may-99'
		return datetime.datetime(*time.strptime(dateString.lower(), "%d-%b-%y")[0:3])
	except:
		pass

	try: # 'may 19, 1999'
		return datetime.datetime(*time.strptime(dateString.lower(), "%b %d, %Y")[0:3])
	except:
		pass
	
	try: # '19-may-1999'
		return datetime.datetime(*time.strptime(dateString.lower(), "%d-%b-%Y")[0:3])
	except:
		pass

	try: # '5/19' current year assumed
		temp = list(time.strptime(dateString.lower(), "%m/%d")[1:3])
		temp.insert(0, datetime.date.today().year)
		return datetime.datetime(*temp)
	except:
		pass

	try: # '19-may' cureent year assumed
		temp = list(time.strptime(dateString.lower(), "%d-%b")[1:3])
		temp.insert(0, datetime.date.today().year)
		return datetime.datetime(*temp)
	except:
		pass

	try: # '5-19' current year assumed
		temp = list(time.strptime(dateString.lower(), "%m-%d")[1:3])
		temp.insert(0, datetime.date.today().year)
		return datetime.datetime(*temp)
	except:
		pass

	try: # '19/may' cureent year assumed
		temp = list(time.strptime(dateString.lower(), "%d/%b")[1:3])
		temp.insert(0, datetime.date.today().year)
		return datetime.datetime(*temp)
	except:
		pass

	raise ValueError ('Unable to parse dateString. Format Error ' + dateString)

__isFloat = lambda n: round(n) - n != 0
__isInteger = lambda n: round(n) - n == 0
__numberSplit = lambda n: (math.floor(n), n - math.floor(n))
__timeTuple = lambda n: \
		(int(__numberSplit(__numberSplit(n)[1] * 24)[0]), \
		int(__numberSplit(__numberSplit(__numberSplit(n)[1] * 24)[1] * 60)[0]), \
		int(round(__numberSplit(__numberSplit(__numberSplit(n)[1] * 24)[1] * 60)[1] * 60)))
__dateTuple = lambda n: __fromordinal(int(math.floor(n-366))).timetuple()[0:3]
__dateTime = lambda n: datetime.datetime(*(__dateTuple(n) + __timeTuple(n)))

