def getPDFContent(path,delimiter='   '):
    import pyPdf
    from vyperlogix.hash import lists
    from vyperlogix.misc.decodeUnicode import decodeUnicode

    d_content = lists.HashedLists2()
    fIn = file(path, "rb")
    try:
	pdf = pyPdf.PdfFileReader(fIn)
	for i in xrange(0, pdf.getNumPages()):
	    d_content[i+1] = " ".join(pdf.getPage(i).extractText().replace("\xa0", " ").strip().split())
    except:
	import sys
	import traceback
	from vyperlogix import misc
        exc_info = sys.exc_info()
        info_string = '\n'.join(traceback.format_exception(*exc_info))
	print >>sys.stderr, '(%s) Error due to "%s".' % (misc.funcName(),info_string)
    finally:
	fIn.close()
    return d_content

