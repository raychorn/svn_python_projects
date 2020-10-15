def scramble(fname)
    f = File.new(fname, "r")
    toks = fname.split('.')
    while (toks.length > 2)
        toks.pop()
    end
    _fname = toks.join('.') + ".descrambled"
    File.exist?(_fname) if File.delete(_fname)
    ff = File.new(_fname, "w+")
    begin
        for l in f
            l.each_byte{|c| ff.putc((c.to_i & 0x7f).chr) }
        end
    rescue
    end
    f.close()
    ff.close()
end

scramble('ScrambleData.rb.scrambled')
