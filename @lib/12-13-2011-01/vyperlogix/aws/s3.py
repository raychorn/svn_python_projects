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
import os,sys

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.http import downloadFileFromURL

from vyperlogix.classes import CooperativeClass

__S3cmd__ = 'http://downloads.vyperlogix.com/Amazon/S3/s3.exe'

__S3DeleteCmd__ = 'http://downloads.vyperlogix.com/Amazon/S3/S3Delete.exe'

__S3DeleteDLL__ = 'http://downloads.vyperlogix.com/Amazon/S3/SprightlySoftAWS.dll'

class S3Shell(CooperativeClass.Cooperative):
    def __init__(self,bucketName,aws_access_key,aws_secret_access_key,callback=None,s3exe=None,S3DeleteExe=None,S3DeleteDLL=None,isDebugging=False,onExit=None,sysout=sys.stderr):
	self.__sysout__ = sysout
	self.__isDebugging__ = isDebugging
	self.__s3_bucketName__ = bucketName
	self.__aws_access_key__ = aws_access_key
	self.__aws_secret_access_key__ = aws_secret_access_key
	self.__callback__ = callback
	self.__onExit__ = onExit
	self.__S3cmd__ = os.sep.join([os.path.abspath('.'),'s3.exe']) if (not s3exe) or (not os.path.exists(s3exe)) else s3exe
	if (not os.path.exists(self.__S3cmd__)):
	    #print >> self.__sysout__, 'WARNING: Was not able to locate "%s" in the local folder or directory, trying to download from "%s".' % (self.__S3cmd__,__S3cmd__)
	    downloadFileFromURL.download(__S3cmd__,fileName=self.__S3cmd__)
	    if (not os.path.exists(self.__S3cmd__)):
		print >> self.__sysout__, 'ERROR: Was not able to locate "%s" in the local folder or directory, AFTER trying to download from "%s".' % (self.__S3cmd__,__S3cmd__)
	self.__S3DeleteCmd__ = os.sep.join([os.path.abspath('.'),'S3Delete.exe']) if (not S3DeleteExe) or (not os.path.exists(S3DeleteExe)) else S3DeleteExe
	if (not os.path.exists(self.__S3DeleteCmd__)):
	    #print >> self.__sysout__, 'WARNING: Was not able to locate "%s" in the local folder or directory, trying to download from "%s".' % (self.__S3DeleteCmd__,__S3DeleteCmd__)
	    downloadFileFromURL.download(__S3DeleteCmd__,fileName=self.__S3DeleteCmd__)
	    if (not os.path.exists(self.__S3DeleteCmd__)):
		print >> self.__sysout__, 'ERROR: Was not able to locate "%s" in the local folder or directory, AFTER trying to download from "%s".' % (self.__S3DeleteCmd__,__S3DeleteCmd__)
	self.__S3DeleteDLL__ = os.sep.join([os.path.abspath('.'),'SprightlySoftAWS.dll']) if (not S3DeleteDLL) or (not os.path.exists(S3DeleteDLL)) else S3DeleteDLL
	if (not os.path.exists(self.__S3DeleteDLL__)):
	    #print >> self.__sysout__, 'WARNING: Was not able to locate "%s" in the local folder or directory, trying to download from "%s".' % (self.__S3DeleteDLL__,__S3DeleteDLL__)
	    downloadFileFromURL.download(__S3DeleteDLL__,fileName=self.__S3DeleteDLL__)
	    if (not os.path.exists(self.__S3DeleteDLL__)):
		print >> self.__sysout__, 'ERROR: Was not able to locate "%s" in the local folder or directory, AFTER trying to download from "%s".' % (self.__S3DeleteDLL__,__S3DeleteDLL__)
	    
    def list(self,callback=None):
	if (os.path.exists(self.__S3cmd__)):
	    from vyperlogix.os.shell import Shell
	    self.__files__ = []
	    if (callable(callback)):
		self.__callback__ = callback
	    def callback1(data):
		import re
		_re_ = re.compile(r"(?P<date>((0?[13578]|10|12)(-|/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[01]?))(-|/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1}))|(0?[2469]|11)(-|/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[0]?))(-|/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1}))))\s(?P<time>[0-9]*:[0-9]*:[0-9]*\s(AM|PM))\s(?P<size>[0-9]*\.[0-9]*M)\s(?P<name>.*)")
		_re2_ = re.compile(".*(?P<num>[0-9]*)files listed.*")
		toks = str(data).split(os.linesep)
		#print '\n'.join(toks)
		matches = [(tt is not None) for tt in [_re_.match(t) for t in toks]]
		matches2 = [(tt is not None) for tt in [_re2_.match(t) for t in toks]]
		if (any(matches)) and (any(matches2)):
		    matches = [tt for tt in [_re_.match(t) for t in toks] if (tt is not None)]
		    self.__files__ = [m.groupdict() for m in matches]
		    if (callable(self.__callback__)):
			try:
			    self.__callback__(self)
			except Exception, ex:
			    info_string = _utils.formattedException(details=ex)
			    print >> self.__sysout__, info_string
	    def onExit():
		if (callable(self.__onExit__)):
		    try:
			self.__onExit__(self)
		    except Exception, ex:
			info_string = _utils.formattedException(details=ex)
			print >> self.__sysout__, info_string
	    self.__command__ = '"%s" list %s /key:%s /secret:%s' % (self.__S3cmd__,self.__s3_bucketName__,self.__aws_access_key__,self.__aws_secret_access_key__)
	    if (self.__isDebugging__):
		print >> self.__sysout__, 'DEBUG: %s' % (self.__command__)
	    self.__shell__ = Shell(self.__command__,callback=callback1,isDebugging=False,isExit=True,isWait=False,onExit=onExit)
	else:
	    print >> self.__sysout__, 'ERROR: Missing "%s" !!!' % (self.__S3cmd__)

    def put(self,bucketKeyName,fpath,callback=None):
	if (os.path.exists(self.__S3cmd__)):
	    from vyperlogix.os.shell import Shell
	    self.__files__ = None
	    if (callable(callback)):
		self.__callback__ = callback
	    def callback3(data):
		toks = str(data).split(os.linesep)
		self.__lines__ = [t for t in toks if str(t).endswith(os.path.basename(fpath))]
		if (len(self.__lines__) > 0):
		    if (callable(self.__callback__)):
			try:
			    self.__callback__(self,lines=self.__lines__)
			except Exception, ex:
			    info_string = _utils.formattedException(details=ex)
			    print >> self.__sysout__, info_string
	    def onExit():
		if (callable(self.__onExit__)):
		    try:
			self.__onExit__(self)
		    except Exception, ex:
			info_string = _utils.formattedException(details=ex)
			print >> self.__sysout__, info_string
	    self.__command__ = '"%s" put %s "%s" /key:%s /secret:%s /yes' % (self.__S3cmd__,bucketKeyName+('/' if (not str(bucketKeyName).endswith('/')) else ''),fpath,self.__aws_access_key__,self.__aws_secret_access_key__)
	    if (self.__isDebugging__):
		print >> self.__sysout__, 'DEBUG: %s' % (self.__command__)
	    self.__shell__ = Shell(self.__command__,callback=callback3,isDebugging=False,isExit=True,isWait=True,onExit=onExit)
	else:
	    print >> self.__sysout__, 'ERROR: Missing "%s" !!!' % (self.__S3cmd__)

    def get(self,bucketKeyName,s3name,fpath,callback=None):
	if (os.path.exists(self.__S3cmd__)):
	    from vyperlogix.os.shell import Shell
	    self.__files__ = None
	    fp = '/'.join(fpath.replace('//','/').split('/')[0:-1])+'/'+s3name.split('/')[-1]
	    if (callable(callback)):
		self.__callback__ = callback
	    def callback3(data):
		toks = str(data).split(os.linesep)
		self.__lines__ = [t for t in toks if str(t).endswith(os.path.basename(fpath))]
		if (len(self.__lines__) > 0):
		    if (callable(self.__callback__)):
			try:
			    self.__callback__(self,lines=self.__lines__)
			except Exception, ex:
			    info_string = _utils.formattedException(details=ex)
			    print >> self.__sysout__, info_string
	    def onExit():
		if (callable(self.__onExit__)):
		    try:
			self.__onExit__(self,fpath=fp)
		    except Exception, ex:
			info_string = _utils.formattedException(details=ex)
			print >> self.__sysout__, info_string
	    self.__command__ = '"%s" get "%s" "%s" /key:%s /secret:%s' % (self.__S3cmd__,str(bucketKeyName+'/'+s3name).replace('//','/'),fp,self.__aws_access_key__,self.__aws_secret_access_key__)
	    if (self.__isDebugging__):
		print >> self.__sysout__, 'DEBUG: %s' % (self.__command__)
	    self.__shell__ = Shell(self.__command__,callback=callback3,isDebugging=False,isExit=True,isWait=True,onExit=onExit)
	else:
	    print >> self.__sysout__, 'ERROR: Missing "%s" !!!' % (self.__S3cmd__)

    def delete(self,bucketName,keyName,callback=None):
	if (os.path.exists(self.__S3DeleteCmd__)) and (os.path.exists(self.__S3DeleteDLL__)):
	    from vyperlogix.os.shell import Shell
	    self.__lines__ = [keyName]
	    if (callable(callback)):
		self.__callback__ = callback
	    def callback2(data):
		import re
		_re_ = re.compile(r".*Number\sof\sitems\sdeleted:\s(?P<num>[0-9]*).*")
		toks = str(data).split(os.linesep)
		if (any([str(t).find('Program complete.') > -1 for t in toks])):
		    matches = [_re_.match(t) for t in toks]
		    _items_ = [m.groupdict() for m in matches if (m)]
		    if (callable(self.__callback__)):
			try:
			    self.__callback__(self,lines=self.__lines__,items=_items_)
			except Exception, ex:
			    info_string = _utils.formattedException(details=ex)
			    print >> self.__sysout__, info_string
	    def onExit():
		if (callable(self.__onExit__)):
		    try:
			self.__onExit__(self)
		    except Exception, ex:
			info_string = _utils.formattedException(details=ex)
			print >> self.__sysout__, info_string
	    self.__s3_bucketName__ = bucketName
	    self.__command__ = '"%s" -AWSAccessKeyId %s -AWSSecretAccessKey %s -BucketName %s -S3KeyName "%s" -LogOnlyMode False' % (self.__S3DeleteCmd__,self.__aws_access_key__,self.__aws_secret_access_key__,self.__s3_bucketName__,keyName)
	    if (self.__isDebugging__):
		print >> self.__sysout__, 'DEBUG: %s' % (self.__command__)
	    self.__shell__ = Shell(self.__command__,callback=callback2,isDebugging=False,isExit=True,isWait=False,onExit=onExit)
	else:
	    print >> self.__sysout__, 'ERROR: Missing "%s" !!!' % (self.__S3cmd__)

    def S3cmd():
        doc = "get the S3cmd."
        def fget(self):
            return self.__S3cmd__
        return locals()
    S3cmd = property(**S3cmd())

    def files():
        doc = "get the files."
        def fget(self):
            return self.__files__
        return locals()
    files = property(**files())

    def callback():
        doc = "set/get the calllback."
        def fget(self):
            return self.__callback__
        def fset(self,callback):
	    if (callable(callback)):
		self.__callback__ = callback
        return locals()
    callback = property(**callback())

    def lines():
        doc = "get the lines."
        def fget(self):
            return self.__lines__
        return locals()
    lines = property(**lines())

    def s3_bucketName():
        doc = "get the s3_bucketName."
        def fget(self):
            return self.__s3_bucketName__
        return locals()
    s3_bucketName = property(**s3_bucketName())

    def command():
        doc = "get the command."
        def fget(self):
            return self.__command__
        return locals()
    command = property(**command())

    def shell():
        doc = "get the shell."
        def fget(self):
            return self.__shell__
        return locals()
    shell = property(**shell())

################################################################################################

if (__name__ == "__main__"):
    def __callback__(s3):
	print 'BEGIN:'
	for f in s3.files:
	    print f
	print 'END !'
    s = S3Shell('__vyperlogix_svn_backups__','AKIAI52A6BTLWZHHDLCA','E6HT0b8BkiN71ey+iZZxMUhVTPqbHCCdNfhtfgIv',callback=__callback__,s3exe='J:/@Vyper Logix Corp/@Projects/python-projects/svnHotBackups/s3.exe')
    s.list()
    
    # s3 put __vyperlogix_svn_backups__/testing/ "J:/@Vyper Logix Corp/@Projects/python-projects/svnHotBackups/To-Do.txt" /key:AKIAI52A6BTLWZHHDLCA /secret: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 /nogui
    
    # s3 
