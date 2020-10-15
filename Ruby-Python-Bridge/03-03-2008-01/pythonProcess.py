#!/usr/bin/env python

import rubypythonlib

__shutdown__ = 'xxxShutdownxxx'
__ipAddr__ = 'localhost'
__port__ = 2727

b = rubypythonlib.rubyPythonBridgeManager(__ipAddr__, __port__,__shutdown__)
print 'b=(%s)' % (str(b))
b.startup()