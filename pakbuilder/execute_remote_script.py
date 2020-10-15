from vyperlogix.misc import _utils

def do_remote_cmd(bash_script,__sftp__=None,logger=None,__terminate__=None):
    lines = []
    try:
        sname = '%s%scomparefiles.sh' % (os.path.expanduser('~'),os.sep)
        fOut = open(sname,'w')
        print >>fOut, bash_script
        fOut.flush()
        fOut.close()

        sname_dest = '~/%s' % (os.path.basename(sname))

        sftp = __sftp__()
        client = sftp.getSFTPClient
        client.put(sname, sname_dest, callback=__callback__)

        sftp = __sftp__()
        cmd = 'ls -la %s' % (sname_dest)
        responses = sftp.exec_command(cmd)
        logger.info(cmd)
        logger.info('\n'.join(responses))
        lines = [l for l in responses if (l.find('cannot access') > -1) or (l.lower().find('no such file or directory') > -1)]
        if (len(lines) > 0):
            logger.warning('Camnnot continue unless "%s" exists and it should under programmatic control however this is not the case.' % (sname_dest))
            __terminate__()

        sftp = __sftp__()
        cmd = '%s %s %s' % (sname_dest,fname,wrapper_conf_backup_name)
        responses = sftp.exec_command(cmd)
        lines = responses[0].split('\n') if (misc.isIterable(responses)) else responses.split('\n')
        lines = [l.strip() for l in lines if (len(l.strip()) > 0)]
        logger.info(cmd)
        logger.info('\n'.join(responses))
    except Exception, ex:
        logger.exception(_utils.formattedException(details=ex))

    return lines