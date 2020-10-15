import os, sys
import datetime
import random

from vyperlogix.products import keys

from vyperlogix import misc
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.misc import _utils

from vyperlogix.hash import lists

from vyperlogix.pypi import packages

import logging

from vyperlogix import oodb

from vyperlogix.daemon.daemon import Log
from vyperlogix.daemon.daemon import CustomLog
from vyperlogix.logging import standardLogging

_dbx_name = lambda dbx_path, object_name:os.sep.join([dbx_path,'%s.dbx' % (object_name)])
dbx_name = lambda object_name:_dbx_name(_data_path,object_name)

s_section = 'Vyper-SEO'

s_last_run = 'Last_Run'
s_next_run = 'Next_Run'

def set_session_var(section, name, value): 
    dbx_db = oodb.PickledFastCompressedHash2(dbx_name(section))
    try:
        dbx_db[name] = value
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        logging.error(info_string)
    finally:
        dbx_db.sync()
        dbx_db.close()

def get_session_var(section, name): 
    dbx_db = oodb.PickledFastCompressedHash2(dbx_name(section))
    try:
        value = dbx_db[name]
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        logging.error(info_string)
    finally:
        dbx_db.close()
    return value

def bump_version(d):
    if (d.has_key('version')):
        vers = d['version']
        toks = vers.split('.')
        if (len(toks) < 3):
            toks.append('1')
        else:
            try:
                n = int(toks[-1]) + 1
                if (n > 999):
                    n = 0
                    m = int(toks[-2]) + 1
                    toks[-2] = '%d' % (m)
                toks[-1] = '%d' % (n)
            except:
                toks[-1] = '1'
        d['version'] = '.'.join(toks)

def stamp_this_run():
    s = _utils.timeSeconds()
    set_session_var(s_section,s_last_run,s)
    t = _utils.getFromDateTimeStr(_utils.timeStamp(s))
    delay = random.random() * 3600
    next_run = t + datetime.timedelta(seconds=delay)
    set_session_var(s_section,s_next_run,_utils.timeSecondsFromTimeStamp(next_run))

def main(logging):
    _url = 'http://pypi.python.org'

    url = '%s/pypi?%%3Aaction=login' % (_url)
    username = 'raychorn'
    password = keys._decode('7065656B61623030')

    _last_run = get_session_var(s_section,s_last_run)
    if (isinstance(_last_run,list)) and (len(_last_run) == 0):
        _last_run = 0.0
    
    info_string = '1.0 _last_run = %s' % (_last_run)
    logging.warning(info_string)
    
    _is_running = False
    if (_last_run == 0.0):
        _is_running = True
        stamp_this_run()
    else:
        next_run = get_session_var(s_section,s_next_run)
        t = _utils.getFromDateTimeStr(_utils.timeStamp(next_run))
        x = t - _utils.today_localtime()
        _is_running = x.seconds < 0
        if (_is_running):
            stamp_this_run()
        info_string = '1.1 next_run = %s' % (next_run)
        logging.warning(info_string)
    
    info_string = '1.2 _is_running = %s' % (_is_running)
    logging.warning(info_string)
    
    if (_is_running):
        _packages = packages.get_packages(url,username,password,logging=logging)

        info_string = '1.3 _packages = %s' % (_packages)
        logging.warning(info_string)
    
        pkg = None
        _is_targeting = False

        info_string = '1.4 _is_targeting = %s' % (_is_targeting)
        logging.warning(info_string)

        if (_is_targeting):
            pkgs = [p for p in _packages if (p[-1] == 'pyRuby-Python-Bridge')]

            info_string = '1.5 pkgs = %s' % (pkgs)
            logging.warning(info_string)

            if (len(pkgs) > 0):
                pkg = pkgs[0]
        if (pkg is None):
            try:
                pkg = random.sample(_packages,1)
                pkg = tuple(pkg[0])
                
                info_string = '1.6 pkg = %s' % (pkg)
                logging.warning(info_string)
            except Exception, e:
                info_string = 'WARNING: %s' % (_utils.formattedException(details=e))
                logging.warning(info_string)
        if (pkg is not None):
            try:
                packages.edit_a_package(_url,pkg,username,password,callback=bump_version)
            except Exception, e:
                info_string = 'WARNING: %s' % (_utils.formattedException(details=e))
                logging.warning(info_string)
        else:
            info_string = 'ERROR: Cannot retrieve a package that has not been identified.'
            logging.error(info_string)

if (__name__ == '__main__'):
    name = _utils.getProgramName()
    fpath=os.path.dirname(sys.argv[0])
    _log_path = _utils.safely_mkdir_logs(fpath=fpath)
    _log_path = _utils.safely_mkdir(fpath=_log_path,dirname=_utils.timeStampLocalTimeForFileName(delimiters=('_'),format=_utils.formatDate_MMDDYYYY_dashes()))
    _data_path = _utils.safely_mkdir(fpath=fpath,dirname='dbx')

    logFileName = os.sep.join([_log_path,'%s.log' % (name)])

    print '(%s) :: logFileName=%s' % (_utils.timeStampLocalTime(),logFileName)

    _stdOut = open(os.sep.join([_log_path,'stdout.txt']),'w')
    _stdErr = open(os.sep.join([_log_path,'stderr.txt']),'w')
    _stdLogging = open(logFileName,'w')

    sys.stdout = Log(_stdOut)
    sys.stderr = Log(_stdErr)
    _logLogging = CustomLog(_stdLogging)

    standardLogging.standardLogging(logFileName,_level=logging.WARNING,console_level=logging.WARNING,isVerbose=True)

    _logLogging.logging = logging # echos the log back to the standard logging...
    logging = _logLogging # replace the default logging with our own custom logging...

    main(logging)
