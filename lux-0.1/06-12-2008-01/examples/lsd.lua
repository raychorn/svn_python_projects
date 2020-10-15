#!/usr/bin/env lux

-- A utility to list and extract files from scripted documents
-- 17/02/2001 jcw@equi4.com

if not mk then dofile('metakit.lua') end --XXX

function dirwalk(b,c,p,g)
  local r,t=b.root,b.vfs
  local d=r.dirs[c]
  g(p,d)
  local s={}
  for i,v in t[c] do tinsert(s,i) end
  sort(s)
  for i=1,getn(s) do
    local k=s[i]
    dirwalk(b,t[c][k],p..k..'/',g)
  end
end

local totals={bytes=0,compr=0,ndirs=0,files=0}

function percent(a,b)
  return b>1 and a/b*100 or 0
end

function dirstat(p,d)
  local t=%totals
  print('\n/'..p)
  local f=d.files
  for i=1,f:size() do
    local z=f[i].contents
    local h=date('%Y/%m/%d %H:%M:%S',f[i].date)
    local s=f[i].size
    local c=percent(s-strlen(z),s)
    print(format(' %10d %3d%%  %s  %s',s,c,h,f[i].name))
    --if strlen(z)~=f[i].size then
      --local y=mmsub(zdecomp(mmstr(z),1,f[i].size))
      --assert(strlen(y)==f[i].size)
    --end
    t.bytes=t.bytes+f[i].size
    t.compr=t.compr+strlen(z)
  end
  t.ndirs=t.ndirs+1
  t.files=t.files+d.files:size()
end

function kilo(v)
  if v<1000 then return format('%.3g b',v) end
  if v<1000000 then return format('%.3g Kb',v/1024) end
  if v<1000000000 then return format('%.3g Mb',v/(1024*1024)) end
  return format('%.3g Gb',v/(1024*1024*1024))
end

if not argv[1] then
  print [[
  LSD is a utility to list or extract files from scripted documents.
    Usage: lsd datafile ?path-to-extract?
  For details about scripted docs, see http://www.equi4.com/metakit/
]]
  exit(1)
end

db=mk.Open(argv[1])		-- open the Metakit datafile
if not db then
  print('Cannot open as MetaKit datafile: '..argv[1])
  exit(2)
end

db.root=mk.Root(db)		-- create a Lua access layer
db.vfs=mk.VfsIndex(db.root)	-- treat it as a VFS document

if argv[2] then
  --print(mk.VfsFetch(db,'/lib/ftpd0.4/pkgIndex.tcl'))
  text=mk.VfsFetch(db,argv[2])
  if not text then
    print('File not found in "'..argv[1]..'": '..argv[2])
    exit(3)
  end
  write(text)
else
  dirwalk(db,1,'',dirstat)
  print(format('\n    =======  ==='
	     ..'\n %10s %3d%%  (total: %s in %d files, %d dirs)\n',
		  kilo(totals.bytes),
		  percent(totals.bytes-totals.compr,totals.bytes),
		  kilo(totals.compr), totals.files, totals.ndirs))
end

