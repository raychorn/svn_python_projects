import os, sys
import re

import sqlalchemy_models

from vyperlogix import paramiko

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.misc import ReportTheList

from vyperlogix.hash import lists

from vyperlogix.daemon.daemon import Log

from maglib.salesforce.cred import credentials
from maglib.salesforce.auth import CredentialTypes
from maglib.salesforce.auth import magma_molten_passphrase

_use_staging = False

__sf_account__ = credentials(magma_molten_passphrase,CredentialTypes.Magma_RHORN_Production)

from vyperlogix.wx.pyax.SalesForceLoginModel import SalesForceLoginModel
sf_login_model = SalesForceLoginModel(username=__sf_account__['username'],password=__sf_account__['password'])

_server_address = 'admin@64.106.247.200:22'

_target_path = 'molten_utils/monitor_ram_usage/data'

_symbol_colon_colon = '::'

i_months = [('Jan',1),('Feb',2),('Mar',3),('Apr',4),('May',5),('Jun',6),('Jul',7),('Aug',8),('Sept',9),('Oct',10),('Nov',11),('Dec',12)]

d_months = lists.HashedFuzzyLists2(dict(i_months))

__root__ = os.path.dirname(sys.argv[0])

def parse_data(data):
    toks = data.split(_symbol_colon_colon)

def eval_data(item):
    try:
        return eval(item.split(_symbol_colon_colon)[-1].strip())
    except:
        pass
    return []

def datum_as_dicts(data):
    rows = []
    _header = data[0]
    for row in data[1:]:
        d = lists.HashedFuzzyLists()
        i = 0
        for h in _header:
            d[h] = row[i] if (h.lower() != 'COMMAND'.lower()) else ' '.join(row[i:])
            i += 1
        rows.append(d)
    return rows

def get_source_id(fpath):
    anAgent = sqlalchemy_models.new_agent(conn_str)
    anAgent.add_mapper(sqlalchemy_models.Source,sqlalchemy_models.monitor_tables.ps_source)
    items = anAgent.session.query(sqlalchemy_models.Source).filter(sqlalchemy_models.Source.fpath == fpath).all()
    if (len(items) == 0):
        items = put_source(fpath)
    return items

def put_source(fpath):
    anAgent = sqlalchemy_models.new_agent(conn_str)
    anAgent.add_mapper(sqlalchemy_models.Source,sqlalchemy_models.monitor_tables.ps_source)
    anAgent.beginTransaction()
    source = sqlalchemy_models.Source()
    source.fpath = fpath
    anAgent.add(source)
    anAgent.commit()
    anAgent.flush()
    anAgent.close()
    return get_source_id(fpath)

def get_mm_from_month(month):
    s = ''
    for ch in month:
        s += ch
        if (d_months.has_key(s)):
            return d_months[s]
    return -1

def shove_rows_into_db(rows,fpath):
    src_id = -1
    isError = False
    items = get_source_id(fpath)
    if (len(items) > 0):
        src_id = items[0].id
    if (src_id > -1):
        anAgent = sqlalchemy_models.new_agent(conn_str)
        print >>logger, 'Agent using "%s".' % (conn_str)
        anAgent.add_mapper(sqlalchemy_models.PS_Aux,sqlalchemy_models.monitor_tables.ps_aux)
        anAgent.beginTransaction()
        for row in rows:
            ps_aux = sqlalchemy_models.PS_Aux()
            ps_aux.srcid = src_id
            today = _utils.getFromNativeTimeStamp(_utils.timeStamp())
            ps_aux.dt_event = today
            ps_aux.USER = row['user'][0]
            ps_aux.PID = row['pid'][0]
            ps_aux.CPU = row['%cpu'][0]
            ps_aux.MEM = row['%mem'][0]
            ps_aux.VSZ = row['vsz'][0]
            ps_aux.RSS = row['rss'][0]
            ps_aux.TTY = row['tty'][0]
            ps_aux.STAT = row['stat'][0]
            dd = _utils.only_digits(row['start'][0])
            month = row['start'][0].replace(dd,'')
            dd = int(dd)
            mm = get_mm_from_month(month)
            yyyy = today.year
            tttt = row['time'][0]
            tttt_toks = tttt.split(':')
            tttt = ':'.join(['%02d' % (int(t)) for t in tttt_toks])
            mm_dd_yyyy_tttt = '%04d-%02d-%02dT%s' % (yyyy,mm,dd,tttt)
            ps_aux.START_TIME = _utils.getFromNativeTimeStamp(mm_dd_yyyy_tttt,format=_utils._formatShortTimeStr())
            ps_aux.COMMAND = row['command'][0]
            anAgent.add(ps_aux)
            s = str(ps_aux)
            print >>logger, 'Added %s' % (s)
            if (len(anAgent.lastError) > 0):
                print >>logger, anAgent.lastError
                isError = True
            print >>logger, '='*80
        anAgent.commit()
        if (len(anAgent.lastError) > 0):
            print >>logger, anAgent.lastError
            isError = True
        anAgent.flush()
        if (len(anAgent.lastError) > 0):
            print >>logger, anAgent.lastError
            isError = True
        anAgent.close()
        if (len(anAgent.lastError) > 0):
            print >>logger, anAgent.lastError
            isError = True
    else:
        print >>logger, '%s :: WARNING: Cannot determine the source id from "%s".' % (misc.funcName(),fpath)
        
    return isError

