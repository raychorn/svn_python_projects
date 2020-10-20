import os

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

def deleteFile(root,fname):
    os.remove(os.path.join(root, fname))

def processAllFilesUnder(top,action=None,tag=''):
    try:
        for root, dirs, files in os.walk(top, topdown=False):
            if (str(action.__class__).find("'function'") > -1):
                try:
                    action(root,dirs,files,tag)
                except Exception, details:
                    print '(processAllFilesUnder) :: ERROR.2 :: (%s).' % (str(details))
    except Exception, details:
        print '(processAllFilesUnder) :: ERROR.1 :: (%s).' % (str(details))

def copyOSFileFromTo(source,dest):
    try:
        print 'CMD /K XCOPY "%s" "%s" /V' % (source,dest)
        #os.system()
    except:
        pass

def copyAllFilesUnderTo(source,target,action=None):
    try:
        for root, dirs, files in os.walk(source, topdown=True):
            for f in files:
                mask = root.replace(source,'')
                srcFName = root+os.sep+f
                dstFName = target+os.sep+mask+os.sep+f
                if (str(action.__class__).find("'function'") > -1):
                    try:
                        action(srcFName,dstFName)
                    except Exception, details:
                        print '(copyAllFilesUnderTo) :: ERROR.2 :: (%s).' % (str(details))
                else:
                    copyOSFileFromTo(srcFName,dstFName)
    except Exception, details:
        print '(copyAllFilesUnderTo) :: ERROR.1 :: (%s).' % (str(details))
