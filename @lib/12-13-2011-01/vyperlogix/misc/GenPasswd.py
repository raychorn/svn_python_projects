import string
from random import choice

chars_printable = string.letters + string.digits + string.punctuation

chars_intuitive = ''.join(list(set(chars_printable)-set('`iouvOwW0"\'')))

_chars_numerics = _chars_friendly = ([chr(ch) for ch in xrange(ord('0'),ord('9')+1)])

_chars_friendly = _chars_friendly = ([chr(ch) for ch in xrange(ord('a'),ord('z')+1)] + [chr(ch) for ch in xrange(ord('A'),ord('Z')+1)] + [chr(ch) for ch in xrange(ord('0'),ord('9')+1)])

chars_friendly = ''.join(list(set(_chars_friendly)-set('iIlLoOuUvV01')))

_chars_friendly_alpha_only = ''.join(list(set(_chars_friendly)-set(_chars_numerics)-set('iIlLoOuUvV01')))

def GenPasswd(length=8, chars=chars_printable, uniquely=False):
    '''Use string.printable'''
    pwd = []
    _s = set()
    s = chars
    for i in xrange(length):
        if (uniquely):
            s = ''.join(list(set(chars) - set(pwd)))
        pwd.append(choice(s))
    return ''.join(pwd)

def GenPasswdIntuitive(uniquely=False):
    return GenPasswd(length=choice(xrange(10,30)),chars=chars_intuitive,uniquely=uniquely)

def GenPasswdFriendly(maxlength=10,uniquely=False):
    return GenPasswd(length=maxlength,chars=chars_friendly,uniquely=uniquely)

def GenPasswdFriendlyAlphas(maxlength=10,uniquely=False):
    return GenPasswd(length=maxlength,chars=_chars_friendly_alpha_only,uniquely=uniquely)
