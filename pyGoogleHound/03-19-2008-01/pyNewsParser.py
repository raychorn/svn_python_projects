import os
import sys
from vyperlogix import _psyco

# Rules:
# "" means "

_end_digest_symbol = "End of Python-3000 Digest"
_end_message = "------------------------------"
_beginning_list_trailer = "_______________________________________________"
_end_digest_header = "----------------------------------------------------------------------"
_beginning_digest = "*******************************************"
_message_colon = "Message:"

isCloakingEmails = True

rx = '\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b'

_psyco.importPsycoIfPossible()

fname = 'python-3000-news.CSV'

def cleanMessage(msg):
    while (len(msg[0]) == 0):
        del msg[0]
    bools = [l.startswith(_message_colon) for l in msg]
    for b in bools:
        if b:
            break
        else:
            del msg[0]
    if (isCloakingEmails):
        for l in msg:
            pass

def handleMessage():
    global _message
    cleanMessage(_message)
    print '\n'
    print '#'*80
    print '\n'.join(_message)
    print '@'*80
    print '\n\n'
    _message = []

fHand = open(fname,'r')
lines = [l.strip() for l in fHand.readlines()]
print 'len(lines)=(%s)' % len(lines)
#print lines[0]
toks = lines[0].split(',')
#print 'len(toks)=(%s)' % len(toks)
_message = []
for l in lines[1:]:
    if (l == _end_message):
        handleMessage()
    else:
        #print '+' # ' (%s)' % l
        _message.append(l)
fHand.close()
print 'len(lines)=(%s)' % len(_message)
print 'END-OF-PROCESS!'
