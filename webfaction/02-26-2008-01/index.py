
import sys
import mod_python
def index(req):
    return "Hello, this is your default mod_python-%s site with python-%s" % (
            mod_python.version, sys.version)
