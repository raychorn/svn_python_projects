#!/usr/bin/env lux

-- Base 64 encoding
-- 10/02/2001 jcw@equi4.com

if not join then dofile('util.lua') end --XXX
if not tester then dofile('tester.lua') end --XXX

base64={}

function base64.encode(s)
  local m={} -- this could be inited once instead of every time
  local z='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	..'abcdefghijklmnopqrstuvwxyz0123456789+/'
  for i=1,strlen(z) do m[i-1]=strsub(z,i,i) end
  local f=function (n,b) return %m[band(rshift(n,b),63)] end
  -- processing starts here
  local t,e={},strlen(s)
  for i=1,e,45 do
    local o=''
    for j=1,45,3 do
      if i+j-1>e then break end
      local n=0
      for k=-1,1 do
	n=n*256
	if i+j+k<=e then n=n+strbyte(s,i+j+k) end
      end
      o=o..f(n,18)..f(n,12)..f(n,6)..f(n,0)
      if i+j+1>e then
	o=strsub(o,1,-2)..'='
	if i+j>e then o=strsub(o,1,-3)..'==' end
      end
    end
    tinsert(t,o)
  end
  --return join(t,'\n')
  return t
end

tester [[
              base64.encode('Hi')[1] == "SGk="
             base64.encode('abc')[1] == "YWJj"
      base64.encode('1234567890')[1] == "MTIzNDU2Nzg5MA=="
]]

base64.x='This is a test, this is only a test, what a boring test...'
base64.y=[[VGhpcyBpcyBhIHRlc3QsIHRoaXMgaXMgb25seSBhIHRlc3QsIHdoYXQgYSBi
b3JpbmcgdGVzdC4uLg==]]
base64.z=join(base64.encode(base64.x),'\n')
assert(base64.z == base64.y)
