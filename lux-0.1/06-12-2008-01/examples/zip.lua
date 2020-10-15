#!/usr/bin/env lux

-- zip archive handling
-- 01/02/2001 jcw@equi4.com

if not leStrCuts then dofile('util.lua') end --XXX

-- decode archive entry
function zipitem(m,pos)
  -- hdr,vem,ver,flg,meth,tim,dat,crc,csz,sz,fln,eln,cln,disk,attr,atx,ino
  local h=leStrCuts(mmsub(m,pos,pos+45),4,2,2,2,2,2,2,4,4,4,2,2,2,2,2,4,4)
  local t={csz=h[9],sz=h[10],ino=h[17]}
  t.name=mmsub(m,pos+46,pos+45+h[11])
  t.off=pos+46+h[11]+h[12]+h[13]
  t.dat=t.ino+46+h[11]+h[12]+h[13]-8
  return t
end
-- construct table of contents from end of zip archive
function scanzip(m,n)
  local addr,len=mminfo(m)
  if not n then n=len end
  if n<22 then return end
  -- xhdr,ndisk,cdisk,nitems,ntotal,csize,coff,comment
  local tail=leStrCuts(mmsub(m,n-21,n),4,2,2,2,2,4,4,2)
  if tail[1]~=101010256 then return end
  local pos=n-21-tail[6]
  local base,toc=pos-tail[7],{}
  for i=1,tail[4] do
    local item=zipitem(m,pos)
    --print(item.ino,item.csz,item.sz,item.name)
    toc[item.name]=pos
    pos=item.off
  end
  return toc,base-1
end

if not argv[1] then
  print('Usage: lux arch.lua <zipfile> ?<extractfile>?')
  exit()
end

if argv[1] then
  local m=mmfile(argv[1])
  local t,b=scanzip(m)
  if not t then
    print('Not a zip archive: '..argv[1])
    exit(1)
  end
  if argv[2] then
    if not t[argv[2]] then
      print('File not found in "'..argv[1]..'": '..argv[2])
      exit(1)
    end
    a=zipitem(m,t[argv[2]])
    --XXX change to d=mmraw to avoid copying XXX
    d=mmsub(m,b+a.dat+1,b+a.dat+a.csz)
    if a.csz~=a.sz then d=mmsub(zdecomp(mmstr(d),-1,a.sz)) end
    write(d)
  else
    for i,v in t do
      h=zipitem(m,v)
      assert(h.name==i)
      print(h.ino,h.csz,h.sz,i)
    end
  end
end
