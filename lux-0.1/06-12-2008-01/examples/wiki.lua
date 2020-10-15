-- Wippler's wicked wiki renderer
-- 12/02/2001 jcw@equi4.com

if not linesplit then dofile('util.lua') end --XXX

wiki={}

function wiki.linetype(l)
  local l=gsub(l,'%s*$','')
  local l=gsub(l,'(\t)','    ')
  local x={cat='-',txt=l}
  local f=function (t,m)
	    local a,b,c,d,e
	    a,b,c,d,e=strfind(%l,m)
	    if a and imod(strlen(c),3)==0 then
	      %x.cat,%x.depth,%x.aux,%x.txt=t,strlen(c)/3,d,e
	      return %x
	    end
  	  end
  if f('U','^(   +)(%*) (.+)$') then return x end
  if f('O','^(   +)([1-9#])%. (.+)$') then return x end
  if f('D','^(   +)([^:]+):   (.+)$') then return x end
  if strsub(l,1,1)==' ' then
    x.cat,x.depth='Q',1
  elseif strfind(l,'^%-%-%-%-+$') then
    x.cat='H'
  end
  return x
end

function wiki.brackets(l)
  l=gsub(l,'%[%[','[')
  l=gsub(l,'%]%]',']')
  return l
end

function wiki.hilites(l)
  l=gsub(l,"'''([^'].-)'''","<B>%1</B>")
  l=gsub(l,"''([^'].-)''","<I>%1</I>")
  return l
end

function wiki.refs(l,t,r)
  if t then
    l=gsub(l,'%[%[','&lbra;')
    local f=function (u)
	      local s=strsub(u,2,-2)
	      local n=%t[strlower(s)]
	      if n then
		tinsert(%r,n)
	        u='<A HREF="'..n..'">'..s..'</A>'
	      end
	      return u
	    end
    l=gsub(l,'(%b[])',f)
    l=gsub(l,'&lbra;','[[')
  end
  return l
end

function wiki.links(l,u)
  local types={http=1,https=1,ftp=1,news=1,mailto=1}
  local f=function (t,p)
	    local a=t..':'..p
	    if %types[t] then
	      tinsert(%u,a)
	      a='<A HREF="'..a..'">'..a..'</A>'
	    end
	    return a
	  end
  l=gsub(l,'(%w+):([^%s]+[^%]%)%s%.,!%?;:\'>])',f)
  return l
end

function wiki.urls(l,u)
  l=gsub(l,'%[%[','&lbra;')
  local f=function (r)
	    if not %u[r] then
	      tinsert(%u,r)
	      %u[r]=getn(%u)
	    end
	    return '[<A HREF="'..r..'">'..%u[r]..'</A>]'
	  end
  l=gsub(l,'%[<A HREF="(.-)">%1</A>%]',f)
  l=gsub(l,'&lbra;','[[')
  return l
end

function wiki.genhtml(v,t)
  local last,reset,depth,o,r,u='','',0,{},{},{}
  tinsert(v,{cat='-',txt=''})
  for i=1,getn(v) do
    local x,d=v[i],0
    local l=htmlize(x.txt)
    if x.cat==last and x.depth then d=x.depth end
    while d<depth do
      o[getn(o)]=o[getn(o)]..reset
      depth=depth-1
    end
    if x.depth then d=x.depth end
    local p=''
    while d>depth do
      if x.cat=='Q' then
	l='<PRE>'..l
	reset='</PRE>'
      else
	p='<'..x.cat..'L>'..p
      end
      depth=depth+1
    end
    if x.cat=='H' then
      l='<HR SIZE='..(strlen(l)-3)..'>'
    elseif x.cat=='U' or x.cat=='O' then
      l='<LI>'..l
      reset='</'..x.cat..'L>'
    elseif x.cat=='D' then
      l='<DT>'..x.aux..'<DD>'..l
      reset='</DL>'
    elseif x.cat=='-' and l=='' then
      if last=='-' then l='<P>' else l='<BR>' end
    end
    l=p..l
    if x.cat=='Q' then
      l=wiki.links(l,u)
    else
      l=wiki.refs(l,t,r)
      l=wiki.links(l,u)
      l=wiki.urls(l,u)
      l=wiki.brackets(l)
      l=wiki.hilites(l)
    end
    tinsert(o,l)
    last=x.cat
  end
  return o,r,u
end

-- call this to enable lookup of titles and page numbers
function wiki.LoadTitles(f)
  local t={}
  for i,v in linesplit(f) do
    local n=strfind(v,'\t')
    if n then
      local a,b=tonumber(strsub(v,1,n-1)),strsub(v,n+1)
      t[a],t[strlower(b)]=b,a
    end
  end
  return t
end

-- convert string with wiki markup into a html representation
function wiki.Render(text,titles)
  return wiki.genhtml(map(linesplit(text),wiki.linetype),titles)
end
