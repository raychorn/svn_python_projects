import threading
import Queue
import sys
import traceback

def dummy():
  return

class QueuedThreadingModelTerminateException(Exception):
  pass

class QueuedThreadingModel:

  def __init__(self):
    self.q   = Queue.Queue()
    self.e_text = []
    self.target = None
    self.running = 0
    self.num_worker_threads = 1
    self.itemCount = 0

  def put_message(self, msg):
    self.q.put_nowait(msg)
    self.itemCount += 1

  def cancel(self):
    self.running = 0

  def isRunning(self):
    return self.running

  def getErrors(self):
    return self.e_text

  def start(self, target, num_threads=1):
    self.target = target
    self.running = 1
    self.num_worker_threads = num_threads
    for i in xrange(self.num_worker_threads):
      t = threading.Thread(target=self.worker)
      t.setDaemon(False)
      t.start()

  def worker(self):
    try:
      while (self.running == 1):
        if (self.q.empty() == False):
          item = self.q.get()
          self.target(self,item)
          self.q.task_done()
    except Exception, details:
      self.e_text.append(details)
    self.running = 0

def testProc(model,item):
  print 'testProc() :: (%s) :: item=(%s)' % (model.itemCount,str(item))

if __name__ == '__main__':
  model = QueuedThreadingModel()
  model.start(testProc,10)
  for i in xrange(20):
    model.put_message([i,i+1,i+2,i+3,i+4])
  model.q.join()
  print 'model.getErrors()=(%s)' % str(model.getErrors())
  model.cancel()
