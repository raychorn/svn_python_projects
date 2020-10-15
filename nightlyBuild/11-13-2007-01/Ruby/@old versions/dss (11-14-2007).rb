require "rubyscript2exe"
RUBYSCRIPT2EXE.bin = ["dss.zip"]

t = RUBYSCRIPT2EXE.exedir("dss.zip")
d = Dir.entries(RUBYSCRIPT2EXE.exedir)
if File.exists?(t)
  print 'dss.zip found !\n'
else
  print "dss.zip not found at (", t, ")\n"
end
print "d=(", d.inspect, ")\n"

t = RUBYSCRIPT2EXE.appdir("dss.zip")
d = Dir.entries(RUBYSCRIPT2EXE.appdir)
if File.exists?(t)
  print 'dss.zip found !\n'
else
  print "dss.zip not found at (", t, ")\n"
end
print "d=(", d.inspect, ")\n"

toks = RUBYSCRIPT2EXE.appdir.split('/')
toks.pop()
p = toks.join('/')
begin
  d = Dir.entries(p)
  print "p=(", p, ")\n"
  print "d=(", d.inspect, ")\n"
rescue
end

toks = p.split('/')
toks.push('bin')
p = toks.join('/')
toks.push('dss.zip')
z = toks.join('/')
begin
  d = Dir.entries(p)
  print "p=(", p, ")\n"
  print "d=(", d.inspect, ")\n"
rescue
end

if File.exists?(z)
  print "(+) dss.zip found at (", z, ")\n"
else
  print "(+) dss.zip not found at (", z, ")\n"
end

t = RUBYSCRIPT2EXE.userdir("dss.zip")
if File.exists?(t)
  print 'dss.zip found !\n'
else
  print "dss.zip not found at (", t, ")\n"
end
begin
  d = Dir.entries(RUBYSCRIPT2EXE.userdir)
  print "d=(", d.inspect, ")\n"
rescue
end
