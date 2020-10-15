#!/usr/bin/env python
import os
from os import path
from itertools import imap
import string

scramble_table = dict((chr(i), chr(i | 0x80)) for i in xrange(256)) 

scramble_translation = string.maketrans(''.join(chr(i) for i in xrange (256)), ''.join(chr(i|0x80) for i in xrange(256))) 
def scramble_translate(line): 
    return string.translate(line, scramble_translation) 

def _scrambleLine(line):
    return ''.join(imap(scramble_table.__getitem__, line))

def scrambleLine(line):
    return ''.join( [scramble_table[c] for c in line] )

def descrambleLine(line):
    return ''.join( [chr(ord(c) & 0x7f) for c in line] )

def scrambleFile(fname,action=1):
    if (path.exists(fname)):
        try:
            f = open(fname, "r")
            fname = '.'.join(fname.split('.')[:2])
            if (action == 1):
                ff = open(fname + '.scrambled', "w")
                ff.write('\r\n'.join([scramble_translate(l) for l in f]))
            elif (action == 0):
                ff = open(fname + '.descrambled', "w")
                ff.write('\r\n'.join([descrambleLine(l) for l in f]))
            f.close()
            ff.close()
        except Exception, details:
            print 'ERROR :: (%s)' % details
    else:
        print 'WARNING :: Missing file "%s" - cannot continue.' % fname

def __scrambleFile(fname,action=1):
    if (path.exists(fname)):
        try:
            f = open(fname, "r")
            toks = fname.split('.')
            while (len(toks) > 2):
                toks.pop()
            fname = '.'.join(toks)
            if (action == 1):
                _fname = fname + '.scrambled'
            elif (action == 0):
                _fname = fname + '.descrambled'
            if (path.exists(_fname)):
                os.remove(_fname)
            ff = open(_fname, "w+")
            if (action == 1):
                for l in f:
                    ff.write(scrambleLine(l))
            elif (action == 0):
                for l in f:
                    ff.write(descrambleLine(l))
        except Exception, details:
            print 'ERROR :: (%s)' % details
        finally:
            f.close()
            ff.close()
    else:
        print 'WARNING :: Missing file "%s" - cannot continue.' % fname

def _scrambleFile(fname,action=1):
    if (path.exists(fname)):
        try:
            f = open(fname, "r")
            toks = fname.split('.')
            while (len(toks) > 2):
                toks.pop()
            fname = '.'.join(toks)
            if (action == 1):
                _fname = fname + '.scrambled'
            elif (action == 0):
                _fname = fname + '.descrambled'
            if (path.exists(_fname)):
                os.remove(_fname)
            ff = open(_fname, "w+")
            #gc.disable()
            for l in f:
                s = ''
                for ch in l:
                    if (action == 1):
                        z = chr(ord(ch) | 0x80)
                    elif (action == 0):
                        z = chr(ord(ch) & 0x7f)
                    s += z
                ff.write(s)
            #gc.enable()
        except Exception, details:
            print 'ERROR :: (%s)' % details
        finally:
            f.close()
            ff.close()
    else:
        print 'WARNING :: Missing file "%s" - cannot continue.' % fname
