import os, sys

import logging

import win32serviceutil

from vyperlogix import misc

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix.enum.Enum import Enum

class ServiceActions(Enum):
    none = 0
    stop = 2^1
    start = 2^2
    restart = 2^3
    status = 2^4
is_service_action_valid = lambda value:(ServiceActions(value) is not None)

_valid_service_actions = ['stop','start','restart','status']

def service_info(action, machine, service):
    if (action == 'stop') or (action == ServiceActions.stop): 
        win32serviceutil.StopService(service, machine)
        print '%s stopped successfully' % service
    elif (action == 'start') or (action == ServiceActions.start): 
        win32serviceutil.StartService(service, machine)
        print '%s started successfully' % service
    elif (action == 'restart') or (action == ServiceActions.restart): 
        win32serviceutil.RestartService(service, machine)
        print '%s restarted successfully' % service
    elif (action == 'status') or (action == ServiceActions.status):
        if win32serviceutil.QueryServiceStatus(service, machine)[1] == 4:
            print "%s is running normally" % service 
        else:
            print "%s is *not* running" % service 

if __name__ == '__main__':
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
	    '--machine=?':'windows machine name.',
	    '--service=?':'windows service name.',
	    '--action=?':'one of %s' % ([n.name for n in ServiceActions._items_]),
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

	if (misc.isString(_machine_name)) and (len(_machine_name) > 0):
	    if (misc.isString(_service_name)) and (len(_service_name) > 0):
		if (_service_action) and (_service_action != ServiceActions.none):
		    service_info(_service_action, _machine_name, _service_name)
		else:
		    logging.error('Service action must be valid.')
	    else:
		logging.error('Service name cannot be blank or empty and must be a valid Windows Service Name for the Machine Name.')
	else:
	    logging.error('Machine name cannot be blank or empty and must be a valid Windows Machine Name for your Network.')
