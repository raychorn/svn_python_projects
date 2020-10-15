from distutils.core import setup
import os
import sys
import re
import compileall

compileall.compile_dir('.', rx=re.compile('/[.]svn'), force=True)
