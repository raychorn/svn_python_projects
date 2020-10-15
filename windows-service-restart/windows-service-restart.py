import os
import sys

import logging
from logging import handlers

verbose = False
import imp
if (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__")):
    import zipfile
    import pkg_resources

    import re
    __regex_libname__ = re.compile(r"(?P<libname>.*)_2_7\.zip", re.MULTILINE)

    my_file = pkg_resources.resource_stream('__main__',sys.executable)
    if (verbose):
        print '%s' % (my_file)

    import tempfile
    __dirname__ = os.path.dirname(tempfile.NamedTemporaryFile().name)

    zip = zipfile.ZipFile(my_file)
    files = [z for z in zip.filelist if (__regex_libname__.match(z.filename))]
    for f in files:
        libname = f.filename
        print '1. libname=%s' % (libname)
        data = zip.read(libname)
        fpath = os.sep.join([__dirname__,os.path.splitext(libname)[0]])
        __is__ = False
        if (not os.path.exists(fpath)):
            print '2. os.mkdir("%s")' % (fpath)
            os.mkdir(fpath)
        else:
            fsize = os.path.getsize(fpath)
            print '3. fsize=%s' % (fsize)
            print '4. f.file_size=%s' % (f.file_size)
            if (fsize != f.file_size):
                __is__ = True
                print '5. __is__=%s' % (__is__)
        fname = os.sep.join([fpath,libname])
        if (not os.path.exists(fname)) or (__is__):
            print '6. fname=%s' % (fname)
            file = open(fname, 'wb')
            file.write(data)
            file.flush()
            file.close()
        __module__ = fname
        print '7. __module__=%s' % (__module__)

        if (verbose):
            print '__module__ --> "%s".' % (__module__)

        import zipextimporter
        zipextimporter.install()
        sys.path.insert(0, __module__)

    if (verbose):
        print 'BEGIN:'
        for f in sys.path:
            print f
        print 'END !!'
    
import win32serviceutil

from vyperlogix import misc

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix.enum.Enum import Enum

from vyperlogix.services import get_named_service_for_name_or_partial_name

LOG_FILENAME = './windows-service-restart.log'

logger = logging.getLogger('windows-service-restart')
handler = logging.FileHandler(LOG_FILENAME)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler) 
print 'Logging to "%s".' % (handler.baseFilename)

ch = logging.StreamHandler()
ch_format = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(ch_format)
ch.setLevel(logging.INFO)
logger.addHandler(ch)

logging.getLogger().setLevel(logging.INFO)

class ServiceActions(Enum):
    none = 0
    stop = 2^1
    start = 2^2
    restart = 2^3
    status = 2^4
    list = 2^5
is_service_action_valid = lambda value:(ServiceActions(value) is not None)

__valid_service_actions__ = [n.name for n in ServiceActions._items_ if (n.name.lower() != 'none')]

class ServiceStates(Enum):
    none = 0
    Stopped = 2^1
    Started = 2^2
__valid_service_states__ = [n.name for n in ServiceStates._items_ if (n.name.lower() != 'none')]

