'''
This utility prints calendars out similar to the regular UNIX cal 
program.  However, I wanted to customize it to my needs:

    cal.py [year]

With no argument, the program will print a three month calendar 
across, similar to the three months printed when the UNIX cal program
prints the 12 months for a specified year.  The intent is to print
the current month and the following two months, spilling over to the
next year's months if necessary.

In both cases, the current date and time are printed before the 
calendar is printed.

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

import calendar, string, time, sys

cal_len = 9
calendar.setfirstweekday(calendar.SUNDAY)

def GetMonth(month, year):
    '''Return a list of the 8 strings representing the weeks of the
    specified month.
    '''
    if month > 12:
        month = month % 12
        year  = year + 1
    cal = string.split(calendar.month(year, month), "\n")
    for ix in xrange(len(cal)):
        if len(cal[ix]) < 20:
            cal[ix] = cal[ix] + " " * (20 - len(cal[ix]))
        assert(len(cal[ix]) == 20)
    while len(cal) < cal_len:
        cal.append("")
    assert(len(cal) == cal_len)
    return cal

def GetMonthAndYear():
    '''Return current (month, year).  If an integer is given on the
    command line, add it to the months to get the start month in the
    future.
    '''
    t = time.localtime()
    year  = t[0]
    month = t[1]
    if len(sys.argv) > 1:
        month_offset = int(sys.argv[1])
        yr, mo = divmod(month_offset, 12)
        year = year + yr
        month = month + mo
    return month, year

def main():
    month, year = GetMonthAndYear()
    cal1 = GetMonth(month  , year)
    cal2 = GetMonth(month+1, year)
    cal3 = GetMonth(month+2, year)
    sep = " " * 5
    print
    print time.asctime(time.localtime(time.time())), "\n"
    for ix in xrange(len(cal1)):
        print cal1[ix] + sep + cal2[ix] + sep + cal3[ix]

main()
