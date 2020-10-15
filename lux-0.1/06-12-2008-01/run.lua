#!/usr/bin/env lux

-- Standalone startup sequence
-- 02/02/2001 jcw@equi4.com

if not lux.ZipBoot(argv0) then
  if argv and argv[1] then
    argv1=tremove(argv,1)
    if not lux.ZipBoot(argv1) then
      dofile(argv1)
    end
  else
    print(_VERSION)
  end
end
