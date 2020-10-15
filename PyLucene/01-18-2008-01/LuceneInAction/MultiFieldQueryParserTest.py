
import os, sys, unittest

baseDir = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(baseDir)

import lia.advsearching.MultiFieldQueryParserTest
from PyLucene import System

System.setProperty("index.dir", os.path.join(baseDir, 'index'))
unittest.main(lia.advsearching.MultiFieldQueryParserTest)