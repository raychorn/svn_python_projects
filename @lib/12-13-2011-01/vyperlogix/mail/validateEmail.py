import re
import string

regex = r'[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}'

regex2 = '[a-zA-Z0-9._%%-]+@(?P<domain>%s)' % (regex.split('@')[-1])

from vyperlogix.misc import GenPasswd

delimiters = ''.join(list(set([chr(i) for i in xrange(33,127)]) - set(string.ascii_letters + string.digits + '-._!@#$%()^&+=`"<}*/~[{]|?>' + "'" + '\\'))) + '\n'

def validateEmail(email):
    '''Returns True if the email address is valid otherwise False.'''
    _re = re.compile(regex)
    return (_re.search(email) != None) and (email.lower() not in ['null@null.com'])

def make_email_chars_valid(email):
    '''Ensure the email address does not contain any funky Unicode chars that may result in a failed validation.'''
    _re = re.compile(regex)
    return ''.join([match.group() for match in _re.finditer(email)]).strip()

def parseEmail(email):
    '''Returns the email address parsed using a regex.'''
    _re = re.compile(regex2)
    return _re.findall(email)
