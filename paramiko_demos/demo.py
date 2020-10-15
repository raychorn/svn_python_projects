import os, sys
import interactive

from vyperlogix import paramiko

def callback(self):
    self.channel.invoke_shell()
    interactive.interactive_shell(self.channel)

logPath = os.path.abspath(os.path.dirname(sys.argv[0]))
sftp = paramiko.ParamikoSFTP('127.0.0.1',12222,'raychorn',None,callback=callback,logPath=logPath)