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


from lia.analysis.AnalyzerUtils import AnalyzerUtils
from lia.analysis.synonym.WordNetSynonymEngine import WordNetSynonymEngine
from lia.analysis.synonym.SynonymAnalyzer import SynonymAnalyzer


class SynonymAnalyzerViewer(object):

    def main(cls, argv):

        engine = WordNetSynonymEngine(argv[1])

        text = "The quick brown fox jumps over the lazy dogs"
        AnalyzerUtils.displayTokensWithPositions(SynonymAnalyzer(engine), text)

        text = "\"Oh, we get both kinds - country AND western!\" - B.B."
        AnalyzerUtils.displayTokensWithPositions(SynonymAnalyzer(engine), text)

    main = classmethod(main)
