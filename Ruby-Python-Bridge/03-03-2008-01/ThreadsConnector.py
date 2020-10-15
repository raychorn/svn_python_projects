import threading
import Queue
import sys
import traceback
import gettext

MESSAGE_LOG          = 'log'      # Message to logger
MESSAGE_EXIT_CANCEL  = 'cancel'   # Cancel the thread
MESSAGE_EXIT_OK      = 'ok'       # .. succesfully finished
MESSAGE_EXIT_ERROR   = 'error'    # .. finished with error

# Texts are private, do not access them from other classes
TEXT_EXIT_CANCEL     = 'Operation has been cancelled by user'
TEXT_EXIT_ERROR      = 'Operation has been terminated on error'
TEXT_EXIT_OK         = 'Operation has been finished succesfully'

def dummy():
  return

class ThreadsConnectorTerminateException(Exception):
  pass

class ThreadsConnector:

  def __init__(self):
    self.messages   = Queue.Queue()
    self.running    = 1
    self.silent_ack = 0
    self.data = []
    self.callback = dummy

  def put_message(self, msg):
    self.messages.put_nowait(msg)

  def get_message(self):
    return self.messages.get_nowait()

  def cancel(self):
    self.running = 0

  def isRunning(self):
    return self.running

  def ack(self):
    if not(self.running):
      # Raise exception only once and
      # only if current thread is the cakcukations thread.
      # Check for thread is required because logger calls ack(),
      # and gui thread can call caller before calculations thread.
      if not(self.silent_ack):
        if self._thread == threading.currentThread():
          self.silent_ack = 1
          raise ThreadsConnectorTerminateException(TEXT_EXIT_CANCEL)

  def start(self, group, target, name, args, kw):
    self._thread = threading.Thread(group, self.processor, name, (target, args, kw))
    self._thread.start()

  def processor(self, conn, target, args, kw):
    try:
      target(*args)
      self.put_message([MESSAGE_EXIT_OK, TEXT_EXIT_OK])
    except ThreadsConnectorTerminateException:
      # Cancelled
      self.put_message([MESSAGE_EXIT_CANCEL, TEXT_EXIT_CANCEL])
      try:
        self.callback(self.data)
      except Exception, details:
        pass
    except:
      # All other exception
      (exc_type, exc_value, exc_traceback) = sys.exc_info()
      e_seq  = traceback.format_exception(exc_type, exc_value, exc_traceback)
      e_text = ''.join(e_seq)
      self.put_message([MESSAGE_EXIT_ERROR, TEXT_EXIT_ERROR + ' (%s) conn.__class__=(%s), target.__class__=(%s), args.__class__=(%s), kw.__class__=(%s)' % (str(e_text),str(conn.__class__),str(target.__class__),str(args.__class__),str(kw.__class__))])
    self.running = 0

def calc(connector,dummy):
  print 'calc...'
  for i in range(100, 0, -1):
    connector.data = i
    print 'calc :: (%s)' % (str(i))
    connector.ack()
    time.sleep(.2)

def calc_callback():
  print 'calc_callback !'

if __name__ == '__main__':
  conn = ThreadsConnector()
  conn.callback = calc_callback
  conn.start(None, conn, None, calc, 'calc')
  while conn.running:
    print '(INFO) :: conn.running=(%s), conn.data=(%s), conn.messages.qsize=(%s)' % (str(conn.running),str(conn.data),str(conn.messages.qsize()))
    item = None
  if (conn.messages.qsize > 0):
    item = conn.messages.get_nowait()
    print '(DONE) :: conn.running=(%s), conn.data=(%s), conn.messages.qsize=(%s), item=(%s)' % (str(conn.running),str(conn.data),str(conn.messages.qsize()),str(item))
