'''
Julian day routines from Meeus, "Astronomical Formulae for Calculators".
The routines are:

    Julian(month, day, year)            Integer Julian day number
    JulianAstro(month, day, year)       Astronomical Julian day number
    JulianToMonthDayYear(julian_day)    Returns month, day, year tuple
    DayOfWeek(month, day, year)         0 = Sunday
    DayOfYear(month, day, year)         1 to 365 (366 in leap year)
    IsValidDate(month, day, year)       Returns true if date is valid Gregorian
    IsLeapYear(year)                    Returns true if year is leap year
    NumDaysInMonth(month, year)

The JulianAstro function returns the astronomical form and is returned
as a floating point number.  The astronomical Julian day begins at
Greenwich mean noon.  The Julian() function returns the more usual
Julian day as an integer; it is gotten from the astronomical form by
adding 0.55 and taking the integer part.

Warning:  In general, the functions do _not_ check their incoming parameters.

Don Peterson 30 May 1998

Copyright (C) 2002 GDS Software

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the Free
Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
MA  02111-1307  USA

See http://www.gnu.org/licenses/licenses.html for more details.
'''

__version__ = "$Id: julian.py,v 1.3 2002/08/21 12:41:48 donp Exp $"

def NumDaysInMonth(month, year):
    if month == 2:
        if IsLeapYear(year):
            return 29
        else:
            return 28
    elif month == 9 or month == 4 or month == 6 or month == 11:
        return 30
    elif month == 1 or month == 3 or month == 5 or month == 7 or          month == 8 or month == 10 or month == 12:
        return 31
    else:
        raise "Bad month"

def JulianToMonthDayYear(julian_day):
    if julian_day < 0:  raise "Bad input value"
    jd = julian_day + 0.5
    Z = int(jd)
    F = jd - Z
    A = Z
    if Z >= 2299161:
        alpha = int((Z - 1867216.26)/36254.25)
        A = Z + 1 + alpha - int(alpha/4)
    B = A + 1524
    C = int((B - 122.1)/365.25)
    D = int(365.25 * C)
    E = int((B - D)/30.6001)
    day = B - D - int(30.6001 * E) + F
    if E < 13.5:
        month = int(E - 1)
    else:
        month = int(E - 13)
    if month > 2.5:
        year = int(C - 4716)
    else:
        year = int(C - 4715)
    return month, day, year

def DayOfYear(month, day, year):
    if IsLeapYear(year):
        n = int((275*month)/9 -   ((month + 9)/12) + int(day) - 30)
    else:
        n = int((275*month)/9 - 2*((month + 9)/12) + int(day) - 30)
    if n < 1 or n > 366:  raise "Internal error"
    return n

def DayOfWeek(month, day, year):
    julian = int(JulianAstro(month, int(day), year) + 1.5)
    return julian % 7

def IsLeapYear(year):
    if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
        return 1
    else:
        return 0

def IsValidDate(month, day, year):
    '''Returns true if the year is later than 1752 and the month and day
    numbers are valid.
    '''
    if month < 1 or month > 12: return 0
    if int(month) != month    : return 0
    if year < 1753            : return 0
    if day  < 1.0             : return 0
    if int(day) != day:
        if month == 2:
            if IsLeapYear(year):
                if day >= 30.0: return 0
            else:
                if day >= 29.0: return 0
        elif month == 9 or month == 4 or month == 6 or month == 11:
            if day >= 31.0    : return 0
        else:
            if day >= 32.0    : return 0
    else:
        if month == 2:
            if IsLeapYear(year):
                if day >= 29  : return 0
            else:
                if day >= 28  : return 0
        elif month == 9 or month == 4 or month == 6 or month == 11:
            if day >= 30      : return 0
        else:
            if day >= 31      : return 0
    return 1

