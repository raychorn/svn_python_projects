# generators_factorial_2.py
# A simple factorial program using python generators with iterations
# Author: S.Prasanna

def _factorial(n):
    count = 1
    fact = 1
    while count <= n:
        yield fact
        count = count + 1
        fact = fact * count

def factorial(n):
    for i in _factorial(n):
        pass
    return i

if __name__ == "__main__":
    import cProfile
    print "Factorial program using generators."

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

    