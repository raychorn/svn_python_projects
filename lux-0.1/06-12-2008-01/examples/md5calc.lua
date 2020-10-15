#!/usr/bin/env lux

-- An MD5 mplementation in Lua, requires bitlib
-- 10/02/2001 jcw@equi4.com

md5={ff=tonumber('ffffffff',16),consts={}}

gsub([[ d76aa478 e8c7b756 242070db c1bdceee
	f57c0faf 4787c62a a8304613 fd469501
	698098d8 8b44f7af ffff5bb1 895cd7be
	6b901122 fd987193 a679438e 49b40821
	f61e2562 c040b340 265e5a51 e9b6c7aa
	d62f105d 02441453 d8a1e681 e7d3fbc8
	21e1cde6 c33707d6 f4d50d87 455a14ed
	a9e3e905 fcefa3f8 676f02d9 8d2a4c8a
	fffa3942 8771f681 6d9d6122 fde5380c
	a4beea44 4bdecfa9 f6bb4b60 bebfbc70
	289b7ec6 eaa127fa d4ef3085 04881d05
	d9d4d039 e6db99e5 1fa27cf8 c4ac5665
	f4292244 432aff97 ab9423a7 fc93a039
	655b59c3 8f0ccc92 ffeff47d 85845dd1
	6fa87e4f fe2ce6e0 a3014314 4e0811a1
	f7537e82 bd3af235 2ad7d2bb eb86d391
	67452301 efcdab89 98badcfe 10325476 ]],
  '(%w+)', function (s) tinsert(%md5.consts,tonumber(s,16)) end)

function md5.transform(A,B,C,D)
  local f=function (x,y,z) return bor(band(x,y),band(-x-1,z)) end
  local g=function (x,y,z) return bor(band(x,z),band(y,-z-1)) end
  local h=function (x,y,z) return bxor(x,bxor(y,z)) end
  local i=function (x,y,z) return bxor(y,bor(x,-z-1)) end
  local z=function (f,a,b,c,d,x,s,ac)
	    a=band(a+f(b,c,d)+x+ac,md5.ff)
	    -- be *very* careful that left shift does not cause rounding!
	    return bor(lshift(band(a,rshift(md5.ff,s)),s),rshift(a,32-s))+b
	  end
  local a,b,c,d=A,B,C,D
  local t=md5.consts

  a=z(f,a,b,c,d,X[ 0], 7,t[ 1])
  d=z(f,d,a,b,c,X[ 1],12,t[ 2])
  c=z(f,c,d,a,b,X[ 2],17,t[ 3])
  b=z(f,b,c,d,a,X[ 3],22,t[ 4])
  a=z(f,a,b,c,d,X[ 4], 7,t[ 5])
  d=z(f,d,a,b,c,X[ 5],12,t[ 6])
  c=z(f,c,d,a,b,X[ 6],17,t[ 7])
  b=z(f,b,c,d,a,X[ 7],22,t[ 8])
  a=z(f,a,b,c,d,X[ 8], 7,t[ 9])
  d=z(f,d,a,b,c,X[ 9],12,t[10])
  c=z(f,c,d,a,b,X[10],17,t[11])
  b=z(f,b,c,d,a,X[11],22,t[12])
  a=z(f,a,b,c,d,X[12], 7,t[13])
  d=z(f,d,a,b,c,X[13],12,t[14])
  c=z(f,c,d,a,b,X[14],17,t[15])
  b=z(f,b,c,d,a,X[15],22,t[16])

  a=z(g,a,b,c,d,X[ 1], 5,t[17])
  d=z(g,d,a,b,c,X[ 6], 9,t[18])
  c=z(g,c,d,a,b,X[11],14,t[19])
  b=z(g,b,c,d,a,X[ 0],20,t[20])
  a=z(g,a,b,c,d,X[ 5], 5,t[21])
  d=z(g,d,a,b,c,X[10], 9,t[22])
  c=z(g,c,d,a,b,X[15],14,t[23])
  b=z(g,b,c,d,a,X[ 4],20,t[24])
  a=z(g,a,b,c,d,X[ 9], 5,t[25])
  d=z(g,d,a,b,c,X[14], 9,t[26])
  c=z(g,c,d,a,b,X[ 3],14,t[27])
  b=z(g,b,c,d,a,X[ 8],20,t[28])
  a=z(g,a,b,c,d,X[13], 5,t[29])
  d=z(g,d,a,b,c,X[ 2], 9,t[30])
  c=z(g,c,d,a,b,X[ 7],14,t[31])
  b=z(g,b,c,d,a,X[12],20,t[32])

  a=z(h,a,b,c,d,X[ 5], 4,t[33])
  d=z(h,d,a,b,c,X[ 8],11,t[34])
  c=z(h,c,d,a,b,X[11],16,t[35])
  b=z(h,b,c,d,a,X[14],23,t[36])
  a=z(h,a,b,c,d,X[ 1], 4,t[37])
  d=z(h,d,a,b,c,X[ 4],11,t[38])
  c=z(h,c,d,a,b,X[ 7],16,t[39])
  b=z(h,b,c,d,a,X[10],23,t[40])
  a=z(h,a,b,c,d,X[13], 4,t[41])
  d=z(h,d,a,b,c,X[ 0],11,t[42])
  c=z(h,c,d,a,b,X[ 3],16,t[43])
  b=z(h,b,c,d,a,X[ 6],23,t[44])
  a=z(h,a,b,c,d,X[ 9], 4,t[45])
  d=z(h,d,a,b,c,X[12],11,t[46])
  c=z(h,c,d,a,b,X[15],16,t[47])
  b=z(h,b,c,d,a,X[ 2],23,t[48])

  a=z(i,a,b,c,d,X[ 0], 6,t[49])
  d=z(i,d,a,b,c,X[ 7],10,t[50])
  c=z(i,c,d,a,b,X[14],15,t[51])
  b=z(i,b,c,d,a,X[ 5],21,t[52])
  a=z(i,a,b,c,d,X[12], 6,t[53])
  d=z(i,d,a,b,c,X[ 3],10,t[54])
  c=z(i,c,d,a,b,X[10],15,t[55])
  b=z(i,b,c,d,a,X[ 1],21,t[56])
  a=z(i,a,b,c,d,X[ 8], 6,t[57])
  d=z(i,d,a,b,c,X[15],10,t[58])
  c=z(i,c,d,a,b,X[ 6],15,t[59])
  b=z(i,b,c,d,a,X[13],21,t[60])
  a=z(i,a,b,c,d,X[ 4], 6,t[61])
  d=z(i,d,a,b,c,X[11],10,t[62])
  c=z(i,c,d,a,b,X[ 2],15,t[63])
  b=z(i,b,c,d,a,X[ 9],21,t[64])

  return A+a,B+b,C+c,D+d
