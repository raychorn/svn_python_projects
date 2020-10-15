import os, sys

__source__ = r'J:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01\dist_2.7'

__dest__ = '/downloads.vyperlogix.com/web/content/vyperlogix'

if (__name__ == '__main__'):
    from vyperlogix.ssh import sshUtils
    files = [os.sep.join([__source__,f]) for f in os.listdir(__source__)]
    aFile = files[0]
    print aFile
    sshUtils.sftp_to_host('ftp.ord1-1.websitesettings.com', 'raychorn', 'Peek@b00', aFile, __dest__, isSilent=False)
