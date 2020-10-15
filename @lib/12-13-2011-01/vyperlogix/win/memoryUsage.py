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

def getCPULoad():
    import wmi
    i=0
    load=0
    #get proc load, currently only first core for some reason
    try:
        c=wmi.WMI("localhost") #for WMI access
        for p in c.Win32_Processor():
            load += p.LoadPercentage
            i=i+1
        return(load/i)
    except:
        pass
    return -1

def getFreeRam():
    import wmi
    #get total ram and ram available
    try:
        c = wmi.WMI("localhost") #for WMI access
        info = c.Win32_OperatingSystem()[0]
        totalRam = float(info.TotalVisibleMemorySize)
        freeRam = float(info.FreePhysicalMemory)
        return ((freeRam/totalRam)*100.0),freeRam,totalRam
    except:
        pass
    return -1,-1,-1

def toBiggestBytes(n):
    #returns a string where n is in the largest logical measure possible
    i=0 #counter
    units=[" bytes","kb","mb","gb","tb"]
    while(n>=1024):
        n=n/1024
        i=i+1
    return(str(n)+units[i])
