import re
import os,sys

import subprocess

import logging, logging.handlers

__renice_level__ = -19

__pid__ = 'PID'
__item__ = '__item__'
__command__ = 'COMMAND'

__psaux__ = 'ps aux'.split()

__renice__ = 'renice %d %d'

__sample_command_line__ = '''/Applications/VirtualBox.app/Contents/MacOS/../Resources/VirtualBoxVM.app/Contents/MacOS/VirtualBoxVM --comment Ubuntu 11.04 Desktop i386 (jRuby) #2 (09-02-2011a) --startvm 1d190423-6b50-4f11-973a-a7416c0e1ba6 --no-startvm-errormsgbox'''

__re_vmid = re.compile(r"--startvm\s(?P<uuid>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})")

__re_comment = re.compile(r"--comment\s(?P<comment>.*?)(?P<trash>(?=\s--))")

isUsingWindows = (sys.platform.lower().find('win') > -1) and (os.name.lower() == 'nt')
isUsingMacOSX = (sys.platform.lower().find('darwin') > -1) and (os.name.find('posix') > -1) and (not isUsingWindows)
isUsingLinux = (sys.platform.lower().find('linux') > -1) and (os.name.find('posix') > -1) and (not isUsingWindows) and (not isUsingMacOSX)

class CustomLogHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
    def emit(self, record):
        print >> sys.stderr, record.message

if (__name__ == '__main__'):
    logging.basicConfig(filename='log.txt',level=logging.DEBUG)
    logger = logging.getLogger()

    logging.handlers.SysLogHandler = CustomLogHandler
    custHandler = logging.handlers.SysLogHandler()
    custHandler.setLevel(logging.INFO)
    
    logger.addHandler(custHandler)

    if (isUsingMacOSX or isUsingLinux):
        p = subprocess.Popen(__psaux__, stdout=subprocess.PIPE)
        out, err = p.communicate()
        lines = out.split('\n')
        logger.debug('err=%s' % (err))
        _header = lines[0].split()
        _lines_ = []
        for item in lines[1:]:
            _d_ = {}
            toks = item.split()
            if (len(toks) > 0):
                for tok in _header[0:-1]:
                    _d_[tok] = toks[0]
                    del toks[0]
                _d_[_header[-1]] = ' '.join(toks)
                _d_[__item__] = item
            _lines_.append(_d_)
        if (err is None):
            try:
                for aLine in _lines_:
                    if (aLine.has_key(__command__)) and (aLine.has_key(__pid__)):
                        logger.debug(aLine[__command__])
                        results_vmid = __re_vmid.findall(aLine[__command__])
                        logger.debug('results_vmid=%s' % (results_vmid))
                        results_comment = __re_comment.findall(aLine[__command__])
                        logger.debug('results_comment=%s' % (results_comment))
                        if (len(results_vmid) > 0) and (len(results_comment) > 0):
                            _renice_ = __renice__ % (__renice_level__,int(aLine[__pid__]))
                            _renice_ = _renice_.split()
                            print >>sys.stdout, ' '.join(_renice_), ' --> ', aLine[__command__]
                            p = subprocess.Popen(_renice_, stdout=subprocess.PIPE)
                            out, err = p.communicate()
                            if (not err is None):
                                logger.warning('%s failed with "%s".' % (_renice_,err))
                            pass
            except Exception, ex:
                import traceback
                logger.warning('Cannot understand what just happened but it was not good because %s at %s.' % (str(ex),traceback.format_exception(*sys.exc_info())))
        else:
            logger.error('Something went wrong because: %s' % (err))
    else:
        # http://stackoverflow.com/questions/1632234/python-list-running-processes-64bit-windows ?!?
        logger.error('Cannot run this program using Windows, check back for an update.')