def JulianAstro(month, day, year):
    "Note that day can be either an integer or a float."
    if month < 3:
        year  = year - 1
        month = month + 12
    julian = int(365.25*year) + int(30.6001*(month+1)) + day + 1720994.5
    tmp = year + month / 100.0 + day / 10000.0
    if tmp >= 1582.1015:
        A = year / 100
        B = 2 - A + A/4
        julian = julian + B
    return julian * 1.0

def Julian(month, day, year):
    return int(JulianAstro(month, day, year) + 0.55)
        
def Test():
    if Julian(12, 31, 1989)        != 2447892   :  raise "TestError"
    if Julian(1, 1, 1990)          != 2447893   :  raise "TestError"
    if Julian(7, 4, 1776)          != 2369916   :  raise "TestError"
    if Julian(2, 29, 2000)         != 2451604   :  raise "TestError"
    if JulianAstro(1, 27.5, 333)   != 1842713.0 :  raise "TestError"
    if JulianAstro(10, 4.81, 1957) != 2436116.31:  raise "TestError"
    if DayOfWeek(11, 13, 1949)     != 0         :  raise "TestError"
    if DayOfWeek( 5, 30, 1998)     != 6         :  raise "TestError"
    if DayOfWeek( 6, 30, 1954)     != 3         :  raise "TestError"
    if DayOfYear(11, 14, 1978)     != 318       :  raise "TestError"
    if DayOfYear( 4, 22, 1980)     != 113       :  raise "TestError"

    month, day, year = JulianToMonthDayYear(2436116.31)
    if month != 10   : raise "TestError"
    if year  != 1957 : raise "TestError"
    if abs(day - 4.81) > .00001 : raise "TestError"
    month, day, year = JulianToMonthDayYear(1842713.0)
    if month != 1    : raise "TestError"
    if year  != 333  : raise "TestError"
    if abs(day - 27.5) > .00001 : raise "TestError"
    month, day, year = JulianToMonthDayYear(1507900.13)
    if month != 5    : raise "TestError"
    if year  != -584 : raise "TestError"
    if abs(day - 28.63) > .00001 : raise "TestError"

    if NumDaysInMonth( 1, 1999) != 31 :  raise "TestError"
    if NumDaysInMonth( 2, 1999) != 28 :  raise "TestError"
    if NumDaysInMonth( 3, 1999) != 31 :  raise "TestError"
    if NumDaysInMonth( 4, 1999) != 30 :  raise "TestError"
    if NumDaysInMonth( 5, 1999) != 31 :  raise "TestError"
    if NumDaysInMonth( 6, 1999) != 30 :  raise "TestError"
    if NumDaysInMonth( 7, 1999) != 31 :  raise "TestError"
    if NumDaysInMonth( 8, 1999) != 31 :  raise "TestError"
    if NumDaysInMonth( 9, 1999) != 30 :  raise "TestError"
    if NumDaysInMonth(10, 1999) != 31 :  raise "TestError"
    if NumDaysInMonth(11, 1999) != 30 :  raise "TestError"
    if NumDaysInMonth(12, 1999) != 31 :  raise "TestError"

    if NumDaysInMonth( 1, 2000) != 31 :  raise "TestError"
    if NumDaysInMonth( 2, 2000) != 29 :  raise "TestError"
    if NumDaysInMonth( 3, 2000) != 31 :  raise "TestError"
    if NumDaysInMonth( 4, 2000) != 30 :  raise "TestError"
    if NumDaysInMonth( 5, 2000) != 31 :  raise "TestError"
    if NumDaysInMonth( 6, 2000) != 30 :  raise "TestError"
    if NumDaysInMonth( 7, 2000) != 31 :  raise "TestError"
    if NumDaysInMonth( 8, 2000) != 31 :  raise "TestError"
    if NumDaysInMonth( 9, 2000) != 30 :  raise "TestError"
    if NumDaysInMonth(10, 2000) != 31 :  raise "TestError"
    if NumDaysInMonth(11, 2000) != 30 :  raise "TestError"
    if NumDaysInMonth(12, 2000) != 31 :  raise "TestError"

if __name__ == "__main__":
    Test()
