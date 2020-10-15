
import os, sys

sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))

from lia.meetlucene.Searcher import Searcher
Searcher.main(sys.argv)
