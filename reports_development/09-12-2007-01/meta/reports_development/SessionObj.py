class SessionObj(object):
    def __init__(self, id, uuid, theDate):
        self.id = id
        self.uuid = uuid
        self.theDate = theDate
        
    def __repr__(self):
        return "<Session(%r,%r,%r)>" % (self.id, self.uuid, self.theDate)

