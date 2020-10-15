# ====================================================================
# Copyright (c) 2004-2005 Open Source Applications Foundation.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions: 
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software. 
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
# ====================================================================
#

from math import sqrt
from PyLucene import SortField, Term, IndexReader

#
# A SortComparatorSource implementation
#

class DistanceComparatorSource(object):

    def __init__(self, x, y):

        self.x = x
        self.y = y

    def newComparator(self, reader, fieldName):

        #
        # A ScoreDocComparator implementation
        # 
        class DistanceScoreDocLookupComparator(object):

            def __init__(self, reader, fieldName, x, y):

                enumerator = reader.terms(Term(fieldName, ""))
                self.distances = distances = [0.0] * reader.numDocs()

                if reader.numDocs() > 0:
                    termDocs = reader.termDocs()
                    try:
                        while True:
                            term = enumerator.term()
                            if term is None:
                                raise RuntimeError, "no terms in field %s" %(fieldName)
                            if term.field() != fieldName:
                                break
                            
                            termDocs.seek(enumerator)
                            while termDocs.next():
                                xy = term.text().split(',')
                                deltax = int(xy[0]) - x
                                deltay = int(xy[1]) - y

                                distances[termDocs.doc()] = sqrt(deltax ** 2 +
                                                                 deltay ** 2)
            
                            if not enumerator.next():
                                break
                    finally:
                        termDocs.close()

            def compare(self, i, j):

                if self.distances[i.doc] < self.distances[j.doc]:
                    return -1
                if self.distances[i.doc] > self.distances[j.doc]:
                    return 1
                return 0

            def sortValue(self, i):

                return self.distances[i.doc]

            def sortType(self):

                return SortField.FLOAT

        return DistanceScoreDocLookupComparator(reader, fieldName,
                                                self.x, self.y)

    def __str__(self):

        return "Distance from ("+x+","+y+")"
