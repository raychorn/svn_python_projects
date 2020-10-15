'''
Utility for extracting specified lines from a file.

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

import sys, getopt, string

no  = 0
yes = 1
debug = no

# State variables
number_lines     = no
reverse_sense    = no

def Usage():
    print '''Usage:  fcut [options] file n:m [n1:m2 ...]

Prints specified line number ranges of a file.  Line numbering is 1-based
and ranges are inclusive.

    n:m      Print lines n through m
    n:       Print from line n to end of file
     :m      Print from line 1 to line m
     :       Print all lines of the file

If n is negative, it means to count from the last line of the file 
backwards.

Options:  -n numbers the lines and -r reverses the sense of the
specification.

Examples:
    fcut file 10:-10
        Chop off the first and last 10 lines of the file.

    fcut file :10 -10:
    fcut -r file 10:-10
        Prints the first 10 and last 10 lines of the file.

    fcut -n file :
        Number all the lines of the file
'''
    sys.exit(1)

def ProcessLineSpecs(line_specs, num_lines):
    '''Return a list of pairs of integers that reflect the region of
    line numbers of the file that the user asked for.  Return line number 
    specs that are 0-based.
    '''
    specs = []
    for spec in line_specs:
        if spec == ":":
            low  = 1
            high = num_lines
        else:
            s = string.split(spec, ":")
            if len(s) == 1 or s[0] == "" or s[1] == "":
                if spec[-1] == ":":   # If it ends in ':'
                    low  = int(s[0])
                    high = num_lines
                elif spec[0] == ":":  # If it begins with ':'
                    low  = 1
                    high = int(s[1])
                else:
                    raise "Missing a ':' character"
            else:
                low  = int(s[0])
                high = int(s[1])
                if low > high:
                    low, high = (high, low)
        if low < 0:
            low = num_lines + low +1
        if high < 0:
            high = num_lines + high +1
        if low > high:
            low, high = (high, low)
        # Handle sense reversing and convert to 0-based
        if reverse_sense:
            if low != 1:
                specs.append((0, low-1))
            if high != num_lines:
                specs.append((high-1, num_lines-1))
        else:
            specs.append((low-1, high-1))
    if debug == yes:
        print "+ specs =", specs
    return specs

def MatchesSpec(line_num, specs):
    '''If the line number given (0-based) is in the range(s) specified in
    the list of ranges specs (also 0-based numbers), return yes.  Otherwise
    return no.
    '''
    if debug == yes:
            print "+ Checking line %d" % line_num
    for spec in specs:
        low  = spec[0]
        high = spec[1]
        if line_num >= low and line_num <= high:
                return yes
    return no

def main():
    global reverse_sense
    global number_lines
    if len(sys.argv) < 3:
        Usage()
    try:
        optlist, symbols = getopt.getopt(sys.argv[1:], "nr")
    except getopt.error, str:
        print str
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-n":
            number_lines = yes
        if opt[0] == "-r":
            reverse_sense = yes
    if len(symbols) < 2:
        Usage()
    file       = symbols[0]
    line_specs = symbols[1:]
    # Slurp in all the lines
    ofp = open(file)
    lines = ofp.readlines()
    ofp.close()
    specs = ProcessLineSpecs(line_specs, len(lines))
    for ix in xrange(len(lines)):
        line = lines[ix]
        if number_lines == yes:
            line = ("%d\t" % (ix+1)) + line  # Remember ix is 0-based
        if MatchesSpec(ix, specs):
            sys.stdout.write(line)

main()

