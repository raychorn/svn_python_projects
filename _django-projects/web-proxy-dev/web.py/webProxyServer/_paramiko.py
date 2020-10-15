import os, sys
import interactive

import time

from vyperlogix import paramiko

from vyperlogix.misc import _utils

def callback(self):
    try:
        sftp = self.getSFTPClient
    
        # dirlist on remote host
        dirlist = sftp.listdir('.')
        print 'BEGIN: Dirlist.'
        for d in dirlist:
            print d
        print 'END!!! Dirlist.'
        
        responses = self.exec_command('ls -la')
        print 'BEGIN: responses.'
        for response in responses:
            print response
        print 'END!!! responses.'
    
        #sftp.open('demo_sftp_folder/README', 'w').write('This was created by demo_sftp.py.\n')
        #data = open('demo_sftp.py', 'r').read()
        #sftp.open('demo_sftp_folder/demo_sftp.py', 'w').write(data)
        #print 'created demo_sftp_folder/ on the server'
        
        ## copy the README back here
        #data = sftp.open('demo_sftp_folder/README', 'r').read()
        #open('README_demo_sftp', 'w').write(data)
        #print 'copied README back here'
        
        ## BETTER: use the get() and put() methods
        #sftp.put('demo_sftp.py', 'demo_sftp_folder/demo_sftp.py')
        #sftp.get('demo_sftp_folder/README', 'README_demo_sftp')
        
        print 'Closing sftp session.'
        sftp.close()
        print 'Closing transport.'
        self.close()
        print 'Terminate program.'
        os._exit(0)
        
    except Exception, _details:
        info_string = _utils.formattedException(details=_details)
        print info_string

logPath = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),'log')
sftp = paramiko.ParamikoSFTP('127.0.0.1',12222,'raychorn',callback=callback,auto_close=False,logPath=logPath)

print 'Sleeping...'
time.sleep(60)

print 'Force Closing sftp session.'
sftp.close()
print 'Terminate main program.'
os._exit(0)
