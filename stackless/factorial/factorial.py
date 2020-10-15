import stackless 

def call_wrapper(f, args, kwargs, result_ch): 
    try:
        result_ch.send(f(*args, **kwargs)) 
    except TaskletExit, e:
        pass
    # ... should also catch and forward exceptions ... 

def call(f, *args, **kwargs): 
    result_ch = stackless.channel() 
    stackless.tasklet(call_wrapper)(f, args, kwargs, result_ch) 
    return result_ch.receive() 

def factorial(n): 
    if n <= 1: 
        return 1 
    return n * call(factorial, n-1) 

if __name__ == "__main__":
    import cProfile
    print "Factorial program using Stackless."

    from vyperlogix.misc import ioTimeAnalysis
    
    reason = '5!'
    ioTimeAnalysis.initIOTime(reason)
    ioTimeAnalysis.ioBeginTime(reason)
    print "%s = %s" % (reason,factorial(5)) 
    ioTimeAnalysis.ioEndTime(reason)
    
    cProfile.run('factorial(5)')
    
    reason = '1000! / 998!'
    ioTimeAnalysis.initIOTime(reason)
    ioTimeAnalysis.ioBeginTime(reason)
    print "%s = %s" % (reason,factorial(1000)/factorial(998)) 
    ioTimeAnalysis.ioEndTime(reason)

    cProfile.run('factorial(1000)/factorial(998)')
    
    reason = '10000! / 9998!'
    ioTimeAnalysis.initIOTime(reason)
    ioTimeAnalysis.ioBeginTime(reason)
    print "%s = %s" % (reason,factorial(10000)/factorial(9998)) 
    ioTimeAnalysis.ioEndTime(reason)

    cProfile.run('factorial(10000)/factorial(9998)')
    
    ioTimeAnalysis.ioTimeAnalysisReport()
