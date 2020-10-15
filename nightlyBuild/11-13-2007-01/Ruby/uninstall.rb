require "rubyscript2exe"

if RUBYSCRIPT2EXE.is_compiling?
  begin
    d = Dir.entries("../dist")
  rescue
    d = []
  end

  RUBYSCRIPT2EXE.bin = ["../setup.yml"]

  d.each { |item| RUBYSCRIPT2EXE.bin.push("../dist/"+item) if ( (item != ".") && (item != "..") ) }
end

toks = RUBYSCRIPT2EXE.appdir.split('/')
toks.pop()
p = toks.join('/')

toks = p.split('/')
toks.push('bin')
p = toks.join('/')
toks.push('setupProduct.exe')
s = toks.join('/')
toks.pop()
toks.push('setup.yml')
y = toks.join('/')

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

  if (Dir.getwd() != 'c:\\DSS')
    cmd = s + ' --target=c:\\DSS\\ --yml="' + y + '" --uninstall > uninstaller-log-file.txt'
    print "Starting the Product Uninstallation Process... Please stand-by...  This may take a few minutes."

    begin
      exec(cmd)
    rescue
      print "Cannot run the Uninstaller Command."
    end
  else
      print "Please move the Uninstaller file to a different folder other than '#{Dir.getwd()}'."
  end
end
