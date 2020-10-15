import threading
from socket import *
import time

from vyperlogix import misc

f_out = open('%s.txt' % (__file__.split('.')[0]), mode='w', buffering=1)

a = 0
b = 0
c = ""
d = ""
a_cnt = b_cnt = c_cnt = d_cnt = e_cnt = f_cnt = g_cnt = h_cnt = i_cnt = 0

def fprintf(msg):
    print msg
    print >> f_out, msg

def ScanLow():
    global a_cnt
    global c

    fprintf('BEGIN: %s' % (misc.funcName()))
    for i in xrange(0, 1000):  
        s = socket(AF_INET, SOCK_STREAM)  
        fprintf('%s :: scanning %s:%d' % (misc.funcName(),TargetIP,i))
        result = s.connect_ex((TargetIP, i))  

        if(result == 0) :  
            c = "Port %d: OPEN\n" % (i,)  

        s.close()  
        a_cnt += 1
    fprintf('END!  %s' % (misc.funcName()))

def ScanHigh():
    global b_cnt
    global d

    fprintf('BEGIN: %s' % (misc.funcName()))
    for i in xrange(1001, 2000):  
        s = socket(AF_INET, SOCK_STREAM)  
        fprintf('%s :: scanning %s:%d' % (misc.funcName(),TargetIP,i))
        result = s.connect_ex((TargetIP, i))  

        if(result == 0) :  
            d = "Port %d: OPEN\n" % (i,)  

        s.close()  
        b_cnt += 1
    fprintf('END!  %s' % (misc.funcName()))

def ScanHigh2():
    global c_cnt
    global d

    fprintf('BEGIN: %s' % (misc.funcName()))
    for i in xrange(2001, 10000):  
        s = socket(AF_INET, SOCK_STREAM)  
        fprintf('%s :: scanning %s:%d' % (misc.funcName(),TargetIP,i))
        result = s.connect_ex((TargetIP, i))  

        if(result == 0) :  
            d = "Port %d: OPEN\n" % (i,)  

        s.close()  
        c_cnt += 1
    fprintf('END!  %s' % (misc.funcName()))

def ScanHigh3():
    global d_cnt
    global d

    fprintf('BEGIN: %s' % (misc.funcName()))
    for i in xrange(10001, 20000):  
        s = socket(AF_INET, SOCK_STREAM)  
        fprintf('%s :: scanning %s:%d' % (misc.funcName(),TargetIP,i))
        result = s.connect_ex((TargetIP, i))  

        if(result == 0) :  
            d = "Port %d: OPEN\n" % (i,)  

        s.close()  
        d_cnt += 1
    fprintf('END!  %s' % (misc.funcName()))

def ScanHigh4():
    global e_cnt
    global d

    fprintf('BEGIN: %s' % (misc.funcName()))
    for i in xrange(20001, 30000):  
        s = socket(AF_INET, SOCK_STREAM)  
        fprintf('%s :: scanning %s:%d' % (misc.funcName(),TargetIP,i))
        result = s.connect_ex((TargetIP, i))  

        if(result == 0) :  
            d = "Port %d: OPEN\n" % (i,)  

        s.close()  
        e_cnt += 1
    fprintf('END!  %s' % (misc.funcName()))

def ScanHigh5():
    global f_cnt
    global d

    fprintf('BEGIN: %s' % (misc.funcName()))
    for i in xrange(30001, 40000):  
        s = socket(AF_INET, SOCK_STREAM)  
        fprintf('%s :: scanning %s:%d' % (misc.funcName(),TargetIP,i))
        result = s.connect_ex((TargetIP, i))  

        if(result == 0) :  
            d = "Port %d: OPEN\n" % (i,)  

        s.close()  
        f_cnt += 1
    fprintf('END!  %s' % (misc.funcName()))

def ScanHigh6():
    global g_cnt
    global d

    fprintf('BEGIN: %s' % (misc.funcName()))
    for i in xrange(40001, 50000):  
        s = socket(AF_INET, SOCK_STREAM)  
        fprintf('%s :: scanning %s:%d' % (misc.funcName(),TargetIP,i))
        result = s.connect_ex((TargetIP, i))  

        if(result == 0) :  
            d = "Port %d: OPEN\n" % (i,)  

        s.close()  
        g_cnt += 1
    fprintf('END!  %s' % (misc.funcName()))

def ScanHigh7():
    global h_cnt
    global d

    fprintf('BEGIN: %s' % (misc.funcName()))
    for i in xrange(50001, 60000):  
        s = socket(AF_INET, SOCK_STREAM)  
        fprintf('%s :: scanning %s:%d' % (misc.funcName(),TargetIP,i))
        result = s.connect_ex((TargetIP, i))  

        if(result == 0) :  
            d = "Port %d: OPEN\n" % (i,)  

        s.close()  
        h_cnt += 1
    fprintf('END!  %s' % (misc.funcName()))

def ScanHigh8():
    global i_cnt
    global d

    fprintf('BEGIN: %s' % (misc.funcName()))
    for i in xrange(60001, 65535):  
        s = socket(AF_INET, SOCK_STREAM)  
        fprintf('%s :: scanning %s:%d' % (misc.funcName(),TargetIP,i))
        result = s.connect_ex((TargetIP, i))  

        if(result == 0) :  
            d = "Port %d: OPEN\n" % (i,)  

        s.close()  
        i_cnt += 1
    fprintf('END!  %s' % (misc.funcName()))

Target = raw_input("Enter Host To Scan:")
TargetIP = gethostbyname(Target)

fprintf("Start Scan On Host %s" % (TargetIP))
Start = time.time()

threading.Thread(target = ScanLow).start()
threading.Thread(target = ScanHigh).start()
threading.Thread(target = ScanHigh2).start()
threading.Thread(target = ScanHigh3).start()
threading.Thread(target = ScanHigh4).start()
threading.Thread(target = ScanHigh5).start()
threading.Thread(target = ScanHigh6).start()
threading.Thread(target = ScanHigh7).start()
threading.Thread(target = ScanHigh8).start()

e = a_cnt + b_cnt + c_cnt + d_cnt + e_cnt + f_cnt + g_cnt + h_cnt + i_cnt

while(e < 65535):
    fprintf('Sleeping... (%2.2f%%)' % ((e/65535)*100.0))
    time.sleep(1)
    e = a_cnt + b_cnt + c_cnt + d_cnt + e_cnt + f_cnt + g_cnt + h_cnt + i_cnt

End = time.time() - Start
fprintf(c)
fprintf(d)
fprintf(End)

f_out.flush()
f_out.close()
