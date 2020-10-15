#Edited by Dan:
#Now takes raw encoding as arguments for Set/Get EncodedText.
#Also removed some uneeded code.

#***************************************************************************
#drDetectUTF_8
#   Programmer: limodou
#   E-mail:     limodou@users.sourceforge.net
#
#   Copyright 2004 limodou
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#   DrPython is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import wx, re

def utf8Detect(text):
    """Detect if a string is utf-8 encoding"""
    lastch=0
    begin=0
    BOM=True
    BOMchs=(0xEF, 0xBB, 0xBF)
    good=0
    bad=0
    for char in text:
        ch=ord(char)
        if begin < 3:
            BOM = (BOMchs[begin]==ch) and BOM
            begin += 1
            continue
        if (begin == 4) and BOM:
            break
        if (ch & 0xC0) == 0x80:
            if (lastch & 0xC0) == 0xC0:
                good += 1
            elif (lastch &0x80) == 0:
                bad += 1
        elif (lastch & 0xC0) == 0xC0:
            bad += 1

        lastch = ch

    #modi limodou 2004/04/16
    #if all characters are ascii, its encoding also can be ascii encoding or default encoding
    #in most cases, I think it's better that not recognizing it as utf-8 encoding
    if ((begin == 4) and BOM) or (good >= bad and good > 0):
        return True
    else:
        return False

#/drDetectUTF_8
#***************************************************************************

#Autodetect:  If the user has enabled autodetection,
#and the file has the proper special comment for encoding,
#return the encoding used (or None if nothing is found):

reencoding = re.compile(r'\#\s*-\*-.+-\*-')

def CheckForEncodingComment(text):
    encodingmatch = reencoding.search(text)
    if encodingmatch is not None:
        t = encodingmatch.group()
        i = t.find(':') + 1
        encoding = t[i:].rstrip('-*-').strip()

        return encoding

    return None

#What if python is not built with unicode support, but wxPython is?
#So, here is a safe way to test for ascii.

def CheckAscii(text):
    #Optimize this a little.
    _ord = ord
    for a in text:
        n = _ord(a)
        if (n < 0) or (n > 127):
            return False
    return True

def DecodeTextWith(text, encoding):
    #Try the encoding
    try:
        text = text.encode(encoding)
        return text
    except:
        pass

    return None

def DecodeText(frame, text, encoding='<Default Encoding>'):
    if wx.USE_UNICODE:

        etext = None

        if encoding != '<Default Encoding>':
            etext = DecodeTextWith(text, encoding)
            if etext is not None:
                return etext

        defaultencoding = len(frame.prefs.defaultencoding) > 0

        if frame.prefs.autodetectencoding:
            enco = CheckForEncodingComment(text)
            if enco is not None:
                etext = DecodeTextWith(text, enco)
                if etext is not None:
                    return etext

            if utf8Detect(text):
                etext = DecodeTextWith(text, 'utf-8')
                if etext is not None:
                    return etext

        if defaultencoding:
            etext = DecodeTextWith(text, frame.prefs.defaultencoding)
            if etext is None:
                frame.ShowMessage('There was an error using the encoding "%s".' % (frame.prefs.defaultencoding), 'Encoding Error')
            else:
                return etext

        if CheckAscii(text):
            return text

        if etext is None:
            etext = DecodeTextWith(text, wx.GetDefaultPyEncoding())
            if etext is None:
                raise Exception, 'Encoding Error!'
            else:
                return etext

    else:
        return text

def EncodeTextWith(text, encoding):
    #Try the encoding
    try:
        #AB, 25.02.2007:
        import types
        if type(text)==types.UnicodeType:
            return text
        text = unicode(text, encoding)
        return text
    except:
        print "ERROR EncodeTextWith ",text,type(text)
        return None


def EncodeText(frame, text, encoding='<Default Encoding>', returnEncoding=False):

    if wx.USE_UNICODE:

        etext = None

        if encoding != '<Default Encoding>':
            etext = EncodeTextWith(text, encoding)
            if etext is not None:
                if returnEncoding:
                    return etext, encoding
                else:
                    return etext

        defaultencoding = len(frame.prefs.defaultencoding) > 0

        if frame.prefs.autodetectencoding:
            enco = CheckForEncodingComment(text)
            if enco is not None:
                etext = EncodeTextWith(text, enco)
                if etext is not None:
                    if returnEncoding:
                        return etext, enco
                    else:
                        return etext

            if utf8Detect(text):
                etext = EncodeTextWith(text, 'utf-8')
                if etext is not None:
                    if returnEncoding:
                        return etext, 'utf-8'
                    else:
                        return etext

        if defaultencoding:
            etext = EncodeTextWith(text, frame.prefs.defaultencoding)
            if etext is None:
                frame.ShowMessage('There was an error using the encoding "%s".' % (frame.prefs.defaultencoding), 'Encoding Error')
            else:
                if returnEncoding:
                    return etext, frame.prefs.defaultencoding
                else:
                    return etext

        if CheckAscii(text):
            if returnEncoding:
                return text, 'ascii'
            else:
                return text


        if etext is None:
            etext = EncodeTextWith(text, wx.GetDefaultPyEncoding())
            if etext is None:
                # Patch by knuger, Jan 2007: added "Please try..." to error message
                raise Exception, \
                'Encoding Error! Please try another Default Encoding  (See Options  -> Preferences -> General)'
            else:
                if returnEncoding:
                    return text, wx.GetDefaultPyEncoding()
                else:
                    return text

    else:
        if returnEncoding:
            return text, '<Default Encoding>'
        else:
            return text