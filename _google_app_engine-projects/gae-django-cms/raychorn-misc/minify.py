import re
import os, sys

import time
import zipfile

sys.path.insert(0,'z:\\python projects\\@lib')

from vyperlogix.misc import Args
from vyperlogix.js import minify
from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

__copyright_notice__ = '''
/*
 * VyperBlog(tm) v0.27
 * http://www.vyperlogix.com/
 *
 * Copyright 2010, Vyper Logix Corp.
 * Licensed under the GNU General Public License version 3 (GPLv3).
 * http://www.opensource.org/licenses/gpl-3.0.html
 *
 * Date: %s
 */
'''

__python_notice__ = '''
__copyright__ = """\
(c). Copyright 2008-2010, Vyper Logix Corp., All Rights Reserved.

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
'''

ignore_these = re.compile('[._]svn|[._]min|[.]db')

# --deploy --source="Z:\python projects\_google_app_engine-projects\gae-django-cms\raychorn-misc\js-source" --dest="Z:\python projects\_google_app_engine-projects\gae-django-cms\raychorn-misc\js.min"

def get_comments_from(s):
    import re
    match = re.search(r"///.*?/?\*.+?(?=\n|\r)|/\*[\s\S]*?//[\s\S]*?\*/", s, re.IGNORECASE | re.MULTILINE)
    if match:
        result = match.group()
    else:
        result = ""
    return result

def minify_fname(f):
    toks = list(os.path.splitext(f))
    toks[-1] = '.min%s' % (toks[-1])
    return ''.join(toks)

def minify_css(s):
    import cssmin
    return cssmin.cssmin(s)

def minify_js(src,dst,isAlreadyMinified=False):
    isCSS = (os.path.splitext(src)[-1] == '.css')
    isMinify_JS = False
    print >> sys.stdout, 'Reading from... "%s".' % (src)
    s = _utils.readFileFrom(src)
    cs = get_comments_from(s).strip() if (not isCSS) else ''
    c = ''
    if (len(cs) > 0):
	s = s.replace(cs,'')
	c = cs
    elif (not isCSS):
	c = __copyright_notice__ % (_utils.getAsSimpleDateStr(_utils.today_localtime(),str(_utils.formatDjangoDateTimeStr())))
    if (not isAlreadyMinified):
	if (_yuiCompressor) and (isCSS):
	    print >> sys.stdout, 'Minify CSS !'
	    t = minify_css(s)
	else:
	    isMinify_JS = True
	    print >> sys.stdout, 'Minify JS !'
	    t = minify.minify_js(s)
    else:
	isMinify_JS = isAlreadyMinified
	t = s
    print >> sys.stdout, 'Writing to... "%s".' % (dst)
    _utils.makeDirs(os.path.dirname(dst))
    __ct = t
    if (_python) and (isAlreadyMinified or isMinify_JS):
	ioBuf = _utils.stringIO()
	t = ''.join(t.split('\n'))
	print >>ioBuf, "js = '''%s\n%s\n'''" % (c,t)
	__ct = ioBuf.getvalue()
	toks = dst.split(os.sep)
	_toks = toks[0:-1]
	dst_init = os.sep.join(_toks+['__init__.py'])
	dst = os.sep.join(_toks+[toks[-1].replace('.min.js','_min_js.py')])
	if (not os.path.exists(dst_init)):
	    _utils.writeFileFrom(dst_init,'')
    else:
	__ct = c.replace(chr(10),chr(13)).replace(chr(13)+chr(13),chr(13))+t
    _utils.writeFileFrom(dst,__ct)
    return isMinify_JS
        
def safely_remove_files_under(fpath):
    try:
	_utils.removeAllFilesUnder(fpath)
    except:
	time.sleep(1)
    iLoop = 0
    while (iLoop < 10):
	if (not os.path.exists(fpath)):
	    try:
		time.sleep(1)
		os.makedirs(fpath)
		break;
	    except:
		iLoop += 1
	else:
	    try:
		_utils.removeAllFilesUnder(fpath)
	    except:
		time.sleep(1)
	    iLoop += 1

