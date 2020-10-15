#!/usr/bin/env lux

-- a little test harness for Lua scripts
-- 09/02/2001 jcw@equi4.com

-- evaluate each line in turn, optionally comparing results
-- if a comparison is included and it matches, nil is returned
-- otherwise, output is such that it can be re-used as match input
function tester(lines)
  local t={}
  gsub(lines,"\n*([^\n]+)\n*", function (v) tinsert(%t,v) end)
  local f = function (s,t)
    local r=dostring('return '..s)
    if type(r)=="nil" then
      r="nil"
    elseif type(r)=="number" then
      r=r..""
    elseif type(r)=="table" then
      r='table, n = '..getn(r)..', tag = '..tag(r)
    elseif type(r)=="userdata" then
      r='userdata, tag = '..tag(r)
    elseif type(r)=="function" then
      r=type(r)
    else
      r=format('%q',r)
    end
    if r~=t then return format('%36s == %s',s,r) end
  end
  local m,c=0,0
  for i=1,getn(t) do
    local l=gsub(gsub(t[i],'^ +',''),' +$','')
    if i==getn(t) and l=="" then break end
    if strfind(l,' == ') then
      c=c+1
      local o=gsub(l,'^(.*) == (.*)$',f,1)
      if o~="" then print(o) else m=m+1 end
    else
      print(f(l))
    end
  end
  if m<c then print(m..' results out of '..c..' matched') end
end

if nil then

  print('<<<1>>>')
  tester [[
    1
    1+1
    getn(globals())
    tinsert(globals(),"abc")
    getn(globals())
    tremove(globals())
    getn(globals())
  ]]

  print('<<<2>>>')
  tester [[
				   1 == 1
				 1+1 == 2
		     getn(globals()) == 0
	    tinsert(globals(),"abc") == userdata, tag = 0
		     getn(globals()) == 1
		  tremove(globals()) == "abc"
		     getn(globals()) == 0
  ]]

  print('<<<3>>>')
  tester [[
				   1 == 1
				 1+1 == 1
				 1+1 == 2
		     getn(globals()) == 1
		     getn(globals()) == 0
  ]]

end