def callback(self):
    try:
        sftp = self.getSFTPClient
    
        dirlist = ListWrapper(sftp.listdir('.'))
        toks = _target_path.split('/')
        for t in toks:
            i = dirlist.findFirstContaining(t,returnIndexes=True)
            if (i > -1):
                sftp.chdir(dirlist[i])
                _cwd = sftp.getcwd()
                print >>logger, _cwd
                dirlist = ListWrapper(sftp.listdir('.'))
            else:
                print >>logger, 'WARNING: Cannot retrieve data from the server because index of "%s" is %d in %s.' % (t,i,dirlist)
                sys.exit(1)
                break
            
        print >>logger, '%s !' % (_cwd)
        dirlist = ListWrapper(sftp.listdir(_cwd))
        
        dirlist.sort()
        ReportTheList.reportTheList(dirlist, 'Data Files')
        
        for f in dirlist:
            _f = '/'.join([_cwd,f])
            _data = self.read(sftp,_f)
            _datum = [eval_data(item) for item in _data.split('\n') if (item.find(_symbol_colon_colon) > -1)]
            _rows = datum_as_dicts(_datum)
            isError = shove_rows_into_db(_rows,_f)
            if (not isError):
                print >>logger, 'Removing the host file "%s".' % (_f)
                sftp.remove(_f)
            else:
                print >>logger, 'Cannot Remove the host file "%s" due to errors and possible local data loss.' % (_f)
    
    except Exception, _details:
        info_string = _utils.formattedException(details=_details)
        print >>logger, info_string

def _main():
    _re = re.compile(r"(?P<username>[a-zA-Z0-9]*)@(?P<ip>(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)):(?P<port>[0-9]*)")
    result = _re.findall(_server_address)
    username, ip, ip1,ip2,ip3,ip4, port = result[0]
    
    logPath = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),'log')
    sftp = paramiko.ParamikoSFTP(ip,int(port),username,None,callback=callback,logPath=logPath)

def main():
    if (sys.platform != 'win32'):
        from vyperlogix.process import Popen
        
        _found_count = 0
        _seeking = os.path.join(__root__,'%s' % (os.path.basename(sys.argv[0])))
	
	print >>logger, '_seeking is "%s".' % (_seeking)
        
        shell, commands, tail = ('sh', ['ps -ef | grep python'], '\n')
    
	_text = ''
	
        a = Popen.Popen(shell, stdin=Popen.PIPE, stdout=Popen.PIPE)
        t = Popen.recv_some(a)
	_text += t
        #print '(**)', t,
        toks = t.split(_seeking)
        if (len(toks) > 1):
            _found_count += len(toks)-1
        for cmd in commands:
            Popen.send_all(a, cmd + tail)
            t = Popen.recv_some(a)
	    _text += t
            #print '(**)', t,
            toks = t.split(_seeking)
            if (len(toks) > 1):
                _found_count += len(toks)-1
        Popen.send_all(a, 'exit' + tail)
        a.wait()
        
        #print
        #print _found_count
        if (_found_count > 1):
            print 'Already running - cannot run again.'
            sys.exit(1)
	else:
	    _main()

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)
    
    conn_str = sqlalchemy_models.get_conn_str()
    
    from vyperlogix.misc import Args

    args = {'--help':'show some help.',
            '--verbose':'output more stuff.',
            '--test':'delete the specified keypath.',
            '--server=?':'the address of the server (admin@64.106.247.200:22).',
            }
    _argsObj = Args.Args(args)

    _progName = _argsObj.programName

    if (_argsObj.vars.isVerbose):
        print '_argsObj=(%s)' % str(_argsObj)

    if (_argsObj.vars.isHelp):
        Args.ppArgs(_argsObj)
    else:
	_stderr = sys.stderr
	_stdout = sys.stdout
	try:
	    if (_use_staging):
		sf_login_model.isStaging = True
		sf_login_model.perform_login(end_point=sf_login_model.get_endpoint(sf_login_model.sfServers['sandbox']))
	    else:
		sf_login_model.isStaging = False
		sf_login_model.perform_login(end_point=sf_login_model.get_endpoint(sf_login_model.sfServers['production']))
	finally:
	    sys.stderr = _stderr
	    sys.stdout = _stdout
	if (sf_login_model.isLoggedIn) and (not _argsObj.vars.isTest):
	    _server_address = _argsObj.vars.server if (_argsObj.vars.server) else _server_address
	    _dataPath = os.path.dirname(sys.argv[0])

	    _logPath = os.path.join(_dataPath,'log')
            _utils._makeDirs(_logPath)
            fname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
            fLog = open(os.path.join(_logPath,'%s_%s.log' % (fname,_utils.timeStampForFileName())),'a')
            logger = Log(fLog)
            _stdout = sys.stdout
            sys.stdout = logger
            
            try:
		main()
            finally:
                sys.stdout = _stdout
    