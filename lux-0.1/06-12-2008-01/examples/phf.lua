#!/usr/bin/env lux

-- generate perfect hash function, see DDJ Feb 2001 pp. 151
-- 03/02/2001 jcw@equi4.com

-- try a specified row displacement
function faildisp(r,b,k,d)
  local i
  for i=1,getn(r) do
    local v=r[i]
    if k[d+v-b+1] then return 1 end
  end
  for i=1,getn(r) do
    local v=r[i]
    k[d+v-b+1]=v
  end
end
-- first-fit decreasing method
function ffdm(S,t)
  local rows,last,curr,i={},-1
  for i=1,getn(S) do
    local v=S[i]
    if last~=floor(v/t) then
      last=floor(v/t)
      curr={}
      tinsert(rows,curr)
    end
    tinsert(curr,v)
  end
  sort(rows,function (a,b) return getn(b)<getn(a) end)
  local o,k={},{}
  for i=1,getn(rows) do
    local r=rows[i]
    local b=floor(r[1]/t)*t
    local d=b-r[1]
    while faildisp(r,b,k,d) do d=d+1 end
    tinsert(o,d)
  end
  return getn(k)-getn(S),o,k
end
-- try a couple of sizes to find the best variant
function findphf(S)
  sort(S) -- just in case
  local t,g,b,i=1,1e6,-1 -- XXX 1e6?
  while t*t<=S[getn(S)] do t=t+1 end
  for i=t,t+3 do
    local n=ffdm(S,i)
    if n<g then g,b=n,i end
  end
  return b,ffdm(S,b)
end
-- join vector with separator string
function join(v,s)
  s=s or " "
  local r,i=""
  for i=1,getn(v) do
    if i>1 then r=r..s end
    r=r..(v[i] or "nil")
  end
  return r
end

S={0,3,4,7,10,13,15,18,19,21,22,24,26,29,30,34}
print("\n  S=["..join(S,",").."]")

local t,n,o,k=findphf(S)

print(format([[
  -- H(K) returns the perfect hash for given key
  local R=[%s]
  function H(K) do
    return %%R[floor(K/%d)]+imod(K,%d)
  end
  -- V(K) returns perfect hash if key is valid, else nil
  local C=[%s]
  function V(K) do
    local i=H(K)
    return %%C[i]==K and i
  end
]], join(o,","), t, t, join(k,",")))
