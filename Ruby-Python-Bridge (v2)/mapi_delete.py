import os, sys
import win32com.client
import traceback

try:
  win32com.client.gencache.EnsureDispatch ("MAPI.Session")
except Exception, details:
  print 'ERROR due to "%s".' % details
  traceback.print_exc()
  print 'Cannot continue, obviously.'
  sys.exit(-1)

def explainMessage(msg):
  s = ''
  try:
    s += '%s\n' % str(message)
  except:
    pass
  try:
    s += 'message.Subject=[%s]\n' % message.Subject
  except:
    pass
  try:
    _sender = message.Sender
    _sender_dd = getMAPIObjectAttrs(_sender)
    _s = _sender.Address
    s += 'message.Sender=[%s]\n' % _s
    for k,v in _sender_dd.iteritems():
      s += 'message.Sender.%s=[%s]\n' % (k,v)
  except Exception, details:
    print 'ERROR due to "%s".' % str(details)
  s += '\n'
  try:
    _recipients = message.Recipients
    _recipients_dd = getMAPIObjectAttrs(_recipients)
    _r = _recipients.Address
    s += 'message.Recipients=[%s]\n' % _r
    for k,v in _recipients_dd.iteritems():
      s += 'message.Recipients.%s=[%s]\n' % (k,v)
  except:
    pass
  return s

def process_message (message):
  message_d = getMAPIObjectAttrs(message)
  print "Message=[%s]" % (explainMessage(message))
  print '-'*80
  for k,v in message_d.iteritems():
    print '%s=[%s]' % (k,v)
  print '-'*80
  print '='*80
  print '\n'
  #message.Delete()

def getMAPIObjectAttrs(obj):
  d = {}
  dd = {}
  try:
    d = obj._prop_map_get_
    for k,v in d.iteritems():
      dd[k] = eval('obj.%s' % k)
  except:
    pass
  return dd

if __name__ == '__main__':
  session = win32com.client.gencache.EnsureDispatch ("MAPI.Session")
  session.Logon ()
  inbox_dd = getMAPIObjectAttrs(session.Inbox)
  messages = session.Inbox.Messages
  messages_d = getMAPIObjectAttrs(messages)
  _count = messages_d['Count']
  print 'There are %d messages in your INBOX.' % _count
  message = messages.GetFirst()
  message_d = getMAPIObjectAttrs(message)
  i = 0
  while message:
    process_message (message)
    message = messages.GetNext()
    i += 1
    if (i > min(_count,1000)):
      break