#!/usr/bin/env python

from itertools import imap 
import string
import psyco

def scramble(line): 
    s = '' 
    for c in line: 
        s += chr(ord(c) | 0x80)
    return s 

def scramble_listcomp(line): 
    return ''.join([chr(ord(c) | 0x80) for c in line]) 

def scramble_gencomp(line): 
    return ''.join(chr(ord(c) | 0x80) for c in line) 

def scramble_map(line): 
    return ''.join(map(chr, map(0x80.__or__, map(ord,line)))) 

def scramble_imap(line): 
    return ''.join(imap(chr, imap(0x80.__or__,imap(ord,line)))) 

scramble_table = dict((chr(i), chr(i | 0x80)) for i in xrange(255)) 

def scramble_dict(line): 
     s = '' 
     for c in line: 
         s += scramble_table[c] 
     return s 

def scramble_dict_map(line): 
     return ''.join(map(scramble_table.__getitem__, line)) 

def scramble_dict_imap(line): 
     return ''.join(imap(scramble_table.__getitem__, line)) 

scramble_translation = string.maketrans(''.join(chr(i) for i in xrange (256)), ''.join(chr(i|0x80) for i in xrange(256))) 
def scramble_translate(line): 
    return string.translate(line, scramble_translation) 

if __name__=='__main__': 
    funcs = [scramble, scramble_listcomp, scramble_gencomp, 
             scramble_map, scramble_imap, 
             scramble_dict, scramble_dict_map, scramble_dict_imap, scramble_translate] 
    s = 'abcdefghijklmnopqrstuvwxyz' * 100 
    assert len(set(f(s) for f in funcs)) == 1 
    from timeit import Timer
    before = {}
    after = {}
    setup = "import __main__; line = %r" % (s) 
    for name in (f.__name__ for f in funcs): 
        timer = Timer("__main__.%s(line)" % name, setup)
        before[name] = min(timer.repeat(3,1000))
        print '%s:\t%.3f' % (name, before[name])
    print '\nNow with Psyco...'
    print 'psyco.bind(scramble)...'
    psyco.bind(scramble)
    print 'psyco.bind(scramble_listcomp)...'
    psyco.bind(scramble_listcomp)
    print 'psyco.bind(scramble_gencomp)...'
    psyco.bind(scramble_gencomp)
    print 'psyco.bind(scramble_map)...'
    psyco.bind(scramble_map)
    print 'psyco.bind(scramble_imap)...'
    psyco.bind(scramble_imap)
    print 'psyco.bind(scramble_dict)...'
    psyco.bind(scramble_dict)
    print 'psyco.bind(scramble_dict_map)...'
    psyco.bind(scramble_dict_map)
    print 'psyco.bind(scramble_dict_imap)...'
    psyco.bind(scramble_dict_imap)
    print 'psyco.bind(scramble_translate)...'
    psyco.bind(scramble_translate)
    for name in (f.__name__ for f in funcs): 
        timer = Timer("__main__.%s(line)" % name, setup) 
        after[name] = min(timer.repeat(3,1000))
        diff = before[name] - after[name]
        xdiff = before[name] / after[name]
        adverb = (diff > 0) and 'faster' or 'slower'
        print '%s:\t%.3f\t%.3f\t%.3fx %s' % (name, after[name],diff,xdiff,adverb)



