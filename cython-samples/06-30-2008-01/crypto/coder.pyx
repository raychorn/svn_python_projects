def encode(data):
    return ''.join([chr(ord(ch)|128) for ch in data])

def decode(data):
    return ''.join([chr(ord(ch)&127) for ch in data])

if (__name__ == '__main__'):
    print '(c). Copyright 1990-2014, Vyper Logix Corp., All Rights Reserved., Published under Creative Commons License (http://creativecommons.org/licenses/by-nc/3.0/) restricted to non-commercial educational use only., See also: http://www.VyperLogix.com and http://python2.near-by.info for details.'
