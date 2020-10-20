import os
import sys
import traceback
import subprocess

from vyperlogix import misc

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

def normalizeArg(arg):
    s = arg.strip()
    if (s.endswith('=')):
        s = s[0:-1]
    return s

def normalizeVal(val):
    s = val.strip()
    toks = s.split(' ')
    if (len(toks) > 1):
        s = '"'+s+'"'
    return s

def isQuoted(ch, target):
    if (ch == target):
        return 1
    return 0

def normalize(progName):
    if (os.path.exists(progName)):
        return '"%s"' % progName
    i = len(progName) - 1
    val = []
    arg = []
    phrases = []
    verbPhase = 0
    verbs = [{'"':'"', '=':1},{' ':2}]
    _verbs = {'"':'"', 1:'=', 2:' '}
    target = ''
    isLookingForValue = True
    while (i >= 0):
        ch = progName[i]
        if ((verbs[verbPhase]).has_key(ch)):
            target = (verbs[verbPhase])[ch]
            if (len(val) > 0):
                isLookingForValue = False
                verbPhase += 1
                if (verbPhase > (len(verbs)-1)):
                    verbPhase = 0
                    phrases.insert(0,(normalizeArg(''.join(arg)),normalizeVal(''.join(val))))
                    val = []
                    arg = []
            else:
                isLookingForValue = True
                verbPhase = 0
        else:
            if (isLookingForValue):
                if ( (len(val) > 0) and (ch == ' ') and (target != '"') ):
                    phrases.insert(0,(normalizeArg(''.join(val)),normalizeVal(''.join(arg))))
                    val = []
                    arg = []
                val.insert(0,ch)
            else:
                arg.insert(0,ch)
            if (misc.isString(target)):
                if (ch == target):
                    if (len(val) > 0):
                        isLookingForValue = False
                        verbPhase += 1
                        if (verbPhase > (len(verbs)-1)):
                            verbPhase = 0
                            phrases.insert(0,(normalizeArg(''.join(arg)),normalizeVal(''.join(val))))
                            val = []
                            arg = []
                            isLookingForValue = True
                    elif (len(arg) > 0):
                        isLookingForValue = True
                        verbPhase = 0
                    target = ''
            elif (isinstance(target,int)):
                _ch = ''
                if (_verbs.has_key(target)):
                    _ch = _verbs[target]
                if ( (target == 1) and (ch == _ch) ):
                    if (len(val) > 0):
                        isLookingForValue = False
                        verbPhase += 1
                        if (verbPhase > (len(verbs)-1)):
                            verbPhase = 0
                            phrases.insert(0,(normalizeArg(''.join(arg)),normalizeVal(''.join(val))))
                            val = []
                            arg = []
                            isLookingForValue = True
                    elif (len(arg) > 0):
                        isLookingForValue = True
                        verbPhase = 0
                elif ( (target == 2) and (ch == _ch) ):
                    if (len(val) > 0):
                        isLookingForValue = False
                        verbPhase += 1
                        if (verbPhase > (len(verbs)-1)):
                            verbPhase = 0
                            phrases.insert(0,(normalizeArg(''.join(arg)),normalizeVal(''.join(val))))
                            val = []
                            arg = []
                            isLookingForValue = True
                    elif (len(arg) > 0):
                        isLookingForValue = True
                        verbPhase = 0
                        phrases.insert(0,(normalizeArg(''.join(arg)),normalizeVal(''.join(val))))
                        val = []
                        arg = []
                    val = []
                    arg = []
                    target = ''
        i -= 1
    if ( (len(arg) == 0) and (len(val) > 0) ):
        arg = [v for v in val]
        val = []
    phrases.insert(0,(normalizeArg(''.join(arg)),normalizeVal(''.join(val))))
    _sentence = []
    for p in phrases:
        if (len(p[1]) > 0):
            _sentence.append(p[0]+'='+p[1])
        else:
            _sentence.append(p[0])
    i = len(_sentence)-1
    while (i >= 0):
        _fe = -1
        _f = _sentence[i].find('.exe')
        if (_f > -1):
            _fe = (_sentence[i])[0:_f].find('=')
        if ( (_sentence[i].find(os.sep) > -1) or (_sentence[i].find('/') > -1) or ( ((_f > -1)) and ((_fe == -1)) ) ):
            break
        i -= 1
    _sentence[0] = '"'+_sentence[0].replace('"','')
    _sentence[i] = _sentence[i].replace('"','')
    _sentence[i] += '"'
    return [' '.join(_sentence[0:i]),' '.join(_sentence[i+1:])]

def callExternalProgram(progName,args=''):
    _cmd = normalize(progName)
    if (len(args) > 0):
        _cmd.append(args)
    print '(callExternalProgram) :: _cmd=%s' % str(_cmd)
    try:
        retcode = subprocess.call(_cmd, shell=True)
        if retcode < 0:
            print >>sys.stderr, "Child was terminated by signal", -retcode
        else:
            print >>sys.stderr, "Child returned", retcode
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e
        retcode = -9999
    return retcode
