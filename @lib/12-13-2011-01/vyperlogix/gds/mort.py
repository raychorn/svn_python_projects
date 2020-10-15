'''
Program that will print out a table of factors to derive a
monthly payment for a mortgage, given the interest rate in %/yr
and the length of the mortgage in years.  The user divides the
principal by 1000 and multiplies this by the table entry to get
the monthly payment.

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

import math, sys
__version__ = "$Id: mort.py,v 1.4 2002/08/21 12:41:48 donp Exp $"

interest_step  = 0.5
begin_interest = 2.0
end_interest   = 15.0

years = [3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30]

fp = sys.stdout

# Print the header information 
fp.write("Monthly payment per $1000 principal\n\n")
fp.write("                                   Years\n")
fp.write("%/yr     ")
for year in years:
    fp.write("%2d    " % year)
fp.write("\n" + "-" * 6)
fp.write("-" * 6 * len(years) + "\n")

interest = begin_interest
factor_array = []

while interest <= end_interest:
    # Calculate the current row's factors 
    factor_array = []
    for i in xrange(len(years)):
        tmp=math.pow(1+interest/1200.0, -years[i]*12.0);
        factor = 1000.0*(interest/1200.0)/(1.0-tmp);
        factor_array.append(factor)
    # Now print the factors
    fp.write("%5.2f  " % interest)
    for i in xrange(len(years)):
        fmt = "%5.2f "
        if factor_array[i] < 10.0:
            fmt = "%5.3f "
        if factor_array[i] >= 100.0:
            fmt = "%5.1f "
        fp.write(fmt % factor_array[i])
    fp.write("\n");
    interest = interest + interest_step

fp.write("\nExample:  A 10 year loan of $38000 at 8.0% per year will require\n")
fp.write("a payment of 38 * 12.13 = $461.\n\n")

fp.write("Formula:  let i = yearly interest in %\n")
fp.write("              T = time in years\n")
fp.write("              A = (1 + i/1200)^(-T*12)\n")
fp.write("Then factor = 1000 * (i/1200)/(1 - A)\n")

