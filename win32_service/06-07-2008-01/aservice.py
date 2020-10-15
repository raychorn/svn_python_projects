import win32service
import win32serviceutil
import win32api
import win32con

class aservice(win32serviceutil.ServiceFramework):
    _svc_name_ = "aservice"
    _svc_display_name_ = "aservice - It Does nothing"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.isAlive = True
    
    def SvcDoRun(self):
        import servicemanager
    
        while self.isAlive:
            servicemanager.LogInfoMsg("aservice - is alive and well")
            win32api.SleepEx(10000, True)
            servicemanager.LogInfoMsg("aservice - Stopped")
    
    def SvcStop(self):
        import servicemanager
        
        servicemanager.LogInfoMsg("aservice - Recieved stop signal")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.isAlive = False
    
def ctrlHandler(ctrlType):
    return True

if (__name__ == '__main__'):
    win32api.SetConsoleCtrlHandler(ctrlHandler, True)
    win32serviceutil.HandleCommandLine(aservice)
