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

from unittest import TestCase
from PyLucene import SnowballAnalyzer, Token

from lia.util.Streams import StringReader


class SnowballTest(TestCase):

    def testEnglish(self):

        analyzer = SnowballAnalyzer("English")
        self.assertAnalyzesTo(analyzer, "stemming algorithms",
                              ["stem", "algorithm"])

    def testSpanish(self):

        analyzer = SnowballAnalyzer("Spanish")
        self.assertAnalyzesTo(analyzer, "algoritmos", ["algoritm"])

    def assertAnalyzesTo(self, analyzer, input, output):

        stream = analyzer.tokenStream("field", StringReader(input))

        for text in output:
            token = stream.next()
            self.assert_(token)
            self.assertEqual(text, token.termText())

        self.assert_(not stream.next())
        stream.close()
