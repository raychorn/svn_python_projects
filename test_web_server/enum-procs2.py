from ctypes import *

psapi = windll.psapi

print "[+] PID dumper by Y"
print "[+] contact : If you know me then give me a shout"

def getListOfProcesses():
    max_array = c_ulong * 4096 # define long array to capture all the processes
    pProcessIds = max_array() # array to store the list of processes
    pBytesReturned = c_ulong() # the number of bytes returned in the array
    #EnumProcess 
    psapi.EnumProcesses(byref(pProcessIds),
                        sizeof(pProcessIds),
                        byref(pBytesReturned))

    # get the number of returned processes
    nReturned = pBytesReturned.value/sizeof(c_ulong())
    pidProcessArray = [i for i in pProcessIds][:nReturned]
    for processes in pidProcessArray:
        print "[+] Running Process PID %d" % processes 

getListOfProcesses()