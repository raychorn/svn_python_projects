#!/usr/bin/env tclsh

set auto_path [linsert $auto_path 0 .]
package require tclux

tclux gs print "Hello Lux, I am Tclish"
tclux gss setglobal argv0 $argv0
tclux gs dostring "argv={}"

foreach a $argv {
  tclux ggs tinsert argv $a
}

tclux gs dofile run.lux
