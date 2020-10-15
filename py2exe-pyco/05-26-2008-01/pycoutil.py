# ======================================================================
# Copyright 2001, 2002 by Solus Software
#
#                         All Rights Reserved
#
# Permission to use, copy, modify, and distribute this software and
# its documentation for any purpose and without fee is hereby
# granted, provided that the above copyright notice appear in all
# copies and that both that copyright notice and this permission
# notice appear in supporting documentation.
#
# SOLUS SOFTWARE DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN
# NO EVENT SHALL SOLUS SOFTWARE BE LIABLE FOR ANY SPECIAL, INDIRECT OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
# ======================================================================

'''
Takes a base file and list of files to tack onto the end of that
file. Compresses and adds each file followed by a pointer to the first file.
Also has routines to dump out info on files stored.

Each file is stored like:
4 bytes - compressed size
4 bytes - uncompressed size
1 byte - file name len
1 byte - iscompressed
n bytes - file name
nn bytes - file data

the last 4 bytes of the finished file represent an offset from the start of
the file of the first entry.
'''
import struct, zlib, os, shutil, glob, sys

TOC_ENTRY_FMT = '<iibb'
TOC_ENTRY_FMT_LEN = struct.calcsize(TOC_ENTRY_FMT)
OFFSET_SIZE = 4

def ReadTOC(fileName):
    'Returns list of (compressedSize, uncompressedSize, isCompressed, name)'
    f = open(fileName, 'rb')
    f.seek(-OFFSET_SIZE, 2)
    offset = struct.unpack('<i', f.read(OFFSET_SIZE))[0]
    f.seek(offset)
    toc = []
    while 1:
        data = f.read(TOC_ENTRY_FMT_LEN)
        if not data or len(data) == OFFSET_SIZE: break
        compressedSize, uncompressedSize, nameLen, isCompressed = struct.unpack(TOC_ENTRY_FMT, data)
        name = f.read(nameLen)
        toc.append((compressedSize, uncompressedSize, isCompressed, name))
        q = f.read(compressedSize) # Skip over the file itself
    return toc

def DumpBundle(fileName, sorted=1):
    toc = ReadTOC(fileName)
    if sorted:
        toc.sort()
    for compSize, uncompSize, isComp, name in toc:
        print isComp, compSize, uncompSize, name

def MakeEntry(name, data, compressed):
    'Returns a string ready for insertion into a bundle, including TOC entry'
    name = os.path.basename(name)
    origSize = len(data)
    if compressed:
        data = zlib.compress(data, 9)
    compressSize = len(data)
    return '%s%s%s' % (struct.pack(TOC_ENTRY_FMT, compressSize, origSize, len(name), compressed), \
                     name, data)
    
def AddFile(bundleData, name, data, compressed):
    bundleData, firstOffset = bundleData[:-OFFSET_SIZE], bundleData[-OFFSET_SIZE:]
    return '%s%s%s' % (bundleData, MakeEntry(name, data, compressed), firstOffset)
    
def CreateBundle(inFileName, outFileName, bundleDir):
    firstFileOffset = os.path.getsize(inFileName)
    shutil.copyfile(inFileName, outFileName)
    f = open(outFileName, 'a+b')
    for file in os.listdir(bundleDir):
        data = open(os.path.join(bundleDir, file), 'rb').read()
        name = os.path.basename(file)
        f.write(MakeEntry(name, data, 1))
    f.write(struct.pack('<i', firstFileOffset))

def Usage():
    print 'Usage:', sys.argv[0], 'dump filename'
    print '      ', sys.argv[0], 'build stubname outname filesdir'
    sys.exit(1)
    
if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        Usage()
    
    cmd = args[1].lower()
    if not cmd in ['dump','build']:
        Usage()

    if cmd == 'dump':
        if len(args) != 3: Usage()
        DumpBundle(args[2])
    else:
        if len(args) != 5: Usage()
        CreateBundle(*args[2:])
        
