'''
Script to print moon phase times for a given year, which should be the
single parameter passed on the command line.  The times will be converted
to your local time by the ut_offset value, which gets added to the 
calculated universal time for the phase.  You'll want to modify the
ConvertToLocalTime() function to make its output appropriate for your
location.  You can also make it do nothing, which results in the 
program printing its times in UT.

Converted to python from moon.c program from June 1995.  Algorithms
from Meeus, Astronomical Formulas for Calculators, 2nd ed., 1982.

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

#########################################################################

from math import pi, sin, cos, floor
import sys
import pdb
xx = pdb.set_trace

NEW   = 0
FIRST = 1
FULL  = 2
LAST  = 3
RAD   = pi/180.0    # Converts degrees to radians
desired_year = 0

# GetJulianFromPhase  Derive the julian day number corresponding to the 
# number k.  k is the integer corresponding to new moon and phase is 0 
# for new, 1 for first quarter, 2 for full, and 3 for last quarter.
# Returns a float.  From Meeus, pg 159.

def GetJulianFromPhase(k, phase):
    if phase != NEW and phase != FIRST and phase != FULL and phase != LAST:
        raise "Illegal phase value"
    k1 = k + phase/4.0
    T = k1/1236.85
    T2 = T*T
    T3 = T2*T
    # Get time of mean phase
    julian = 2415020.75933 + 29.53058868*k1 + 1.178e-4*T2 - 1.55e-7*T3              +3.3e-4*sin(RAD*(166.56 + 132.87*T - 0.009173*T2))
    # Compute the corrections to get the time of true phase
    M      = 359.2242 + 29.10535608*k - 3.33e-5*T2 - 3.47e-6*T3
    Mprime = 306.0253 + 385.81691806*k + 0.0107306*T2 + 1.236e-5*T3
    F      = 21.2964 + 390.67050646*k - 1.6528e-3*T2 - 2.39e-6*T3
    # Adjust these values to the interval [0, 360] 
    M      = M - 360.0*(floor(M/360.0))
    Mprime = Mprime - 360.0*(floor(Mprime/360.0))
    F      = F - 360.0*(floor(F/360.0))
    # Convert them to radians
    M      = M*RAD
    Mprime = Mprime*RAD
    F      = F*RAD
    # Perform the corrections
    if phase == NEW or phase == FULL:
        correction = (0.1734 - 3.93e-4*T)*sin(M)                  + 0.0021*sin(2*M)                  - 0.4068*sin(Mprime)                  + 0.0161*sin(2*Mprime)                  - 0.0004*sin(3*Mprime)                  + 0.0104*sin(2*F)                  - 0.0051*sin(M+Mprime)                  - 0.0074*sin(M-Mprime)                  + 0.0004*sin(2*F+M)                  - 0.0004*sin(2*F-M)                  - 0.0006*sin(2*F+Mprime)                  + 0.0010*sin(2*F-Mprime)                  + 0.0005*sin(M+2*Mprime)
    else:
        correction = (0.1721 - 0.0004*T)*sin(M)                  + 0.0021*sin(2*M)                  - 0.6280*sin(Mprime)                  + 0.0089*sin(2*Mprime)                  - 0.0004*sin(3*Mprime)                  + 0.0079*sin(2*F)                  - 0.0119*sin(M+Mprime)                  - 0.0047*sin(M-Mprime)                  + 0.0003*sin(2*F+M)                  - 0.0004*sin(2*F-M)                  - 0.0006*sin(2*F+Mprime)                  + 0.0021*sin(2*F-Mprime)                  + 0.0003*sin(M+2*Mprime)                  + 0.0004*sin(M-2*Mprime)                  - 0.0003*sin(2*M+Mprime)
    julian = julian + correction
    if phase == FIRST:
        julian = julian + 0.0028 - 0.0004*cos(M) + 0.0003*cos(Mprime)
    if phase == LAST:
        julian = julian + -0.0028 + 0.0004*cos(M) - 0.0003*cos(Mprime)
    return julian

# Returns a structure that contains the calendar date associated 
# with a julian day.  The tuple is (year, month, day) where year
# and month are integers; day is a float.  The julian parameter
# is expected to be a float.  Ref. Meeus pg 26.

def caldate(julian):
    julian = julian + 0.5
    Z = int(julian)
    F = julian - Z
    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z-1867216.25)/36524.25)
        A = Z + 1 + alpha - int(alpha/4)
    B = A + 1524
    C = int((B - 122.1)/365.25)
    D = int(365.25*C)
    E = int((B - D)/30.6001)
    day = B - D - int(30.6001*E) + F
    if E < 13.5:
        month = int(E - 1)
    else:
        month = int(E - 13)
    if month > 2.5:
      year =  int(C - 4716)
    else:
      year =  int(C - 4715)
    return (year, month, day)

# UnivTimeCorrect  Ref. Meeus pg 35.  Calculates the correction to ephemeris
# time to get universal time.  The correction is gotten purely by his 
# approximate formula; the error is a maximum of 1.2 minutes between 1710
# and 1987.  

def UnivTimeCorrect(year):
  T = (year - 1900.0)/100.0
  return (0.41 + 1.2053*T + 0.4992*T*T)/60.0

def GetPhaseData(desired_year, phase):
    # Return a list of the julian days for the given year of each phase.
    # Start by getting a k that is in the middle of the previous year
    if desired_year < 1900:
        raise "Desired year should be > 1900"
    k1 = (desired_year - .5 - 1900) * 12.3685
    k = int(k1)
    done = 0
    data = []
    while not done:
        julian = GetJulianFromPhase(k, phase)
        year, month, day = caldate(julian)
        if year == desired_year:
            data.append([julian, phase])
        if year > desired_year:
            done = 1
        k = k + 1
    return data

def PrintItem(julian):
    month_name = ["", "Jan", "Feb", "Mar", "Apr", "May",
           "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    year, month, day = caldate(julian)
    Day = int(day)
    fraction = day - Day
    hours = 24.0*fraction
    decimal_time = hours + 12.0 + UnivTimeCorrect(year)
    if decimal_time > 24.0:
        day = day + 1
        decimal_time = decimal_time - 24.0
    minutes = int((decimal_time - int(decimal_time))*60)
    print "  %02d %s %02d:%02d " %         (Day, month_name[month], int(decimal_time), minutes)

def main():
    desired_year = 2002
    if len(sys.argv) > 1:
        desired_year = int(sys.argv[1])
    # Get a list of the phase times in julian days.  Each element of the
    # list is another list containing the julian day and the phase number.
    results = []
    data = GetPhaseData(desired_year, NEW)
    results = results + data
    data = GetPhaseData(desired_year, FIRST)
    results = results + data
    data = GetPhaseData(desired_year, FULL)
    results = results + data
    data = GetPhaseData(desired_year, LAST)
    results = results + data
    # Print header
    print "Moon phases for", desired_year
    # Convert to a dictionary keyed by the phase
    dict = {}
    for result in results:
        julian = result[0]
        phase  = result[1]
        if dict.has_key(phase):
            dict[phase].append(julian)
        else:
            dict[phase] = [julian]
    phases = ["New", "First", "Full", "Last"]
    for phase in range(4):
        print phases[phase]
        for date in dict[phase]:
            PrintItem(date)
            

main()
