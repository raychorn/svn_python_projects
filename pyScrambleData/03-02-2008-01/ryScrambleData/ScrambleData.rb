require 'rubygems'
require 'ruby-prof'
require 'zip/ziprequire'

#require "rubyscript2exe"
#exit if RUBYSCRIPT2EXE.is_compiling?

$h = Hash.new
(0..127).select {|x| $h[x.chr] = ((x & 0x7f) | 0x80).chr}

def scramble( fname) 
    _fname = fname + ".scrambled" 
    if File.exist?(_fname) then
        File.delete(_fname)
    end
    mask = 0x8080808080808080 
    data = File.open( fname, "rb" ){|f| f.read } 
    pad = (8 - (data.size % 8)) % 8 
    data << "p" * pad 
    File.open( _fname, "wb"){|ff| 
        array = data.unpack('Q*') 
        array.map!{|x| x | mask } 
        ff.write( array.pack('Q*')[0 ... -pad] ) 
    } 
end 

def _scramble2(fname)
    f = File.new(fname, "rb")
    _fname = fname + ".scrambled"
    begin
        if File.exist?(_fname) then
            File.delete(_fname)
        end
    rescue
    end
    ff = File.new(_fname, "wb+")
    for l in f
        l.each_byte{|c| ff.write((c | 0x80).chr) }
    end
    f.close()
    ff.close()
end

def _scramble1(fname)
    f = File.new(fname, "rb")
    _fname = fname + ".scrambled"
    begin
        if File.exist?(_fname) then
            File.delete(_fname)
        end
    rescue
    end
    ff = File.new(_fname, "wb+")
    for l in f
        l.each_byte{|c| ff.write($h[c]) }
    end
    f.close()
    ff.close()
end

result = RubyProf.profile do
    scramble('reports_production.sql')
    #_scramble1('reports_production.sql')
    #_scramble2('reports_production.sql')
end

printer = RubyProf::GraphPrinter.new(result)
printer.print(STDOUT, 0)

#scramble('ScrambleData.rb')
