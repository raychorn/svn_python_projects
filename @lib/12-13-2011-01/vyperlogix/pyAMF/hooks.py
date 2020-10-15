import os, sys
from vyperlogix.misc import _utils
from vyperlogix import misc
from vyperlogix.hash import lists
import logging

_metadata = lists.HashedLists2()

def data_hook(data_path):
    global _metadata
    logging.info('%s.1 :: %s' % (misc.funcName(),data_path))
    if (os.path.exists(data_path)):
        logging.info('%s.2 :: %s' % (misc.funcName(),data_path))
        _metadata['_data_path'] = None
        _metadata['_data_path'] = data_path if (sys.platform[:3] != 'win') else data_path.replace('/',os.sep)
    return data_path

