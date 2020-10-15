import logging

from vyperlogix.enum import Enum

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

class LoggingLevels(Enum.Enum):
    none = 0
    info = logging.INFO
    warning = logging.WARNING
    error = logging.ERROR
    debug = logging.DEBUG

def explainLogging(level):
    x = LoggingLevels(level)
    if (x):
        return x.name
    return 'logging is UNDEFINED'

def appendLogging(stream=None,filename=None,_format='%(levelname)-8s %(asctime)s %(filename)s] %(message)s',console_level=logging.INFO,isVerbose=False):
    if (filename is None):
        console = logging.StreamHandler() if (stream is None) else logging.StreamHandler(stream)
    else:
        console = logging.FileHandler(filename)
    console.setLevel(console_level)
    formatter = logging.Formatter(_format)
    console.setFormatter(formatter)
    if (isVerbose):
        logging.getLogger('').addHandler(console)

def standardLogging(logFileName,_format='%(levelname)-8s %(asctime)s %(filename)s] %(message)s',_level=logging.INFO,console_level=logging.INFO,isVerbose=False,stream=None,filename=None):
    logging.root.handlers = []
    logging.basicConfig( level=_level, format=_format, filename=logFileName, filemode='w')

    appendLogging(_format=_format,console_level=console_level,isVerbose=isVerbose)
    if (stream is not None):
        appendLogging(stream=stream,_format=_format,console_level=console_level,isVerbose=isVerbose)
    if (filename is not None):
        appendLogging(filename=filename,_format=_format,console_level=console_level,isVerbose=isVerbose)
