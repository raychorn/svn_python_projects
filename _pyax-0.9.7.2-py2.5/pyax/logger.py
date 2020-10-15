"""
NOTE: An apparent bug in Python 2.4's logging library throws some errors at exit time
"""
import logging, logging.config

INSANITY = 1

class PyaxLogger(logging.Logger):

    def __init__(self, name, level=logging.NOTSET):
        logging.Logger.__init__(self, name, level)
        return
    ## END __init__

    # methods to support custom logging levels
    def insanity(self, msg, *args, **kw):
        global INSANITY
        self.log(INSANITY, msg, *args, **kw)
        return
    
    insane = insanity
