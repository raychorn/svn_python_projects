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

from sys import stdout

from PyLucene import \
     StandardAnalyzer, Term, TermQuery, \
     Fragmenter, Highlighter, QueryScorer, SimpleFragmenter, SimpleHTMLFormatter

from lia.util.Streams import StringReader


class HighlightIt(object):

    # from http://www.lipsum.com
    text = \
      """
      Contrary to popular belief, Lorem Ipsum is
      not simply random text. It has roots in a piece of
      classical Latin literature from 45 BC, making it over
      2000 years old. Richard McClintock, a Latin professor
      at Hampden-Sydney College in Virginia, looked up one
      of the more obscure Latin words, consectetur, from
      a Lorem Ipsum passage, and going through the cites
      of the word in classical literature, discovered the
      undoubtable source. Lorem Ipsum comes from sections
      1.10.32 and 1.10.33 of "de Finibus Bonorum et
      Malorum" (The Extremes of Good and Evil) by Cicero,
      written in 45 BC. This book is a treatise on the
      theory of ethics, very popular during the
      Renaissance. The first line of Lorem Ipsum, "Lorem
      ipsum dolor sit amet..", comes from a line in
      section 1.10.32.
      """

    def main(cls, argv):

        query = TermQuery(Term("f", "ipsum"))
        scorer = QueryScorer(query)
        formatter = SimpleHTMLFormatter("<span class=\"highlight\">", "</span>")
        highlighter = Highlighter(formatter, scorer)
        fragmenter = SimpleFragmenter(50)
        highlighter.setTextFragmenter(fragmenter)

        analyzer = StandardAnalyzer()
        tokenStream = analyzer.tokenStream("f", StringReader(cls.text))
        result = highlighter.getBestFragments(tokenStream, cls.text, 5, "...")

        stdout.write("<html>")
        stdout.write("<style>\n")
        stdout.write(".highlight {\n")
        stdout.write(" background: yellow\n")
        stdout.write("}\n")
        stdout.write("</style>")

        stdout.write("<body>")
        stdout.write(result)
        stdout.write("</body></html>\n")
        stdout.flush()
        
    main = classmethod(main)
