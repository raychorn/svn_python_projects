from vyperlogix.misc import ObjectTypeName
from vyperlogix.stackless.framework.events import EventHandler

class Switch(EventHandler.EventHandler):
    def __init__(self,initialState=0,*outputs):
        EventHandler.EventHandler.__init__(self,*outputs)
        self.state = initialState

    def processMessage(self,val):
        print "%s :: Setting input to %s" % (ObjectTypeName.objectSignature(self),val)
        self.state = val

    def notify(self,output):
        output((self,self.state))
