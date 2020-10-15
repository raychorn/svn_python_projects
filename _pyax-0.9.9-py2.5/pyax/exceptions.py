class ApiFault(Exception):
    def __init__(self, code, message):
        self.exception_code = code
        self.exception_message = message
        return

    def __str__(self):
        return str(self.exception_message)


class NoConnectionError(Exception):
    pass


class SObjectTypeError(TypeError):
    pass


def install_exceptions(module):
    for exception in (ApiFault, NoConnectionError, SObjectTypeError):
        module_exception = getattr(module, exception.__name__, None)
        if module_exception is not None:
            module_exception.__bases__ += (exception,)