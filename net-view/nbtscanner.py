# Gather known Netbios machine names with their IP addresses.

import os, sys
import re

from vyperlogix import paramiko

from vyperlogix import misc
from vyperlogix.misc  import _utils
from vyperlogix.misc import ReportTheList
from vyperlogix.lists import ListWrapper

from vyperlogix.hash import lists

from vyperlogix.daemon.daemon import Log

from vyperlogix.process import Popen

from vyperlogix.products import keys

StringIO = _utils.stringIO

_nbtscan = 'nbtscan'

_re = re.compile(r"\A%s(.*)\.exe\Z" % (_nbtscan))

_ipconfig = 'ipconfig /all'

_re_ip = re.compile(r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b")

_default_gateway = 'Default Gateway'

_hosts_lines = []
d_hosts_lines_ip = lists.HashedLists2()
d_hosts_lines_host = lists.HashedLists2()

def _password():
    return keys._decode('7369736B6F403736363024626F6F')

def contains_ip_address(a,b):
    x = _re_ip.search(a)
    return x is not None

def sftp_callback(self):
    try:
        sftp = self.getSFTPClient
    
        _fpath = '/etc'
        files = ListWrapper.ListWrapper(['/'.join([_fpath,f]) for f in sftp.listdir(_fpath) if (f == 'hosts')])
        i = files.findFirstContaining('hosts')
	if (i > -1):
	    line_no = 0
	    _vectors = []
	    fname = files[i]
	    data = sftp.open(fname, 'r').read()
	    lines = [_l for _l in [l.strip() for l in data.split('\n')]]
	    _lines = []
	    for l in lines:
		is_ip = _re_ip.search(l)
		if (is_ip is not None):
		    toks = l.split()
		    _ip = toks[0]
		    ip_lookup = d_hosts_lines_ip[_ip]
		    if (ip_lookup is not None):
			toks[1] = ip_lookup
			del d_hosts_lines_ip[_ip]
			if (len(_vectors) == 0):
			    _vectors.append(line_no)
			else:
			    _vectors[0] = line_no
		    _lines.append('\t'.join(toks))
		else:
		    _lines.append(l)
		line_no += 1
	    line_no = _vectors[0] if (len(_vectors) > 0) else len(_lines)-1
	    line_no += 1
	    for k,v in d_hosts_lines_ip.iteritems():
		_lines.insert(line_no,'%s\t%s' % (k,v))
	    data = '\n'.join(_lines)
	    sftp.open(fname, 'w').write(data)
    except Exception, _details:
        info_string = _utils.formattedException(details=_details)
        print info_string

def main():
    if (sys.platform == 'win32'):
	_path = os.path.abspath('.')
	files = [os.path.join(_path,f) for f in os.listdir(_path) if (_re.match(f))]
	
	if (len(files) > 0):
	    buf = StringIO()
	    shell = Popen.Shell([_ipconfig],isExit=True,isWait=True,isVerbose=True,fOut=buf)
	    lines = ListWrapper.ListWrapper([l for l in buf.getvalue().split('\n') if (len(l.strip()) > 0) and (l.find(' : ') > -1)])
	    matches = [(l,_re_ip.search(l).group(),_re_ip.search(l)) for l in lines if (_re_ip.search(l)) and (l.find(_default_gateway) > -1)]
	    #if (_isVerbose):
		#ReportTheList.reportTheList(matches,_ipconfig,fOut=sys.stdout)
		
	    if (len(matches) > 0):
		_cmd = files[0]
		buf = StringIO()
		shell = Popen.Shell(['"%s" %s/24' % (_cmd,matches[0][1])],isExit=True,isWait=True,isVerbose=True,fOut=buf)
		lines = ListWrapper.ListWrapper([l for l in buf.getvalue().split('\n') if (len(l.strip()) > 0)])
		matches = [(ListWrapper.ListWrapper(l.split()),_re_ip.search(l).group(),_re_ip.search(l)) for l in lines if (_re_ip.search(l)) and (l.find(_cmd) == -1)]
		for m in matches:
		    i = m[0].findFirstMatching('',callback=contains_ip_address)
		    if (i > -1):
			try:
			    name = m[0][i+1]
			except:
			    name = ''
			machine_name = name.split('\\')[-1]
			if (len(machine_name) > 0):
			    _ip = m[0][0]
			    t = (_ip,machine_name)
			    _hosts_lines.append(t)
			    d_hosts_lines_ip[_ip] = machine_name
			    d_hosts_lines_host[machine_name] = _ip
		logPath = os.path.join(_path,'log')
		_utils._makeDirs(logPath)
		for aHost in _host_list:
		    try:
			ip,port = aHost.split(':')
			port = int(port)
		    except:
			ip,port = aHost,22
		    sftp = paramiko.ParamikoSFTP(ip,port,'root',_password(),callback=sftp_callback,logPath=logPath)
		#if (_isVerbose):
		    #ReportTheList.reportTheList(matches,_cmd,fOut=sys.stdout)
		    
		if (_isVerbose):
		    print 'END: %s' % (_utils.timeStampApache())
		    print '='*80
	    else:
		print 'ERROR: Cannot locate %s from the %s command.' % (_default_gateway,_ipconfig)
	else:
	    print 'ERROR: Cannot continue without the %s program that must reside in the default directory which is %s.' % (_nbtscan,_path)
    else:
	print 'ERROR: Requires Win32 OS.'

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)
    
    from vyperlogix.misc import Args
    from vyperlogix.misc import PrettyPrint

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--hosts=?':'list of Linux hosts with which to sync netbios hosts.',
	    }
    _argsObj = Args.Args(args)

    _progName = _argsObj.programName
    _isVerbose = False
    try:
	if _argsObj.booleans.has_key('isVerbose'):
	    _isVerbose = _argsObj.booleans['isVerbose']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_isVerbose = False
    
    _isHelp = False
    try:
	if _argsObj.booleans.has_key('isHelp'):
	    _isHelp = _argsObj.booleans['isHelp']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_isHelp = False
	
    _host_list = []
    try:
	if _argsObj.arguments.has_key('hosts'):
	    _host_list += _argsObj.arguments['hosts'].split(',')
	    _host_list = list(set(_host_list))
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	
    if (_isHelp):
	ppArgs()
    else:
	_dataPath = os.path.dirname(sys.argv[0])
	main()
 