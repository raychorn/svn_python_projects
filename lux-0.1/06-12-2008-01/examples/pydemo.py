#!/usr/bin/env python

# An example of the Python <-> Lux binding
# 09/02/2001 jcw@equi4.com

import pylux

# Shorthand to run a Lua script with "lux('script')" 
def lux(script):
  pylux.eval("gv", "dostring", script)

# Shorthand to define a Python proc as callback for Lua
def luxcb(name,func):
  pylux.eval("gvc", "setglobal", name, func)

luxGlobals=[]
luxcb("luxAppend", luxGlobals.append)
lux("""
  for i,v in globals() do
    luxAppend(i)
  end
""")
luxGlobals.sort()
print luxGlobals
