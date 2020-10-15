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

from PyLucene import \
     PhraseQuery, RangeQuery, SpanNearQuery, SpanTermQuery, Term

from lia.extsearch.queryparser.NumberUtils import NumberUtils

#
# A QueryParser or a MultiFieldQueryParser extension
#

class CustomQueryParser(object):

    def getFuzzyQuery(self, super, field, termText, minSimilarity):
        raise AssertionError, "Fuzzy queries not allowed"

    def getWildcardQuery(self, super, field, termText):
        raise AssertionError, "Wildcard queries not allowed"

    #
    # Special handling for the "id" field, pads each part
    # to match how it was indexed.
    #
    def getRangeQuery(self, super, field, part1, part2, inclusive):

        if field == "id":

            num1 = int(part1)
            num2 = int(part2)

            return RangeQuery(Term(field, NumberUtils.pad(num1)),
                              Term(field, NumberUtils.pad(num2)),
                              inclusive)

        if field == "special":
            print part1, "->", part2

            if part1 == '*':
                t1 = None
            else:
                t1 = Term("field", part1)

            if part2 == '*':
                t2 = None
            else:
                t2 = Term("field", part2)

            return RangeQuery(t1, t2, inclusive)

        return super.getRangeQuery(field, part1, part2, inclusive)

    #
    # Replace PhraseQuery with SpanNearQuery to force in-order
    # phrase matching rather than reverse.
    #
    def getFieldQuery(self, super, field, queryText, slop):

        if slop is None:
            return super.getFieldQuery(field, queryText)

        # let QueryParser's implementation do the analysis
        orig = super.getFieldQuery(field, queryText, slop)

        if not orig.isPhraseQuery():
            return orig

        pq = orig.toPhraseQuery()
        clauses = [SpanTermQuery(term) for term in pq.getTerms()]

        return SpanNearQuery(clauses, slop, True);
