import stackless 

from decorator import ioTimeDeco

__reason__ = 'UNKNOWN'

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

@ioTimeDeco.analyze('factorial')
def factorial(n):
    if n <= 1: 
        return 1 
    return n * call(factorial, n-1) 

def complex(a,b):
    return factorial(a)/factorial(b)

if __name__ == "__main__":
    print "Factorial program using Stackless."

    print factorial(5)
    print complex(1000,998)
    print complex(10000,9998)
    
    ioTimeDeco.ioTimeAnalysis.ioTimeAnalysisReport()
