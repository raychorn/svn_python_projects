import sys

def reportTheList(l,title,callback=None,asCSV=False,fOut=sys.stdout):
    '''Report the List using a callback or asCSV or the default str(item) method.'''
    from vyperlogix.hash import lists
    from vyperlogix.parsers import CSV
    from vyperlogix import misc
    from vyperlogix.misc import ObjectTypeName

    print >>fOut, 'BEGIN: %s num=(%s)' % (title,len(l))
    i = 1
    if (misc.isIterable(l)) or (misc.isList(l)):
	for item in l:
	    if (isinstance(item,tuple)):
		item = list(item)
	    if (isinstance(item,list)):
		if (lists.isDict(item[0])):
		    lists.prettyPrint(item[0],title='%d :: %s' % (i,title),asCSV=asCSV,fOut=fOut)
		    i += 1
		else:
		    isHandled = False
		    if (callable(callback)):
			try:
			    print >>fOut, '\t%s' % (callback(item[0]))
			    isHandled = True
			except:
			    pass
		    if (not isHandled):
			if (asCSV):
			    print >>fOut, '%s' % (CSV.asCSV(item))
			else:
			    print >>fOut, '\t%s' % (item[0])
		    i += 1
		for _item in item[1:]:
		    if (misc.isList(_item)):
			for __item in _item:
			    if (lists.isDict(__item)):
				lists.prettyPrint(__item,title='%d :: %s' % (i,title),asCSV=asCSV,fOut=fOut)
				i += 1
			    else:
				isHandled = False
				if (callable(callback)):
				    try:
					print >>fOut, '\t\t%d :: %s' % (ii,callback(__item))
					isHandled = True
				    except:
					pass
				if (not isHandled):
				    if (asCSV):
					print >>fOut, '"%d","%s"' % (ii,__item)
				    else:
					print >>fOut, '\t\t%d :: %s' % (ii,__item)
				i += 1
		    else:
			if (lists.isDict(_item)):
			    lists.prettyPrint(_item,title='%d :: %s' % (i,title),asCSV=asCSV,fOut=fOut)
			    i += 1
			else:
			    isHandled = False
			    if (callable(callback)):
				try:
				    print >>fOut, '\t\t%s' % (callback(__item))
				    isHandled = True
				except:
				    pass
			    if (not isHandled):
				if (asCSV):
				    print >>fOut, '"%s"' % (_item)
				else:
				    print >>fOut, '\t\t%s' % (_item)
			    i += 1
	    else:
		if (lists.isDict(item)):
		    lists.prettyPrint(item,title='%d :: %s' % (i,title),asCSV=asCSV,fOut=fOut)
		    i += 1
		else:
		    isHandled = False
		    if (callable(callback)):
			try:
			    print >>fOut, '\t%d :: %s' % (i,callback(item))
			    isHandled = True
			except:
			    pass
		    if (not isHandled):
			if (asCSV):
			    print >>fOut, '"%d","%s"' % (i,item)
			else:
			    print >>fOut, '\t%d :: %s' % (i,item)
		    i += 1
    else:
	print >>fOut, 'NOTHING TO REPORT, List is EMPTY or not an interable; just for the record type "%s" is not iterable.' % (ObjectTypeName.typeClassName(l))
    print >>fOut, 'END! %s' % (title)

