import pod

class Entity(pod.Object):
    pass

class File(Entity):

    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)     

    def pre_delete(self):
        pass
        
    def __str__(self):
        values = []
        for k,v in self.iteritems():
            values.append('%s=%s'%(k,v))
        return '<%s>' % (', '.join(values))

