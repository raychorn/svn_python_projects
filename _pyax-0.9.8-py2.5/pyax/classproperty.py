
class ClassProperty(property):
    def __get__(self, obj, objtype):
        if self.fget is None:
            raise AttributeError('Unreadable Attribute')
        return self.fget(objtype)