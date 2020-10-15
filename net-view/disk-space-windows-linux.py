"""
mount_list
Taste the system and return a list of mount points.
On UNIX this will return what a df will return
On DOS based systems run through a list of common drive letters and
test them to see if a mount point exists. Whether a floppy or CDROM on DOS is
currently active may present challenges.

Curtis W. Rendon 6/27/200 v.01
  6/27/2004 v.1 using df to make portable, and some DOS tricks to get active
drives. Will try chkdsk on DOS to try to get drive size as statvfs()
doesn't exist on any system I have access to...

"""
import sys,os,string
from stat import *

if (sys.platform[:3] == 'win'):
    sys.path += ['Z:\\python projects\\@lib']
else:
    import socket
    c = socket.gethostbyname_ex(socket.gethostname())[0].lower()
    if (c == 'river.magma-da.com'):
        sys.path += ['/home/sfscript/@misc/script_deployments/eggs/VyperLogixLib-1.0-py2.5.egg']
    else:
        print >>sys.stderr, 'UNKOWN Python Configuration for "%s".' % (c)

from vyperlogix.hash import lists
from vyperlogix.daemon import daemon

_isVerbose = False

def processDF_command(df_cmd='df'):
    _stderr = sys.stderr
    _stdout = sys.stdout
    fStderr = open(os.sep.join([os.path.abspath('.'),'stderr.txt']),'w')
    fStdout = open(os.sep.join([os.path.abspath('.'),'stdout.txt']),'w')
    sys.stdout = daemon.Log(fStdout)
    sys.stderr = daemon.Log(fStderr)
    def shove_line_into_rows(d,l,_def):
        i = 0
        for f in _def:
            d_rows[f] = l[i]
            i += 1
    
    df_file = os.popen(df_cmd, stderr=sys.stderr)
    df_lists = [l.strip().lower() for l in df_file.readlines() if (len(l.strip()) > 0) and (l.find('df: ') == -1)]
    d_rows = lists.HashedLists2()
    aLine = []
    _line_def = ['file_sys','disc_size','disc_used','disc_avail','disc_cap_pct','mount']
    n_line_def = len(_line_def)
    for df_list in df_lists:
        if ('filesystem' in df_list):
            continue
        if ('proc' in df_list):
            continue
        toks = df_list.split()
        if (len(toks) == n_line_def):
            file_sys,disc_size,disc_used,disc_avail,disc_cap_pct,mount = toks
            shove_line_into_rows(d_rows,aLine,_line_def)
        else:
            aLine += df_list.split()
            if (len(aLine) == n_line_def):
                file_sys,disc_size,disc_used,disc_avail,disc_cap_pct,mount = aLine
                shove_line_into_rows(d_rows,aLine,_line_def)
    sys.stderr.close()
    sys.stderr = _stderr
    sys.stdout.close()
    sys.stdout = _stdout
    return d_rows

def mount_list():
    """
    returns a list of mount points
    """

    doslist=['%s:\\' % (chr(ord('a')+n)) for n in xrange(0,26)]
    mount_list=[]

    """
    see what kind of system
    if UNIX like
        use os.path.ismount(path) from /... use df?
    if DOS like
        os.path.exists(path) for  a list of common drive letters
    """
    if (_isVerbose):
        print >>sys.stdout, 'sys.platform[:3]=%s' % (sys.platform[:3])
    if sys.platform[:3] == 'win':
        doslistlen=len(doslist)
        for apath in doslist:
            if os.path.exists(apath):
                if (_isVerbose):
                    print >>sys.stdout, 'apath=%s' % (apath)
                if os.path.isdir(apath):
                    mode = os.stat(apath)
                    try:
                        dummy=os.listdir(apath)
                        mount_list.append(apath)
                    except:
                        continue
                else:
                    continue
        return (mount_list)

    else:
        """
        AIX and SYSV are somewhat different than the GNU/BSD df, try to catch
        them. This is for AIX, at this time I don't have a SYS5 available to see
        what the sys.platform returns... CWR
        """
        if 'aix' in sys.platform.lower():
            df_file=os.popen('df')
            while True:
                df_list=df_file.readline().strip().lower()
                if not df_list:
                    break #EOF
                if 'filesystem' in df_list:
                    continue
                if 'proc' in df_list:
                    continue
                if (len(df_list) > 0):
                    file_sys,disc_size,disc_avail,disc_cap_pct,inodes,inodes_pct,mount=df_list.split()
                    mount_list.append(mount)
        else:
            d_rows = processDF_command()
            mount_list += d_rows['mount']

    return (mount_list)

