from vyperlogix.misc import ObjectTypeName
from vyperlogix.stackless.framework.events import EventHandler

class Reporter(EventHandler.EventHandler):
    def __init__(self,msg="%(sender)s send message %(value)s"):
        EventHandler.EventHandler.__init__(self)
        self.msg = msg
        
    def processMessage(self,msg):
        sender,value=msg
        print "%s :: %s" % (ObjectTypeName.objectSignature(self),self.msg % {'sender':sender,'value':value})
