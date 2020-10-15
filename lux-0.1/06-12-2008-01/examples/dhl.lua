#!/usr/bin/env lux

-- Diminutive HTTPD server in Lua
-- Inspired by "Dustmote", written in Tcl by Harold Kaplan
-- 07/02/2001 jcw@equi4.com

if not bind then
  local h,e=dynopen('./luasocket.so')
  if h then dyncall(h,'lua_socketlibopen') else print(e) end
end

-- To run this example, make sure ./dhldocs/index.html exists, start
-- this server as "lux dhl.lua", then try to fetch that file in your
-- web browser, using the url http://127.0.0.1:8080/ ... c'est tout!

root	= './dhldocs'
default	= 'index.html'
port	= 8080

print('Starting server on port '..port..', root: '..root..'/')
server=bind('*',port)

function one(p)
  if strsub(p,-1)=='/' then p=p..default end
  local f,e,h,b=openfile(root..p,'rb')
  if f then
    h,b='200 OK',read(f,'*a')
    closefile(f)
  else
    h,b='404 Not found','*** '..e..': '..p
  end
  return 'HTTP/1.0 '..h..'\n\n'..b
end

while 1 do
  local session=accept(server)
  local line=receive(session)
  print(line)
  send(session,gsub(line,'^%w+%s+([^%s]+)',one,1))
  close(session)
end
