#   Programmer: Daniel Pozmanter
#   E-mail:     drpython@bluebottle.com
#   Note:       You must reply to the verification e-mail to get through.
#
#   Copyright 2003-2007 Daniel Pozmanter
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

#Functions for getting information about blocks

import re

reNotEmpty = re.compile('\S')

def CheckIfBlockStart(lines, targetline):
    LineIndent = GetLineIndentation(lines, targetline)

    if LineIndent == -1:
        LineIndent = FindValidLine(lines, targetline)
        if LineIndent == -1:
            return False

    #try till the end
    l = len(lines)
    li = 1
    result = -1
    while result == -1:
        if targetline + li >= l:
            break
        result = GetLineIndentation(lines, targetline+li)
        li += 1

    if result > LineIndent:
        return li - 1
    return False

def FindValidLine(lines, targetline):
    #try till the end
    l = len(lines)
    li = 1
    result = -1
    while result == -1:
        if targetline + li >= l:
            break
        result = GetLineIndentation(lines, targetline+li)
        if result == -1:
            if targetline - li <= 0:
                break
            result = GetLineIndentation(lines, targetline-li)
        li += 1

    return result

def RestructureExplicitLineJoining(lines):
    editedlines = [lines[0]]
    x = 1
    l = len(lines)
    while x < l:
        lline = len(lines[x-1])
        if lline > 0:
            if lines[x-1][lline - 1] == '\\':
                editedlines.append(' ')
            else:
                editedlines.append(lines[x])
        else:
            editedlines.append(lines[x])
        x += 1

    return editedlines

def RestructureImplicitLineJoining(lines):
    editedlines = []
    x = 0
    l = len(lines)
    while x < l:
        p1 = _get_paren_spread(lines[x], '[', ']')
        p2 = _get_paren_spread(lines[x], '(', ')')
        p3 = _get_paren_spread(lines[x], '{', '}')

        end = 0

        if p1:
            end = _find_paren_end_line(lines, x+1, p1, '[', ']')
            if end == -1:
                editedlines.extend(lines[x:])
                break
        if p2:
            tend = _find_paren_end_line(lines, x+1, p2, '(', ')')
            if tend == -1:
                editedlines.extend(lines[x:])
                break
            if tend > end:
                end = tend
        if p3:
            tend = _find_paren_end_line(lines, x+1, p3, '{', '}')
            if tend == -1:
                editedlines.extend(lines[x:])
                break
            if tend > end:
                end = tend

        editedlines.append(lines[x])

        if end > 0:
            newlines, x = _make_lines_whitespace(lines, x+1, end)
            editedlines.extend(newlines)
        else:
            x += 1

    return editedlines


def RemoveComments(lines):
    lines = removeStringQuotedWith(lines, "'''")
    lines = removeStringQuotedWith(lines, '"""')
    lines = removeStringQuotedWith(lines, "'")
    lines = removeStringQuotedWith(lines, '"')

    editedlines = []

    for line in lines:
        c = line.find('#')
        if c > -1:
            editedlines.append(line[:c] + ' ')
        else:
            editedlines.append(line)

    return editedlines

def removeQuoteFromSingleLine(line, start, target):
    ft2 = line[start:].find(target)
    s = reNotEmpty.search(line).start()
    #Only remove the string if it is not the first bit of the line.
    if (ft2 > -1) and (start > s):
        ft2 += start
        return line[:start] + ' ' + line[:ft2]
    return None

def removeStringQuotedWith(lines, target):
    editedlines = []
    x = 0
    l = len(lines)
    while x < l:
        ft = lines[x].find(target)
        if ft > -1:
            sameline = removeQuoteFromSingleLine(lines[x], ft, target)
            if sameline is not None:
                editedlines.append(sameline)
            else:
                editedlines.append(lines[x][:ft])
                start = x
                x += 1
                end = -1
                while x < l:
                    ft = lines[x].find(target)
                    if ft > -1:
                        end = x
                        break
                    x += 1
                if end == -1:
                    return editedlines
                else:
                    newlines, x = _make_lines_whitespace(lines, start, end)
                    editedlines.extend(newlines)
        else:
            editedlines.append(lines[x])
        x += 1

    return editedlines

