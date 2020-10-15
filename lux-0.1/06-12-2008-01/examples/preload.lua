-- Pre-loaded code, included in Lux core
-- 19/02/2001 jcw@equi4.com

lux={}

-- convert raw string to little-endian int
function lux.leInt(s)
  local v=0
  for i=strlen(s),1,-1 do v=v*256+strbyte(s,i) end
  return v
end
-- cut up a string in little-endian ints of given size
function lux.leStrCuts(s,...)
  local o,r=1,{}
  for i=1,getn(arg) do
    tinsert(r,lux.leInt(strsub(s,o,o+arg[i]-1)))
    o=o+arg[i]
  end
  return r
end
-- decode a zip archive entry header
function lux.zipitem(m,pos)
  -- hdr,vem,ver,flg,meth,tim,dat,crc,csz,sz,fln,eln,cln,disk,attr,atx,ino
  local h=lux.leStrCuts(mmsub(m,pos,pos+45),4,2,2,2,2,2,2,4,4,4,2,2,2,2,2,4,4)
  local t={csz=h[9],sz=h[10],ino=h[17]}
  t.name=mmsub(m,pos+46,pos+45+h[11])
  t.off=pos+46+h[11]+h[12]+h[13]
  t.dat=t.ino+46+h[11]+h[12]+h[13]-8
  return t
end
-- construct table of contents from end of zip archive
function lux.zipscan(m,n)
  local addr,len=mminfo(m)
  if not n then n=len end
  if n<22 then return end
  -- xhdr,ndisk,cdisk,nitems,ntotal,csize,coff,comment
  local tail=lux.leStrCuts(mmsub(m,n-21,n),4,2,2,2,2,4,4,2)
  if tail[1]~=101010256 then return end
  local pos=n-21-tail[6]
  local base,toc=pos-tail[7],{}
  for i=1,tail[4] do
    local item=lux.zipitem(m,pos)
    --print(item.ino,item.csz,item.sz,item.name)
    toc[item.name]=pos
    pos=item.off
  end
  return toc,base-1
end
-- open zip archive and scan its table of contents
function lux.ZipOpen(f)
  local m=mmfile(f)
  local t,b=lux.zipscan(m)
  if t then return {map=m,toc=t,base=b} end
end
-- read and unpack a zip archive entry
function lux.ZipFetch(z,f)
    if not z.toc[f] then return end
    local a=lux.zipitem(z.map,z.toc[f])
    --XXX change to d=mmraw to avoid copying XXX
    local d=mmsub(z.map,z.base+a.dat+1,z.base+a.dat+a.csz)
    if a.csz~=a.sz then d=mmsub(zdecomp(mmstr(d),-1,a.sz)) end
    return d
end
-- run bootstrap script if present
function lux.ZipBoot(f)
  lux.zip=lux.ZipOpen(f)
  if lux.zip then
    local s=lux.ZipFetch(lux.zip,'boot.lux')
    if s then return dostring(s,f..'/boot.lux') end
  end
end

if luxlibvers then
  local d,n=luxlibvers()
  _VERSION=_VERSION..' - luxlib 0.'..n..', '..d
end

