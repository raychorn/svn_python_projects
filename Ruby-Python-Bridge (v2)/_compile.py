#!/usr/bin/env python

import compileall

import re
compileall.compile_dir('lib', rx=re.compile('/[.]svn'), force=True)

