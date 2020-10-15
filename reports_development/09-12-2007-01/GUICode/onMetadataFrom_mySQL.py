import logging
import time
import gettext
_ = gettext.gettext

def process(connector, progress):
  logger = logging.getLogger(__name__)
  progress.set(0, 100)
  for i in range(100, 0, -1):
    logger.info (_('Countdown value is %i'), i)
    progress.tick()
    connector.ack() # can be ommitted in this program
    time.sleep(.2)
  logger.info(_('Done!'))

if __name__ == '__main__':
  logging.basicConfig()
  logging.getLogger().setLevel(logging.INFO)
  class dummy:
    def ack(self):
      pass
    def set(self, a, b):
      pass
    def tick(self):
      pass
  process(dummy(), dummy())
