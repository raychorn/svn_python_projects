def wrap(instance):
    '''
    Python method injection Decorator wrapper
    
    Usage:
    
    @wrap(instance)
    def method(self, blah):
        pass
        
    Hint: Neer completed and tested.
    '''
    def decorator(f):
        from vyperlogix.classes.SmartObject import SmartObject
        class Wrapper(SmartObject):
            def __init__(self, obj):
                self.__object__ = obj
                SmartObject.__init__(self,{})
        return Wrapper(instance)
    return decorator


