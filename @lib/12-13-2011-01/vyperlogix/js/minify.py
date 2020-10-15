def minify_js(source):
    from vyperlogix.misc import _utils
    from vyperlogix.misc import jsmin
    
    jsm = jsmin.JavascriptMinify()
    fIn = _utils.stringIO(source)
    fOut = _utils.stringIO()
    try:
	jsm.minify(fIn, fOut)
    except:
	pass
    return fOut.getvalue()
