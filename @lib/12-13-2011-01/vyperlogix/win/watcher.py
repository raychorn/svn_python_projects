import wmi
import pythoncom

from vyperlogix.misc import threadpool

_Q_ = threadpool.ThreadQueue(5, isDaemon=False)

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

@threadpool.threadify(_Q_)
def watch_process(*args):
    """args[0]: if function is executed on its own thread
        args[1]: name of the process to wathc_for
        args[2]: notification type, Creation or Deletion
    """
    if args[0] == True:
        pythoncom.CoInitialize()

    process_name = args[1]

    c = wmi.WMI()
    watcher = c.watch_for (
        notification_type=args[2],
        wmi_class="Win32_Process",
        delay_secs=2,
        Name=process_name
    )
    print process_name
    process_created = watcher()
    print process_created

@threadpool.threadify(_Q_)
def watch_usb(*args):
    '''This function has not been tested however it may prove useful.'''
    c = wmi.WMI () 
    usb_watcher = c.watch_for ( 
        notification_type="Deletion", 
        wmi_class="Win32_DiskDrive", 
        delay_secs=2, 
        InterfaceType="USB" 
    ) 

    while True: 
        usb_removed = usb_watcher() # can optionally timeout 
        print usb_removed.PNPDeviceID 

if __name__ == '__main__':
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

    #watch_process(True,'calc.exe','Creation',)
    #watch_process(True,'notepad.exe','Creation',)
