
import os, sys

baseDir = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(baseDir)

from lia.advsearching.BooksLikeThis import BooksLikeThis
from PyLucene import System

System.setProperty("index.dir", os.path.join(baseDir, 'index'))
BooksLikeThis.main(sys.argv)
