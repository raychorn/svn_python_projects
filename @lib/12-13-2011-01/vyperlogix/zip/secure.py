import os,sys

from vyperlogix.enum import Enum
from vyperlogix.misc import _utils

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

class ZipType(Enum.Enum):
    none = 0
    zip = 2**0  # no encryption
    ezip = 2**1 # XTEAEncryption using Hex
    xzip = 2**2 # XTEAEncryption using No-Hex
    bzip = 2**3 # Blowfish
    z7 = 2**4   # 7zip

def zipper(top,archive_path,archive_type=ZipType.zip,_iv=None,passPhrase=None,sevenZ=None,fOut=sys.stdout):
    '''archive_type can be one of ZipType where ezip is an encrypted ZIP file using XTEAEncryption.
    _iv is used for ezip only and must be no more than 8 chars.
    passPhrase is used for bzip only.
    '''
    import os, sys, zipfile
    from vyperlogix import misc
    from vyperlogix.misc import _utils
    
    def add_to_zip(baton, dirname, names):
	'''Make this more efficient by using a list to hold all the file names.'''
	zp = baton[0]
	root = os.path.join(baton[1], '')
    
	for file in names:
	    path = os.path.join(dirname, file)
	    if os.path.isfile(path):
		try:
		    zp.write(path, path[len(root):])
		except Exception, ex:
		    print >>fOut, 'ERROR: root=%s, len(root)=%s, path=%s\n%s' % (root,len(root),path,_utils.formattedException(details=ex))
	    elif os.path.isdir(path) and os.path.islink(path):
		os.path.walk(path, add_to_zip, (zp, path))
    
    if (misc.isStringValid(sevenZ)) and (os.path.exists(sevenZ)):
	from vyperlogix.process import Popen

	parts = list(os.path.splitext(archive_path))
	del parts[-1]
	archive_path = ''.join(parts)

	try:
	    _cmd_ = '"%s" a -t7z -mhe -mx9 -p%s -r -y "%s" "%s"' % (sevenZ,passPhrase,archive_path,top)
	    print >>fOut, '+++DEBUG: 7z=%s, _cmd_=%s' % (sevenZ,_cmd_)
	    Popen.Shell(_cmd_, shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=fOut)
	except OSError, ex:
	    print >>fOut, 'ERROR: %s' % (_utils.formattedException(details=ex))
    else:
	parts = list(os.path.splitext(archive_path))
	parts[-1] = '.%s' % (archive_type.name)
	archive_path = ''.join(parts)

	zp = zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED, allowZip64=_utils.isUsingWindows)
	zp.setpassword(passPhrase)
	try:
	    os.path.walk(top, add_to_zip, (zp, top))
	finally:
	    print >>fOut, 'Closing %s' % (zp.filename)
	    zp.close()
	
def zipInfo_comparator(a, b):
    try:
	return -1 if (a.file_size < b.file_size) else 0 if (a.file_size == b.file_size) else 1
    except:
	return 0

