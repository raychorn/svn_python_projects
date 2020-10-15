#!/usr/bin/env lux

-- bin2c recoded in Lua and extended, see tolua-3.2/src/bin/code.lua
-- 02/02/2001 jcw@equi4.com

-- lux/lua command-line compatibility
if getargs then argv=getargs() end
if argv[1]=="-f" then tremove(argv,1) end

write('\n{ /* begin embedded code */\n')
tremove(argv,1)
local sz,fmt={},{}
for i=1,getn(argv) do
  local fp=openfile(argv[i],'rb')
  local s=read(fp,'*a')
  closefile(fp)
  sz[i]=strlen(s)
  local fn=gsub(argv[i],'%...?.?$','')
  local l='  static unsigned char B'..i..'[] = { /* '..fn..' */ '
  for j=1,strlen(s) do
    if strlen(l)>75 then print(l); l='    ' end
    l=l..strbyte(s,j)..','
  end
  print(l..' };')
  if strbyte(s,1)==31 then fmt[i]="z" else fmt[i]="lua" end
end
for i=1,getn(argv) do
  local fn=gsub(argv[i],'%...?.?$','')
  print('  '..fmt[i]..'_dobuffer(L,(const char*)B'..i..','
  					..sz[i]..',"'..fn..'");')
end
write('} /* end of embedded code */\n\n')
