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

def readWordDoc(fname):
    import win32com.client
    
    text = None
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Documents.Open(fname)
        text = word.ActiveDocument.content.text
        word.Documents.Close()
        word = None
    except Exception, details:
        import sys
        from vyperlogix.misc import _utils
        print >>sys.stderr, _utils.formattedException(details=details)
    
    #text = text.encode('Latin-1')
    
    return text

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

    def cb(*args):
        print str(args)
    
    import os, sys
    from vyperlogix.misc.ReportTheList import reportTheList
    from vyperlogix.misc import _utils
    fname = _utils.searchForFileNamed('*.doc',top=r'c:\python25',callback=cb,options=_utils.FileFolderSearchOptions.callback_folders | _utils.FileFolderSearchOptions.skip_svn)
    if (os.path.exists(fname)) and (os.path.isfile(fname)):
        t = readWordDoc(fname)
        lines = t.split('\n')
        reportTheList(lines,'%s' % (fname),fOut=sys.stdout)
    else:
        print >>sys.stderr, 'Cannot use "%s".' % (fname)