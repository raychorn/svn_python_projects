'''
These functions generate combinations and permutations in lexical order.

    ******************************************************
    *                                                    *
    *   WARNING:  These functions are not reentrant!     *
    *                                                    *
    ******************************************************

If you must use these functions with multiple threads, you'll have to 
develop thread-save storage for the global variables.  One way to do
this would be to change the function signatures so that you pass in a 
list of the globals needed.

The python algorithms here were implemented to return one combination or
permutation with each call to a function.  These are intended to be used
with schemes to exhaustively search all combinations or permutations of
some problem without having to generate a large list or file of the 
combinatorial data.

Two places to get C routines are:
    http://remus.rutgers.edu/~rhoads/Code/code.html
    http://sue.uvic.ca/~cos/inf/comb/CombinationsInfo.html.
        Note:  this site requires you to get each routine one at a
        time and have it sent to you via email.

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

import sys, pdb
__version__ = "$Id$"

# The following global variables are used to save the state within the
# routines so that they can be called once for each combination or 
# permutation.

# Globals for the combination routine
c_jx      = 0
c_array   = []
c_0_based = 0

# Globals for the permutation routine
p_ix      = 0
p_jx      = 0
p_array   = []
p_0_based = 0

def GetCombination(n, k, init=0, zero_based=0):
    '''Each call will return a tuple of the next combination of n items 
    taken k at a time.  The procedure for use is:

        1.  Call with init == 1.  This will return a list of the integers
            from 1 to k in their initial order.
        2.  Subsequent calls with init == 0 will return a list of k integers
            that is next in the sequence of k combinations of n items.
        3.  All the combinations have been returned when the function 
            returns None.

    If you wish the returned tuple of numbers to be zero based (which is
    handy for selecting items from python sequences), set zero_based to
    1 on the initialization call.

    This routine is adapted from a C routine given at
    http://remus.rutgers.edu/~rhoads/Code/lex_comb.c, which is a C
    implementation by Glenn C. Rhoads of an algorithm from "Combinatorial
    Algorithms" by Reingold, Nievergelt, Deo.
    '''
    assert(n > 0 and k > 0 and n >= k)
    global c_jx, c_array, c_0_based
    if init:
        c_array = range(k+1)
        c_jx = 1
        c_0_based = zero_based
        if zero_based:
            c_0_based = 1
            return tuple(map(lambda x: x-1, c_array[1:]))
        else:
            return tuple(c_array[1:])
    if c_jx:
        c_jx = k
        while c_array[c_jx] == n - k + c_jx:
            c_jx = c_jx - 1
        if c_jx == 0:
            return None
        c_array[c_jx] = c_array[c_jx] + 1
        for ix in xrange(c_jx+1, k+1):
            c_array[ix] = c_array[ix-1] + 1
        if c_0_based:
            return tuple(map(lambda x: x-1, c_array[1:]))
        else:
            return tuple(c_array[1:])
    else:
        return None

def PrintArray(array, stream, num_places):
    if num_places == 0:
        fmt = "%d "
    else:
        fmt = "%%%dd " % num_places
    for num in array:
        stream.write(fmt % num)
    stream.write("\n")

def C(n, k, stream=sys.stdout, num_places=3):
    '''Print all (n, k) combinations to a stream.  n is the number of the
    items to choose from, k is the number of items in the combination,
    stream is where the combinations get printed, and num_places is the 
    width of the integer field.

    Examples:  C(5, 2) prints
        1   2 
        1   3 
        1   4 
        1   5 
        2   3 
        2   4 
        2   5 
        3   4 
        3   5 
        4   5 
    C(5, 2, sys.stdout, 1) prints
        1 2 
        1 3 
        1 4 
        1 5 
        2 3 
        2 4 
        2 5 
        3 4 
        3 5 
        4 5 
    '''
    PrintArray(GetCombination(n, k, 1), stream, num_places)
    array = GetCombination(n, k, 0)
    while array:
        PrintArray(array, stream, num_places)
        array = GetCombination(n, k, 0)

def GetPermutation(n, init=0, zero_based=0):
    '''Each call will return a tuple of the next permutation of n items 
    The procedure for use is:

        1.  Call with init == 1.  This will return a tuple of the integers
            from 1 to k in their initial order.
        2.  Subsequent calls with init == 0 will return a tuple of k integers
            that is next in the sequence of permutations of n items.
        3.  All the permutations have been returned when the function 
            returns None.

    If you wish the returned tuple of numbers to be zero based (which is
    handy for selecting items from python sequences), set zero_based to
    1 on the initialization call.

    This routine is adapted from a C routine given at
    http://remus.rutgers.edu/~rhoads/Code/perm_lex.c, which is a C
    implementation by Glenn C. Rhoads of an algorithm due to Dijkstra.
    '''
    assert(n > 0)
    global p_ix, p_jx, p_array, p_0_based
    if init:
        p_array = range(n+1)
        p_ix = 1
        if zero_based:
            p_0_based = 1
            return tuple(map(lambda x: x-1, p_array[1:]))
        else:
            return tuple(p_array[1:])
    if p_ix:
        p_ix = n - 1
        while p_array[p_ix] > p_array[p_ix+1]:
            p_ix = p_ix - 1
        p_jx = n
        while p_array[p_ix] > p_array[p_jx]:
            p_jx = p_jx - 1
        temp = p_array[p_ix]
        p_array[p_ix] = p_array[p_jx]
        p_array[p_jx] = temp
        r = n
        s = p_ix + 1
        while r > s:
            temp = p_array[r]
            p_array[r] = p_array[s]
            p_array[s] = temp
            r = r - 1
            s = s + 1
        if p_array[1] != 0:
            if p_0_based:
                return tuple(map(lambda x: x-1, p_array[1:]))
            else:
                return tuple(p_array[1:])
        else:
            return None
    else:
        return None

def P(n, stream=sys.stdout, num_places=3):
    '''Print all n permutations to a stream.  n is the number of objects
    to permute, stream is the stream to print the permutations to, and 
    num_places is the width of the integer field.

    Example:  P(3) prints:
        1   2   3 
        1   3   2 
        2   1   3 
        2   3   1 
        3   1   2 
        3   2   1 
    whereas P(3, sys.stdout, 1) prints
        1 2 3 
        1 3 2 
        2 1 3 
        2 3 1 
        3 1 2 
        3 2 1 
    '''
    PrintArray(GetPermutation(n, 1), stream, num_places)
    array = GetPermutation(n, 0)
    while array:
        PrintArray(array, stream, num_places)
        array = GetPermutation(n, 0)