def size(mount_point):
    """
    have another function that returns max,used for each...
    maybe in discmonitor
    """
    if (_isVerbose):
        print >>sys.stdout, 'sys.platform[:3]=%s' % (sys.platform[:3])
    if sys.platform[:3] == 'win':
        #dos like
        dos_cmd='dir /s '+ mount_point
        check_file=os.popen(dos_cmd)
        while True:
            check_list=check_file.readline().lower()
            if (_isVerbose):
                print >>sys.stdout, 'len(check_list)=%s' % (len(check_list))
            if not check_list:
                break #EOF
            _is_total_files_listed = 'total files listed' in check_list
            if (_isVerbose):
                print >>sys.stdout, "_is_total_files_listed=%s" % (_is_total_files_listed)
            if (_is_total_files_listed):
                check_list=check_file.readline().lower()

                _is_file_in_checklist = 'file' in check_list
                if (_isVerbose):
                    print >>sys.stdout, "_is_file_in_checklist=%s" % (_is_file_in_checklist)
                if (_is_file_in_checklist):
                    _is_bytes_in_checklist = 'bytes' in check_list
                    if (_isVerbose):
                        print >>sys.stdout, "_is_bytes_in_checklist=%s" % (_is_bytes_in_checklist)
                    if (_is_bytes_in_checklist):
                        numfile,filtxt,rawnum,junk=check_list.split(None,3)
                        total_used=string.replace(rawnum,',','')
                        #return (0,int(total_size),int(total_size))
                        #break
                check_list=check_file.readline().lower()
                _is_dir_in_checklist = 'dir' in check_list
                if (_isVerbose):
                    print >>sys.stdout, "_is_dir_in_checklist=%s" % (_is_dir_in_checklist)
                if (_is_dir_in_checklist):
                    _is_free_in_checklist = 'free' in check_list
                    if (_isVerbose):
                        print >>sys.stdout, "_is_free_in_checklist=%s" % (_is_free_in_checklist)
                    if (_is_free_in_checklist):
                        numdir,dirtxt,rawnum,base,junk=check_list.split(None,4)
                        base = base.lower()
                        multiplier=1
                        if 'mb' in base:
                            multiplier=1000000
                        if 'kb' in base:
                            multiplier=1000

                        rawnum=string.replace(rawnum,',','')
                        free_space=float(rawnum)*multiplier
                return (0,int(free_space)+int(total_used),int(total_used))
            else:
                continue
    else:
        #UNIX like
        """
        AIX and SYSV are somewhat different than the GNU/BSD df, try to catch
        them. This is for AIX, at this time I don't have a SYS5 available to see
        what the sys.platform returns... CWR
        """
        df_cmd = 'df '+ mount_point
        if 'aix' in sys.platform.lower():
            df_file=os.popen(df_cmd)
            while True:
                df_list=df_file.readline()
                if not df_list:
                    break #EOF
                dflistlower = df_list.lower()
                if 'filesystem' in dflistlower:
                    continue
                if 'proc' in dflistlower:
                    continue

            file_sys,disc_size,disc_avail,disc_cap_pct,inodes,inodes_pct,mount=df_list.split()
            return(0,int(disc_size),int(disc_size)-int(disc_avail))
        else:
            d_rows = processDF_command(df_cmd)
            return(0,int(d_rows['disc_size']),int(d_rows['disc_used']))

def main():
    mnts = mount_list()
    print(mnts)

    #for m in mnts:
        #print size(m)
        
    print '%s' % (mnts[0]), size(mnts[0])

if __name__ == '__main__':
    from vyperlogix.misc import _psyco
    
    _psyco.importPsycoIfPossible(main)
    
    main()
    