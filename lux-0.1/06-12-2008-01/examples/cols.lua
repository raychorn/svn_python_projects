#!/usr/bin/env lux

-- experiments with column-wise structures
-- 31/01/2001 jcw@equi4.com

View = {
  _tag_ = newtag(),
  -- construct a new view with specified fields
  create = function (self,...)
    v = { n=0, fields=arg }
    for i=1,getn(arg) do rawset(v,i,{}) end
    return settag(v,self._tag_)
  end,
  -- insert args as row at specified position
  insert = function (self,pos,...)
    for i=1,self:cols() do tinsert(self[i],pos,arg[i]) end
    rawset(self,"n",self:size()+1)
  end,
  -- append args as row at end
  append = function (self,...)
    for i=1,self:cols() do tinsert(self[i],arg[i]) end
    rawset(self,"n",self:size()+1)
  end,
  -- delete specified row
  delete = function (self,pos)
    for i=1,self:cols() do tremove(self[i],pos) end
    rawset(self,"n",self:size()-1)
  end,
  -- return specified row
  getrow = function (self,i)
    r = {}
    for j=1,self:cols() do tinsert(r,self[j][i]) end
    return r
  end,
  -- set specified row to new values
  setrow = function (self,i,r)
    for j=1,self:cols() do self[j][i]=r[j] end
  end,
  -- return the number of rows
  size = function (self)
    return self.n
  end,
  -- return the number of columns
  cols = function (self)
    return getn(self.fields)
  end,
  -- dump info about this view and its contents
  dump = function (self)
    print("size",self:size(),"cols",self:cols())
    hdump(self.fields)
    for i=1,self:size() do
      write("  ",i,":\t")
      hdump(self:getrow(i))
    end
  end,
}
-- define tag behavior
settagmethod(View._tag_,"index",
  function (x,i) return %View[i] end)
settagmethod(View._tag_,"settable",View.setrow)
-- horizontal dump
function hdump(t)
  s="("
  for i=1,getn(t) do
    write(s,t[i])
    s=","
  end
  write(")\n")
end
-- vertical dump
function vdump(t)
  for i=1,getn(t) do
    print("#" .. i .. ": " .. t[i])
  end
end
-- raw table dump
function rdump(t)
  for i,v in t do
    print(i .. " =", v)
  end
end

view = View:create('name','age','shoesize')
view:append('john',19,44)
view:append('ray',81,41)
print "=================="
view:dump()
print "=================="
rdump(view)
print "=================="
view[2]={'billie',9,25}
view:dump()

print "OK"
