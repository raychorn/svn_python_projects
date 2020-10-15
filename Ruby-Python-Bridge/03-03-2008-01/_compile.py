#!/usr/bin/env python

import compileall

#compileall.compile_dir('', force=True)

# Perform same compilation, excluding files in .svn directories.
import re
compileall.compile_dir('', rx=re.compile('/[.]svn'), force=True)

