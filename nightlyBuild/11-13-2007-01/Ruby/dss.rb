require "rubyscript2exe"

if RUBYSCRIPT2EXE.is_compiling?
  begin
    d = Dir.entries("../dist")
  rescue
    d = []
  end

  RUBYSCRIPT2EXE.bin = ["../dss.zip","../setup.yml","uninstall.exe"]

  d.each { |item| RUBYSCRIPT2EXE.bin.push("../dist/"+item) if ( (item != ".") && (item != "..") ) }
end

#print "RUBYSCRIPT2EXE.bin.inspect=", RUBYSCRIPT2EXE.bin.inspect + "\n"

#print "RUBYSCRIPT2EXE.is_compiling?=(#{RUBYSCRIPT2EXE.is_compiling?})\n"

#print "RUBYSCRIPT2EXE.is_compiled?=(#{RUBYSCRIPT2EXE.is_compiled?})\n"

toks = RUBYSCRIPT2EXE.appdir.split('/')
toks.pop()
p = toks.join('/')

toks = p.split('/')
toks.push('bin')
p = toks.join('/')
toks.push('dss.zip')
z = toks.join('/')
toks.pop()
toks.push('setupProduct.exe')
s = toks.join('/')
toks.pop()
toks.push('setup.yml')
y = toks.join('/')

if File.exists?(z)
  #print "(+) dss.zip found at (#{z})\n"
else
  print "(+) dss.zip not found at (#{z})\n"
end

if File.exists?(s)
  #print "(+) setupProduct.exe found at (#{s})\n"
else
  print "(+) setupProduct.exe not found at (#{s})\n"
end

if RUBYSCRIPT2EXE.is_compiled?
  begin
    d = Dir.entries(p)
  rescue
    d = []
  end

  #d.each { |item| print "(+) :: #{p}/#{item}\n" }
  
  #print "Current Dir is '#{Dir.getwd()}'."
  
  if (Dir.getwd() != 'c:\\DSS')
    cmd = s + ' --target=c:\\DSS\\ --yml="' + y + '" --zipPath="' + z + '" > installer-log-file.txt'
    #print "cmd=(#{cmd})"
    print "Starting the Product Setup Process... Please stand-by...  This may take a few minutes."

    begin
      exec(cmd)
    rescue
      print "Cannot run the Setup Command."
    end
  else
      print "Please move the Installer file to a different folder other than '#{Dir.getwd()}'."
  end

#  Dir.chdir('c:\\DSS\\rails\\reports')
#  cmd = 'mongrel_start.cmd'
#  begin
#    system(cmd)
#  rescue
#    print "Cannot run the Mongrel Command."
#  end
end