def service_action(action, machine, service):
    if (action == 'stop') or (action == ServiceActions.stop): 
        srvc = get_named_service_for_name_or_partial_name(machine,service,state=ServiceStates.Started)
        if (srvc):
            print 'Found "%s" and trying to Stop it.' % (srvc.Caption)
            win32serviceutil.StopService(service if (service == srvc.Caption) else srvc.Caption, machine)
            srvc = get_named_service_for_name_or_partial_name(machine,service,state=ServiceStates.Stopped)
            if (srvc):
                print '"%s" stopped successfully.' % srvc.Caption
            else:
                print '"%s" was not stopped or was not prevously started or was not properly referenced.' % service
        else:
            print '"%s" cannot be stopped because it is not Started or was not properly referenced.' % service
    elif (action == 'start') or (action == ServiceActions.start): 
        srvc = get_named_service_for_name_or_partial_name(machine,service,state=ServiceStates.Stopped)
        if (srvc):
            print 'Found "%s" and trying to Start it.' % (srvc.Caption)
            win32serviceutil.StartService(service if (service == srvc.Caption) else srvc.Caption, machine)
            srvc = get_named_service_for_name_or_partial_name(machine,service,state=ServiceStates.Started)
            if (srvc):
                print '"%s" started successfully.' % srvc.Caption
            else:
                print '"%s" was not started or was not prevously started or was not properly referenced.' % service
        else:
            print '"%s" cannot be started because it is not Stopped or was not properly referenced.' % service
    elif (action == 'restart') or (action == ServiceActions.restart): 
        srvc = get_named_service_for_name_or_partial_name(machine,service,state=ServiceStates.Started)
        if (srvc):
            print 'Found "%s" and trying to Restart it.' % (srvc.Caption)
            win32serviceutil.RestartService(service if (service == srvc.Caption) else srvc.Caption, machine)
            srvc = get_named_service_for_name_or_partial_name(machine,service,state=ServiceStates.Started)
            if (srvc):
                print '"%s" restarted successfully.' % srvc.Caption
            else:
                print '"%s" was not restarted or was not prevously started or was not properly referenced.' % service
        else:
            win32serviceutil.StartService(service if (service == srvc.Caption) else srvc.Caption, machine)
            srvc = get_named_service_for_name_or_partial_name(machine,service,state=ServiceStates.Started)
            if (srvc):
                print '"%s" started successfully.' % srvc.Caption
            else:
                print '"%s" was not started or was not prevously started or was not properly referenced.' % service
    elif (action == 'status') or (action == ServiceActions.status):
        srvc = get_named_service_for_name_or_partial_name(machine,service)
        if (srvc):
            print 'Found "%s" and trying to Query it.' % (srvc.Caption)
            if win32serviceutil.QueryServiceStatus(srvc.Caption, machine)[1] == 4:
                print '"%s" is running normally.' % srvc.Caption 
            else:
                print '"%s" is *not* running.' % srvc.Caption 
    elif (action == 'list') or (action == ServiceActions.list):
        import wmi
        c = wmi.WMI(machine)
        services = c.Win32_Service()
        if (services):
            if (service):
                srvc = get_named_service_for_name_or_partial_name(machine,service)
                if (srvc):
                    print srvc.Caption
            else:
                for s in services:
                    print s.Caption
        else:
            print 'There are no services !!!'

if (__name__ == '__main__'):
    def ppArgs():
        pArgs = [(k,args[k]) for k in args.keys()]
        pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
        pPretty.pprint()

    args = {'--help':'show some help.',
            '--verbose':'output more stuff.',
            '--debug':'debug some stuff.',
            '--machine=?':'windows machine name.',
            '--service=?':'windows service name.',
            '--action=?':'one of %s' % (__valid_service_actions__),
            '--schedule=?':'specify a schedule file.',
            '--dryrun':'scheduler crontab dryrun mode.',
            }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
        ppArgs()
    else:
        _progName = __args__.programName

        _isVerbose = __args__.get_var('isVerbose',bool,False)
        _isDebug = __args__.get_var('isDebug',bool,False)
        _isHelp = __args__.get_var('isHelp',bool,False)

        if (_isHelp):
            ppArgs()
            sys.exit()

        _machine_name = __args__.get_var('machine',misc.isString,None)
        _service_name = __args__.get_var('service',misc.isString,None)
        _service_action = __args__.get_var('action',lambda value:is_service_action_valid(value),ServiceActions.none)
        _schedule_fpath = __args__.get_var('schedule',misc.isString,None)
        _isDryrun = __args__.get_var('isDryrun',bool,False)
        
        if (os.path.exists(_schedule_fpath)) and (misc.isStringValid(_machine_name)) and (misc.isStringValid(_service_name)):
            '''
            crontab jobs must specify the windows-service-restart command when performing restart operations.
            '''
            from vyperlogix.crontab.scheduler import crontab
            crontab(_schedule_fpath,dry_run=_isDryrun,threaded=True,verbose=_isVerbose)
        else:
            print 'WARNING: Cannot establish the crontab thread due to issues with the command line options; requiring Machine Name and Service Name when wanting to run crontab jobs.'

        if (misc.isString(_machine_name)) and (len(_machine_name) > 0):
            if (_service_action) and (_service_action != ServiceActions.none):
                service_action(_service_action, _machine_name, _service_name)
            else:
                logging.error('Service action must be valid.')
        else:
            logging.error('Machine name cannot be blank or empty and must be a valid Windows Machine Name for your Network.')