end

function md5.Calc(s)
  local msgLen=strlen(s)
  local padLen=56-imod(msgLen,64)
  if imod(msgLen,64)>56 then padLen=padLen+64 end
  if padLen==0 then padLen=64 end
  s=s..strchar(128)..strrep(strchar(0),padLen-1)
  s=s..leIstr(8*msgLen)..leIstr(0)
  assert(imod(strlen(s),64)==0)
  local t=md5.consts
  local a,b,c,d=t[65],t[66],t[67],t[68]
  for i=1,strlen(s),64 do
    X=leStrCuts(strsub(s,i,i+63),4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4)
    assert(getn(X)==16)
    X[0]=tremove(X,1) -- zero based!
    a,b,c,d=md5.transform(a,b,c,d)
  end
  local swap=function (w) return beInt(leIstr(w)) end
  return format("%08x%08x%08x%08x",swap(a),swap(b),swap(c),swap(d))
end

-- convert little-endian 32-bit int to a 4-char string
function leIstr(i)
  local f=function (s) return strchar(band(rshift(%i,s),255)) end
  return f(0)..f(8)..f(16)..f(24)
end

do -- from util.lua
  -- convert raw string to big-endian int
  function beInt(s)
    local v=0
    for i=1,strlen(s) do v=v*256+strbyte(s,i) end
    return v
  end
  -- convert raw string to little-endian int
  function leInt(s)
    local v=0
    for i=strlen(s),1,-1 do v=v*256+strbyte(s,i) end
    return v
  end
  -- cut up a string in little-endian ints of given size
  function leStrCuts(s,...)
    local o,r=1,{}
    for i=1,getn(arg) do
      tinsert(r,leInt(strsub(s,o,o+arg[i]-1)))
      o=o+arg[i]
    end
    return r
  end
end

s0='message digest'
s1='abcdefghijklmnopqrstuvwxyz'
s2='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
s3='1234567890123456789012345678901234567890'
 ..'1234567890123456789012345678901234567890'

    assert(md5.Calc('')=='d41d8cd98f00b204e9800998ecf8427e')
   assert(md5.Calc('a')=='0cc175b9c0f1b6a831c399e269772661')
 assert(md5.Calc('abc')=='900150983cd24fb0d6963f7d28e17f72')
    assert(md5.Calc(s0)=='f96b697d7cb7938d525a2f31aaf161d0')
    assert(md5.Calc(s1)=='c3fcd3d76192e4007dfb496cca67e13b')
    assert(md5.Calc(s2)=='d174ab98d277d9f5a5611c2c9f419d9f')
    assert(md5.Calc(s3)=='57edf4a22be3c955ac49da2e2107b67a')

if 1 then 
  sizes={10,50,100,500,1000,5000,10000}
  for i=1,getn(sizes) do
    local s=strrep(' ',sizes[i])
    local t=clock()
    for j=1,10 do
      md5.Calc(s)
    end
    print(format('%6d bytes: %4d mSec',sizes[i],(clock()-t)*100))
  end
end
