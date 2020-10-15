#!/usr/bin/env wish

# An example of the Tcl <-> Lux binding
# 08/02/2001 jcw@equi4.com

set auto_path [linsert $auto_path 0 .]
package require tclux

# Shorthand to run a Lua script with "lux <script>" 
proc lux {script} {
  uplevel 1 [list tclux gs dostring $script]
}

# Make Tcl's "eval" command available to Lua as "tcl"
tclux gsc setglobal tcl eval

set luxGlobals {}
lux {
  for i,v in globals() do
    tcl('lappend','luxGlobals',i)
  end
}
puts [lsort $luxGlobals]

proc xbutton {args} {
  puts [llength $args]
  puts $args
}

lux {
  -- define a "tk" namespace with a couple of functions
  tk = {
    button =  function (t)
		local x={'button'}
		for i=1,getn(t) do
		  tinsert(x,t[i])
		end
		for i,v in t do
		  if type(i)=="string" then
		    tinsert(x,'-'..i)
		    tinsert(x,'{'..v..'}')
		  end
		end
		call(tcl,x)
		return t[1]
	      end,
    pack = function (t) tinsert(t,1,'pack'); call(tcl,t) end,
  }

  -- now call them
  tk.pack {
    tk.button { '.a'; text='Hello world!', command='bell; exit' }
  }
}
