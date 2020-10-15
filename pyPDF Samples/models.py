import pod
import pod.set

class Entity(pod.Object):

    def __str__(self):
        values = []
        for k,v in self.iteritems():
            values.append('%s=%s'%(k,v))
        return '<%s>' % (', '.join(values))

class Statement(Entity):

    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)                                          
        self.elements = pod.set.Set()

class LineItem(Entity):

    def __init__(self, statement, **kwargs):
        Entity.__init__(self, **kwargs)     
        self.statement = statement
        self.statement.elements.add(self)
        self.elements = pod.set.Set()

    def pre_delete(self):
        self.statement.elements.remove(self)

class Element(Entity):

    def __init__(self, item, **kwargs):
        Entity.__init__(self, **kwargs)     
        self.item = item
        self.item.elements.add(self)

    def pre_delete(self):
        self.item.elements.remove(self)
