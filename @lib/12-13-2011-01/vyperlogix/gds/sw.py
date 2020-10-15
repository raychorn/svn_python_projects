'''
Python script to provide stopwatch like behavior.  It is specific to 
the 32 bit Windows environment.

Instructions for use:
    1.  Start the program
    2.  When you press a key, the split time, total elapsed time,
        time/date and key pressed are printed on a line.

Special keys are:

    q        Quit
    Z        Rezero the timer
    C        Get prompted for a comment

If a file is included on the command line, the data are also logged to
that file.

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

import msvcrt, time, string, sys

done       = 0
start      = time.time()
last_time  = start
num_spaces = 10
fmt        = "%%%d.1f %%%d.1f     %%s   %%s" % (num_spaces, num_spaces)
log_stream = None

# The Keys dictionary is used to decode special keystrokes
Keys = {
    ";"  :  "F1",
    "<"  :  "F2",
    "="  :  "F3",
    ">"  :  "F4",
    "?"  :  "F5",
    "@"  :  "F6",
    "A"  :  "F7",
    "B"  :  "F8",
    "C"  :  "F9",
    "D"  :  "F10",
    "E"  :  "F11",
    "F"  :  "F12",
}

#-----------------------------------------------------------------------------

def Usage():    
    print '''Commands:
  q       Quit
  Z       Zero time
  C       Enter a comment

Any other keys take a split.  Start with a filename on the command
line to also have the data appended to that file.  A state summary
report will be written to the file.
'''

def Header():
    return '''Times are in seconds

 Diff time Total time
 --------- ----------'''

def Log(str, quiet=0):
    if not quiet:
        print str
    if log_stream:
        log_stream.write(str + "\n")

def Print(key):
    global last_time
    t = time.time()
    # Get current time string
    loc = time.localtime(t)
    str = time.asctime(loc)
    Log(fmt % ((t-last_time), (t-start), str, key))
    last_time = t

def GetKey():
    '''Return a string that represents the key pressed.  If the first
    getch() returns a '\000' character, then we call getch() again to
    get the second character and then perform a lookup in the Keys
    dictionary to get the string which represents the key pressed.
    '''
    key = msvcrt.getch()
    if key == '\003':  # Always exit on a ctrl-C
        sys.exit(0)
    if key == '\000':
        key = msvcrt.getch()
        key = "+" + key
    return key

def main():
    global start, last_time, log_stream
    Usage()
    if len(sys.argv) > 1:
        log_stream = open(sys.argv[1], "w")
    Log(Header())
    while 1:
        while not msvcrt.kbhit():
            pass
        key = GetKey()
        if key == "q":
            Print("Quitting")
            if log_stream:
                log_stream.close()
            sys.exit(0)
        elif key == "Z":
            start = time.time()
            last_time = start
            Log("Time reset")
        elif key == "C":
            # Prompt the user for a string
            str = raw_input("Enter comment string, '.<cr>' to finish:\n")
            while str != ".":
                Log("+ " + str)
                str = raw_input("")
        else:
            Print(key)

if __name__ == "__main__":
    main()
