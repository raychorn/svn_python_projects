import os,sys

import win32net
import win32api

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.process.Popen import Shell

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

_allowed_user_list = ['rhorn']

_delay = 10

_commands = '''rundll32.exe user32.dll, LockWorkStation
'''

try:
    user = win32net.NetUserGetInfo(win32net.NetGetAnyDCName(), win32api.GetUserName(), 1)
    _username = user['name']
except:
    user = {'name':win32api.GetUserName()}
    _username = user['name']
    

def __lock_the_workstation():
    from vyperlogix.win import SendKeys
    SendKeys.SendKeys("""{LWIN}{PAUSE 0.5}{TAB}{TAB}{PAUSE 0.5}{RIGHT}{PAUSE 0.5}{DOWN}{DOWN}{PAUSE 0.5}{ENTER}""")

def _lock_the_workstation(fout):
    if (fout):
        print >> fout, '%s :: LockWorkStation !!!' % (misc.funcName())
    try:
	_fname = _utils.tempFile(__args__.progID)+'.cmd'
        _c = '%s'%(_commands)
	_utils.writeFileFrom(_fname,_c)
        if (fout):
            print >> fout, '%s :: _c=%s' % (misc.funcName(),_c)
        Shell(_fname,isExit=True,isWait=False,fOut=fout)
    except:
        info_string = _utils.formattedException(details=e)
        if (fout):
            print >>_fout, info_string

def lock_the_workstation(fout):
    import random
    import time
    from vyperlogix.win import workstation
    random.seed()
    _count = 0
    _delay_total = 0
    is_locked = workstation.workstation_is_locked()
    while (not is_locked):
	_lock_the_workstation(fout)
	num = random.randint(0,_delay)
	time.sleep(num)
	_delay_total += num
	_count += 1
	is_locked = workstation.workstation_is_locked()
        if (fout):
            print >> fout, '%s :: is_locked=%s, _count=%s, _delay_total=%s' % (misc.funcName(),is_locked,_count,_delay_total)
	if (not is_locked) and ( (_count > 10) or (_delay_total > 60) ):
	    __lock_the_workstation()
	    _count = 0
	    _delay_total = 0

_is_lock_workstation_required = False

def should_workstation_be_locked():
    global _is_lock_workstation_required
    
    try:
	_fpath = os.path.dirname(__file__)
    except:
	_fpath = os.getcwd()
    __fpath = _fpath
    _fpath = _utils.safely_mkdir_logs(_fpath)
    _fname = os.path.join(_fpath,os.path.splitext(os.path.basename(_fpath))[0]+'_%s.log'%(_utils.timeStampForFileName()))
    _fout = open(_fname,'a+')
    try:
	print >> _fout, str(user)
	print >> _fout, '%s :: name="%s", _allowed_user_list="%s".' % (misc.funcName(),_username,_allowed_user_list)
	if (_username not in _allowed_user_list):
	    lock_the_workstation(_fout)
	else:
	    print >> _fout, '%s :: Expected User has logged-in...' % (misc.funcName())
    except Exception, e:
	_is_lock_workstation_required = True
	info_string = _utils.formattedException(details=e)
	print >>_fout, info_string
    if (_is_lock_workstation_required):
	lock_the_workstation(_fout)
    _fout.flush()
    _fout.close()

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
	    '--profiler':'use profiler.',
	    '--allowed=?':'''list of comma-separated usernames that are allowed to login in the form of a regular Python list "['user1','user2']".''',
	    '--delay=?':'number of seconds to delay at most such as "10".',
	    }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_value_ = __args__.__vars__['allowed']
	if (_value_ != []):
	    _allowed_user_list = _value_
	    del _value_
	_value_ = __args__.__vars__['delay']
	if (_value_ != []):
	    _delay = _value_
	    del _value_
	if (__args__._isProfiler):
	    import cProfile
	    cProfile.run('should_workstation_be_locked()')
	else:
	    should_workstation_be_locked()
	
        
