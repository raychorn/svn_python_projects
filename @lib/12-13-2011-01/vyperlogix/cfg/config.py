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
import os, sys

import re

from vyperlogix.misc import _utils
from vyperlogix.classes import SmartObject
from vyperlogix.lists import ListWrapper

def reader(source):
    __re_subject__ = re.compile(r"\[(?P<name>.*)\]", re.MULTILINE)
    __re_details__ = re.compile("(?P<name>.*)=(?P<value>.*)", re.MULTILINE)
    
    _d_ = _dd_ = SmartObject.SmartFuzzyObject(args={})

    try:
        if (os.path.exists(source)):
            _cfg_ = ListWrapper.ListWrapper(initlist=[s for s in _utils.readFileFrom(source, mode='r', noCRs=False).split('\n') if (len(s) > 0)])
            for item in _cfg_:
                subjects = __re_subject__.findall(item)
                if (len(subjects) > 0):
                    _d_[subjects[0]] = SmartObject.SmartFuzzyObject(args={})
                    _dd_ = _d_[subjects[0]]
                else:
                    details = __re_details__.findall(item)
                    if (len(details) > 0):
                        for detail in details:
                            _dd_[detail[0]] = detail[-1]
    except:
        pass
    return _d_
