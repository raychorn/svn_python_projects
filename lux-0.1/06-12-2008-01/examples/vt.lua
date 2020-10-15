#!/usr/bin/env lux

-- experiments with virtual table dispatch
-- 31/01/2001 jcw@equi4.com

local vtable = {
  _tag_ = newtag(),
  times = function (self,i) return self.v * i end,
  hello = function () return "hi!" end,
}

settagmethod(vtable._tag_, "index",
  function (x,i) return %vtable[i] end)

t = {}
settag(t, vtable._tag_)

t.v=111

assert(t.v == 111)
assert(t.none == nil)
assert(t:times(222) == 24642)
assert(t.hello() == "hi!")
print('OK')
