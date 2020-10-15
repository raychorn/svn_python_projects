#!/usr/bin/env lux

-- Tiny encryption algorithm by David Wheeler and Roger Needham
-- 19/02/2001 jcw@equi4.com

-- see http://www.cl.cam.ac.uk/ftp/papers/djw-rmn-tea.html
-- results not verified, only code/decode identity has been checked
-- also, apparently TEA is not extremely secure (hearsay, from Steve B)

if not tester then dofile('util.lua') end --XXX

tea={
  m32=tonumber('ffffffff',16),
  delta=tonumber('9e3779b9',16),
}

function tea.Code(k0,k1,k2,k3,y,z)
  local sum,m27=0,rshift(tea.m32,5)
  for i=1,32 do
    sum=sum+tea.delta
    y=y+band(bxor(bxor(lshift(z,4)+k0,z+sum),band(rshift(z,5),m27)+k1),tea.m32)
    z=z+band(bxor(bxor(lshift(y,4)+k2,y+sum),band(rshift(y,5),m27)+k3),tea.m32)
  end
  return band(y,tea.m32),band(z,tea.m32)
end

function tea.Decode(k0,k1,k2,k3,y,z)
  local sum,m27=band(lshift(tea.delta,5),tea.m32),rshift(tea.m32,5)
  for i=1,32 do
    z=z-band(bxor(bxor(lshift(y,4)+k2,y+sum),band(rshift(y,5),m27)+k3),tea.m32)
    y=y-band(bxor(bxor(lshift(z,4)+k0,z+sum),band(rshift(z,5),m27)+k1),tea.m32)
    sum=sum-tea.delta
  end
  return band(y,tea.m32),band(z,tea.m32)
end

-- convert little-endian 32-bit int to a 4-char string (from md5)
function tea.leIstr(i)
  local f=function (s) return strchar(band(rshift(%i,s),255)) end
  return f(0)..f(8)..f(16)..f(24)
end
-- a quick solution to encoding strings with strings (caveat emptor)
function tea.StrCode(k,t)
  if strlen(k)<16 then k=strrep(k..strchar(0),16) end
  local z=lux.leStrCuts(k,4,4,4,4)
  local z0,z1,z2,z3=z[1],z[2],z[3],z[4]
  local r=''
  for i=1,strlen(t),8 do
    local u=strsub(t,i,i+7)
    if strlen(u)<8 then u=u..strrep(strchar(0),8) end
    local v=lux.leStrCuts(u,4,4)
    v[1],v[2]=tea.Code(z0,z1,z2,z3,v[1],v[2])
    r=r..(tea.leIstr(v[1])..tea.leIstr(v[2]))
  end
  return r
end
-- decode a string, problem: result may have 1..7 extra nullbytes at end
function tea.StrDecode(k,t)
  if strlen(k)<16 then k=strrep(k..strchar(0),16) end
  local z=lux.leStrCuts(k,4,4,4,4)
  local z0,z1,z2,z3=z[1],z[2],z[3],z[4]
  local r=''
  for i=1,strlen(t),8 do
    local v=lux.leStrCuts(strsub(t,i,i+7),4,4)
    v[1],v[2]=tea.Decode(z0,z1,z2,z3,v[1],v[2])
    r=r..(tea.leIstr(v[1])..tea.leIstr(v[2]))
  end
  return r
end

function D(...)
  local s=''
  for i=1,getn(arg) do s=s..' '..arg[i] end
  return strsub(s,2)
end

tester [[
D(tea.Code(1,2,3,4,5,6)) == "2965611328 3722928155"
D(tea.Decode(1,2,3,4,tea.Code(1,2,3,4,5,6))) == "5 6"

D(tea.Code(1,2,3,4,55,66)) == "247759287 1040026046"
D(tea.Decode(1,2,3,4,tea.Code(1,2,3,4,55,66))) == "55 66"

D(tea.Code(11,22,33,44,55,66)) == "2816725138 114698891"
D(tea.Decode(11,22,33,44,tea.Code(11,22,33,44,55,66))) == "55 66"

D(tea.Code(-1,-2,-3,-4,5,6)) == "2451225513 141017392"
D(tea.Decode(-1,-2,-3,-4,tea.Code(-1,-2,-3,-4,5,6))) == "5 6"

D(tea.Code(1,2,3,4,1111111111,2222222222)) == "1919880277 679282949"
D(tea.Decode(1,2,3,4,tea.Code(1,2,3,4,1111111111,2222222222))) == "1111111111 2222222222"

D(tea.Code(123456789,234567890,345678901,456789012,1111111111,2222222222)) == "4226277723 598578853"
D(tea.Decode(123456789,234567890,345678901,456789012,tea.Code(123456789,234567890,345678901,456789012,1111111111,2222222222))) == "1111111111 2222222222" 

hex(tea.StrCode('abc','defghijk')) == "1BEF8974B8F4D813"
tea.StrDecode('abc',tea.StrCode('abc','defghijk')) == "defghijk"

hex(tea.StrCode('abc','def')) == "A2354817D632B33A"
tea.StrDecode('abc',tea.StrCode('abc','def')) == "def\000\000\000\000\000" 
]]