if (__name__ == '__main__'):
    args = {'--source=?':'JavaScript file name or path.',
            '--dest=?':'Destination path for the deployable files.',
            '--deploy':'Deploy the code into "js".',
            '--python':'Pack JS code into Python Scripts.',
            '--target=?':'Destination path for the deployable zip file.',
            '--yui':'Compress using the YUI Compressor.',
            '--zip':'Deploy as a ZIP file.',
            }
    _argsObj = Args.Args(args)
    print >>sys.stderr, '_argsObj=(%s)' % str(_argsObj)
    
    _root = os.path.dirname(__file__)
    _runyui = os.path.join(_root,'runyui.cmd')
    if (os.path.exists(_runyui)):
        os.remove(_runyui)
        _utils.writeFileFrom(_runyui,'@echo off\n')
    fOut_runyui = open(_runyui,mode='w')

    try:
        _python = _argsObj.booleans['isPython'] if _argsObj.booleans.has_key('isPython') else False
    except:
        _python = False

    try:
        _deploy = _argsObj.booleans['isDeploy'] if _argsObj.booleans.has_key('isDeploy') else False
    except:
        _deploy = False

    try:
        _yuiCompressor = _argsObj.booleans['isYui'] if _argsObj.booleans.has_key('isYui') else False
    except:
        _yuiCompressor = False

    try:
        _isZIP = _argsObj.booleans['isZip'] if _argsObj.booleans.has_key('isZip') else False
    except:
        _isZIP = False

    try:
        _source = _argsObj.arguments['source'] if _argsObj.arguments.has_key('source') else None
    except:
        _source = None

    try:
        _dest = _argsObj.arguments['dest'] if _argsObj.arguments.has_key('dest') else None
    except:
        _dest = None
    _destP = _dest

    try:
        _target = _argsObj.arguments['target'] if _argsObj.arguments.has_key('target') else None
    except:
        _target = None

    if (_source) and (_dest) and (_deploy):
	if (_isZIP) and (_target):
	    toks = _dest.split(os.sep)
	    toks[-1] = toks[-1].split('.')[0]+'.zip'
	    toks[0:-1] = _target.split(os.sep)
	    _zipName = os.sep.join(toks)
	    if (os.path.exists(_zipName)):
		try:
		    os.remove(_zipName)
		except WindowsError:
		    print >> sys.stderr, 'WARNING: Cannot write a replacement ZIP file because... you need to stop debugging your code. Doh !'
		    sys.exit(status=-1)
	    _zip = zipfile.ZipFile(_zipName,'a' if (os.path.exists(_zipName)) else 'w',zipfile.ZIP_DEFLATED)
	if (_python):
	    _destP = os.sep.join(_dest.split(os.sep)[0:-1]+['js.py'])
        try:
	    iCount = 0
	    safely_remove_files_under(_dest)
	    if (_python):
		safely_remove_files_under(_destP)
            for dirName, dirs, files in _utils.walk(_source,rejecting_re=ignore_these):
                for f in files:
                    iCount += 1
                    t_dirName = os.sep.join([_destP if (f.find('.js') > -1) else _dest,os.sep.join([t for t in dirName.replace(_source,'').split(os.sep) if (len(t) > 0)])])
                    _utils.makeDirs(t_dirName)
                    f_ext = os.path.splitext(f.lower())[-1]
		    f_minified = os.sep.join([dirName,f.replace('.js','.min.js')])
		    isIgnored = (f_ext == '.ufo')
		    isAlreadyMinified = os.path.exists(f_minified) and (f_ext == '.js')
                    isMinifiable = (f_ext == '.js') if (not _yuiCompressor) else (f_ext in ['.js','.css'])
                    src_fname = os.sep.join([dirName,f if (not isAlreadyMinified) else os.sep.join([n for n in f_minified.replace(dirName,'').split(os.sep) if (len(n) > 0)])])
                    dst_fname = os.sep.join([t_dirName,minify_fname(f) if (isMinifiable) and (f_ext != '.css') else f])
		    isMinifiable = isMinifiable if (not isAlreadyMinified) or (_python and isAlreadyMinified) else False
		    isMinify_JS = False
		    __isZIP = _isZIP
                    if (isMinifiable):
                        isMinify_JS = minify_js(src_fname,dst_fname,isAlreadyMinified=isAlreadyMinified)
			__isZIP = False if (_python and isMinify_JS) else _isZIP
                    elif (not isIgnored):
                        fn = os.path.dirname(dst_fname)
                        if (not os.path.exists(fn)):
                            os.makedirs(fn)
                        _utils.copyFile(src_fname,dst_fname)
		    if (__isZIP) and (_target) and (not isIgnored):
			_zip.write(dst_fname,dst_fname.replace(_dest,''),zipfile.ZIP_DEFLATED)
                    print '%d%s :: %s --> %s' % (iCount,'!' if (isMinifiable) else '',src_fname,dst_fname)
        except Exception, e:
            info_string = _utils.formattedException(details=e)
            print >>sys.stderr, 'ERROR: %s' % (info_string)
        fOut_runyui.flush()
        fOut_runyui.close()
	if (_isZIP) and (_target):
	    _zip.close()
        print 'End of Run !'
    else:
        print >>sys.stderr, 'ERROR... Try again...'
