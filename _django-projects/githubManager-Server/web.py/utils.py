import re
import os, sys
import tempfile

import json

from vyperlogix.enum import Enum

from vyperlogix.misc import ObjectTypeName

class Options(Enum.Enum):
    none = 0
    installer = 1
    uninstaller = 2

class RegexMatches(Exception):
    pass

class CustomJSONENcoder(json.JSONEncoder):
    def default(self, o):
        from vyperlogix.misc import ObjectTypeName
        obj = {'__class__':ObjectTypeName.typeClassName(o)}
        try:
            for k,v in o.__dict__.iteritems():
                obj[k] = v
        except AttributeError:
            if (ObjectTypeName.typeClassName(o) == 'file'):
                obj['name'] = o.name
                obj['mode'] = o.mode
            else:
                pass
            pass
        return obj

def __make_it_noninteractive__(package,option=Options.none):
    '''
export DEBIAN_FRONTEND=noninteractive
apt-get -q -y install package

export DEBIAN_FRONTEND=noninteractive
apt-get -q -y --purge remove package
    '''
    __fname__ = tempfile.NamedTemporaryFile().name

    fHandle = open(__fname__,'w')
    __verb__ = 'install' if (option == Options.installer) else '--purge remove' if (option == Options.uninstaller) else ''
    if (len(__verb__) > 0):
        print >> fHandle, 'export DEBIAN_FRONTEND=noninteractive'
        print >>fHandle, 'apt-get -q -y %s %s' % (__verb__,package)
    fHandle.flush()
    fHandle.close()
    
    return fHandle.name

def make_noninteractive_installer(package):
    return __make_it_noninteractive__(package,option=Options.installer)

def make_noninteractive_uninstaller(package):
    return __make_it_noninteractive__(package,option=Options.uninstaller)

def handle_noninteractive_actions(sftp,package,log_all_callback=None,logger=None,exception=None):
    __re__ = re.compile(r".*\sgit\W\scommand\snot\sfound", re.MULTILINE)
    responses = sftp.exec_command(package)
    matches = [__re__.search(r) for r in responses]
    log_all_callback(responses) if (callable(log_all_callback)) else None
    if any(matches):
        script_fname = make_noninteractive_installer(package)
        logger.info('make_noninteractive_installer --> "%s".' % (script_fname))

        __remote_dir__ = '/root'
        __remote__ = 'install-%s-noninteractive.sh' % (package)
        try:
            __sftp__ = sftp.getSFTPClient
            __sftp__.chdir(__remote_dir__)
            __cwd__ = __sftp__.getcwd()
            assert __cwd__ == __remote_dir__, 'WARNING: Cannot continue this way...'
            __sftp__.put(script_fname, __remote__, callback=None, confirm=True)
            logger.info('remote make_noninteractive_installer --> "%s".' % (__remote__))
        except:
            logger.exception('Failed to upload "%s".' % (__remote__))
        
        if (os.path.exists(script_fname)):
            os.remove(script_fname)

        responses = sftp.exec_command('chmod +x %s' % (__remote__))
        log_all_callback(responses) if (callable(log_all_callback)) else None

        responses = sftp.exec_command(__remote__)
        log_all_callback(responses) if (callable(log_all_callback)) else None
        
        __sftp__.remove(__remote__)

        responses = sftp.exec_command(package) # determine if git has been installed ?
        matches = [__re__.search(r) for r in responses]
        log_all_callback(responses) if (callable(log_all_callback)) else None
        if any(matches):
            if (exception):
                try:
                    raise exception('Cannot use %s, cannot install or it is missing.' % (package))
                except:
                    raise ValueError('Not able to raise the proper exception due to some kind of malfunction.')

def handle_command(sftp,command,regex=None,log_all_callback=None,return_matches=False):
    responses = sftp.exec_command(command)
    log_all_callback(responses) if (callable(log_all_callback)) else None
    if (ObjectTypeName.typeName(regex) == '_sre.SRE_Pattern'):
        matches = [regex.search(r) for r in responses]
        if any(matches):
            if (not return_matches):
                raise RegexMatches('Regex matches !!!')
            
    return responses if (not return_matches) else tuple([responses,matches])

def socks_proxy_off(proxyHandle):
    import time
    import socket
    from vyperlogix.sockets.proxies.socks import socks
    
    socks._defaultproxy = proxyHandle.__default_proxy_before__
    socket.socket = proxyHandle.__socket_socket_before__
    
    time.sleep(5)

def socks_proxy_on(proxyHandle):
    import socket
    from vyperlogix.sockets.proxies.socks import socks

    socks._defaultproxy = proxyHandle.__default_proxy_after__
    socket.socket = proxyHandle.__socket_socket_after__

