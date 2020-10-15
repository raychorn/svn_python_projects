#!/usr/bin/env python

def myeval(statement, globals_=None, locals_=None): 
    try: 
        return eval(statement, globals_, locals_) 
    except SyntaxError: 
        if locals_ is None: 
            import inspect 
            locals_ = inspect.currentframe().f_back.f_locals 
        exec statement in globals_, locals_ 