def spacefill(length):
    result = ''
    for x in range(length):
        result += ' '
    return result

def _get_paren_spread(text, openp, closep):
    opencount = text.count(openp)
    if opencount > 0:
        closecount = text.count(closep)
        if opencount > closecount:
            return opencount - closecount
    return 0

def _find_paren_end_line(lines, pos, spread, openp, closep):
    x = pos
    l = len(lines)
    count = 0
    while x < l:
        count += lines[x].count(closep)
        spread += lines[x].count(openp)
        if count >= spread:
            return x
        x += 1
    return -1

def _make_lines_whitespace(lines, startline, endline):
    newlines = []
    x = startline
    while x <= endline:
        newlines.append(reNotEmpty.sub(' ', lines[x]))
        x += 1

    return newlines, x

def GetLines(Document):
    text = Document.GetText()
    eol = Document.GetEndOfLineCharacter()
    lines = text.split(eol)
    lines = RestructureExplicitLineJoining(lines)
    lines = RemoveComments(lines)
    lines = RestructureImplicitLineJoining(lines)
    return lines

def GetBlockStart(lines, targetline):
    LineIndent = GetLineIndentation(lines, targetline)

    if LineIndent == -1:
        LineIndent = FindValidLine(lines, targetline)
        if LineIndent == -1:
            return -1

    x = targetline - 1
    while x > 0:
        i = GetLineIndentation(lines, x)
        if i != -1:
            if i < LineIndent:
                return x
        x -= 1

    return 0

def GetBlockEnd(lines, targetline):
    l = len(lines)
    LineIndent = GetLineIndentation(lines, targetline)

    if LineIndent == -1:
        LineIndent = FindValidLine(lines, targetline)
        if LineIndent == -1:
            return -1

    x = targetline + 1
    last = targetline
    while x < l:
        i = GetLineIndentation(lines, x)
        if i != -1:
            if i >= LineIndent:
                last = x
            if i < LineIndent:
                return last
        x += 1

    if last != x:
        return last

    return len(lines) - 1

def GetKeyWordStart(lines, targetline, kword, kwordlength):
    start = GetBlockStart(lines, targetline)
    if kwordlength == 0:
        return start
    while lines[start].strip()[:kwordlength] != kword:
        start = GetBlockStart(lines, start)
        if start == 0:
            break
    return start

def GetKeyWordEnd(lines, targetline, kword, kwordlength):
    if (kwordlength == 0) or (lines[targetline].strip()[:kwordlength] == kword):
        startofblock = CheckIfBlockStart(lines, targetline)
        if startofblock:
            targetline += startofblock
    else:
        targetline = GetKeyWordStart(lines, targetline, kword, kwordlength) + 1

    end = GetBlockEnd(lines, targetline)

    return end

def GetLineIndentation(lines, current):
    result = reNotEmpty.search(lines[current])
    if result == None:
        return -1
    return result.start()

def GoToBlockEnd(Document, kword=''):
    lines = GetLines(Document)
    kwordl = len(kword)
    l = GetKeyWordEnd(lines, Document.GetCurrentLine(), kword, kwordl)
    i = GetLineIndentation(lines, l)
    if i < 0:
        i = 0
    Document.EnsureVisible(l)
    Document.GotoLine(l)
    p = Document.PositionFromLine(l) + i
    Document.GotoPos(p)
    Document.SetSTCFocus(True)

def GoToBlockStart(Document, kword=''):
    lines = GetLines(Document)
    kwordl = len(kword)
    l = GetKeyWordStart(lines, Document.GetCurrentLine(), kword, kwordl)
    i = GetLineIndentation(lines, l)
    if i < 0:
        i = 0
    Document.EnsureVisible(l)
    Document.GotoLine(l)
    p = Document.PositionFromLine(l) + i
    Document.GotoPos(p)
    Document.SetSTCFocus(True)
