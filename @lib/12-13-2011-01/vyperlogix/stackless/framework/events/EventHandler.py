import stackless

class EventHandler:
    def __init__(self,*outputs):
        if outputs==None:
            self.outputs=[]
        else:
            self.outputs=list(outputs)

        self.channel = stackless.channel()
        stackless.tasklet(self.listen)()

    def listen(self):
        try:
            while 1:
                val = self.channel.receive()
                self.processMessage(val)
                for output in self.outputs:
                    self.notify(output)
        except TaskletExit:
            pass
                
    def processMessage(self,val):
        pass

    def notify(self,output):
        pass

    def registerOutput(self,output):
        self.outputs.append(output)
    
    def __call__(self,val):
        self.channel.send(val)
