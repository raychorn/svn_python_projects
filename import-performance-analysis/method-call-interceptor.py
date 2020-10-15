import sys
from vyperlogix.decorators import ioTimeAnalysis
from vyperlogix.mixins.ioTimeAnalysis import IoTimeAnalysis

class Foo(IoTimeAnalysis):
    def __init__(self):
        self.__is__ = True
        
    def tis(self):
        return self.__is__
    
    def delay(self,secs):
        import time
        time.sleep(secs)

if (__name__ == '__main__'):
    IoTimeAnalysis.__is__ = True
    if (IoTimeAnalysis.__is__):
        ioTimeAnalysis.ioTimeAnalysis.__init__()
    f = Foo()
    print f.tis()
    f.delay(5)
    if (IoTimeAnalysis.__is__):
        ioTimeAnalysis.ioTimeAnalysis.ioTimeAnalysisReport(fOut=sys.stdout)
