import sys
import os
import ctypes

message = """curdir: %s
exedir: %s
sys.winver: %s
sys.argv: %r
__name__ = %r
__file__ = %r
sys.path = %r
PYTHONHOME = %r""" % (
    os.path.abspath(os.curdir),
    os.path.abspath(os.path.dirname(sys.argv[0])),
    sys.winver,
    sys.argv,
    __name__,
    __file__,
    sys.path,
    os.environ.get('PYTHONHOME', '<not set>'),
)

print message
ctypes.windll.user32.MessageBoxA(0, message, "%s - Message" % os.path.basename(sys.executable), 0x30)
