
import os, sys

sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))

from lia.tools.BerkeleyDbSearcher import BerkeleyDbSearcher
BerkeleyDbSearcher.main(sys.argv)