def unzipper(archive_path,dest,archive_type=ZipType.zip,_iv=None,passPhrase=None,isMultiUnzipper=False,sevenZ=None):
    '''archive_type can be one of ZipType where ezip is an encrypted ZIP file using XTEAEncryption.'''
    import os, sys, zipfile, time
    from vyperlogix import misc
    from vyperlogix.misc import _utils
    #from vyperlogix.crypto import XTEAEncryption
    #from vyperlogix.crypto import blowfish
    #from vyperlogix.win import memoryUsage
    #from vyperlogix.classes.SmartObject import SmartFuzzyObject
    #from vyperlogix.misc import threadpool

    #report_ram = lambda t:'(%-3.2f, %d, %d)'%(t) 
    #explode_ram = lambda l:{'pcent':l[0],'freeRam':l[1],'totalRam':l[2]}
    #diff_ram = lambda r1,r2:tuple([(max(r2.pcent)-min(r1.pcent)),(max(r2.freeRam)-min(r1.freeRam)),(max(r2.totalRam)-min(r1.totalRam))])

    #if (isMultiUnzipper):
	#__Q__ = threadpool.ThreadQueue(10)
	    
	#@threadpool.threadify(__Q__)
	#def worker1():
	    #while (1):
		#_freeRam = memoryUsage.getFreeRam()
		#freeRam = SmartFuzzyObject(explode_ram(list(_freeRam)))
		#print >>sys.stdout, 'RAM: %s' % (report_ram(_freeRam))
		#time.sleep(5)
	#worker1()

    #if (archive_type.value == ZipType.ezip.value) and ( (_iv is None) or (len(_iv) < 8) ):
	#print >>sys.stderr, 'Cannot run %s using source as "%s" and target as "%s" due to the _iv which is "%s".' % (misc.funcName(),top,archive_path,_iv)
	#return
    #if (archive_type.value == ZipType.bzip.value) and ( (passPhrase is None) or (len(passPhrase) < 8) ):
	#print >>sys.stderr, 'Cannot run %s using source as "%s" and target as "%s" due to the passPhrase which is "%s".' % (misc.funcName(),top,archive_path,passPhrase)
	#return
    #if (archive_type.value == ZipType.ezip.value):
	#_iv = XTEAEncryption.iv(_iv)

    parts = list(os.path.splitext(archive_path))
    parts[-1] = '.%s' % (archive_type.name)
    archive_path = ''.join(parts)
    if (misc.isStringValid(sevenZ)) and (os.path.exists(sevenZ)):
	print >>sys.stdout, '+++DEBUG: 7z=%s' % (sevenZ)
    zp = zipfile.ZipFile(archive_path, 'r', zipfile.ZIP_DEFLATED, allowZip64=_utils.isUsingWindows)
    zp.setpassword(passPhrase)
    #print >>sys.stdout, 'DEBUG: isMultiUnzipper=%s' % (isMultiUnzipper)
    n = len(zp.filelist)
    #if (isMultiUnzipper):
	#zipinfos = misc.copy(zp.filelist)
	#zipinfos.sort(zipInfo_comparator) # tail has the largest files, head has the smallest files.
	#try:
	    #print >>sys.stdout, 'BEGIN: zp.extractall(path="%s")' % (dest)
	    #zp.extractall(path=dest)
	    #print >>sys.stdout, 'END:   zp.extractall(path="%s")' % (dest)
	#except Exception, details:
	    #print >>sys.stdout, 'ERROR: Cannot read the file named "%s" due to "%s".' % (archive_path,str(details))
	    #import traceback
	    #exc_info = sys.exc_info()
	    #info_string = '\n'.join(traceback.format_exception(*exc_info))
	    #print >>sys.stdout, info_string
	#finally:
	    #print >>sys.stdout, 'Closing %s' % (zp.filename)
	    #zp.close()
	#i = 1
	#while (len(zipinfos) > 0):
	    #zInfo = zipinfos.pop()
	    #fn = os.path.join(dest,zInfo.filename).replace(os.sep,'/')
	    #assert os.path.exists(fn), 'WARNING:  Doh!!!  Someone forgot something important...'
	    #_bytes = _utils.readBinaryFileFrom(fn)
	    #if (archive_type.value == ZipType.ezip.value):
		#_bytes = XTEAEncryption._decryptode(_bytes,_iv)
	    #elif (archive_type.value == ZipType.xzip.value):
		#_bytes = XTEAEncryption.f_decryptode(_bytes,_iv)
	    #elif (archive_type.value == ZipType.bzip.value):
		#_bytes = blowfish.decryptData(_bytes,passPhrase)
	    #_utils.writeFileFrom(fn,_bytes,mode='wb')
	    #print >>sys.stdout, '%-5d of %-5d --> (%s)%s %-30s' % (i,n,max(zInfo.file_size,zInfo.compress_size),'*' if (zInfo.compress_size > zInfo.file_size) else '',fn)
	    #i += 1
    #else:
    try:
	print >>sys.stdout, 'BEGIN: zp.extractall(path="%s")' % (dest)
	zp.extractall(path=dest)
	print >>sys.stdout, 'END:   zp.extractall(path="%s")' % (dest)
	#i = 1
	#report_ram = lambda t:'(%-3.2f, %d, %d)'%(t)
	#explode_ram = lambda l:{'pcent':l[0],'freeRam':l[1],'totalRam':l[2]}
	#diff_ram = lambda r1,r2:tuple([(r2.pcent-r1.pcent),(r2.freeRam-r1.freeRam),(r2.totalRam-r1.totalRam)])
	#for top,dirs,files in _utils.walk(dest):
	    #for fn in [os.path.join(top,f).replace(os.sep,'/') for f in files]:
		#_freeRam1 = memoryUsage.getFreeRam()
		#freeRam1 = SmartFuzzyObject(explode_ram(list(_freeRam1)))
		#_bytes = _utils.readBinaryFileFrom(fn)
		#if (archive_type.value == ZipType.ezip.value):
		    #_bytes = XTEAEncryption._decryptode(_bytes,_iv)
		#elif (archive_type.value == ZipType.xzip.value):
		    #_bytes = XTEAEncryption.f_decryptode(_bytes,_iv)
		#elif (archive_type.value == ZipType.bzip.value):
		    #_bytes = blowfish.decryptData(_bytes,passPhrase)
		#_utils.writeFileFrom(fn,_bytes,mode='wb')
		#_freeRam2 = memoryUsage.getFreeRam()
		#freeRam2 = SmartFuzzyObject(explode_ram(list(_freeRam2)))
		#print >>sys.stdout, '%s of %s --> %s, RAM: %s to %s, Used: %s' % (i,n,fn,report_ram(_freeRam1),report_ram(_freeRam2),report_ram(diff_ram(freeRam1,freeRam2)))
		#i += 1
    except Exception, details:
	print >>sys.stderr, 'ERROR: Cannot read the file named "%s" due to "%s".' % (archive_path,str(details))
	import traceback
	exc_info = sys.exc_info()
	info_string = '\n'.join(traceback.format_exception(*exc_info))
	print >>sys.stderr, info_string
    finally:
	print >>sys.stdout, 'Closing %s' % (zp.filename)
	zp.close()
