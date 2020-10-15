'''
ping a location every once in a while to keep an Internet connection 
open.  Pass the time in hours you want it to stay connected in on 
the command line; defaults to 1 hour.

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

import os, time, sys, string
__version__ = "$Id: lock.py,v 1.3 2002/08/21 12:41:48 donp Exp $"

# Global variables
site = "www.hcfa.gov"
ping = "c:/winnt/system32/ping"
cmd = ping + " " + site + " " + ">nul 2>&1"
bad_count = 0

def ConvertHours(numstr):
    numstr = string.replace(numstr, "h", "")
    return int(float(numstr) * 3600)

def ConvertMinutes(numstr):
    numstr = string.replace(numstr, "m", "")
    return int(float(numstr) * 60)

def ConvertDays(numstr):
    numstr = string.replace(numstr, "d", "")
    return int(float(numstr) * 3600 * 24)

def Initialize():
    time_in_sec = 3600     # Default is 1 hour
    if len(sys.argv) >= 2:
        numstr = sys.argv[1]
        if string.find(numstr, "h") != -1:
            time_in_sec = ConvertHours(numstr)
            print "Locking for %.1f hours" % (time_in_sec/3600.)
        elif string.find(numstr, "m") != -1:
            time_in_sec = ConvertMinutes(numstr)
            print "Locking for %.1f minutes" % (time_in_sec/60.)
        elif string.find(numstr, "d") != -1:
            time_in_sec = ConvertDays(numstr)
            print "Locking for %.2f days" % (time_in_sec/(3600.*24))
        else:
            time_in_sec = ConvertHours(numstr + "h")
            print "Locking for %.1f hours" % (time_in_sec/3600.)
    else:
        time_in_sec = 3600
        print "Locking for %.1f hours" % (time_in_sec/3600.)
    # Perform an initial ping after the typical connect time in case this
    # forces a modem to connect.
    for ix in xrange(10):
        time.sleep(1)
    if os.system(cmd) != 0:
        print "'cmd' failed. Apparently not connected."
        sys.exit(1)
    return time_in_sec


def PrintTimeLeft(seconds_left):
    days = seconds_left/(3600.*24)
    hours = seconds_left/(3600.)
    minutes = seconds_left/(60.)
    if days >= 1.0:
        print "%.1f days left (%.1f minutes)" % (days, minutes)
    elif hours > 1.0:
        print "%.1f hours left (%.1f minutes)" % (hours, minutes)
    else:
        if minutes > 0.0:
            print "%.1f minutes left" % minutes

def main():
    sleep_time = 60  # How many seconds to sleep between pings
    time_in_sec = Initialize()
    start = time.time()
    while time.time() - start < time_in_sec:
        startloop = time.time()
        while time.time() - startloop < sleep_time:
            # Loop on short delays to avoid waiting a long time for Ctrl-C to
            # take effect.
            time.sleep(1)
        if os.system(cmd) != 0:
            bad_count = bad_count + 1
            if bad_count > 5:
                print "More than 5 pings returned nonzero status"
                sys.exit(0)

        seconds_left = time_in_sec - (time.time() - start)
        PrintTimeLeft(seconds_left)

main()
