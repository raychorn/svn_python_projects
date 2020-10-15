class staticmethod(object):
    """Make @staticmethods play nice with @decorators."""

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        """Call the static method with no instance."""
        return self.func(*args, **kwargs)
    
