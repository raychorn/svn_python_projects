#!/usr/bin/env python

import pylux, sys

pylux.eval("gv", "print", "Hello Lux, I am Pythonic")
pylux.eval("gvv", "setglobal", "argv0", sys.argv[0])
pylux.eval("gv", "dostring", "argv={}")

for i in range(1,len(sys.argv)):
  pylux.eval("ggv", "tinsert", "argv", sys.argv[i])

pylux.eval("gv", "dofile", "run.lux")
